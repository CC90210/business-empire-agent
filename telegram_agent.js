require('dotenv').config({ path: '.env.agents' });
const TelegramBot = require('node-telegram-bot-api');
const { spawn, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

// ============================================================
// BRAVO TELEGRAM BRIDGE V7.2
//
// Root cause of all previous failures:
// Using shell:true with gemini.cmd causes cmd.exe to misparse
// the prompt (parentheses, quotes, special chars break it).
// Gemini then sees both a positional arg AND -p flag → error.
//
// Fix: Spawn node.exe directly with shell:false. Node's spawn
// passes each arg as a separate argv entry via CreateProcess,
// completely bypassing cmd.exe character parsing.
// ============================================================

const TELEGRAM_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const LOG_FILE = path.join(__dirname, 'memory', 'telegram_bridge.log');

if (!TELEGRAM_TOKEN) {
    console.error('TELEGRAM_BOT_TOKEN missing in .env.agents');
    process.exit(1);
}

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

const log = (msg) => {
    const line = `[${new Date().toISOString()}] ${msg}\n`;
    console.log(line.trim());
    try { fs.appendFileSync(LOG_FILE, line); } catch (_) {}
};

log('Bravo Telegram Bridge V7.2 starting...');

// ---- PATHS ----
// Resolve actual script paths so we spawn node directly (no .cmd wrappers)
const NODE_EXE = process.execPath; // The node.exe running this script
const GEMINI_SCRIPT = path.join(
    process.env.APPDATA || '',
    'npm', 'node_modules', '@google', 'gemini-cli', 'dist', 'index.js'
);
const CLAUDE_EXE = path.join(
    process.env.USERPROFILE || '', '.local', 'bin', 'claude.exe'
);

// Verify paths exist at startup
if (!fs.existsSync(GEMINI_SCRIPT)) {
    log(`[WARN] Gemini script not found: ${GEMINI_SCRIPT}`);
}
if (!fs.existsSync(CLAUDE_EXE)) {
    log(`[WARN] Claude exe not found: ${CLAUDE_EXE}`);
}

// ---- CONFIG ----
const EXEC_TIMEOUT = 120000; // 2 min

const SYSTEM_PROMPT = `You are BRAVO, CC's autonomous AI agent. Answer directly in 1-5 sentences. No preamble. Use MCP tools when needed. CC's question:`;

// Detect which MCP servers a query needs (keeps Gemini startup fast)
const detectMcps = (text) => {
    const t = text.toLowerCase();
    const mcps = [];
    if (/post|tweet|schedule|social|linkedin|instagram|threads|tiktok|bluesky|content/i.test(t)) mcps.push('late');
    if (/database|supabase|table|sql|query|schema/i.test(t)) mcps.push('supabase');
    if (/workflow|n8n|automat/i.test(t)) mcps.push('n8n-mcp');
    if (/stripe|payment|invoice|subscription|balance/i.test(t)) mcps.push('stripe');
    if (/browse|website|screenshot|url|http/i.test(t)) mcps.push('playwright');
    if (/docs|library|documentation|api reference/i.test(t)) mcps.push('context7');
    // Always include lightweight ones
    mcps.push('memory', 'sequential-thinking');
    return mcps;
};

// ---- PROCESS TRACKING ----
const activeChildren = new Set();

const killTree = (pid) => {
    try {
        // Windows: taskkill /T kills entire process tree
        spawn('taskkill', ['/pid', String(pid), '/T', '/F'], {
            windowsHide: true,
            stdio: 'ignore',
            shell: false
        });
    } catch (_) {}
};

// ---- CLI EXECUTION ----
const executeCli = (tool, userPrompt) => {
    return new Promise((resolve) => {
        const fullPrompt = `${SYSTEM_PROMPT} ${userPrompt}`;
        let cmd, args;

        if (tool === 'claude') {
            // Claude Code: -p = --print (headless output mode)
            cmd = CLAUDE_EXE;
            args = [
                '-p', fullPrompt,
                '--dangerously-skip-permissions',
                '--output-format', 'text',
                '--max-turns', '3',
                '--model', 'sonnet'
            ];
        } else {
            // Gemini CLI: -p = --prompt (headless non-interactive mode)
            // CRITICAL: Spawn node directly, NOT gemini.cmd
            // shell:false means Node passes args via CreateProcess — no cmd.exe parsing
            const mcps = detectMcps(userPrompt);
            // CRITICAL: yargs only accepts ONE value per --allowed-mcp-server-names flag
            // Must repeat the flag for each server name, NOT space-separate them
            const mcpArgs = mcps.flatMap(m => ['--allowed-mcp-server-names', m]);
            cmd = NODE_EXE;
            args = [
                '--no-warnings=DEP0040',
                GEMINI_SCRIPT,
                '-p', fullPrompt,
                '--approval-mode', 'yolo',
                '--output-format', 'text',
                ...mcpArgs
            ];
            log(`[MCP] Loading: ${mcps.join(', ')}`);
        }

        log(`[EXEC] ${tool}: "${userPrompt.substring(0, 60)}..."`);

        const child = spawn(cmd, args, {
            env: {
                ...process.env,
                CI: 'true',
                NONINTERACTIVE: 'true',
                PAGER: 'cat',
                NO_COLOR: '1',
                FORCE_COLOR: '0'
            },
            stdio: ['ignore', 'pipe', 'pipe'], // CRITICAL: ignore stdin prevents interactive hang
            shell: false, // CRITICAL: no cmd.exe — bypass all special char parsing issues
            windowsHide: true,
            cwd: __dirname
        });

        activeChildren.add(child);

        let stdout = '';
        let stderr = '';
        child.stdout.on('data', (d) => { stdout += d.toString(); });
        child.stderr.on('data', (d) => { stderr += d.toString(); });

        const timer = setTimeout(() => {
            log(`[TIMEOUT] ${tool} killed after ${EXEC_TIMEOUT / 1000}s`);
            killTree(child.pid);
            resolve('Timed out. Try a simpler question or use !claude prefix.');
        }, EXEC_TIMEOUT);

        child.on('close', (code) => {
            clearTimeout(timer);
            activeChildren.delete(child);
            log(`[DONE] ${tool} code=${code} stdout=${stdout.length}b stderr=${stderr.length}b`);

            const raw = (stdout.trim() || stderr.trim());
            if (!raw) {
                resolve(code === 0 ? 'Done.' : `Error (code ${code}).`);
                return;
            }
            resolve(cleanOutput(raw));
        });

        child.on('error', (err) => {
            clearTimeout(timer);
            activeChildren.delete(child);
            log(`[ERROR] ${tool}: ${err.message}`);
            resolve(`Error: ${err.message}`);
        });
    });
};

// Strip ANSI codes and CLI noise
const cleanOutput = (raw) => {
    let text = raw
        .replace(/[\u001b\u009b][[()#;?]*(?:[0-9]{1,4}(?:;[0-9]{0,4})*)?[0-9A-ORZcf-nqry=><]/g, '')
        .replace(/[⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏]/g, '');

    const noise = [
        /^[█▓░▀▄▐▌]+/,
        /logged in with/i,
        /waiting for mcp/i,
        /^Gemini CLI/i,
        /^Using model/i,
        /^Loading/i,
        /YOLO mode is enabled/i,
        /Loaded cached credentials/i,
        /supports tool updates/i,
        /^Bravo online\.?\s*$/i,
        /^Memory synced\.?\s*$/i,
        /Listening for changes/i,
        /^Server '/i,
        /^\s*$/
    ];

    return text.split('\n')
        .filter(line => !noise.some(p => p.test(line.trim())))
        .join('\n')
        .trim() || text.trim();
};

// ---- TELEGRAM HANDLER ----
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;
    if (!text) return;

    const user = msg.from.username || msg.from.first_name || '?';
    log(`[MSG] ${user}: ${text}`);

    if (text === '/start' || text === '/help') {
        return bot.sendMessage(chatId, [
            'Bravo Bridge V7.2',
            'Type any question (routes to Gemini).',
            '!claude <query> — route to Claude Code',
            '!sys <cmd> — run shell command'
        ].join('\n'));
    }

    try {
        // Shell passthrough
        if (text.startsWith('!sys ')) {
            await bot.sendMessage(chatId, 'Running...');
            exec(text.slice(5), { windowsHide: true, timeout: 30000 }, (err, out, serr) => {
                const r = out || serr || (err ? err.message : 'Done.');
                bot.sendMessage(chatId, r.substring(0, 4000));
            });
            return;
        }

        const isClaude = text.startsWith('!claude ');
        const prompt = text.replace(/^!(claude|gemini|bravo)\s+/, '');

        await bot.sendChatAction(chatId, 'typing');
        await bot.sendMessage(chatId, isClaude ? '🧠 Claude...' : '✨ Thinking...');

        // Keep typing indicator alive
        const typing = setInterval(() => {
            bot.sendChatAction(chatId, 'typing').catch(() => {});
        }, 5000);

        const result = await executeCli(isClaude ? 'claude' : 'gemini', prompt);
        clearInterval(typing);

        // Telegram limit is 4096 chars
        const chunks = (result || 'No response.').match(/[\s\S]{1,4000}/g) || ['No response.'];
        for (const c of chunks) {
            await bot.sendMessage(chatId, c);
        }
    } catch (err) {
        log(`[CRASH] ${err.message}`);
        bot.sendMessage(chatId, `Error: ${err.message}`).catch(() => {});
    }
});

// ---- SHUTDOWN ----
const shutdown = (sig) => {
    log(`[SHUTDOWN] ${sig}`);
    for (const c of activeChildren) killTree(c.pid);
    bot.stopPolling();
    process.exit(0);
};
process.on('SIGINT', () => shutdown('SIGINT'));
process.on('SIGTERM', () => shutdown('SIGTERM'));
bot.on('polling_error', (e) => log(`[POLL] ${e.message}`));

log('Bridge ready.');
