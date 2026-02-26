Debug the issue described below. Follow this process exactly:

1. Read the error message or bug description: $ARGUMENTS
2. Search the codebase for the relevant files — read them, do not assume contents
3. Identify the root cause from actual code and logs
4. Apply a minimal fix — do NOT refactor unrelated code
5. Run `npm run build` to verify the fix compiles
6. If the fix fails: log the attempt, try again (max 3 attempts total)
7. If still broken after 3 attempts: STOP. Report what you tried, what the error still is, and your best theory
8. On success: commit with a descriptive message
9. Report what was wrong and what you changed in 2-3 sentences
10. If the bug was caused by agent error, log to `memory/MISTAKES.md`
