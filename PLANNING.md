# Skills Library Planning

**Current Sprint:** Workflow Orchestrator Skill
**Date:** 2025-12-26
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### Workflow Orchestrator Skill v2.0 (IN PROGRESS)

| Task | Status |
|------|--------|
| Update PLANNING.md and archive completed work | in_progress |
| Clean up Backlog.md | pending |
| Create workflow-orchestrator-skill folder | pending |
| Write SKILL.md with YAML frontmatter | pending |
| Create 8 reference/*.md files | pending |
| Create 4 template files | pending |
| Update SKILLS_INDEX.md | pending |
| Package as .skill zip | pending |
| Update deploy.sh for symlinks | pending |
| Test and commit | pending |

### Worktree-Manager .env Enhancement (COMPLETED 2025-12-24)

| Task | Status |
|------|--------|
| Update SKILL.md env copy logic | complete |
| Update config.json envFilePriority | complete |
| Update templates/worktree.json | complete |
| Add safety warning | complete |
| Add model selection (opus/sonnet/haiku) | complete |
| Regenerate dist/ zip | complete |
| Update global skill | complete |
| Git commit & push | complete |
| Security audit | complete |

---

## Next Up (From Backlog P1)

- [ ] Test each skill activation with trigger phrases
- [ ] Add reference/ folders for complex skills
- [ ] Document worktree workflow in README
- [ ] Create skill dependency graph

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
