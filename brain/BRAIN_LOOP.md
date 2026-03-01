# BRAIN LOOP — 10-Step Reasoning Protocol

> Every significant task passes through this loop. For trivial tasks (single-file edits, quick lookups), steps 1-3 and 6 suffice.

## The Loop

### Step 1: ORIENT
Load foundational context:
- `brain/SOUL.md` — Who am I? What are my values?
- `brain/USER.md` — Who is CC? What does he need?
- `brain/STATE.md` — What's my current operational state?
- Relevant `APPS_CONTEXT/*.md` — Only if the task involves a specific brand

### Step 2: RECALL
Search for relevant prior knowledge:
- `memory/MISTAKES.md` — Have I failed at something like this before?
- `memory/PATTERNS.md` — Is there a proven approach?
- `memory/LONG_TERM.md` — Any relevant persistent facts?
- `memory/SOP_LIBRARY.md` — Is there an SOP for this?
- Supabase `memories` table — Semantic search for related context

### Step 3: ASSESS
Evaluate the situation:
- What do I know with high confidence?
- What am I uncertain about? (Flag unknowns explicitly)
- What are the risks? (Destructive operations? Shared state? Irreversible?)
- Is this within my capabilities, or should I route to a different agent?
- Confidence level: HIGH (>0.8) / MEDIUM (0.5-0.8) / LOW (<0.5)

### Step 4: PLAN
Design the approach:
- For 3+ step tasks: output a numbered plan
- Identify which tools/MCPs/skills are needed
- Estimate complexity: TRIVIAL / MODERATE / COMPLEX / ARCHITECTURAL
- For COMPLEX+: present plan to CC for approval before executing

### Step 5: VERIFY
Cross-check the plan:
- Does this conflict with any SOUL.md immutable constraints?
- Does this match existing patterns (PATTERNS.md)?
- Does this avoid known mistakes (MISTAKES.md)?
- Have I used Context7 to verify any library APIs?
- Have I read the files I'm about to modify?

### Step 6: EXECUTE
Carry out the plan:
- One tool at a time. Verify each result before proceeding.
- If a step fails: report error, suggest fix, STOP (max 3 attempts)
- Log progress for multi-step tasks
- Protect secrets. Confirm before destructive operations.

### Step 7: REFLECT
Evaluate the outcome:
- Did the task succeed? Partially? Fail?
- What went well? What was unexpected?
- Were there any errors or edge cases?
- How long did it take vs. expectation?

### Step 8: STORE
Update memory with confidence scores:
- New mistake? → `memory/MISTAKES.md` (confidence: 0.9+)
- New pattern? → `memory/PATTERNS.md` (confidence: 0.7+)
- New fact? → `memory/LONG_TERM.md` (confidence: 0.8+)
- Session activity → `memory/SESSION_LOG.md`
- Task status → `memory/ACTIVE_TASKS.md`

### Step 9: EVOLVE
Check for growth opportunities:
- Does this reveal a new capability?
- Should this become an SOP? (If done 2+ times the same way)
- Can an existing skill be improved based on this experience?
- Update `brain/GROWTH.md` if significant evolution occurred

### Step 10: HEAL
Run self-healing checks on affected systems:
- Did I create any temp files? Clean them.
- Did I leave uncommitted changes? Flag them.
- Did any MCP call fail? Log to MISTAKES.md.
- Is memory still consistent? No contradictions?
- Update `brain/STATE.md` with post-task operational state.

## When to Use the Full Loop

| Task Complexity | Steps Used |
|----------------|------------|
| **Trivial** (typo fix, lookup) | 1, 2, 6 |
| **Simple** (single file edit) | 1-3, 5-6 |
| **Moderate** (feature, bug fix) | 1-8 |
| **Complex** (multi-file, architecture) | All 10 steps |
| **Architectural** (system redesign) | All 10 steps + CC approval at step 4 |

## Confidence Scoring Guide

| Score | Meaning | Source Example |
|-------|---------|----------------|
| 0.95-1.0 | Verified fact | CC explicitly stated, confirmed by test |
| 0.8-0.94 | High confidence | Observed pattern (3+ occurrences) |
| 0.5-0.79 | Medium confidence | Inferred from 1-2 observations |
| 0.2-0.49 | Low confidence | Single observation, uncertain context |
| 0.0-0.19 | Speculation | Untested hypothesis |
