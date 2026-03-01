# HEARTBEAT — Proactive Autonomous Operations

> Unlike a cron job that fires blindly, the heartbeat exercises judgment.
> It checks conditions and only acts when action is warranted.

## Trigger

The heartbeat runs at **session start** (IDE-based agent, not daemon). When Bravo wakes up, it runs through this checklist before engaging with CC's request.

## Session-Start Heartbeat Checks

### 1. Memory Consistency (Priority: HIGH)
```
CHECK: Are memory files internally consistent?
- Read ACTIVE_TASKS.md — any tasks marked "in progress" from a previous session?
- Read SESSION_LOG.md (last 3 entries) — any incomplete work?
- Read MISTAKES.md — any recent mistakes that apply to today's work?
- Read PATTERNS.md — any new patterns to internalize?
ACTION: Flag stale tasks. Carry forward or close them.
```

### 2. Infrastructure Health (Priority: HIGH)
```
CHECK: Are critical systems operational?
- git status — clean working tree? Uncommitted changes?
- MCP servers — any known issues from last session?
- .env.agents — referenced but never read values
ACTION: Report any issues before starting work.
```

### 3. Pending Heartbeat Tasks (Priority: MEDIUM)
```
CHECK: Are there scheduled tasks in memory/ACTIVE_TASKS.md?
- Overdue items (marked with dates)
- Blocked items (waiting on dependencies)
- Priority items flagged by CC
ACTION: Present status to CC. Suggest next action.
```

### 4. Self-Healing Scan (Priority: MEDIUM)
```
CHECK: Is the workspace healthy?
- Junk files in project root? (*.js, *.txt, *.log, debug dumps)
- Memory bloat? (SESSION_LOG > 200 lines? ACTIVE_TASKS > 50 items?)
- Stale context? (CONTEXT files older than 30 days without update?)
ACTION: Auto-clean junk. Suggest compression for bloated files.
```

### 5. Growth Check (Priority: LOW)
```
CHECK: Has Bravo learned anything new recently?
- New patterns discovered in last 3 sessions?
- New skills used for the first time?
- Recurring problems that could become SOPs?
ACTION: Log insights to brain/GROWTH.md if significant.
```

## Session-End Heartbeat (Self-Heal Protocol)

Execute `/commands/self-heal.md` with enhanced checks:

1. **Context Diagnostics** — Prune temp files, compress logs
2. **API Hardening** — Did anything fail? Log to MISTAKES.md
3. **Code Verification** — Any uncommitted changes? Remind CC.
4. **Pattern Distillation** — Extract new patterns/mistakes from this session
5. **Memory Sync** — Update ACTIVE_TASKS, SESSION_LOG
6. **State Update** — Update brain/STATE.md with current operational state

## Heartbeat Response Format

When reporting heartbeat results to CC:
```
HEARTBEAT COMPLETE
- Memory: [OK/ISSUES FOUND]
- Infrastructure: [OK/ISSUES FOUND]
- Pending Tasks: [X items]
- Workspace: [CLEAN/NEEDS ATTENTION]
- Growth: [X new insights]
Ready for orders, CC.
```

## Future: Daemon Mode

When n8n webhook triggers are configured, heartbeat can run on a schedule:
- n8n cron trigger → Telegram bot → Claude Code CLI → heartbeat check
- This enables 24/7 autonomous monitoring without CC opening the IDE
- See: telegram_agent.js for the existing Telegram → CLI bridge
