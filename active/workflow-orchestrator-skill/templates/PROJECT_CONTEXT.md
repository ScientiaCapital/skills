# Project Context

**Generated**: {{DATE}}  
**Session ID**: {{SESSION_ID}}  
**Duration**: {{SESSION_DURATION}}

## Current Sprint
**Sprint Goal**: {{SPRINT_GOAL}}  
**Sprint End**: {{SPRINT_END_DATE}}  
**Progress**: {{PROGRESS_PERCENTAGE}}%

## Active Work

### Current Feature/Task
- **Name**: {{CURRENT_TASK_NAME}}
- **Branch**: {{CURRENT_BRANCH}}
- **Started**: {{TASK_START_DATE}}
- **Status**: {{TASK_STATUS}}
- **Blockers**: {{BLOCKERS}}

### In Progress
| Task | Branch | Status | Assigned Agent | Est. Complete |
|------|--------|--------|----------------|---------------|
{{#IN_PROGRESS_TASKS}}
| {{TASK_NAME}} | {{BRANCH}} | {{STATUS}} | {{AGENT}} | {{ETA}} |
{{/IN_PROGRESS_TASKS}}

### Completed This Sprint
{{#COMPLETED_TASKS}}
- [x] {{TASK_NAME}} - {{COMPLETION_DATE}} ({{TIME_TAKEN}})
{{/COMPLETED_TASKS}}

## Architecture Decisions
{{#DECISIONS}}
### {{DECISION_DATE}}: {{DECISION_TITLE}}
**Context**: {{CONTEXT}}  
**Decision**: {{DECISION}}  
**Consequences**: {{CONSEQUENCES}}  
{{/DECISIONS}}

## Code Metrics
- **Files Changed**: {{FILES_CHANGED}}
- **Lines Added**: {{LINES_ADDED}}
- **Lines Removed**: {{LINES_REMOVED}}
- **Test Coverage**: {{COVERAGE}}%
- **Tests Added**: {{TESTS_ADDED}}
- **Performance**: {{PERFORMANCE_DELTA}}

## Dependencies & APIs
### External Services
{{#EXTERNAL_SERVICES}}
- **{{SERVICE_NAME}}**: {{STATUS}} ({{RESPONSE_TIME}}ms avg)
{{/EXTERNAL_SERVICES}}

### Critical Dependencies
{{#DEPENDENCIES}}
- {{DEP_NAME}} v{{VERSION}} - {{STATUS}}
{{/DEPENDENCIES}}

## Team Notes
### Recent Decisions
{{#TEAM_DECISIONS}}
- {{DATE}}: {{DECISION}}
{{/TEAM_DECISIONS}}

### Action Items
{{#ACTION_ITEMS}}
- [ ] {{ITEM}} - @{{ASSIGNEE}} by {{DUE_DATE}}
{{/ACTION_ITEMS}}

## Risk Register
| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
{{#RISKS}}
| {{RISK_NAME}} | {{PROBABILITY}} | {{IMPACT}} | {{MITIGATION}} |
{{/RISKS}}

## Next Session Priorities
1. {{PRIORITY_1}}
2. {{PRIORITY_2}}
3. {{PRIORITY_3}}

## Environment Status
- **Git Status**: {{GIT_STATUS}}
- **CI/CD**: {{CI_STATUS}}
- **Staging**: {{STAGING_STATUS}}
- **Production**: {{PROD_STATUS}}

## Cost Summary
- **Today**: ${{TODAY_COST}}
- **Week TD**: ${{WEEK_COST}}
- **Month TD**: ${{MONTH_COST}}
- **Budget Remaining**: ${{BUDGET_REMAINING}} ({{BUDGET_PERCENT}}%)

## Quick Links
- [Current PR]({{CURRENT_PR_URL}})
- [Project Board]({{PROJECT_BOARD_URL}})
- [Documentation]({{DOCS_URL}})
- [Monitoring Dashboard]({{MONITORING_URL}})

---

## Agent Assignments
{{#AGENT_ASSIGNMENTS}}
### {{AGENT_NAME}}
- **Current Task**: {{TASK}}
- **Status**: {{STATUS}}
- **Next Action**: {{NEXT_ACTION}}
{{/AGENT_ASSIGNMENTS}}

## Worktree Status
{{#WORKTREES}}
- {{WORKTREE_NAME}}: {{BRANCH}} ({{STATUS}})
{{/WORKTREES}}

## Session Log Highlights
{{#LOG_HIGHLIGHTS}}
- {{TIMESTAMP}}: {{EVENT}}
{{/LOG_HIGHLIGHTS}}