# Skills Library Planning

**Current Sprint:** Config.json Backfill + Version Tracking
**Date:** 2026-02-07
**Constraint:** M4 24GB RAM - max 5-6 parallel agents

---

## Active Work

### Feb 2026 Platform Updates — 4 Skill Updates (COMPLETE)

| Task | Skill | Status |
|------|-------|--------|
| Add 15 hook events, agent/async/skill-scoped hooks, `once: true` | extension-authoring v1.1.0 | ✅ complete |
| Add `disable-model-invocation`, skill-scoped hooks section | extension-authoring v1.1.0 | ✅ complete |
| Add display modes, limitations, TeammateIdle/TaskCompleted hooks | agent-teams v1.1.0 | ✅ complete |
| Update M4 24GB constraints, display_mode config | agent-teams v1.1.0 | ✅ complete |
| Update rate card: Opus $5/$25, Haiku $1/$5 | cost-metering v1.1.0 | ✅ complete |
| Fix model refs (4.5→4.6), add native `--worktree` section | worktree-manager v1.1.0 | ✅ complete |
| Update workflow-orchestrator cost table | workflow-orchestrator | ✅ complete |
| Update PLANNING.md, SKILLS_INDEX.md | project docs | ✅ complete |

**Scope:** Verified against official docs at code.claude.com (Feb 2026). New features: `disable-model-invocation`, `once: true`, agent hooks, async hooks, 15 lifecycle events, display modes, `--worktree` flag, updated model pricing.

### Dual-Team Workflow — workflow-orchestrator v2.0.0 (COMPLETE)

| Task | Status |
|------|--------|
| Create reference/dual-team-architecture.md | ✅ complete |
| Create reference/observer-patterns.md | ✅ complete |
| Create reference/devils-advocate.md | ✅ complete |
| Create templates/OBSERVER_QUALITY.md | ✅ complete |
| Create templates/OBSERVER_ARCH.md | ✅ complete |
| Update SKILL.md to v2.0.0 (dual-team, <500 lines) | ✅ complete |
| Update config.json (v2.0.0, new integrations/triggers) | ✅ complete |
| Update CLAUDE.md, SKILLS_INDEX.md, DEPENDENCY_GRAPH.md | ✅ complete |
| Deploy and verify | ✅ complete |

**Scope:** Major update adding Builder + Observer concurrent teams, devil's advocate pattern, contract-first development, Observer BLOCKER gates, and Native Agent Teams integration (experimental).

### Config.json Backfill + Version Tracking (COMPLETE)

| Task | Status |
|------|--------|
| Push unpushed commit | ✅ complete |
| Update 3 existing configs (docker-compose, openrouter, worktree-manager) | ✅ complete |
| Create 27 new config.json files | ✅ complete |
| Verify all 37 have version field | ✅ complete |
| Update metadata docs | ✅ complete |
| Commit + verify | ✅ complete |

**Result:** 100% config.json coverage (37/37) with standardized schema + `version: "1.0.0"`.

### Previous Sprint: hubspot-revops-skill (#37) — COMPLETE

All tasks delivered. See [ARCHIVE.md](./ARCHIVE.md).

### Previous Sprint: Full Library Upgrade (31 → 36) — COMPLETE

All phases delivered. See [ARCHIVE.md](./ARCHIVE.md).

---

## Next Up

- [x] Auto-healing for broken skills (/heal-skill) — ✅ shipped as skill #38
- [ ] Skill usage analytics
- [ ] Integration tests for skill activation

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
- Max 6 concurrent (24GB M4)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed sprints.
