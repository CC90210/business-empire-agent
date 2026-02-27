Execute the "Remote Vercel Pipeline" Deployment Strategy. Follow these steps exactly:

1. Validate the targeted Repository and the specific files to be edited.
2. If working remotely (no local clone), use the **GitHub MCP** to create a new feature branch from `main`.
3. Use the GitHub MCP to push file updates directly to the new branch. 
4. If working locally with a clone, run `npm run build` and `npm run lint` first, then stage and push via Bash Git.
5. Create a Pull Request (PR) from your feature branch to `main`.
6. Provide CC with the PR link. Inform CC that Vercel is generating a "Preview Deployment" build.
7. PAUSE. Wait for CC's confirmation that the Preview Deployment successfully built and visually functions as expected.
8. If the build or features failed, read the Vercel logs or the Vercel preview site, fix the issues remotely, and push updates to the branch.
9. Upon CC's explicit approval, use the GitHub MCP to merge the PR into `main`, which will trigger the Production Vercel Build.
10. Log the successful deployment to `memory/SESSION_LOG.md`.
