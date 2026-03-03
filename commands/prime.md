---
description: Load full project context and build comprehensive codebase understanding
---

# Prime: Load Project Context

## 1. Core Documentation
Read silently (do NOT output raw contents to CC):
- `brain/SOUL.md` — Identity and values
- `brain/STATE.md` — Current operational state
- `brain/USER.md` — CC's profile and preferences
- `memory/ACTIVE_TASKS.md` — What's in progress
- `memory/PATTERNS.md` — Proven approaches
- `memory/MISTAKES.md` — Known pitfalls

## 2. Project Structure
Map the directory structure:
```bash
git ls-files | head -100
```

## 3. Current State
```bash
git log -10 --oneline
git status
git branch --show-current
```

## 4. Infrastructure Health
- Check MCP server connectivity (attempt a simple call to each)
- Check .env.agents exists and has expected keys (by name, never log values)
- Check package.json for any issues

## 5. Output Report
Provide a concise summary:

| Dimension | Status |
|-----------|--------|
| **Branch** | {current branch} |
| **Recent Work** | {last 3 commits summary} |
| **Active Tasks** | {count pending, count blocked} |
| **Known Issues** | {from STATE.md} |
| **MCP Health** | {which servers responding} |

**Top 3 priorities from ACTIVE_TASKS.md:**
1. ...
2. ...
3. ...

**Ready for work. What's the focus?**
