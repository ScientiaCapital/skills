# Skills Library Backlog

## P1: Current Priority

All P1 items complete (see [ARCHIVE.md](./ARCHIVE.md)).

---

## P2: Recently Completed

- [x] subagent-teams-skill (in-session Task tool orchestration)
- [x] agent-capability-matrix-skill (task → agent routing)
- [x] cost-metering-skill (API cost tracking + budgets)
- [x] portfolio-artifact-skill (GTME metrics extraction)
- [x] miro-skill (Miro board interaction via MCP)
- [x] hubspot-revops-skill (HubSpot SQL analytics, lead scoring, pipeline forecasting)
- [x] Workflow-orchestrator polish (cost gate, progress rendering)
- [x] Global hooks (PostToolUse formatting)

---

## P3: Future Enhancements

- [x] Skill version tracking (completed 2026-02-07 — config.json backfill)
- [x] Auto-healing for broken skills (/heal-skill) — completed 2026-02-07
- [ ] Skill usage analytics
- [ ] Integration tests for skill activation

---

## Recurring: Worktree Maintenance

**Weekly (Monday):**
- Run `wt-audit` to check status
- Clean merged: `wt-clean-merged`
- Review stale worktrees (7+ days)

**Monthly (1st):**
- Full audit + clean orphans
- Review audit log: `wt-log-full`

**Before new worktrees:**
- Check memory: `wt-memory`
- Max 6 concurrent (24GB M4)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed work.
