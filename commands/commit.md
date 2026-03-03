---
description: Smart commit with change analysis and conventional commit format
---

# Commit Changes

## Step 1: Analyze Changes
```bash
git status
git diff HEAD
git diff --cached
```

## Step 2: Categorize
Determine commit type from the changes:
- `feat` — New feature or capability
- `fix` — Bug fix
- `refactor` — Code restructuring (no behavior change)
- `docs` — Documentation only
- `style` — Formatting, no code change
- `test` — Adding or updating tests
- `chore` — Build process, dependencies, config
- `perf` — Performance improvement

## Step 3: Stage
- Stage ONLY relevant files (no `.env`, credentials, or junk)
- If changes span multiple concerns, suggest splitting into multiple commits
- Never stage files that likely contain secrets

## Step 4: Commit
Format: `bravo: {type} — {concise description}`

Examples:
- `bravo: feat — add Playwright browser automation skill`
- `bravo: fix — resolve FFmpeg path resolution on Windows`
- `bravo: refactor — streamline MCP routing in CLAUDE.md`

## Step 5: Verify
```bash
git log -1 --oneline
git status
```

Confirm clean working tree or list remaining unstaged changes.

## Rules
- NEVER commit .env files or credentials
- NEVER amend without CC's explicit approval
- NEVER force push
- If pre-commit hook fails: fix the issue, create a NEW commit
- Update memory/ACTIVE_TASKS.md if the commit completes a tracked task
