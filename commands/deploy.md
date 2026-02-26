Deploy the current project to production. Follow these steps exactly:

1. Run the linter and fix any issues: `npm run lint`
2. Run the build to check for errors: `npm run build`
3. Run tests if they exist: `npm test` (skip if no test script)
4. Stage all changes: `git add .`
5. Commit with this message: $ARGUMENTS
6. Push to the current branch
7. If we're on a feature branch, create a pull request to main with a clear description
8. Report back what was deployed and any issues found

If ANY step fails, stop and report the error. Do not continue to the next step.
