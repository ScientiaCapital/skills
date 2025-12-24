# Skills Library Planning

**Current Sprint:** Add 8 External Skills
**Start Date:** 2025-12-23
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Workstreams

| Stream | Status | Agent |
|--------|--------|-------|
| worktree-manager-skill | ✅ complete | Wave 1 |
| create-plans-skill | ✅ complete | Wave 1 |
| debug-like-expert-skill | ✅ complete | Wave 1 |
| create-subagents-skill | ✅ complete | Wave 2 |
| create-agent-skills-skill | ✅ complete | Wave 2 |
| create-hooks-skill | ✅ complete | Wave 2 |
| create-slash-commands-skill | ✅ complete | Wave 2 |
| create-meta-prompts-skill | ✅ complete | Wave 2 |

---

## Review Gates

- [x] RG1: Repos cloned successfully
- [x] RG2: All SKILL.md have valid YAML frontmatter
- [x] RG3: No OpenAI refs in main skills (only LangChain examples in reference/)
- [x] RG4: All 8 skills in ~/.claude/skills/
- [x] RG5: SKILLS_INDEX.md shows 25 skills
- [x] RG6: Git commit clean

---

## Memory Budget (8GB M1)

| Component | RAM |
|-----------|-----|
| macOS base | ~2GB |
| Ghostty | ~100MB |
| Claude agent | ~1.5GB each |
| **Available** | ~4GB (2-3 agents max) |

---

## Completed This Session (2025-12-23)

- [x] Created PLANNING.md
- [x] Created BACKLOG.md
- [x] Cloned worktree-manager-skill + taches-cc-resources
- [x] Converted all 8 skills to Tim's format
- [x] Created M1/8GB optimized config.json (4 worktrees, Ghostty)
- [x] Deployed all 25 skills to ~/.claude/skills/
- [x] Updated SKILLS_INDEX.md (17 → 25)
- [x] Created dist/ zips for Claude Desktop
- [x] Created audit.sh with logging
- [x] Added shell aliases (wt, wt-audit, wt-cleanup, wt-memory)
- [x] Initialized worktree registry
- [x] Security sweep: secrets=0, CVEs=0, env=clean
- [x] Updated 24 Next.js projects to 15.5.9 (critical vulns fixed)
