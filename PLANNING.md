# Skills Library Planning

**Current Sprint:** Doc Hygiene + Skill Testing
**Date:** 2026-02-05
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### Doc Hygiene + YAML Fixes (COMPLETED)

| Task | Status |
|------|--------|
| Update PROJECT_CONTEXT.md | ✅ complete |
| Update PLANNING.md | ✅ complete |
| Create skill activation test matrix | ✅ complete |
| Fix stable skill YAML frontmatter | ✅ complete |
| Update skill count 25→26 | ✅ complete |

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

- [ ] Test each skill activation with trigger phrases
- [ ] Triage backlog skill ideas (git-workflow, api-testing, docker-compose)
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
