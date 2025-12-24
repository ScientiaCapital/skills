# Skills Library Backlog

## P1: Current Priority

- [ ] Test each skill activation with trigger phrases
- [ ] Add reference/ folders for complex skills
- [ ] Document worktree workflow in README
- [ ] Create skill dependency graph

---

## P2: Future Enhancements

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

- [ ] git-workflow-skill (conventional commits, PR templates)
- [ ] api-testing-skill (Postman/Bruno patterns)
- [ ] docker-compose-skill (local dev environments)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed work.
