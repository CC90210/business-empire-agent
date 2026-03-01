# MONTHLY AI SYSTEM AUDIT & EVOLUTION PROTOCOL
**Trigger:** Executed manually via the IDE, via n8n cron job on the 1st of every month, or via Telegram `!audit`.
**Purpose:** Ensure the AI framework (Bravo), core directives, tools, and CC's Profile adapt continuously to CC's entrepreneurial growth, technical stack changes, and personal state.

## PHASE 1: Data Aggregation & Pattern Recognition
1. **Read Logs:** Scan `memory/SESSION_LOG.md` and `memory/MISTAKES.md` for the past 30 days.
2. **Frequency Analysis:** Identify the top 3 recurring errors or friction points in workflow execution.
3. **Growth Trajectory:** Read `references/CC_PROFILE.md` and assess if the user's focus has shifted (e.g., from cold calling to product scaling, or from one SaaS to another).

## PHASE 2: Codebase & Cost Optimization (Self-Healing)
1. **Script Validation:** Review all active NodeJS scripts (like `telegram_agent.js`) for deprecated packages, security flaws, or inefficient API calls.
2. **Performance Check:** Ensure no giant files or `.gguf` local models have accidentally been downloaded into the main `Business-Empire-Agent` directory. (Run structure checks).
3. **Execution Routing:** Verify if a workflow currently relying on Claude/Claude Code API can be structurally offloaded to the free local Ollama endpoint to save costs without sacrificing output quality.

## PHASE 3: System Directive Updates (The Evolution)
1. **Profile Calibration:** Edit `references/CC_PROFILE.md`. Add any newly established traits, newly acquired companies, or updated personal goals discovered in the chat logs.
2. **Constraint Patching:** Edit `AGENT_CORE_DIRECTIVES.md`. Add new Anti-Patterns to the BANNED list based on the Phase 1 frequency analysis to prevent repetitive future failures.
3. **Skill Upgrades:** Create or update `skills/[skill-name].md` files if CC has requested new technological frameworks over the past month.

## PHASE 4: The Board Report
Generate `AUDIT_REPORT_YYYY_MM.md` and deliver it to CC. The report must contain:
1. **Financial Optimization:** Dollars saved / API efficiency updates.
2. **Evolution Summary:** What new traits or rules Bravo has officially adopted this month.
3. **Codebase Health:** Repaired scripts, compacted logs, and deleted temp files.
4. **Actionable Suggestions:** 3 recommendations for CC to improve his operations next month.
