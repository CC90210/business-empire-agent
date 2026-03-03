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

console.log(`[${new Date().toISOString()}] Bravo Telegram Router V5.5 starting...`);
console.log(`[${new Date().toISOString()}] Workspace: ${process.cwd()}`);
console.log(`[${new Date().toISOString()}] Waiting for messages from CC...`);

// System context loading removed — prompt wrapper now handles context.
// Brain files are loaded by the CLI agent via GEMINI.md / CLAUDE.md if needed.

// --- AUTONOMOUS PROMPT WRAPPER (V5.5 — WAT Query-First) ---
const getAutonomousPrompt = (userPrompt) => {
    return `You are BRAVO V5.5, CC's AI assistant. This is a Telegram message — CC expects a SHORT, DIRECT answer.

IMPORTANT RULES:
1. ANSWER THE QUESTION using MCP tools. Keep it under 5 sentences for simple queries.
2. Do NOT read brain files, do NOT dump state, do NOT write audit reports.
3. Do NOT describe your thought process. Just give the answer.
4. If an MCP tool fails, say the error in ONE sentence.
5. If CC asks for a report or summary, read memory/ACTIVE_TASKS.md and brain/STATE.md, then summarize the key action items in a SHORT bullet list.

CC's question: ${userPrompt}`;
};

// --- CLI EXECUTION ENGINES ---
const EXEC_TIMEOUT = 120000; // 2 minutes max per CLI execution

const executeClaude = (promptText) => {
    return new Promise((resolve) => {
        const safePrompt = getAutonomousPrompt(promptText).replace(/"/g, '\\"');
        const cmd = `npx @anthropic-ai/claude-code -p "${safePrompt}" --dangerously-skip-permissions --no-user-prompt`;

        exec(cmd, { env: { ...process.env, CI: 'true', NONINTERACTIVE: 'true' }, timeout: EXEC_TIMEOUT }, (error, stdout, stderr) => {
            if (error && error.killed) resolve("Timed out after 2 minutes. Try a simpler query or use !sys for direct commands.");
            else resolve(stdout || stderr || "Done.");
        });
    });
};

const executeGemini = (promptText) => {
    return new Promise((resolve) => {
        const safePrompt = getAutonomousPrompt(promptText).replace(/"/g, '\\"');
        const cmd = `gemini "${safePrompt}" --approval-mode yolo`;

        exec(cmd, { env: { ...process.env }, timeout: EXEC_TIMEOUT }, (error, stdout, stderr) => {
            if (error && error.killed) resolve("Timed out after 2 minutes. Try a simpler query or use !sys for direct commands.");
            else resolve(stdout || stderr || "Done.");
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
