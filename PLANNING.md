# Skills Library Planning

**Current Sprint:** Add 8 External Skills
**Start Date:** 2025-12-23
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Workstreams

| Stream | Status | Agent |
|--------|--------|-------|
| worktree-manager-skill | in_progress | Wave 1 |
| create-plans-skill | in_progress | Wave 1 |
| debug-like-expert-skill | pending | Wave 1 |
| create-subagents-skill | pending | Wave 2 |
| create-agent-skills-skill | pending | Wave 2 |
| create-hooks-skill | pending | Wave 2 |
| create-slash-commands-skill | pending | Wave 2 |
| create-meta-prompts-skill | pending | Wave 2 |

---

## Review Gates

- [ ] RG1: Repos cloned successfully
- [ ] RG2: All SKILL.md have valid YAML frontmatter
- [ ] RG3: No OpenAI references
- [ ] RG4: All 8 skills in ~/.claude/skills/
- [ ] RG5: SKILLS_INDEX.md shows 25 skills
- [ ] RG6: Git commit clean

---

## Memory Budget (8GB M1)

| Component | RAM |
|-----------|-----|
| macOS base | ~2GB |
| Ghostty | ~100MB |
| Claude agent | ~1.5GB each |
| **Available** | ~4GB (2-3 agents max) |

---

## Completed This Session

- [x] Created PLANNING.md
- [x] Created BACKLOG.md
