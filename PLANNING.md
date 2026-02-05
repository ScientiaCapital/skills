# Skills Library Planning

**Current Sprint:** Doc Hygiene + Skill Testing
**Date:** 2026-02-05
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### langgraph-agents-skill Polish (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Add Functional API reference | ✅ complete |
| Add Deep Agents reference | ✅ complete |
| Add MCP Integration reference | ✅ complete |
| Add Streaming Patterns reference | ✅ complete |
| Update orchestration-patterns with HITL | ✅ complete |
| Update state-schemas with runtime context | ✅ complete |
| Update context-engineering with 3 context types | ✅ complete |
| Update SKILL.md with new patterns | ✅ complete |
| Test skill activation | ✅ complete |

### git-workflow-skill (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Create SKILL.md | ✅ complete |
| Create commit-examples reference | ✅ complete |
| Test skill activation | ✅ complete |

### api-testing-skill (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Create SKILL.md | ✅ complete |
| Create postman-patterns reference | ✅ complete |
| Create bruno-patterns reference | ✅ complete |
| Create test-design reference | ✅ complete |
| Create data-management reference | ✅ complete |
| Create ci-integration reference | ✅ complete |
| Update SKILLS_INDEX.md | ✅ complete |
| Deploy and test activation | ✅ complete |
| Update SKILL_TEST_MATRIX.md | ✅ complete |

---

## Completed Work

### Workflow Orchestrator Skill v2.0 (COMPLETED 2026-01-23)
Full workflow orchestration system with cost tracking, model routing, and 70+ agent catalog.

### Spec Compliance Audit (COMPLETED 2026-01-23)
All 25 skills now comply with Anthropic YAML specification.

### Testing/Security/API Skills (COMPLETED 2026-01-23)
Added testing-skill, security-skill, and api-design-skill to Dev Tools category.

### Worktree-Manager Enhancements (COMPLETED 2025-12-24)
Boris Cherny workflow integration, .env handling, model selection.

---

## Next Up (From Backlog P1)

- [x] Test remaining skill activations ✅ 28/28 passing
- [x] Triage backlog api-testing-skill ✅ CREATED
- [ ] Triage backlog docker-compose-skill
- [ ] Create skill dependency graph
- [ ] Document worktree workflow in README

---

## Worktree Maintenance Schedule

**Weekly (Monday):**
- Run `wt-audit` to check status
- Clean merged: `wt-clean-merged`
- Review stale worktrees (7+ days)

**Monthly (1st):**
- Full audit + clean orphans
- Review audit log: `wt-log-full`

**Before new worktrees:**
- Check memory: `wt-memory`
- Max 4 concurrent (8GB M1, warning at 5GB)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed sprints.
