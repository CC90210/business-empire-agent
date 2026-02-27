# Business Empire Agent — BRAVO V4

> Autonomous AI operations hub for CC's business empire. Manages codebases, deployments, content pipelines, and business operations across OASIS AI Solutions, PropFlow, and Nostalgic Requests.

---

## Directory Structure

```
Business-Empire-Agent/
│
├── AGENT_CORE_DIRECTIVES.md    ← Core brain: identity, routing, verification, quality gates
├── AGENT_SYSTEM_PROMPT.md      ← Bravo V4 system prompt for Anti-Gravity IDE
├── ANTIGRAVITY_CHEAT_SHEET.md  ← CC's quick reference for talking to the agent
├── AUDIT_REPORT.md             ← Latest diagnostic findings
├── README.md                   ← This file
├── .gitignore                  ← Git ignore rules
│
├── agents/                     ← 12 sub-agent definitions
│   ├── architect.md            ← System design (Opus)
│   ├── content-creator.md      ← Ghostwriting, social content (Sonnet)
│   ├── debugger.md             ← Bug investigation (Sonnet)
│   ├── documenter.md           ← Documentation, memory updates (Haiku)
│   ├── explorer.md             ← Codebase navigation, read-only (Haiku)
│   ├── git-ops.md              ← Git operations, PRs (Haiku)
│   ├── researcher.md           ← Market research via Playwright (Sonnet)
│   ├── reviewer.md             ← Code review, security audit (Sonnet)
│   ├── social-publisher.md     ← Late API posting (Haiku)
│   ├── video-editor.md         ← Video production (Sonnet)
│   ├── workflow-builder.md     ← n8n workflow creation (Sonnet)
│   └── writer.md               ← Code writing, features (Sonnet)
│
├── commands/                   ← 13 slash commands
│   ├── add-feature.md          ← /add-feature — plan and build
│   ├── build-workflow.md       ← /build-workflow — n8n automation
│   ├── cleanup.md              ← /cleanup — junk file removal
│   ├── client-onboard.md       ← /client-onboard — new client setup
│   ├── content.md              ← /content — create content in CC's voice
│   ├── debug.md                ← /debug — systematic bug fixing
│   ├── deploy.md               ← /deploy — lint, build, push, PR
│   ├── edit-video.md           ← /edit-video — video editing pipeline
│   ├── health.md               ← /health — workspace health check
│   ├── post.md                 ← /post — publish via Late API
│   ├── research.md             ← /research — competitive intel
│   ├── review.md               ← /review — code quality audit
│   └── status.md               ← /status — project status report
│
├── memory/                     ← Persistent memory across sessions
│   ├── ACTIVE_TASKS.md         ← Current work in progress
│   ├── CONTEXT.md              ← CC profile and business context
│   ├── DECISIONS.md            ← Architectural decisions log
│   ├── MISTAKES.md             ← Bug root cause analysis
│   ├── PATTERNS.md             ← Proven approaches and anti-patterns
│   └── SESSION_LOG.md          ← Session-end summaries
│
├── skills/                     ← 31 skills library (READ-ONLY)
│   ├── brainstorming/          ← Socratic design refinement
│   ├── canvas-design/          ← Visual art/poster creation
│   ├── dispatching-parallel-agents/ ← Parallel investigation
│   ├── docx/                   ← Word document operations
│   ├── executing-plans/        ← Batch execution with checkpoints
│   ├── frontend-design/        ← Production-grade web UI design
│   ├── mcp-builder/            ← Build MCP servers
│   ├── n8n-mcp-integration/    ← n8n workflow via MCP
│   ├── pdf/                    ← PDF operations
│   ├── pptx/                   ← Slide deck creation
│   ├── systematic-debugging/   ← 4-phase root cause debugging
│   ├── test-driven-development/← RED-GREEN-REFACTOR cycle
│   ├── webapp-testing/         ← Playwright browser testing
│   ├── writing-plans/          ← Implementation planning
│   ├── xlsx/                   ← Spreadsheet operations
│   └── [16 more skills]       ← See skills/ directory
│
├── APPS_CONTEXT/               ← Per-business context files
│   ├── OASIS_AI_CLAUDE.md      ← OASIS AI Solutions
│   ├── PROPFLOW_CLAUDE.md      ← PropFlow SaaS
│   ├── NOSTALGIC_REQUESTS_CLAUDE.md ← Nostalgic Requests
│   ├── CONTENT_BRAND_CLAUDE.md ← CC's personal brand
│   ├── AI_TRAINING_CLAUDE.md   ← AI Training business
│   └── OASIS_WORKFLOWS.md      ← n8n workflow registry
│
└── references/                 ← Setup guides and config references (gitignored)
    ├── Claude_Setup_Guide.md
    ├── Claude_Global_MCP.json
    ├── Claude_Global_Settings.json
    └── awesome-claude-skills/
```

---

## MCP Servers (Anti-Gravity IDE)

| Server | Tools | Purpose | Status |
|--------|-------|---------|--------|
| Late | 19 | Social media posting across 8+ platforms | Active |
| Playwright | 22 | Browser automation, web research | Active |
| Sequential Thinking | 1 | Structured reasoning | Active |
| Stripe | 28 | Payment operations across 3 brands | Active |
| Supabase | 29 | Database management | Needs token |
| Context7 | 2 | Live library documentation | Active |
| Memory | 8 | Knowledge graph persistence | Active |
| n8n | 3 | Workflow automation | Active |

---

## Quick Start

1. Agent loads `AGENT_SYSTEM_PROMPT.md` (Anti-Gravity) or `AGENT_CORE_DIRECTIVES.md` (Claude Code)
2. Agent reads `memory/ACTIVE_TASKS.md` for current work
3. CC gives a task — agent matches to a routing workflow
4. Agent reads relevant `APPS_CONTEXT/` file for project-specific context
5. Agent reads relevant `skills/` files for execution methodology

---

## Key Principle

This directory is the agent's brain, not a code repository. Software project source code lives in external directories. Do not store build artifacts, `node_modules`, or project source code here.

---

*Bravo V4 — "Only good things from now on."*
