# LEARNED PATTERNS
> What works, what doesn't. Check this BEFORE starting a task type you've done before.

## Effective Patterns

### Late API Posting Workflow
**Context:** When CC says "post this" or "schedule this" to any social platform
**Pattern:** 1) Validate char limits per platform → 2) Rewrite condensed versions for short platforms (X=280) → 3) Present all versions to CC → 4) Post via Late MCP → 5) Log to SESSION_LOG
**Why it works:** Prevents API rejections and ensures platform-optimized content

### Multi-Agent Task Routing
**Context:** Any task that comes into the workspace
**Pattern:** Simple/isolated tasks → Blackbox or Gemini. Multi-file architecture → Claude Code. Research → Anti-Gravity (has Playwright). Content → Any (all read AGENT_CORE_DIRECTIVES)
**Why it works:** Cost-efficient — Haiku/Gemini for grunt work, Opus for the heavy lifting

### GitHub Remote Edit Strategy
**Context:** When deploying changes to client repos (PropFlow, Nostalgic Requests, OASIS)
**Pattern:** Use GitHub MCP to branch → edit files remotely → open PR → Vercel auto-deploys preview → CC visually confirms → merge
**Why it works:** Saves disk space (no local clones), instant Vercel previews, clean git history

### MCP Error Recovery
**Context:** Any MCP server returns an error
**Pattern:** 1) Report exact error code + message → 2) Check if auth-related (401) or schema-related → 3) Suggest specific fix → 4) STOP. Never retry in a loop. Never create bypass scripts.
**Why it works:** Prevents junk file creation and infinite retry loops that waste context

## Anti-Patterns (NEVER Do These)

### Creating Bypass Scripts When MCP Fails
**What it looks like:** MCP call fails → agent writes a direct_post.js or similar file to call the API directly
**Why it fails:** Creates junk files, exposes API keys, clutters workspace
**Do this instead:** Report the error, suggest the fix, STOP

### Posting Identical Content Across Platforms
**What it looks like:** Same exact text sent to X, LinkedIn, Instagram
**Why it fails:** Each platform has different char limits, audience, and tone expectations
**Do this instead:** Rewrite per platform. Same core message, different delivery.

### Guessing Library APIs Without Context7
**What it looks like:** Agent writes code using method names from training data
**Why it fails:** Libraries change. Training data is stale.
**Do this instead:** Always call Context7 to verify current API before writing code
