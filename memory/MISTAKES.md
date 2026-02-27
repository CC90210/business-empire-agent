# MISTAKES LOG
> Every mistake logged with root cause and prevention. Check this BEFORE repeating a task type.

---

### 2026-02-27 — Late MCP Pydantic Schema Crash
**What happened:** Late API returns `profileId` as a dict object, but the Late Python SDK Pydantic models expect a string. Calls to `accounts_list`, `profiles_list`, `posts_list` fail with validation errors.
**Root cause:** Late API schema changed; SDK models not updated.
**Prevention:** Before using Late list operations, test with a single call first. If Pydantic error occurs, report to CC — do NOT patch SDK files from within agent code.

### 2026-02-27 — X/Twitter Post Rejected for Length
**What happened:** Content drafted for LinkedIn (3000 char limit) was sent to X (280 char limit). Late API returned Error Code 207 "Tweet text is too long."
**Root cause:** No per-platform character validation before posting.
**Prevention:** ALWAYS validate content length against platform limits BEFORE calling Late MCP. See social-publisher.md for the limits table.

### 2026-02-27 — __future__ Import Ordering Broke Late MCP Server
**What happened:** Patching Pydantic models in uv cache to fix profileId pushed `from __future__ import annotations` to line 2 instead of line 1, causing a Python SyntaxError on server boot.
**Root cause:** `__future__` imports must be the first statement in a Python file. The patch inserted an import above it.
**Prevention:** When patching Python SDK files, NEVER insert code above the `__future__` import line. Verify the file loads after patching: `python -c "import module"`.

---
