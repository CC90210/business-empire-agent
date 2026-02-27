# ANTI-GRAVITY CHAT INTERFACE — Cheat Sheet (V4)
## How to Talk to Your Business Empire Agent

---

## THE AGENT TIERS

| Interface | Engine | Role | Best For |
|-----------|--------|------|----------|
| **Anti-Gravity** | Gemini 3.1 Pro | Infantry / Hybrid | Daily ops, research, posting, fast execution |
| **Claude Code** | Opus 4.6 | General / Architect | Multi-file refactoring, deep debugging, system design |
| **Blackbox AI** | Blackbox | Rapid Infantry | Boilerplate, isolated functions, quick edits |

All three share the same brain (`AGENT_CORE_DIRECTIVES.md`), memory (`memory/`), and tasks (`ACTIVE_TASKS.md`).

---

## SLASH COMMANDS

| Command | What It Does |
|---------|-------------|
| `/mcp` | Check which external tools are connected |
| `/clear` | Wipe context — fresh start |
| `/compact` | Compress conversation to save memory |
| `/deploy "message"` | Build, test, commit, push, create PR |
| `/debug "the problem"` | Find and fix a bug (max 3 attempts) |
| `/add-feature "what"` | Plan and build a new feature |
| `/review` | Audit codebase for security + quality |
| `/status` | Quick project health check |
| `/health` | Full workspace diagnostic (MCP, files, git, memory) |
| `/cleanup` | Find and remove junk files (asks before deleting) |
| `/condense` | Garbage-collect memory files, archive old sessions |
| `/post "message"` | Publish to social via Late API |
| `/content "idea"` | Generate platform-optimized content in CC's voice |
| `/research "topic"` | Playwright web research → actionable brief |

---

## TRIGGER PHRASES (Natural Language)

| Trigger | What Happens | Example |
|---------|-------------|---------|
| **"Research [topic]"** | Playwright browses web, reads articles, synthesizes brief | *"Research AI automation trends for HVAC companies"* |
| **"Content: [idea]"** | Generates X + LinkedIn + IG versions in CC's voice | *"Content: Working at Nicky's Donuts while hitting $10k MRR"* |
| **"Post: [message]"** | Validates char limits, publishes via Late API | *"Post: Schedule that for X and LinkedIn tomorrow 9am"* |
| **"Edit Video: [file]"** | FFmpeg + Remotion trimming, captions, platform export | *"Edit Video: Trim input.mp4, make vertical, add captions"* |
| **"Review [code]"** | Security audit with severity ratings | *"Review the payment webhook in PropFlow"* |
| **"Build [feature]"** | Creates branch, plans, implements, commits | *"Build a dark mode toggle for the settings page"* |
| **"Fix [bug]"** | Reads error, traces root cause, minimal fix | *"The signup form crashes when email is empty"* |

---

## PLATFORM CHARACTER LIMITS (Social Posting)

| Platform | Max Chars | Video Format |
|----------|-----------|-------------|
| X/Twitter | **280** | 16:9, 1:1 |
| Instagram | 2,200 | 9:16, <90s |
| LinkedIn | 3,000 | 16:9, 1:1 |
| TikTok | 4,000 | 9:16, <3min |
| Threads | 500 | 16:9, 1:1 |

The agent auto-validates and condenses per platform before posting.

---

## CONTEXT MANAGEMENT

| Situation | What to Do |
|-----------|-----------|
| Starting a new task | `/clear` if last task was very different |
| Conversation getting slow | `/compact` to compress context |
| Agent seems confused | "Re-read AGENT_CORE_DIRECTIVES.md and tell me what you understand" |
| Switching projects | Navigate to project folder in file explorer first |
| Want to save progress | "Log this session" (updates SESSION_LOG.md) |
| Memory getting bloated | `/condense` to archive old entries |

---

## WHAT THE AGENT CAN ACCESS

| Tool | What It Does |
|------|-------------|
| **Your Files** | Read, edit, create, delete any file in the workspace |
| **Terminal** | Run any shell command (npm, git, node, python, ffmpeg) |
| **Playwright** | Full browser automation — web search, scraping, testing |
| **Late API** | Publish/schedule posts on 8+ social platforms |
| **Supabase** | Database queries, schema, migrations, auth |
| **Stripe** | Payments across PropFlow, Nostalgic Requests, OASIS AI |
| **n8n** | Workflow automation management |
| **Context7** | Live documentation for any library |
| **Memory** | Persistent knowledge graph across sessions |
| **Sequential Thinking** | Structured multi-step reasoning |
| **GitHub** | Remote repo management (branch, PR, edit, merge) |

---

## THE GOLDEN RULES

1. **Be direct.** "Build X" beats "Could you maybe try..."
2. **One task at a time.** Don't ask for 5 things in one message.
3. **Let it plan big things.** "Write a plan first" for anything complex.
4. **Trust but verify.** Let it build, review before deploying.
5. **Use /clear between unrelated tasks.** Fresh context = better output.
6. **Call out hallucinations.** "That's wrong. Read the actual file and try again."
7. **Save your wins.** "Log this session" after productive work.
