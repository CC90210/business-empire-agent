---
description: Smart git commit with conventional format and staged file analysis
---
// turbo-all

## Steps

1. Run `git status --short` to see what's changed.

2. Run `git diff --stat` to see the scope of changes.

3. Analyze the changes and generate a conventional commit message:
   - Format: `bravo: type — description`
   - Types: `feat`, `fix`, `refactor`, `docs`, `config`, `content`, `chore`
   - Keep description under 72 chars

4. Stage the appropriate files:
   - Run `git add [files]` — stage only relevant files, not junk
   - NEVER stage `.env`, `.env.agents`, or files with secrets

5. Show CC the proposed commit message and staged files. Wait for approval.

6. Run `git commit -m "[message]"`.

7. Report: "Committed: [message] — [X] files changed."

8. Ask CC if they want to push (NEVER push to main/master directly — create a branch or PR).
