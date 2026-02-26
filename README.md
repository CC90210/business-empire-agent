# BUSINESS EMPIRE AGENT — Workspace Map

> This is the intelligence hub for CC's Business Empire Agent running in Anti-Gravity IDE. Project source code lives in external project directories — this folder contains only the agent's brain, skills, memory, and operating procedures.

---

## Directory Structure

```
Business-Empire-Agent/
│
├── AGENT_CORE_DIRECTIVES.md    ← The brain. Identity, rules, verification protocol, request routing, quality gates.
├── AUDIT_REPORT.md             ← Latest audit findings and file ratings.
├── ANTIGRAVITY_CHEAT_SHEET.md  ← CC's quick reference for talking to the agent.
├── README.md                   ← This file. Workspace map.
│
├── agents/                     ← Sub-agent definitions for task delegation
│   ├── explorer.md             ← Read-only codebase navigation (Haiku — cheap)
│   ├── writer.md               ← Code writing and implementation (Sonnet)
│   ├── debugger.md             ← Bug investigation and fixing (Sonnet)
│   ├── workflow-builder.md     ← n8n workflow creation (Sonnet)
│   ├── architect.md            ← System design decisions (Opus — use sparingly)
│   └── documenter.md           ← Documentation and logging (Haiku — cheap)
│
├── commands/                   ← Slash command workflows
│   ├── add-feature.md          ← /add-feature — plan and build a feature
│   ├── build-workflow.md       ← /build-workflow — create an n8n automation
│   ├── client-onboard.md       ← /client-onboard — onboard a new OASIS AI client
│   ├── debug.md                ← /debug — systematic bug fixing
│   ├── deploy.md               ← /deploy — lint, build, commit, push, PR
│   ├── review.md               ← /review — code quality audit
│   └── status.md               ← /status — project health check
│
├── memory/                     ← Persistent memory across sessions
│   ├── ACTIVE_TASKS.md         ← Read at session start. Current work in progress.
│   ├── SESSION_LOG.md          ← Appended at session end. What was done.
│   ├── DECISIONS.md            ← Architectural decisions with rationale.
│   ├── MISTAKES.md             ← Bugs and errors with root cause analysis.
│   └── PATTERNS.md             ← Proven approaches and anti-patterns.
│
├── skills/                     ← Skills library (GitHub repos + custom)
│   ├── n8n-patterns.md         ← Custom: n8n workflow patterns and JSON templates
│   ├── ai-integration.md       ← Custom: LLM API, RAG, and voice agent patterns
│   ├── supabase-patterns.md    ← Custom: database design, RLS, query patterns
│   ├── n8n-mcp-integration/    ← Custom: n8n MCP server integration skill
│   ├── brainstorming/          ← Superpowers: Socratic design refinement
│   ├── writing-plans/          ← Superpowers: detailed implementation planning
│   ├── executing-plans/        ← Superpowers: batch execution with checkpoints
│   ├── systematic-debugging/   ← Superpowers: 4-phase root cause debugging
│   ├── test-driven-development/← Superpowers: RED-GREEN-REFACTOR cycle
│   ├── subagent-driven-development/ ← Superpowers: fast iteration with review
│   ├── frontend-design/        ← Anthropic: avoid AI slop, bold design decisions
│   ├── mcp-builder/            ← Anthropic: build high-quality MCP servers
│   ├── webapp-testing/         ← Anthropic: Playwright browser testing
│   └── [28 more skill folders] ← Full Superpowers + Anthropic skills library
│
├── APPS_CONTEXT/               ← Per-business configuration files
│   ├── OASIS_AI_CLAUDE.md      ← OASIS AI Solutions context
│   ├── PROPFLOW_CLAUDE.md      ← PropFlow SaaS context
│   ├── NOSTALGIC_REQUESTS_CLAUDE.md ← Nostalgic Requests context
│   ├── CONTENT_BRAND_CLAUDE.md ← CC's personal brand context
│   ├── AI_TRAINING_CLAUDE.md   ← AI Training business context
│   └── OASIS_WORKFLOWS.md     ← n8n workflow registry (auto-updated)
│
└── references/                 ← Setup guides and original config files
    ├── Claude_Setup_Guide.md   ← Original setup instructions
    ├── Claude_Global_MCP.json  ← MCP server configurations
    ├── Claude_Global_Settings.json ← Claude Code settings reference
    └── awesome-claude-skills/  ← Skills discovery reference list
```

---

## Quick Start

1. **Agent reads `AGENT_CORE_DIRECTIVES.md`** — this is the operating system.
2. **Agent reads `memory/ACTIVE_TASKS.md`** — what's in progress.
3. **CC tells the agent what to work on** — the agent matches to a request routing workflow.
4. **Agent reads relevant `APPS_CONTEXT/` file** — for project-specific context.
5. **Agent reads relevant `skills/` files** — for execution methodology.

---

## MCP Servers (Configured in `~/.mcp.json`)

| Server | Status | Purpose |
|--------|--------|---------|
| GitHub | ✅ Active | Git operations, PRs, repo management |
| n8n-mcp | ✅ Active | Workflow management via supergateway |
| Supabase | ⏳ Pending | Database queries, schema, migrations |
| Context7 | ✅ Active | Library documentation lookup |
| Sequential Thinking | ✅ Active | Complex multi-step reasoning |
| Memory | ✅ Active | Cross-session context persistence |
| Fetch | ✅ Active | Read any public URL, docs, APIs |
| Playwright | ✅ Active | Browser automation, JS-rendered scraping |
| Filesystem | ✅ Active | File system access to Projects/ |

---

## Key Principle

This directory is the agent's brain, not a code repository. Software project code lives in external directories (e.g., `C:\Users\User\Projects\oasis-ai`). Do not store build artifacts, `node_modules`, or project source code in this directory.
