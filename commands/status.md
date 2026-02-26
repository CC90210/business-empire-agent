Give me a quick status report on this project:

1. Check `git status` — any uncommitted changes?
2. Check `git log --oneline -5` — what were the last 5 commits?
3. Check if `npm run build` succeeds without errors
4. Check which branch we're on
5. List any TODO or FIXME comments in the codebase: `grep -r "TODO\|FIXME" --include="*.ts" --include="*.tsx" --include="*.js" -l`
6. Check package.json for outdated critical dependencies

Give me a clean summary in a table format. Keep it brief.
