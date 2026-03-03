# ACTIVE TASKS
> Read this FIRST at the start of every session. Priority is marked with [P0] Critical, [P1] High, [P2] Medium.

## Target: $1,000 Net MRR by March 31, 2026

To reach this goal, we need **3 new clients** for OASIS (assuming ~$300-$500/mo retainer or high-ticket setup fee).

### Current Progress
- **Current Net:** ~$191
- **Gap to Goal:** +$809 Net
- **Next Milestone:** Close 1st client of March by **March 10**.

## Weekly Blitz (March 2-8, 2026)

### Monday (March 2) — Infrastructure & Authority Boost
- [x] [P0] IDE Restart — Finalize all MCP connections DONE 2026-03-02: All 4 config files synced (8 servers each), using reliable 'env' object.
- [x] [P0] Fix Telegram Bot — Updated to V5.5 query-first routing, removed dead CC_PROFILE.md ref, restarted. Now running.
- [x] [P0] Fix Agent Entry Points — GEMINI.md, ANTIGRAVITY.md, telegram_agent.js all use query-first routing.
- [x] [P1] Lead Research — 15+ local businesses & DJs researched. Owners identified.
- [x] [P0] MCP Infrastructure Fix — Root cause: IDE doesn't inject env vars. Fix: cmd wrapper scripts for n8n & Late. Stripe & Supabase removed (will reconfigure manually). 6/6 active servers ready.
- [ ] [P0] **IDE RESTART** — Restart to pick up new wrapper configs. All 6 servers should work after this.
- [ ] [P0] Create reusable Google Meet link — Store in .env.agents as GOOGLE_MEET_LINK
- [x] [P1] Send outreach emails — 13 emails sent (3 RE, 7 Local Business, 3 DJs) with Meet invites attached.
- [x] [P1] PropFlow Follow-up — Sent stern but professional follow-up email to Pazit regarding the 50/50 partnership and NDA status.
- [x] [P1] Video Production Pipeline — FFmpeg 8.0.1, Python 3.12, Whisper, ElevenLabs, Remotion 4.0.431 all installed. Pipeline tested end-to-end.
- [x] [P1] Agent Enhancement — 5 new commands (/plan-feature, /execute, /prime, /commit, /create-prd), 2 new skills (browser-automation, e2e-testing), .agents/plans/ dir, CAPABILITIES.md updated. Inspired by Cole Medin's link-in-bio repo.
- [ ] [P1] OASIS Content Engine — Post first authority-building LinkedIn/X content (The "Why AI" pivot)
- [ ] [P1] Build Lead Tracker — Create simple Supabase table to track outreach → replies → meetings
- [ ] [P2] Add ELEVENLABS_API_KEY to .env.agents — CC to provide key for voiceover generation
- [ ] [P2] Reconfigure Stripe MCP — Install manually (not from MCP store). Use cmd wrapper if env vars needed.
- [ ] [P2] Reconfigure Supabase MCP — Install manually (not from MCP store). Use npx with --access-token.

### Tuesday (March 3) — Outreach Blitz Day 1
- [ ] [P0] Personalized Outreach — Send 10+ personalized emails to local businesses (HVAC, fitness, wellness)
- [ ] [P0] Objection Handling Prep — Draft a one-pager on "The Leverage of AI for Local Services"
- [ ] [P1] Follow-ups — Use n8n to track email opens and trigger follow-up tasks

### Wednesday (March 4) — Closing & Content
- [ ] [P0] Initial Calls — Goal: Book 2 meetings for Thursday/Friday
- [ ] [P1] OASIS Content Engine — Post second authority-building content piece
- [ ] [P2] Refine Sales Pitch — Focus on ROI and leverage, not "cool tech"

### Thursday (March 5) — Outreach Blitz Day 2
- [ ] [P0] Personalized Outreach — Send 10+ more personalized emails
- [ ] [P1] OASIS Content Engine — Post third authority-building content piece
- [ ] [P1] Track metrics — Analyze open rates and response rates

### Friday (March 6) — Follow-Up & Finalize
- [ ] [P0] The "Weekend Closes" — Follow up on all outstanding leads before the weekend
- [ ] [P1] Review week — What angles converted? What were the main objections?
- [ ] [P2] Weekend Content Strategy — Schedule authority content for Saturday/Sunday

## Up Next (Week of March 9+)

- [ ] [P0] Onboard first new client of March
- [ ] [P1] Scale outreach to 15+ emails/day
- [ ] [P1] Build "High-Ticket Automation Template" for rapid delivery

## Blocked / Waiting

| Task | Blocked By | Since |
|------|-----------|-------|
| ~~n8n workflow automation~~ | ~~No MCP trigger nodes~~ **RESOLVED** — switched to community n8n-mcp (REST API), 44 workflows accessible | 2026-02-27 → FIXED 2026-03-02 |
| PropFlow development | Monitoring — pivoting dev hours to OASIS | 2026-03-01 |

*Last updated: 2026-03-02*
