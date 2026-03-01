# CAPABILITIES — Tool & Integration Registry

> Complete inventory of what Bravo can do. Updated when new tools are added.

## MCP Servers (By Interface)

### Claude Code (Opus 4.6 — Lead Architect)
| Server | Purpose | Key Tools |
|--------|---------|-----------|
| **Playwright** | Browser automation, ALL web research, scraping, testing | navigate, snapshot, click, type, evaluate |
| **Context7** | Live library documentation lookup | resolve-library-id, query-docs |
| **Memory** | Persistent knowledge graph across sessions | create_entities, search_nodes, open_nodes |
| **n8n** | Workflow automation management | search_workflows, execute_workflow, get_workflow_details |
| **Late** | Social media posting (8+ platforms) | posts_create, posts_list, accounts_list, posts_cross_post |
| **Supabase** | Database queries, migrations, schema (npx, project-level .claude/mcp.json) | execute_sql, apply_migration, list_tables, list_projects |
| **Sequential Thinking** | Structured multi-step reasoning | sequentialthinking |

### Anti-Gravity (Gemini 3.1 Pro — Infantry/Hybrid)
| Server | Purpose | Config |
|--------|---------|--------|
| **GitHub** | Remote git ops, PRs, branches, file editing | npx github-mcp |
| **Late** | Social media posting | uvx late-sdk[mcp] |
| **Stripe** | Payment management (3 brands) | npx @stripe/mcp --tools=all |
| **Supabase** | Database operations | npx @supabase/mcp-server-supabase |
| **Sequential Thinking** | Multi-step reasoning | npx @modelcontextprotocol/server-sequential-thinking |
| **Chrome** | Built-in browser (replaces Playwright) | Native to IDE |

### Blackbox AI (Rapid Execution)
- No MCPs — CLI + file access only
- For: boilerplate, simple edits, isolated functions

### Gemini CLI (Diagnostic & Inference)
- Tool: `@google/gemini-cli` (v0.31.0)
- Purpose: Direct local inference, diagnostic support, fallback agent
- Interface: `gemini` command

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

## Commands (16)

| Command | Trigger |
|---------|---------|
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

## Skills (37)

| Category | Skills |
|----------|--------|
| **Agent Intelligence** | heartbeat, self-healing, memory-management, growth-engine, sop-breakdown, sequential-reasoning |
| **Development** | systematic-debugging, TDD, verification, executing-plans, writing-plans, finishing-branch, git-worktrees |
| **Content** | writing-skills, doc-coauthoring, internal-comms, brand-guidelines, brainstorming |
| **Code** | mcp-builder, skill-creator, subagent-development, parallel-agents, code-review (2) |
| **Automation** | n8n-mcp-integration, n8n-patterns, supabase-patterns, ai-integration |
| **Creative** | frontend-design, canvas-design, algorithmic-art, theme-factory, web-artifacts |
| **Files** | pdf, docx, pptx, xlsx |
| **Security** | security-protocol, webapp-testing, using-superpowers |
| **Meta** | slack-gif-creator |

## External Services (No MCP)

| Service | Access Method | Purpose |
|---------|---------------|---------|
| n8n | n8n-mcp / API | Workflow automation (Full CRUD via Bravo) |
| Gmail | API / SMTP | Email drafting, research, and approval-based sending |
| Notion | API | Task tracking, project management, and knowledge base |
| ElevenLabs | Chrome/API | Voice & audio generation |
| Vercel | Git push auto-deploy | Hosting & previews |
| GoHighLevel | n8n webhooks | CRM for OASIS clients |
| Twilio | API/n8n | SMS & voice (Nostalgic Requests) |
| Shopify | Admin UI | FromOasis e-commerce |
| Telegram | telegram_agent.js | CLI bridge for remote execution |

## Tech Stack

- **OS:** Windows 11 (Desktop), macOS (MacBook)
- **Languages:** TypeScript (primary), Python (MCP servers)
- **Frameworks:** Next.js 14 (App Router), Tailwind CSS
- **Database:** Supabase (PostgreSQL) — 3 projects, 10-table agent schema
- **Hosting:** Vercel (auto-deploy from git)
- **Payments:** Stripe (3 brand accounts)
- **Automation:** n8n (Hostinger VPS: https://n8n.srv993801.hstgr.cloud)
- **AI Models:** Claude Opus/Sonnet, Gemini 1.5 Pro/Flash, GPT-4o, Gemini CLI (v0.31.0)
