# SOP LIBRARY — Standard Operating Procedures

> SOPs are born from repeated patterns. When Bravo does the same thing 3+ times, it becomes an SOP.
> Each SOP has a success rate tracked over executions.

## SOP Format

```
### SOP-[ID]: [Name]
**Category:** [content/code/deploy/research/automation/admin]
**Trigger:** [What activates this SOP]
**Steps:**
1. [Step]
2. [Step]
3. [Step]
**Success Criteria:** [How to know it worked]
**Executions:** [count] | **Success Rate:** [percentage]
**Last Executed:** [date]
```

## Active SOPs

### SOP-001: Social Media Content Creation & Publishing
**Category:** content
**Trigger:** CC says "Content:" or "Post:" or /content command
**Steps:**
1. Map the request to one of CC's 5 content pillars
2. Write in CC's authentic voice (direct, no hustle-culture, transformation-focused)
3. Open with 2-second hook (pattern interrupt or bold statement)
4. Generate platform-specific versions:
   - X: Max 280 chars (including spaces, URLs, mentions)
   - LinkedIn: Max 3000 chars, professional but personal tone
   - Instagram: Max 2200 chars, visual-first messaging
   - TikTok: Max 4000 chars
   - Threads: Max 500 chars
5. Validate character count for EACH platform version
6. Present to CC for approval
7. Post via Late MCP (posts_create or posts_cross_post)
8. Log result in SESSION_LOG
**Success Criteria:** Post published, no character limit rejections, CC approves content
**Executions:** 2 | **Success Rate:** 50% (1st attempt failed on X char limit)
**Last Executed:** 2026-02-27

### SOP-002: Systematic Bug Investigation
**Category:** code
**Trigger:** CC reports a bug, /debug command, error in logs
**Steps:**
1. Read the error message/description carefully
2. Hypothesize the root cause (don't guess — reason from evidence)
3. Search codebase for relevant files (Grep/Glob)
4. Read the files, trace the logic
5. Identify the root cause with evidence
6. Apply minimal fix
7. Verify: build passes, no regressions
8. If fix fails after 3 attempts → STOP, report findings to CC
9. Log mistake + pattern to memory files
**Success Criteria:** Bug fixed, build passes, root cause documented
**Executions:** 3 | **Success Rate:** 100%
**Last Executed:** 2026-02-27

### SOP-003: Session Start Protocol (Heartbeat)
**Category:** admin
**Trigger:** Session begins
**Steps:**
1. Read brain/SOUL.md (identity check)
2. Read brain/STATE.md (current operational state)
3. Read memory/ACTIVE_TASKS.md (pending work)
4. Read memory/SESSION_LOG.md (last 3 entries)
5. Check git status
6. Report heartbeat status to CC
7. Await orders
**Success Criteria:** Bravo is oriented, CC knows system status
**Executions:** 0 | **Success Rate:** N/A (new SOP)
**Last Executed:** N/A

### SOP-004: Session End Protocol (Self-Heal)
**Category:** admin
**Trigger:** Session ending, /self-heal command
**Steps:**
1. Scan for junk files in project root (*.js, *.txt, *.log, debug dumps)
2. Check for uncommitted changes (git status)
3. Update memory/ACTIVE_TASKS.md (mark completed, flag blocked)
4. Append to memory/SESSION_LOG.md
5. Extract new patterns → memory/PATTERNS.md
6. Extract new mistakes → memory/MISTAKES.md
7. Update brain/STATE.md with final state
8. Compress SESSION_LOG if > 200 lines
**Success Criteria:** Workspace clean, memory updated, state current
**Executions:** 2 | **Success Rate:** 100%
**Last Executed:** 2026-02-28

---

## SOP Promotion Pipeline

*Patterns are promoted to SOPs after 3+ executions with consistent steps.*

| Candidate Pattern | Observations | Status |
|-------------------|-------------|--------|
| Playwright research → brief synthesis | 0 | Watching |
| Git branch → PR → Vercel preview | 1 | Watching |
| Client onboarding flow | 0 | Template exists |
| n8n workflow creation | 0 | Template exists |

## Retired SOPs

*SOPs that are no longer relevant. Kept for reference.*

(None yet)
