# Skills Library Backlog

## P1: Current Sprint (2025-12-23) ✅ COMPLETED

- [x] Create PLANNING.md
- [x] Create BACKLOG.md
- [x] Clone worktree-manager-skill
- [x] Clone taches-cc-resources
- [x] Convert all 8 skills to Tim's format
- [x] Configure worktree-manager for M1/8GB + Ghostty
- [x] Deploy to ~/.claude/skills/
- [x] Update SKILLS_INDEX.md (17 → 25)
- [x] Create dist/ zips for Claude Desktop
- [x] Create audit.sh script with logging
- [x] Add shell aliases (wt-audit, wt-cleanup, etc.)

---

## P2: Post-Sprint

- [ ] Test each skill activation with trigger phrases
- [ ] Add reference/ folders for complex skills
- [ ] Document worktree workflow in README
- [ ] Create skill dependency graph

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

## P3: Future Enhancements

- [ ] Skill version tracking
- [ ] Auto-healing for broken skills (/heal-skill)
- [ ] Skill usage analytics
- [ ] Integration tests for skill activation

---

## Skill Ideas (Inbox)

_Add new skill ideas here for triage_

- [ ] git-workflow-skill (conventional commits, PR templates)
- [ ] api-testing-skill (Postman/Bruno patterns)
- [ ] docker-compose-skill (local dev environments)
