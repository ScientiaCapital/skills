# Skills Library Planning

**Current Sprint:** Skills Library Upgrade (31 → 36)
**Date:** 2026-02-07
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### Full Library Upgrade (IN PROGRESS)

| Task | Status |
|------|--------|
| Phase 0: Doc cleanup (README, CLAUDE.md, SETUP, ARCHIVE) | ✅ complete |
| Phase 1: Global hooks (~/.claude/settings.json) | 🔄 in progress |
| Phase 2: Workflow-orchestrator polish | ⏳ pending |
| Phase 3: 4 new skills (subagent-teams, agent-capability-matrix, cost-metering, portfolio-artifact) | ⏳ pending |
| Phase 4: miro-skill | ⏳ pending |
| Phase 5: Metadata updates (INDEX, DEP_GRAPH, TEST_MATRIX → 36) | ⏳ pending |
| Phase 6: Deploy + test + commit | ⏳ pending |

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
