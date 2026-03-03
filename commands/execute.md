---
description: Execute an implementation plan step by step
argument-hint: [path-to-plan]
---

# Execute: $ARGUMENTS

## Step 1: Load Plan
Read the plan file. If no path given, check `.agents/plans/` for the most recent plan.

## Step 2: Critical Review
- Read the ENTIRE plan
- Understand all tasks and dependencies
- Note validation commands
- If concerns: raise with CC before starting
- If no concerns: create TodoWrite and proceed

## Step 3: Execute Tasks
For each task in the plan:
1. Mark as in_progress in TodoWrite
2. Read existing related files before modifying
3. Implement exactly per spec — no "while I'm here" improvements
4. Run validation command specified in the task
5. If validation fails: fix, re-run. Max 3 attempts per task.
6. After 3 failures: STOP, report, ask CC
7. Mark as completed only after validation passes

## Step 4: Verification Gate
After each batch of 3 tasks:
- Run ALL validation commands from plan
- If any fail: fix before continuing
- Report progress to CC

## Step 5: Final Checklist
- All tasks from plan completed
- All validation commands pass
- Code follows project conventions (check memory/PATTERNS.md)
- No hardcoded secrets (check .env.agents pattern)
- No unnecessary console.log or debug code

## Step 6: Report
- Completed tasks (files created/modified)
- Validation results
- Any deviations from plan and why
- Ready for /commit

## Skills Integration
- **Use:** skills/executing-plans for batch execution
- **Use:** skills/verification-before-completion BEFORE claiming done
- **Use:** skills/systematic-debugging if a task fails
- **Use:** skills/subagent-driven-development for parallel task execution
