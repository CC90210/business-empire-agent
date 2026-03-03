---
description: Check project status — revenue, tasks, MCP health, and system state
---
// turbo-all

## Steps

1. Read `brain/STATE.md` for current operational state (do NOT output raw contents — summarize).

2. Read `memory/ACTIVE_TASKS.md` for pending work.

3. Quick MCP health check — call one tool from each server to verify:
   - `mcp_n8n-mcp_search_workflows` (limit=1)
   - `mcp_late_posts_list` (limit=1)
   - `mcp_memory_search_nodes` (query="bravo")
   - `mcp_context7_resolve-library-id` (libraryName="react", query="test")

4. Report to CC in this format:
   ```
   ## Status — [date]
   **North Star:** $X / $1,000 Net MRR
   **Active Tasks:** [count] — [top 3 tasks]
   **MCP Health:** [X/8 servers responding]
   **Known Issues:** [any blockers]
   ```
