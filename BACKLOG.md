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
- [x] Skill usage analytics — completed 2026-02-22 (PostToolUse hook + reporting script)
- [x] Integration tests for skill activation — completed 2026-02-22 (scripts/test-skills.sh)
- [x] React + Vite SPA patterns for frontend-ui-skill — completed 2026-02-22

---

## P4: Tech Debt (from Observer/Test Findings)

- [ ] **T5 line count violations** — 6 skills over 500 lines. Extract content to reference files. Effort: SMALL per skill, Impact: LOW (advisory only). Skills: agent-teams (717), api-testing (592), gtm-pricing (516), api-design (515), security (515), worktree-manager (510)

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
