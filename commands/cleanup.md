Scan for and remove junk files from the workspace.

PROCEDURE:
1. Scan root directory for files matching DELETE criteria:
   - *.js files (one-off scripts, failed automation)
   - *.txt files (debug/path artifacts)
   - *.log files
   - *.json debug dumps (mcp_out.json, late_tools.json, etc.)
   - Files with _raw_, _err_, _res_ in name
   - Any 0-byte empty files outside of skills/ (Python __init__.py are valid)

2. Present the full list to CC with file sizes:
   ```
   CLEANUP SCAN — [date]
   Files flagged for deletion:
   1. [filename] — [size] — [reason]
   ...
   Total: [X] files, [Y] bytes
   ```

3. WAIT for CC's approval before deleting anything. Do NOT auto-delete.

4. After deletion, run a verification scan to confirm clean state.

5. Report:
   ```
   CLEANUP COMPLETE
   Deleted: [X] files ([Y] bytes freed)
   Remaining: [Z] files in root (all valid)
   ```

PROTECTED FILES (never delete):
- README.md, AGENT_CORE_DIRECTIVES.md, AGENT_SYSTEM_PROMPT.md
- ANTIGRAVITY_CHEAT_SHEET.md, AUDIT_REPORT.md
- .gitignore, .mcp.json, mcp_config.json
- Everything in skills/, agents/, commands/, memory/, APPS_CONTEXT/, references/
