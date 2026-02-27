# ANTI-GRAVITY CHAT INTERFACE — Cheat Sheet
## How to Talk to Your Business Empire Agent

---

## THE BASICS

You're chatting with an AI agent that can actually DO things. Not just answer questions — it can edit files, run commands, push code, query databases, and manage your entire stack. Here's how to get the most out of it.

---

## SLASH COMMANDS (Type These Directly)

| Command | What It Does |
|---------|-------------|
| `/mcp` | Check which external tools are connected |
| `/clear` | Wipe context clean — fresh start |
| `/compact` | Compress conversation to save memory (use when it gets slow) |
| `/help` | Show all available commands |
| `/config` | Open settings |
| `/deploy "message"` | Build, test, commit, push, create PR |
| `/debug "the problem"` | Find and fix a bug |
| `/add-feature "what"` | Plan and build a new feature |
| `/review` | Audit the codebase for issues |
| `/status` | Quick project health check |

---

## BRAVO CORE COMMANDS (New in v3)

You can trigger entire pipelines by mentioning these keywords. Bravo will automatically route the task to the correct specialized sub-agent (like `content-creator`, `researcher`, or `social-publisher`).

| Trigger Phrase | What It Does | Example |
|---------|-------------|---------|
| **"Research [topic]"** | Uses Playwright to browse the web, read articles, and synthesize a 5-point actionable brief with content angles. | *"Research what's trending right now regarding AI automation for real estate agencies."* |
| **"Content: [idea]"** | Generates a platform-optimized script/post using CC's exact voice, 5 content pillars, and no hustle-culture BS. | *"Content: Write a short-form reel script about working the weekend shift at Nicky's Donuts while trying to hit $10k MRR."* |
| **"Post: [message]"** | Uses the **Late** API MCP to format, schedule, and publish your content across all connected platforms (TikTok, X, LinkedIn, etc). | *"Post: Schedule that Nicky's Donuts script as a text post for X/Twitter tomorrow at 9am."* |
| **"Edit Video: [instructions]"** | Uses FFmpeg and Remotion to trim raw footage, add motion graphics, and format for the target platform (9:16 or 16:9). | *"Edit Video: Take input.mp4, trim the first 10 seconds, format it vertical, and add captions."* |
| **"Review [file/code]"** | Acts as a senior QA/security auditor. Hunts for hardcoded secrets, TypeScript errors, and bottleneck issues. | *"Review the payment webhook handler in PropFlow."* |

---

## HOW TO TALK TO IT (Natural Language)

You don't need special syntax. Just be direct. Here's what works:

### Starting Work
- "What's the current state of this project?"
- "Show me the last 5 commits"
- "What branch are we on?"
- "Pull the latest from main and create a feature branch called feature/booking-flow"

### Building Things
- "Build a new API endpoint for client onboarding that accepts name, email, and company"
- "Create a webhook handler that receives n8n workflow triggers and updates the database"
- "Add a dark mode toggle to the settings page"
- "Set up Stripe checkout for the monthly plan at $497/month"

### Fixing Things
- "The signup form crashes when email is empty — fix it"
- "This API call returns 500 — debug it"
- "The build is failing — figure out why and fix it"
- "Users are seeing a blank screen on mobile — investigate"

### n8n / Automation Work
- "Generate an n8n workflow JSON for: webhook trigger → GPT processing → Gmail send → Google Sheets log"
- "Create a lead enrichment workflow that takes an email, looks up the company, and adds it to our CRM"
- "Debug this n8n workflow JSON — it's failing at the HTTP Request node" (paste the JSON)
- "Build a customer support chatbot workflow with RAG from our knowledge base"

### Deploying
- "Deploy this with message: Added tenant screening feature"
- "Create a PR from this branch to main with a detailed description"
- "Run the build and tell me if there are any errors"

### Reviewing
- "Review the code I changed today — any issues?"
- "Are there any security vulnerabilities in this codebase?"
- "Find all TODO comments and list them"
- "Check for any hardcoded API keys or secrets"

---

## POWER MOVES (Advanced Usage)

### Chain Multiple Actions
> "Pull latest from main, create a branch called feature/email-automation, then build an email notification system that sends a welcome email when a new user signs up through Supabase, using the Resend API"

### Have It Plan First
> "I want to build a full tenant screening feature for PropFlow. Don't start coding yet — write a PLAN.md first with the architecture, database changes needed, API endpoints, and frontend components. Then wait for my approval."

### Make It Research First
> "Before building the payment integration, use Context7 to look up the latest Stripe Connect documentation for platform accounts with Express onboarding. Then build it."

### Make It Self-Improve
> "Review your own CLAUDE.md file. Based on our last 3 sessions, what instructions should be added or updated to make you more effective?"

### Workflow Documentation
> "Document everything about this project's current state in a STATUS.md file — architecture, dependencies, deployment process, known issues, and next steps."

---

## CONTEXT MANAGEMENT (Keep It Sharp)

| Situation | What to Do |
|-----------|-----------|
| Starting a new task | `/clear` if the last task was very different |
| Long conversation getting sluggish | `/compact` to compress context |
| Agent seems confused | "Stop. Re-read the CLAUDE.md and tell me what you understand about this project." |
| Switching projects | Navigate to the new project folder in Anti-Gravity's file explorer first |
| Agent lost track of what we built | "Read PLAN.md and STATUS.md to get caught up" |
| Want to save progress | "Write a SESSION_LOG.md with everything we accomplished today and what's next" |

---

## THE GOLDEN RULES

1. **Be direct.** "Build X" works better than "Could you maybe try to build something like X?"
2. **One task at a time.** Don't ask for 5 things in one message.
3. **Let it plan big things.** For anything taking more than 30 minutes, say "Write a plan first."
4. **Trust but verify.** Let it build, then review before deploying.
5. **Use /clear between unrelated tasks.** Fresh context = better output.
6. **If it hallucinates, call it out.** "That's wrong. Read the actual file at [path] and try again."
7. **Save your wins.** After a good session, say "Update the CLAUDE.md with any new patterns or context from this session."

---

## QUICK REFERENCE: What the Agent Can Access

| Tool | What It Can Do |
|------|---------------|
| **Your Files** | Read, edit, create, delete any file in the project |
| **Terminal** | Run any shell command (npm, git, node, python, etc.) |
| **GitHub** | Push, pull, create branches, PRs, manage repos |
| **Supabase** | Query databases, create tables, run migrations |
| **n8n** | Trigger workflows, read workflow configs, manage automations |
| **Web/Browser** | Playwright for complete browser automation (JS-heavy sites, screenshots, web searches) |
| **Memory** | Remember things across sessions (ACTIVE_TASKS, CONTEXT, etc.) |
| **Context7** | Look up current documentation for any library |
| **Sequential Thinking** | Break complex problems into logical steps |
| **Late API (Social)** | Publish and schedule posts on 13+ social platforms |
| **Stripe** | View subscriptions, create products, and manage the Stripe accounts across all 3 portals |
