# SELF-REFLECTIONS — Agent Self-Assessment Log

> Bravo reflects after complex tasks, failures, and milestones.
> Quality gate: Only log reflections that are specific, evidence-based, novel, and useful.

## Reflection Format

```
### [Date] — [Trigger]
**What happened:** [Brief description]
**What I learned:** [Specific insight]
**What I'd do differently:** [Actionable change]
**Confidence in lesson:** [0.0-1.0]
```

## Reflections

### 2026-02-27 — First Live Social Media Posts
**What happened:** Published first LinkedIn + X posts via Late API. X post was rejected initially for exceeding 280 chars.
**What I learned:** Platform character limits must be validated BEFORE calling the API. The Late MCP doesn't validate for you.
**What I'd do differently:** Build character counting into the content creation flow, not as an afterthought.
**Confidence in lesson:** 0.95

### 2026-02-27 — Pydantic Monkey-Patching Failure
**What happened:** Tried to fix Late MCP by prepending code to a Python file. Broke __future__ imports.
**What I learned:** Never modify line 1 of Python files without checking for __future__ imports. Monkey-patching is fragile.
**What I'd do differently:** Read the target file first. Test the patch in isolation before applying.
**Confidence in lesson:** 0.95

### 2026-02-28 — Architecture Evolution (V4 → V5)
**What happened:** Researched OpenClaw architecture and designed enhanced brain/ directory system.
**What I learned:** File-based agent identity (SOUL.md) loaded at every reasoning cycle creates more consistent behavior than scattered directives. The heartbeat pattern enables proactive behavior without daemon mode.
**What I'd do differently:** Should have designed the brain/ architecture from V1 instead of retrofitting.
**Confidence in lesson:** 0.85

---

*New reflections are appended. Archive when >20 entries.*
