# BRAIN LOOP — 10-Step Reasoning Protocol (V5.5 Enhanced)

> Every significant task passes through this loop. For trivial tasks (single-file edits, quick lookups), steps 1-3 and 6 suffice.
> **V5.5 Enhancements:** Multi-hypothesis generation (LATS-inspired), structured Reflexion on failure, activation-scored memory retrieval, Supabase trace logging.

## The Loop

### Step 1: ORIENT
Load foundational context:
- `brain/SOUL.md` — Who am I? What are my values?
- `brain/USER.md` — Who is CC? What does he need?
- `brain/STATE.md` — What's my current operational state?
- Relevant `APPS_CONTEXT/*.md` — Only if the task involves a specific brand

### Step 2: RECALL (Activation-Scored Retrieval)
Search for relevant prior knowledge, prioritized by activation score (recency × 0.3 + frequency × 0.4 + confidence × 0.3):
- `memory/MISTAKES.md` — Have I failed at something like this before?
- `memory/PATTERNS.md` — Is there a proven `[VALIDATED]` approach?
- `memory/LONG_TERM.md` — Any relevant persistent facts?
- `memory/SOP_LIBRARY.md` — Is there an SOP for this? (Check execution count + success rate)
- `memory/SELF_REFLECTIONS.md` — Any prior reflections on this task type?
- Supabase `memories` table — Semantic search for related context
- Supabase `skill_activation` — Which skills/patterns are most active for this domain?

### Step 3: ASSESS
Evaluate the situation:
- What do I know with high confidence?
- What am I uncertain about? (Flag unknowns explicitly)
- What are the risks? (Destructive operations? Shared state? Irreversible?)
- Is this within my capabilities, or should I route to a different agent?
- Confidence level: HIGH (>0.8) / MEDIUM (0.5-0.8) / LOW (<0.5)

### Step 4: PLAN (Multi-Hypothesis — LATS-Inspired)
Design the approach using multi-hypothesis generation:
- For 3+ step tasks: output a numbered plan
- **Generate 2-3 candidate approaches** for MODERATE+ tasks (not just one)
- Rank approaches by: feasibility, risk, estimated effort, confidence
- Select the best approach, but **track alternatives** for backtracking on failure
- Identify which tools/MCPs/skills are needed
- Estimate complexity: TRIVIAL / MODERATE / COMPLEX / ARCHITECTURAL
- For COMPLEX+: present plan to CC for approval before executing
- For LOW confidence (<0.5): present plan AND alternatives to CC

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
- **Log each meaningful action** to Supabase `agent_traces` (Tier 1 logging)
- If a step fails: **try alternative approach from Step 4** before retrying same approach
- If all approaches fail after 3 total attempts → STOP, report findings to CC
- Log progress for multi-step tasks
- Protect secrets. Confirm before destructive operations.

### Step 7: REFLECT (Reflexion Protocol)
Evaluate the outcome using structured Reflexion (Shinn et al., 2023):
- Did the task succeed? Partially? Fail?
- What went well? What was unexpected?
- Were there any errors or edge cases?
- **On failure, generate structured reflection:**
  1. What was attempted? (task + approach)
  2. What went wrong? (specific failure point)
  3. Why did it fail? (root cause)
  4. What should be done differently? (concrete alternative)
  5. Confidence in this reflection? (0.0-1.0)
- Store reflection in `memory/SELF_REFLECTIONS.md` and Supabase
- Was my confidence calibrated correctly? (If I was 0.9 confident and failed → recalibrate)

### Step 8: STORE (Dual-Write: Files + Supabase)
Update memory with confidence scores — **write to both files AND Supabase:**
- New mistake? → `memory/MISTAKES.md` + Supabase `memories` (category='mistake')
- New pattern? → `memory/PATTERNS.md` (tag `[PROBATIONARY]`) + Supabase `memories` (category='pattern')
- New fact? → `memory/LONG_TERM.md` + Supabase `memories` (category='fact')
- Session activity → `memory/SESSION_LOG.md` + Supabase `session_logs`
- Task status → `memory/ACTIVE_TASKS.md`
- Interaction traces → Supabase `agent_traces`
- Self-modifications → `brain/CHANGELOG.md` + Supabase `self_modification_log`

### Step 9: EVOLVE (Voyager-Inspired Skill Growth)
Check for growth opportunities:
- Does this reveal a new capability? → Update `brain/GROWTH.md` capability timeline
- Should this become an SOP? (If done 3+ times the same way → create `[PROBATIONARY]` SOP)
- Can an existing skill be improved based on this experience?
- **Compositionality check**: Can this skill be built from existing simpler skills?
- **Activation update**: Increment access_count for any patterns/SOPs used in Supabase `skill_activation`
- Is this a genuinely novel solution? If yes, flag as skill library candidate

### Step 10: HEAL
Run self-healing checks on affected systems:
- Did I create any temp files? Clean them.
- Did I leave uncommitted changes? Flag them.
- Did any MCP call fail? Log to MISTAKES.md.
- Is memory still consistent? No contradictions?
- Update `brain/STATE.md` with post-task operational state.
- **Supabase sync**: Flush any pending traces, update agent_state
- **Git checkpoint**: If significant changes, stage + commit with `bravo: [verb] — [reason]`

## When to Use the Full Loop

| Task Complexity | Steps Used | Multi-Hypothesis? |
|----------------|------------|-------------------|
| **Trivial** (typo fix, lookup) | 1, 2, 6 | No |
| **Simple** (single file edit) | 1-3, 5-6 | No |
| **Moderate** (feature, bug fix) | 1-8 | Yes (2 approaches) |
| **Complex** (multi-file, architecture) | All 10 steps | Yes (2-3 approaches) |
| **Architectural** (system redesign) | All 10 steps + CC approval at step 4 | Yes (3 approaches + CC picks) |

## Confidence Scoring Guide

| Score | Meaning | Source Example | Autonomy Level |
|-------|---------|----------------|----------------|
| 0.95-1.0 | Verified fact | CC explicitly stated, confirmed by test | Full autonomy |
| 0.8-0.94 | High confidence | Observed pattern (3+ occurrences) | Full autonomy |
| 0.5-0.79 | Medium confidence | Inferred from 1-2 observations | Execute + show CC result |
| 0.2-0.49 | Low confidence | Single observation, uncertain context | Plan → CC approves → execute |
| 0.0-0.19 | Speculation | Untested hypothesis | Ask CC before anything |

## Failure Recovery Protocol

When the primary approach fails:
1. **Don't retry the same approach** — switch to the next ranked alternative from Step 4
2. If no alternatives were generated, **pause and generate them now**
3. After 3 total attempts across all approaches → **STOP and report to CC**
4. **Always generate a Reflexion entry** (Step 7) after any failure
5. The Reflexion is stored and retrieved next time a similar task is attempted (Step 2)
