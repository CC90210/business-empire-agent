---
description: Plan a new feature or task with deep codebase analysis before writing any code
argument-hint: [feature description]
---

# Plan: $ARGUMENTS

## Mission
Transform this request into a comprehensive implementation plan through systematic codebase analysis, research, and strategic planning. **We do NOT write code in this phase.** Goal: context-rich plan for one-pass implementation success.

## Phase 1: Feature Understanding
- Extract core problem being solved
- Determine type: New Feature | Enhancement | Refactor | Bug Fix | Infrastructure
- Assess complexity: Low | Medium | High
- Map affected systems and files

Create User Story:
```
As a <type of user>
I want to <action/goal>
So that <benefit/value>
```

## Phase 2: Codebase Intelligence (Use Parallel Sub-agents)

**Sub-agent 1: Structure Analysis**
- Search for similar implementations in codebase
- Identify coding conventions (naming, file org, error handling)
- Map integration points (files to update, new files to create)
- Check CLAUDE.md, brain/SOUL.md, AGENT_CORE_DIRECTIVES.md for project rules

**Sub-agent 2: Dependency & Pattern Analysis**
- Catalog relevant libraries and how they're integrated
- Find docs in skills/, brain/, or external (use Context7 MCP)
- Identify test patterns (frameworks, structure, coverage requirements)
- Check memory/PATTERNS.md and memory/MISTAKES.md for known gotchas

**Sub-agent 3: External Research (if needed)**
- Research latest library versions and best practices (Context7 MCP)
- Find official documentation with specific section anchors
- Identify common gotchas and breaking changes

Clarify ambiguities with CC BEFORE continuing to Phase 3.

## Phase 3: Strategic Thinking
Use Sequential Thinking MCP for complex features:
- How does this fit existing architecture?
- What are the critical dependencies and order of operations?
- What could go wrong? (edge cases, race conditions, auth gaps)
- How will this be tested comprehensively?
- Performance and security implications?

## Phase 4: Generate Plan

Save to: `.agents/plans/{kebab-case-name}.md`

Use this structure:
```markdown
# Feature: <name>

## User Story
## Problem Statement
## Solution Statement

## Context References
### Files to Read Before Implementing
- path/to/file (lines X-Y) — Why: ...
### New Files to Create
### Patterns to Follow (with code examples from project)

## Implementation Plan
### Phase 1: Foundation
### Phase 2: Core Implementation
### Phase 3: Integration
### Phase 4: Testing & Validation

## Step-by-Step Tasks
Each task uses: CREATE | UPDATE | ADD | REMOVE | REFACTOR

### Task N: {ACTION} {target_file}
- IMPLEMENT: {detail}
- PATTERN: {reference file:line}
- VALIDATE: `{executable command}`

## Testing Strategy
## Validation Commands (must all pass)
## Acceptance Criteria
```

## Phase 5: Report
- Plan saved to `.agents/plans/{name}.md`
- Complexity: X/10
- Confidence score: X/10 for first-attempt success
- Key risks identified
- Offer: "Execute now with /execute or review first?"

## Skills Integration
- **Use:** skills/writing-plans for plan structure
- **Use:** skills/systematic-debugging if investigating a bug
- **Use:** Sequential Thinking MCP for complex architectural decisions
- **Use:** Context7 MCP for library documentation
