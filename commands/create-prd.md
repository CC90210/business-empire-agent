---
description: Generate a comprehensive Product Requirements Document from a conversation or brief
argument-hint: [output filename, default: .agents/PRD.md]
---

# Create PRD

## Output File
Write the PRD to: `$ARGUMENTS` (default: `.agents/PRD.md`)

## PRD Structure (15 Sections)

```markdown
# [Project Name] — Product Requirements Document

## 1. Executive Summary
One paragraph: what it is, who it's for, why it matters.

## 2. Mission
Single sentence defining the project's purpose.

## 3. Target Users
| Persona | Description | Primary Need |
|---------|-------------|--------------|
| ... | ... | ... |

## 4. MVP Scope
### In Scope
- Feature 1
- Feature 2

### Out of Scope
- Feature X (future consideration)
- Feature Y (not aligned with MVP)

## 5. User Stories
- As a [user], I want [action], so that [benefit]
- ...

## 6. Core Architecture & Patterns
- Frontend: ...
- Backend: ...
- Database: ...
- Auth: ...
- Key patterns: ...

## 7. Tools & Features
| Feature | Description | Priority |
|---------|-------------|----------|
| ... | ... | P0/P1/P2 |

## 8. Technology Stack
| Technology | Purpose | Justification |
|------------|---------|---------------|
| ... | ... | ... |

## 9. Security & Configuration
- Auth method: ...
- Environment variables needed: ...
- API security: ...

## 10. API Specification
| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| ... | ... | ... | ... |

## 11. Success Criteria
- [ ] Metric 1
- [ ] Metric 2

## 12. Implementation Phases
### Phase 1: Foundation (Week 1)
- Deliverable 1
### Phase 2: Core Features (Week 2-3)
- Deliverable 2
### Phase 3: Polish & Launch (Week 4)
- Deliverable 3

## 13. Future Considerations
- ...

## 14. Risks & Mitigations
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ... | ... | ... | ... |

## 15. Appendix
- Reference links
- Design mockups (if any)
- Competitor analysis (if relevant)
```

## Instructions
- Extract requirements from conversation history and any provided briefs
- Fill reasonable assumptions where context is missing — mark as [ASSUMPTION]
- Use concrete examples over abstractions
- Keep language clear — this document should be readable by non-technical stakeholders
- After generating, offer: "PRD saved. Run /plan-feature to create the implementation plan?"
