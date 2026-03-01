# BRAVO ROUTING MAP — Context & Skill Requirements

> **PURPOSE:** This file is the "Equipping Station." When you receive a task, look up the task type here and load the "Required Context" and "Mandatory Skills" immediately.

## 1. Task Type: [DEBUG]
*   **Context:** `memory/MISTAKES.md`, `memory/PATTERNS.md`, Project-specific code files.
*   **Skills:** `skills/systematic-debugging/`, `skills/self-healing/`.
*   **Command:** `/debug`.
*   **Mindset:** Root Cause Analysis (RCA). Reproduce before fixing.

## 2. Task Type: [CONTENT]
*   **Context:** `brain/USER.md`, `references/CC_PROFILE.md`, `APPS_CONTEXT/CONTENT_BRAND_CLAUDE.md`.
*   **Skills:** `skills/writing-skills/`, `skills/brainstorming/`.
*   **Command:** `/content`, `/post`.
*   **Mindset:** 5 Pillars of CC. Authentic voice. No hustle-culture jargon.

## 3. Task Type: [ARCHITECT]
*   **Context:** `brain/BRAIN_LOOP.md`, `database/001_bravo_agent_schema.sql`.
*   **Skills:** `skills/sequential-reasoning/`, `skills/executing-plans/`.
*   **Command:** `/add-feature`.
*   **Mindset:** ADR (Architecture Decision Record). Multi-project synchronicity.

## 4. Task Type: [GROWTH]
*   **Context:** `brain/GROWTH.md`, `brain/STATE.md`.
*   **Skills:** `skills/growth-engine/`, `skills/memory-management/`.
*   **Mindset:** Aggressive Revenue Generation. Efficiency over features.

---

## ANTI-LOOP PROTOCOL (For High-Speed Models)
1.  **Search once, verify once.** If a file is found, assume its content is valid for the current step.
2.  **State Confidence.** If confidence is >0.8, proceed to execution. Do not run redundant "check status" commands.
3.  **Direct Action.** Prefer `write_file` or `replace` over multiple rounds of `grep`.
