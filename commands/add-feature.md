Plan and implement a new feature. Follow this process:

1. Understand the feature request: $ARGUMENTS
2. Read existing code in the affected area — check for existing patterns
3. Create a feature branch: `git checkout -b feature/[descriptive-name]`
4. Write a brief implementation plan (3-5 steps max) — save to PLAN.md in the project
5. Implement the feature step by step
6. Add error handling and edge case coverage
7. Run `npm run build` — if it fails, fix before continuing
8. Check: no hardcoded secrets, mobile responsive (if frontend), no `console.log` in production code
9. Stage and commit with a descriptive message
10. Update `memory/ACTIVE_TASKS.md` to reflect completion
11. Report what was built and any follow-up items needed

Ask ONE clarifying question if the requirement is genuinely ambiguous. Otherwise, just build it.
If ANY step fails, stop and report the error. Do not skip steps.
