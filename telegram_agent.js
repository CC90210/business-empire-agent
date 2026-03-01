require('dotenv').config({ path: '.env.agents' });
const TelegramBot = require('node-telegram-bot-api');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const TELEGRAM_TOKEN = process.env.TELEGRAM_BOT_TOKEN;

if (!TELEGRAM_TOKEN) {
    console.error('❌ TELEGRAM_BOT_TOKEN is missing in .env.agents');
    process.exit(1);
}

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

// Prevent crashing if multiple terminals run the bot simultaneously
bot.on('polling_error', (error) => {
    if (error.code === 'EFATAL') {
        console.error('⚠️ Conflict Error: Another terminal is already running this bot!');
    } else {
        console.error('⚠️ Polling error:', error.message);
    }
});

console.log('🤖 AI Powerhouse (Bravo) Router running...');
console.log('📍 Anchored in Workspace: ' + process.cwd());
console.log('📱 Waiting for messages from CC...');

// --- SYSTEM CONTEXT LOADING ---
const getSystemContext = () => {
    let context = "You are BRAVO (V5.0), CC's Autonomous AI OS. You follow the BRAIN-FIRST protocol.\n\n";

    const paths = [
        { name: 'SOUL', path: 'brain/SOUL.md' },
        { name: 'STATE', path: 'brain/STATE.md' },
        { name: 'USER', path: 'brain/USER.md' },
        { name: 'DIRECTIVES', path: 'AGENT_CORE_DIRECTIVES.md' },
        { name: 'CC_PROFILE', path: 'references/CC_PROFILE.md' }
    ];

    paths.forEach(p => {
        const fullPath = path.join(process.cwd(), p.path);
        if (fs.existsSync(fullPath)) {
            context += `--- ${p.name} ---\n${fs.readFileSync(fullPath, 'utf8').substring(0, 2000)}\n\n`;
        }
    });

    return context;
};

// --- AUTONOMOUS PROMPT WRAPPER (V5.3) ---
const getAutonomousPrompt = (userPrompt) => {
    return `[SYSTEM DIRECTIVE]: You are BRAVO V5.3, CC's Autonomous AI OS. You have TOTAL ACCESS to this computer's repository.
MANDATORY RE-ORIENTATION (Every Task):
1. BOOT: Read brain/SOUL.md, brain/STATE.md, and AGENT_CORE_DIRECTIVES.md.
2. EQUIP: Consult brain/ROUTING_MAP.md. Load the "Required Context" and "Mandatory Skills" for the task type.
3. ANTI-LOOP: Search once, verify once. If information is found, move immediately to planning or execution. Stop redundant "check status" commands.
4. PERSISTENCE: Always update memory/ files after completing a task.

[USER REQUEST]: ${userPrompt}`;
};

// --- CLI EXECUTION ENGINES ---
const executeClaude = (promptText) => {
    return new Promise((resolve) => {
        const autonomousPrompt = getAutonomousPrompt(promptText);
        // Escape double quotes for shell command
        const safePrompt = autonomousPrompt.replace(/"/g, '\\"');
        const cmd = `npx @anthropic-ai/claude-code -p "${safePrompt}" --dangerously-skip-permissions --no-user-prompt`;

        exec(cmd, { env: { ...process.env, CI: 'true', NONINTERACTIVE: 'true' } }, (error, stdout, stderr) => {
            resolve(stdout || stderr || "✅ Claude Execution Complete.");
        });
    });
};

const executeGemini = (promptText) => {
    return new Promise((resolve) => {
        const autonomousPrompt = getAutonomousPrompt(promptText);
        // Escape double quotes for shell command
        const safePrompt = autonomousPrompt.replace(/"/g, '\\"');
        const cmd = `gemini "${safePrompt}" --approval-mode yolo`;

        exec(cmd, { env: { ...process.env } }, (error, stdout, stderr) => {
            resolve(stdout || stderr || "✅ Gemini Execution Complete.");
        });
    });
};

// --- MESSAGE ROUTING ---
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;
    if (!text) return;

    const lowerText = text.toLowerCase();

    // Chunking helper
    const sendChunks = (outputStr, formatMsg = false) => {
        if (!outputStr) return;
        const chunks = outputStr.match(/[\s\S]{1,4000}/g) || ["(No Output)"];
        chunks.forEach(chunk => {
            bot.sendMessage(chatId, formatMsg ? `\`\`\`bash\n${chunk}\n\`\`\`` : chunk, formatMsg ? { parse_mode: 'Markdown' } : {});
        });
    };

    try {
        // --- ROUTE 1: RAW SYSTEM COMMAND ---
        if (text.startsWith('!sys ')) {
            const cmd = text.replace('!sys ', '');
            exec(cmd, (error, stdout, stderr) => sendChunks(stdout || stderr || "Done.", true));
            return;
        }

        // --- ROUTE 2: CLAUDE EXECUTION (!claude) ---
        if (text.startsWith('!claude ')) {
            const prompt = text.replace('!claude ', '');
            bot.sendMessage(chatId, `🛠️ Senior Architect (Claude) assigned. Executing autonomously...`);
            const result = await executeClaude(prompt);
            sendChunks(result, false);
            return;
        }

        // --- ROUTE 3: SYSTEM EVOLUTION (!evolve / !audit) ---
        if (lowerText === '!evolve' || lowerText === '!audit') {
            bot.sendMessage(chatId, `🧬 Triggering Autonomous Evolution Protocol...`);
            const result = await executeGemini(`Execute the protocol defined in commands/monthly-audit.md.`);
            bot.sendMessage(chatId, `✅ Evolution Sequence Complete.`);
            sendChunks(result, false);
            return;
        }

        // --- ROUTE 4: BRAVO/GEMINI EXECUTION (DEFAULT) ---
        // Any message that isn't a specific !claude or !sys command defaults to Bravo/Gemini
        if (text.startsWith('!gemini ') || text.startsWith('!bravo ') || !text.startsWith('!')) {
            const prompt = text.replace(/^!(gemini|bravo) /, '');
            bot.sendMessage(chatId, `✨ Bravo (Gemini CLI) activated. Processing autonomously...`);
            const result = await executeGemini(prompt);
            sendChunks(result, false);
            return;
        }

    } catch (err) {
        bot.sendMessage(chatId, `❌ Router Error: ${err.message}`);
    }
});
