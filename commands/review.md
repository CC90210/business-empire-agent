Review the current codebase or recent changes. Focus:

1. Check `git diff` or `git log --oneline -10` for recent changes
2. Read the actual files — do NOT review from memory
3. Check for:
   - **Security:** hardcoded secrets, missing auth checks, unvalidated inputs
   - **Error handling:** missing try/catch, unhandled promise rejections, no user-facing error messages
   - **Type safety:** TypeScript `any` types, missing type definitions
   - **Performance:** unnecessary re-renders, N+1 queries, missing pagination
   - **Dead code:** unused imports, unreachable code, TODO/FIXME comments
4. Verify: environment variables used for all secrets, error messages are user-friendly
5. Rate the code quality 1-10 with specific justification
6. List the top 3 most important improvements to make, with file:line references
7. Log any patterns discovered to `memory/PATTERNS.md`

Be honest and direct. Do not sugarcoat problems.
