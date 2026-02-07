# Skills Library Planning

**Current Sprint:** Skill Polish + Maintenance
**Date:** 2026-02-07
**Constraint:** M1 8GB RAM - max 2-3 parallel agents

---

## Active Work

### Skill Polish Session (COMPLETED 2026-02-07)

| Task | Status |
|------|--------|
| Polish worktree-manager: .claude/ dir propagation, hooks, permissions | ✅ complete |
| Polish agent-teams: CLAUDE.md inheritance, @claude bot, plan mode | ✅ complete |
| Update SKILL_TEST_MATRIX.md: 28 → 31 skills | ✅ complete |
| Deploy + rebuild zips (31/31) | ✅ complete |

---

## Completed Work

### agent-teams-skill (COMPLETED 2026-02-07)

| Task | Status |
|------|--------|
| Create SKILL.md + config.json + 3 reference files | ✅ complete |
| Update SKILLS_INDEX.md + DEPENDENCY_GRAPH.md | ✅ complete |
| Deploy, test activation, git commit | ✅ complete |
| Polish: .claude/ propagation, CLAUDE.md inheritance, @claude bot | ✅ complete |

### langgraph-agents-skill Polish (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Add Functional API reference | ✅ complete |
| Add Deep Agents reference | ✅ complete |
| Add MCP Integration reference | ✅ complete |
| Add Streaming Patterns reference | ✅ complete |
| Update orchestration-patterns with HITL | ✅ complete |
| Update state-schemas with runtime context | ✅ complete |
| Update context-engineering with 3 context types | ✅ complete |
| Update SKILL.md with new patterns | ✅ complete |
| Test skill activation | ✅ complete |

### git-workflow-skill (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Create SKILL.md | ✅ complete |
| Create commit-examples reference | ✅ complete |
| Test skill activation | ✅ complete |

### api-testing-skill (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Create SKILL.md | ✅ complete |
| Create 5 reference files | ✅ complete |
| Update SKILLS_INDEX.md | ✅ complete |
| Deploy and test activation | ✅ complete |

### openrouter-skill (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Create SKILL.md + 7 reference files + config.json | ✅ complete |
| Update SKILLS_INDEX.md | ✅ complete |
| Create dist zip | ✅ complete |

### docker-compose-skill (COMPLETED 2026-02-05)

| Task | Status |
|------|--------|
| Create SKILL.md + 4 reference files + config.json | ✅ complete |
| Update SKILLS_INDEX.md + README | ✅ complete |
| Create dist zip | ✅ complete |

### Workflow Orchestrator Skill v2.0 (COMPLETED 2026-01-23)
Full workflow orchestration system with cost tracking, model routing, and 70+ agent catalog.

### Spec Compliance Audit (COMPLETED 2026-01-23)
All 25 skills now comply with Anthropic YAML specification.

### Testing/Security/API Skills (COMPLETED 2026-01-23)
Added testing-skill, security-skill, and api-design-skill to Dev Tools category.

### Worktree-Manager Enhancements (COMPLETED 2025-12-24)
Boris Cherny workflow integration, .env handling, model selection.

---

## Next Up

- [ ] Create subagent-teams-skill (in-session Task tool orchestration)
- [ ] Skill version tracking
- [ ] Auto-healing for broken skills (/heal-skill)

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
