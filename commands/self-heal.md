# SELF-HEALING & OPTIMIZATION PROTOCOL

This command must be executed during the **Session End** sequence of a workflow. It acts as a diagnostic framework to detect inefficiencies, correct bad patterns, consolidate memory, and make the AI software engineering loop faster, cheaper, and safer.

## 1. Context & Token Diagnostics ⚖️
- **Are we accumulating junk in the workspace?** Identify and delete any temporary scripts (`node -e` scripts written to disk, `.json` dumps from APIs, etc. e.g. `post_to_late.js`, `curl_output.txt`). Use specific tools over terminal processes for OS commands. 
- **Is `ACTIVE_TASKS.md` overloaded?** Close resolved tasks. Do not carry dead weight into the next session.
- **Did the agent "context-loop"?** Identify moments in the prompt history where you repeated a tool call or hit multiple errors on the same task. Determine *why* that loop occurred.

## 2. Hardening API & Platform Interactions 🛡️
- **Pre-Flight Sanity Checks:** Ensure any future script interacting with 3rd party architectures (X/Twitter, Facebook, internal microservices) validates constraints *first* (e.g. Check `payload.length > 280` or HTTP bounds). 
- **Escape Sequencing:** Reject using terminal-based inline string interpolation (e.g., `node -e "code"` or `python -c "code"`) for multiline objects. Mandate writing explicitly formatted structural files via `write_to_file`.
- **Powershell Interfacing Out-File:** Standardize UTF-8 interactions and prevent `>` pipe-redirection encoding errors (`UTF-16LE`) by removing bash hacks and prioritizing native IDE file IO tools.

## 3. Code & State Verification 🛠️
- **Monkey Patching Protocol:** If code was manually injected or patched (e.g., into `.py` or `.js` libraries via regex/replacements), explicitly run syntactic verification commands (`python -m compileall <file>` or `node -c <file>`) immediately. Catch `SyntaxError`s before the module is requested by a client.
- **Dependency Cleanliness:** Run a quick check on package.json or uv caches. Do we have dangling dependencies? 

## 4. Pattern Distillation 📕
- Extract the 1-2 key technical takeaways from the current session and log them into `memory/PATTERNS.md` (What worked well) and `memory/MISTAKES.md` (What failed and exactly how to prevent it, focusing on root causes, not symptoms).
- Once logged, trigger the `/commands/condense.md` rollover protocol if the logs are getting too large.

---
*End of process. Present a brief summary of self-diagnostics to the user.*
