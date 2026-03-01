# MISTAKES LOG
> Every mistake logged with root cause and prevention. Check this BEFORE repeating a task type.

---

### 2026-02-27 — Pydantic `__future__` Syntax Error via Monkey Patching
**What happened:** A regex text replacement prepended `import typing` to `models.py` in the Late SDK cache, inadvertently moving `from __future__ import annotations` from line 1 to line 2. This caused a `SyntaxError` that prevented the whole MCP server from booting.
**Root cause:** Python inherently requires `__future__` module imports to appear at the absolute top of the file before any other code or imports. Monkey patching without checking for `__future__` headers violated this.
**Prevention:** Whenever monkey patching Python files, always use `sed` or regex to append lines *after* the `__future__` block, or explicitly check for its existence first. Never indiscriminately prepend to line 1.

### 2026-02-27 — Exceeded Twitter Character Limit via Late API
**What happened:** The API rejected the payload with "Tweet text is too long", throwing a 207 Multi-Status error where LinkedIn succeeded and Twitter failed.
**Root cause:** I failed to calculate the string length of the payload and cross-reference it with the target platform's specifications (Twitter max characters = 280) before attempting to submit the post.
**Prevention:** **PRE-FLIGHT CHECK PROTOCOL**: Before sending any content to an external API (like social media), calculate the exact payload length and assert it against the platform's known limitations. Do not guess or assume.

### 2026-02-27 — Powershell Output Redirection Encoding (UTF-16LE)
**What happened:** Reading a `>` redirected file output from PowerShell in Node.js failed because the `JSON.parse` could not interpret the string.
**Root cause:** PowerShell's default output encoding for `>` redirection is `UTF-16LE`, whereas Node expects `UTF-8` or standard ASCII. 
**Prevention:** Avoid `>` redirection in PowerShell when capturing command outputs for programmatic environments (like Node/Python). Use `Out-File -Encoding utf8` or, preferably, write the file explicitly within the tool script (e.g. `fs.writeFileSync`).

### 2026-02-27 — Inline JS String Escape Syntax Errors
**What happened:** A Node.js inline script (`node -e "..."`) crashed because unescaped single quotes within the JS payload conflicted with the outer command's execution context.
**Root cause:** Attempting to write complex JSON schemas or multi-line strings directly into terminal arguments creates parsing chaos.
**Prevention:** For complex requests or texts, always write a dedicated `.js` or `.py` file to disk using the file writer tool, run it traditionally (`node script.js`), and delete it afterward. Stop trying to golf inline scripts.

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
