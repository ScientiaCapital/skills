# Skills Library Planning

**Current Sprint:** Config.json Backfill + Version Tracking
**Date:** 2026-02-07
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### Config.json Backfill + Version Tracking (COMPLETE)

| Task | Status |
|------|--------|
| Push unpushed commit | ✅ complete |
| Update 3 existing configs (docker-compose, openrouter, worktree-manager) | ✅ complete |
| Create 27 new config.json files | ✅ complete |
| Verify all 37 have version field | ✅ complete |
| Update metadata docs | ✅ complete |
| Commit + verify | ✅ complete |

**Result:** 100% config.json coverage (37/37) with standardized schema + `version: "1.0.0"`.

### Previous Sprint: hubspot-revops-skill (#37) — COMPLETE

All tasks delivered. See [ARCHIVE.md](./ARCHIVE.md).

### Previous Sprint: Full Library Upgrade (31 → 36) — COMPLETE

All phases delivered. See [ARCHIVE.md](./ARCHIVE.md).

---

## Next Up

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
