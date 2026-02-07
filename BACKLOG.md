# Skills Library Backlog

## P1: Current Priority

All P1 items complete (see [ARCHIVE.md](./ARCHIVE.md)).

---

## P2: In Progress (This Sprint)

- [ ] subagent-teams-skill (in-session Task tool orchestration)
- [ ] agent-capability-matrix-skill (task → agent routing)
- [ ] cost-metering-skill (API cost tracking + budgets)
- [ ] portfolio-artifact-skill (GTME metrics extraction)
- [ ] miro-skill (Miro board interaction via MCP)
- [ ] Workflow-orchestrator polish (cost gate, progress rendering)
- [ ] Global hooks (PostToolUse formatting)

---

## P3: Future Enhancements

- [ ] Skill version tracking
- [ ] Auto-healing for broken skills (/heal-skill)
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
- Max 4 concurrent (8GB M1, warning at 5GB)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed work.
