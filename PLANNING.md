# Skills Library Planning

**Current Sprint:** P4 Tech Debt — Trim Oversized Skills
**Date:** 2026-02-22
**Constraint:** M4 24GB RAM - max 5-6 parallel agents

---

## Active Work

### P4 Tech Debt: Trim 6 Oversized Skills (COMPLETE)

| Skill | Before | After | Reduction |
|-------|--------|-------|-----------|
| agent-teams-skill | 717 | 331 | -54% |
| api-testing-skill | 592 | 261 | -56% |
| gtm-pricing-skill | 516 | 110 | -79% |
| api-design-skill | 515 | 403 | -22% |
| security-skill | 515 | 438 | -15% |
| worktree-manager-skill | 510 | 404 | -21% |

**Scope:** STANDARD — observer-full ran. 6 new reference files created, 6 SKILL.md files trimmed.

**Deliverables:**
- 6 new reference files with extracted content (filtering, rate-limiting, secrets-management, advanced-workflows, workflows-detailed, best-practices-full)
- All 39 skills now under 500-line advisory limit
- All 274 tests passing, 40 zips rebuilt

### P3 Backlog: Analytics, Tests, Vite/SPA Patterns (COMPLETE)

| Task | Status |
|------|--------|
| Create scripts/test-skills.sh (8 test cases, bash+jq) | ✅ complete |
| Create scripts/log-skill-usage.sh (PostToolUse hook target) | ✅ complete |
| Create scripts/skill-analytics-report.sh (usage reporting) | ✅ complete |
| Add PostToolUse Skill hook to .claude/settings.json | ✅ complete |
| Create reference/vite-react-setup.md | ✅ complete |
| Create reference/spa-routing.md | ✅ complete |
| Create templates/vite-react-config.ts | ✅ complete |
| Create templates/spa-app-layout.tsx | ✅ complete |
| Update frontend-ui-skill SKILL.md + config.json for Vite/SPA | ✅ complete |
| Update metadata (PLANNING, BACKLOG, SKILLS_INDEX, README) | ✅ complete |

**Scope:** STANDARD — observer-full ran. 11 new/modified files.

**Deliverables:**
- **Integration tests:** `scripts/test-skills.sh` — 8 automated test cases (T1-T8), `--verbose` and `--skill` options
- **Usage analytics:** PostToolUse Skill hook → JSONL event log, `scripts/skill-analytics-report.sh` for top skills, daily breakdown, unused detection
- **Vite/SPA patterns:** 2 reference files, 2 templates, SKILL.md + config.json updated (24 triggers)

### Previous: Observer Fix + frontend-ui-skill #39 (COMPLETE)

All tasks delivered. See above sprint for continued frontend-ui work.

---

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
- [x] Skill usage analytics — ✅ shipped (PostToolUse hook + reporting script)
- [x] Integration tests for skill activation — ✅ shipped (scripts/test-skills.sh)

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
