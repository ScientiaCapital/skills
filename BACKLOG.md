# Skills Library Backlog

## P1: Current Priority

- [x] Test each skill activation with trigger phrases ✅ 30/30 passing
- [x] Document worktree workflow in README ✅ DONE 2026-02-05
- [x] Create skill dependency graph ✅ DONE 2026-02-05 (DEPENDENCY_GRAPH.md)
- [x] Deploy skills globally with symlinks ✅ Done
- [x] Create agent-teams-skill ✅ IN PROGRESS 2026-02-07

---

## P2: Future Enhancements

- [ ] Create subagent-teams-skill (in-session Task tool orchestration)
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

## Skill Ideas (Inbox)

_Add new skill ideas here for triage_

- [x] git-workflow-skill (conventional commits, PR templates) ✅ DONE 2026-02-05
- [x] api-testing-skill (Postman/Bruno patterns) ✅ DONE 2026-02-05
- [x] openrouter-skill (Chinese LLMs via OpenRouter) ✅ DONE 2026-02-05
- [x] docker-compose-skill (local dev environments) ✅ DONE 2026-02-05
- [x] agent-teams-skill (parallel Claude Code orchestration) ✅ 2026-02-07
- [ ] subagent-teams-skill (in-session Task tool teams)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed work.
