Run a full workspace health check and report status.

PROCEDURE:
1. Scan root for junk files (*.js, *.txt, *.log, *.json debug dumps) — list any found
2. Check directory structure matches expected layout in AGENT_SYSTEM_PROMPT.md
3. Test MCP connections: Late (posts_list), Supabase (list_projects), n8n (search_workflows), Playwright (navigate to about:blank), Context7 (resolve next.js), Memory (read_graph)
4. Check git status — branch, uncommitted changes, unpushed commits
5. Read memory/ACTIVE_TASKS.md — list any stale tasks (older than 7 days)
6. Verify .gitignore covers standard patterns

OUTPUT FORMAT:
```
HEALTH CHECK — [date]
━━━━━━━━━━━━━━━━━━━━━━━━
Workspace:    [CLEAN / X junk files found]
Structure:    [VALID / issues]
MCP Servers:  [X/7 connected]
  - Late:     [status]
  - Supabase: [status]
  - n8n:      [status]
  - Playwright: [status]
  - Context7: [status]
  - Memory:   [status]
  - Seq Think: [status]
Git:          [branch] — [clean / X uncommitted]
Memory:       [X active tasks, Y stale]
```

Do NOT fix anything — report only. CC decides what to act on.
