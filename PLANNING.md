# Skills Library Planning

**Current Sprint:** hubspot-revops-skill (#37)
**Date:** 2026-02-07
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### hubspot-revops-skill (COMPLETE)

| Task | Status |
|------|--------|
| Create SKILL.md + config.json | ✅ complete |
| Create reference/api-guide.md | ✅ complete |
| Create reference/sql-analytics.md | ✅ complete |
| Create reference/enrichment-pipelines.md | ✅ complete |
| Create reference/architecture.md | ✅ complete |
| Update metadata (README, INDEX, DEP_GRAPH, TEST_MATRIX → 37) | ✅ complete |
| Deploy + test + commit | ✅ complete |

### Previous Sprint: Full Library Upgrade (31 → 36) — COMPLETE

All phases delivered. See [ARCHIVE.md](./ARCHIVE.md).

---

## Next Up

- [ ] Skill version tracking
- [ ] Auto-healing for broken skills (/heal-skill)
- [ ] Skill usage analytics
- [ ] Integration tests for skill activation

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
