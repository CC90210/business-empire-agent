---
description: Full system health diagnostic — test all MCP servers, check configs, verify file integrity
---
// turbo-all

## Steps

1. **Test every MCP server** by calling one tool each:
   - n8n-mcp: `mcp_n8n-mcp_search_workflows` (limit=1)
   - Late: `mcp_late_accounts_list`
   - Supabase: `mcp_supabase_list_tables` (if available)
   - Stripe: Any Stripe MCP tool (if available)
   - Playwright: `mcp_playwright_browser_snapshot` (if page open)
   - Context7: `mcp_context7_resolve-library-id` (libraryName="test", query="test")
   - Memory: `mcp_memory_search_nodes` (query="bravo")
   - Sequential Thinking: `mcp_sequential-thinking_sequentialthinking` (simple thought)

2. **Check config sync** — verify these files exist and have matching server configs:
   - `.vscode/mcp.json` (Antigravity)
   - `.claude/mcp.json` (Claude Code)
   - `.gemini/settings.json` (Gemini CLI)

3. **Check brain files** — verify these exist and aren't stale:
   - `brain/STATE.md`
   - `brain/SOUL.md`
   - `brain/CAPABILITIES.md`
   - `memory/ACTIVE_TASKS.md`

4. **Report results** in a table:
   ```
   | Server | Status | Response |
   |--------|--------|----------|
   | n8n    | ✅/❌  | [detail] |
   | Late   | ✅/❌  | [detail] |
   | ...    | ...    | ...      |
   ```

5. If any server is broken, **fix it** (update the config file directly). Do NOT just report it.
