# BRAVO ROUTING MAP — Context, Skills & MCP Routing

> **PURPOSE:** This file is the "Equipping Station." When you receive a task, look up the task type here and load the "Required Context" and "Mandatory Skills" immediately.

## MCP TOOL ROUTING (All Interfaces)

**RULE: When the user's query matches a topic below, call the corresponding MCP tool IMMEDIATELY. Do not theorize — call the tool and return real data.**

| User Asks About | MCP Server | Tools | Priority |
|---|---|---|---|
| n8n workflows, automations, triggers | **n8n-mcp** | `search_workflows`, `get_workflow_details`, `execute_workflow` | CALL FIRST |
| Social media posts, scheduling, accounts | **Late** | `posts_list`, `posts_create`, `accounts_list`, `posts_cross_post` | CALL FIRST |
| Database, SQL, tables, migrations | **Supabase** | `execute_sql`, `list_tables`, `apply_migration`, `list_projects` | CALL FIRST |
| Web browsing, scraping, screenshots | **Playwright** | `browser_navigate`, `browser_snapshot`, `browser_click` | CALL FIRST |
| Library docs, code examples | **Context7** | `resolve-library-id`, `query-docs` | CALL FIRST |
| Knowledge graph, persistent memory | **Memory** | `search_nodes`, `create_entities`, `open_nodes` | CALL FIRST |
| Complex multi-step reasoning | **Sequential Thinking** | `sequentialthinking` | USE FOR MODERATE+ |

---

## 1. Task Type: [DEBUG]
*   **Context:** `memory/MISTAKES.md`, `memory/PATTERNS.md`, Project-specific code files.
*   **Skills:** `skills/systematic-debugging/`, `skills/self-healing/`.
*   **Command:** `/debug`.
*   **MCP:** Supabase (for logs/traces), Playwright (for UI bugs).
*   **Mindset:** Root Cause Analysis (RCA). Reproduce before fixing.

## 2. Task Type: [CONTENT]
*   **Context:** `brain/USER.md`, `references/CC_PROFILE.md`, `APPS_CONTEXT/CONTENT_BRAND_CLAUDE.md`.
*   **Skills:** `skills/writing-skills/`, `skills/brainstorming/`.
*   **Command:** `/content`, `/post`.
*   **MCP:** Late (post/schedule), Playwright (research).
*   **Mindset:** 5 Pillars of CC. Authentic voice. No hustle-culture jargon.

## 3. Task Type: [ARCHITECT]
*   **Context:** `brain/BRAIN_LOOP.md`, `database/001_bravo_agent_schema.sql`.
*   **Skills:** `skills/sequential-reasoning/`, `skills/executing-plans/`.
*   **Command:** `/add-feature`.
*   **MCP:** Supabase (schema), Sequential Thinking (design).
*   **Mindset:** ADR (Architecture Decision Record). Multi-project synchronicity.

## 4. Task Type: [GROWTH]
*   **Context:** `brain/GROWTH.md`, `brain/STATE.md`.
*   **Skills:** `skills/growth-engine/`, `skills/memory-management/`.
*   **MCP:** Supabase (metrics), n8n (automations), Stripe (revenue).
*   **Mindset:** Aggressive Revenue Generation. Efficiency over features.

## 5. Task Type: [AUTOMATION]
*   **Context:** `brain/CAPABILITIES.md`, n8n workflow docs.
*   **Skills:** `skills/n8n-mcp-integration/`, `skills/n8n-patterns/`.
*   **Command:** `/build-workflow`.
*   **MCP:** n8n (search, execute, details).
*   **Mindset:** Workflow-first. Automate before manual.

## 6. Task Type: [SOCIAL]
*   **Context:** `brain/USER.md`, platform character limits.
*   **Skills:** `skills/writing-skills/`.
*   **Command:** `/post`.
*   **MCP:** Late (create, list, cross-post, accounts).
*   **Mindset:** Platform-native content. Validate char limits before posting.

---

## ANTI-LOOP PROTOCOL (For High-Speed Models)
1.  **Search once, verify once.** If a file is found, assume its content is valid for the current step.
2.  **State Confidence.** If confidence is >0.8, proceed to execution. Do not run redundant "check status" commands.
3.  **Direct Action.** Prefer `write_file` or `replace` over multiple rounds of `grep`.
4.  **Tool-First.** If an MCP tool can answer the question, call it. Do not describe what you would do.
