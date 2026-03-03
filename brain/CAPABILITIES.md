# CAPABILITIES — Tool & Integration Registry

> Complete inventory of what Bravo can do. Updated when new tools are added.

## MCP Servers (By Interface)

### Claude Code (Opus 4.6 — Lead Architect)
| Server | Purpose | Key Tools |
|--------|---------|-----------|
| **Playwright** | Browser automation, ALL web research, scraping, testing | navigate, snapshot, click, type, evaluate |
| **Context7** | Live library documentation lookup | resolve-library-id, query-docs |
| **Memory** | Persistent knowledge graph across sessions | create_entities, search_nodes, open_nodes |
| **n8n** | Workflow automation management (community n8n-mcp via REST API) | search_workflows, execute_workflow, get_workflow_details |
| **Late** | Social media posting (8+ platforms) | posts_create, posts_list, accounts_list, posts_cross_post |
| **Supabase** | Database queries, migrations, schema (npx, project-level .claude/mcp.json) | execute_sql, apply_migration, list_tables, list_projects |
| **Sequential Thinking** | Structured multi-step reasoning | sequentialthinking |

### Anti-Gravity IDE (Native Local Agent — Multi-Model)

Models: Gemini 3.1 Pro High/Low, Gemini 3 Flash, Claude Sonnet/Opus 4.6, GPT-OSS 120B Medium
Entry Point: `ANTIGRAVITY.md` | Config: `.vscode/mcp.json`
Workflows: `.agents/workflows/` (10 workflows: post, status, health, prime, content, commit, n8n, sync, research, debug)

**IMPORTANT — Windows env var pattern:** n8n and Late use `cmd /c wrapper.cmd` scripts (in `scripts/`) that `set` env vars before launching. Direct `env` blocks in JSON configs do NOT work on Windows. See `scripts/n8n-mcp-wrapper.cmd` and `scripts/late-mcp-wrapper.cmd`.

| Server | Purpose | Config |
|--------|---------|--------|
| **n8n-mcp** | Workflow automation (44 workflows, REST API) | `cmd /c scripts/n8n-mcp-wrapper.cmd` |
| **Late** | Social media posting (8+ platforms) | `cmd /c scripts/late-mcp-wrapper.cmd` |
| **Playwright** | Browser automation, web research | npx @playwright/mcp --headless |
| **Context7** | Live library documentation | npx @upstash/context7-mcp |
| **Memory** | Persistent knowledge graph | npx @modelcontextprotocol/server-memory |
| **Sequential Thinking** | Multi-step reasoning | npx @modelcontextprotocol/server-sequential-thinking |

**OFFLINE (reconfigure with CC):**
| **Supabase** | Database operations | REMOVED — MCP store download errors |
| **Stripe** | Payment management | REMOVED — MCP store download errors |

### Blackbox AI (Rapid Execution)
- No MCPs — CLI + file access only
- For: boilerplate, simple edits, isolated functions

### Gemini CLI (Diagnostic & Inference — 4th Tier)
- Tool: `@google/gemini-cli`
- Entry Point: `GEMINI.md`
- Purpose: Fast diagnostics, file system cleanup, automated audits, heartbeat monitoring, fallback execution
- Interface: `gemini` command (global npm)
- MCP Access (via `.gemini/settings.json`): n8n, Late, Playwright, Context7, Memory, Sequential Thinking (6 active servers)
- Offline: Supabase, Stripe (removed — will reconfigure with CC)
- Note: Config synced with `.vscode/mcp.json`. n8n and Late use `cmd /c wrapper.cmd` pattern for env vars.

## Supabase Projects

| Project | Region | Purpose |
|---------|--------|---------|
| **Bravo** | us-west-2 | Agent intelligence database (10 tables) |
| **nostalgic-requests** | us-west-2 | Nostalgic Requests platform |
| **oasis-ai-platform** | us-west-2 | OASIS AI platform |

**Organizations:** CC (oktipozhyojufxsytrse), oasis-ai-platform (sajanpiqysuwviucycjh)

## Sub-Agents (12)

| Agent | Model | Specialty |
|-------|-------|-----------|
| architect | Opus | System design, DB schema, multi-service planning |
| content-creator | Sonnet | Copywriting, social content, CC's 5 pillars |
| debugger | Sonnet | Bug investigation, root cause analysis |
| documenter | Haiku | Documentation, memory updates |
| explorer | Haiku | Codebase navigation (read-only) |
| git-ops | Haiku | Git operations, PR management |
| researcher | Sonnet | Market research via Playwright |
| reviewer | Sonnet | Code quality & security audit |
| social-publisher | Haiku | Late API posting, platform char limits |
| video-editor | Sonnet | FFmpeg, Remotion, captions |
| workflow-builder | Sonnet | n8n automation creation |
| writer | Sonnet | Code writing, feature implementation |

## Commands (21)

| Command | Trigger |
|---------|---------|
| /plan-feature | **Deep codebase analysis → implementation plan** (parallel sub-agents, validation commands, confidence scoring) |
| /execute | **Execute plan step-by-step** with verification gates |
| /prime | **Load full project context** — brain, memory, git, MCP health |
| /commit | **Smart commit** — conventional format (`bravo: type — desc`), staged analysis |
| /create-prd | **Generate PRD** for client projects (15-section structure) |
| /add-feature | Plan & build new feature |
| /build-workflow | n8n automation creation |
| /cleanup | Remove junk files |
| /client-onboard | New OASIS client setup |
| /condense | Archive old memory logs |
| /content | Create platform content |
| /debug | Systematic bug fixing |
| /deploy | Build, test, push, PR |
| /edit-video | Video editing pipeline |
| /health | Full workspace diagnostic |
| /monthly-audit | Monthly evolution protocol |
| /post | Publish via Late API |
| /research | Competitive intelligence |
| /review | Code quality audit |
| /self-heal | Session-end diagnostics |
| /status | Project status report |

## Skills (40)

| Category | Skills |
|----------|--------|
| **Agent Intelligence** | heartbeat, self-healing, memory-management, growth-engine, sop-breakdown, sequential-reasoning |
| **Development** | systematic-debugging, TDD, verification, executing-plans, writing-plans, finishing-branch, git-worktrees |
| **Browser & Testing** | **browser-automation** (Playwright MCP reference), **e2e-testing** (parallel sub-agent E2E), webapp-testing |
| **Content** | writing-skills, doc-coauthoring, internal-comms, brand-guidelines, brainstorming |
| **Code** | mcp-builder, skill-creator, subagent-development, parallel-agents, code-review (2) |
| **Automation** | n8n-mcp-integration, n8n-patterns, supabase-patterns, ai-integration |
| **Creative** | frontend-design, canvas-design, algorithmic-art, theme-factory, web-artifacts |
| **Files** | pdf, docx, pptx, xlsx |
| **Security** | security-protocol, using-superpowers |
| **Meta** | slack-gif-creator |

## External Services (No MCP)

| Service | Access Method | Purpose |
|---------|---------------|---------|
| n8n | n8n-mcp / API | Workflow automation (Full CRUD via Bravo) |
| Gmail | API / SMTP | Email drafting, research, and approval-based sending |
| Notion | API | Task tracking, project management, and knowledge base |
| ElevenLabs | Python SDK | Voice & audio generation (elevenlabs pip package) |
| Vercel | Git push auto-deploy | Hosting & previews |
| GoHighLevel | n8n webhooks | CRM for OASIS clients |
| Twilio | API/n8n | SMS & voice (Nostalgic Requests) |
| Shopify | Admin UI | FromOasis e-commerce |
| Telegram | telegram_agent.js (V5.5) | CLI bridge for remote execution — routes to Gemini/Claude via query-first pattern. Start: `npm run telegram` |

## Video Production Pipeline

| Tool | Version | Purpose |
|------|---------|---------|
| FFmpeg | 8.0.1 (full build) | Video encoding, overlays, captions, audio normalization |
| Python | 3.12.10 | Script runtime for edit_content.py |
| Whisper | openai-whisper | Auto-transcription → SRT captions |
| ElevenLabs | elevenlabs SDK | Text-to-speech voiceover generation |
| Remotion | 4.0.431 | Programmatic video/animation generation |

Pipeline script: `scripts/edit_content.py` — probe, transcribe, voiceover, edit
Agent: `agents/video-editor.md` | Command: `/edit-video`

## Tech Stack

- **OS:** Windows 11 (Desktop), macOS (MacBook)
- **Languages:** TypeScript (primary), Python (video pipeline, MCP servers)
- **Frameworks:** Next.js 14 (App Router), Tailwind CSS
- **Database:** Supabase (PostgreSQL) — 3 projects, 10-table agent schema
- **Hosting:** Vercel (auto-deploy from git)
- **Payments:** Stripe (3 brand accounts)
- **Automation:** n8n (Hostinger VPS: https://n8n.srv993801.hstgr.cloud)
- **AI Models:** Claude Opus/Sonnet, Gemini 1.5 Pro/Flash, GPT-4o, Gemini CLI (v0.31.0)
