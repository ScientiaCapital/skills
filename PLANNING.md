# Skills Library Planning

**Current Sprint:** P14 — Harvest, Repair & Full Refinement
**Date:** 2026-07-03
**Constraint:** M4 24GB RAM - max 5-6 parallel agents

---

## Active Work

### P14: Harvest, Repair & Full Refinement (IN PROGRESS)

**Date:** 2026-07-03
**Scope:** FULL — repo was dormant since 2026-04-09 while skill development continued outside version control.

| Task | Status |
|------|--------|
| Phase 1: Harvest 12 unversioned skills (9 from ~/.claude/skills + 3 SDR skills from Downloads) into active/ | Complete |
| Phase 1b: Normalize all 12 (config.json, XML sections, ≤500 lines) — 3 parallel agents | Complete |
| Phase 2: Repair P12 analytics — root cause: capture hook was project-scoped; added user-level SessionStart sweep (scripts/sweep-outcomes.sh); backfilled 5 orphaned June sidecars; first SKILL_HEALTH.md generated | Complete |
| Phase 3: Docs refresh (README/INDEX/GRAPH/TEST_MATRIX to 82 skills) + hygiene (work-artifacts/, stale zips, config name fixes) | In Progress |
| Phase 4: Full quality audit — MCP tool refs, stale identifiers, BDR gates, dedup, line limits | Pending |
| Phase 5: Verify + deploy + commit | Pending |

**Library:** 82 skills (2 stable, 80 active). Naming exceptions (live-automation names, no `-skill` suffix): `nooks-autopilot`, `sdr-dial-lists`, `sdr-call-coaching`, `epiphan-call-playbook` — directory rename would change the deployed skill name and break scheduled tasks.

### P13: Post-Audit Remediation (COMPLETE)

**Date:** 2026-04-09
**Scope:** 28 issues resolved across 4 phases.

| Task | Status |
|------|--------|
| Phase 1: 4 critical bugs + 3 RED skills remediated (Golden Rules gates, MCP tool refs) | Done |
| Phase 2: Stage S `bdr_suppression_until` gate injected into all 13 BDR skills | Done |
| Phase 3: Conflicting activation triggers removed (cold email, callable leads, SOD/morning brief) | Done |
| Phase 4: 3 personal skills promoted to library (ae-handoff-brief, call-recording-analyzer, dead-deal-recovery) → 70 skills | Done |

### P12: Autoresearch Self-Improving Skills (COMPLETE)

**Date:** 2026-03-21
**Scope:** FULL — 5 phases, DA audit, 10 new files, 8 edits.
**Inspired by:** Karpathy's autoresearch (immutable eval + mutable strategy + greedy hill climbing)

| Task | Status |
|------|--------|
| Phase 1: Outcome logging (log-outcome.sh, validate, report, hook, 2 pilot skills) | Complete |
| Phase 2: Feedback capture (/skill-feedback + log-feedback.sh) | Complete |
| Phase 3: Skill health observer (agent, CLI, slash command, morning pipeline) | Complete |
| Phase 4: A/B variants (variant-assigner.sh, cold-email pilot, T9, test-outcomes.sh T10-T14) | Complete |
| Phase 5: Metadata updates (CLAUDE.md, BACKLOG.md, PLANNING.md) | Complete |

**Test Results:** 537 per-skill tests (T1-T9) + 8 infrastructure tests (T10-T14) = 545 total, all passing.

### P11: Worked Examples + Metadata Refresh (COMPLETE)

**Date:** 2026-03-17
**Scope:** STANDARD — 49→67 skills, BDR automation pipeline, sales intelligence imports.

### P10: Strategy Cluster + Tech Debt Cleanup (COMPLETE)

**Date:** 2026-03-16
**Scope:** FULL — observer-full + 4 build agents + 3 simplify agents + DA audit + code reviewer. 34 files modified.

| Task | Status |
|------|--------|
| Create challenger-sale-skill (Teach-Tailor-Take Control) | Done |
| Create never-split-the-difference-skill (tactical empathy, Ackerman) | Done |
| Cross-reference 5 strategy skills (JTBD ↔ Blue Ocean ↔ BMC ↔ Challenger ↔ NSTTD) | Done |
| Add methodology_integration to sales-revenue-skill | Done |
| Fix dependencies→depends_on key in 7 workflow skills | Done |
| Fix "strategy canvas" trigger collision (miro vs blue-ocean) | Done |
| Fix "dashboard" trigger collision (frontend-ui vs data-analysis) | Done |
| Fix 7 one-way integrates_with references | Done |
| Fix agent-teams category casing (dev-tools→Dev Tools) | Done |
| Bulk up gtm-pricing-skill (80→332 lines) | Done |
| Update SKILLS_INDEX, DEPENDENCY_GRAPH, CLAUDE.md, README (47→49) | Done |
| Full DA audit + code review of all 49 skills | Done |
| Simplify pass (3 parallel review agents) | Done |

**Deliverables:**
- 2 new skills: challenger-sale-skill, never-split-the-difference-skill
- 5-skill strategy cluster with first-principles pipeline (JTBD → Blue Ocean → BMC → Challenger → NSTTD)
- All tech debt from code review audit resolved
- All 344 tests passing, 49 zips rebuilt, deployed
- Commit: `1e2898f`

### P9: Full Library Audit & Fixes (COMPLETE)

**Date:** 2026-03-15
**Scope:** STANDARD — observer-full + 3 explore agents + DA audit. 8 files modified.

| Task | Status |
|------|--------|
| Fix blocking UserPromptSubmit hook (.claude/settings.json) | Done |
| Structural audit all 46 skills (SKILL.md + config.json) | Done — 46/46 PASS |
| Tool reference validation (fictional/broken MCP refs) | Done — 45/46 clean, 1 fixed |
| Quality and consistency audit (index sync, scripts, DA) | Done |
| Observer-full drift detection (7 patterns) | Done — all prior alerts resolved |
| Verify DA audit blockers fixed (identify_company, clari_*, triggers) | Done — all 3 fixed |
| Hooks best-practices alignment (vs code.claude.com docs) | Done |
| Fix all issues + simplify | Done |

**Deliverables:**
- Removed broken `UserPromptSubmit` prompt hook (was blocking all input)
- Fixed stale Clay UUID prefix `mcp__00505aa5...` → `mcp__claude_ai_Clay__` (crm-integration)
- Added `<objective>`, `<quick_start>`, `<success_criteria>` XML sections to ibkr-api-skill
- Extracted clay-enrichment-patterns.md reference file (crm-integration 626 → 496 lines)
- Updated Stop hook to canonical `decision: "block"` format per official docs
- Added ibkr-api-skill to DEPENDENCY_GRAPH.md (45 → 46 count)
- Added ibkr-api-skill section to SKILLS_INDEX.md Quick Lookup + detailed listing
- Cleaned up ALERTS.md (5 stale alerts → all resolved)
- Set up Context7 CLI + Skills (replaced quota-exhausted MCP)
- All 323 tests passing, all 46 skills green

### P8: Workflow Wiring Sprint (COMPLETE)

**Date:** 2026-03-15

### P7: LangGraph Agents v2.0.0 + Trading-Signals v2.1 (COMPLETE)

**Date:** 2026-03-13
**Scope:** FULL — observer-full ran. 15+ files modified.

| Task | Skill | Status |
|------|-------|--------|
| Fix 3 CRITICALs (wrong imports, broken APIs) | langgraph-agents | Done |
| Fix 7 WARNINGs (deprecated imports, cross-refs, fictitious APIs) | langgraph-agents | Done |
| 4 new reference files (guardrails, testing, observability, deployment) | langgraph-agents | Done |
| 7 existing reference file updates | langgraph-agents | Done |
| SKILL.md, config.json v2.0.0, SKILLS_INDEX.md | langgraph-agents | Done |
| trading-signals v2.1 (daily workflow, backtesting, deep enhancements) | trading-signals | Done |

**Deliverables:**
- langgraph-agents v2.0.0: 14 reference files, all fictitious APIs removed, correct imports throughout
- trading-signals v2.1: 18 reference files, daily trading workflow automation, backtesting patterns
- All 274 tests passing, 40 zips rebuilt, gitleaks clean
- Observer quality: 0 BLOCKERs, 0 CRITICALs at end of session

### P6: Observer Debt Cleanup (COMPLETE)

| Task | Scope | Changes |
|------|-------|---------|
| Bare `except:` in data-wrangling.md | MINIMAL | Lines 111, 427: narrowed to specific exception types |
| Bare `except:` in debug-methodology.md | MINIMAL | Line 15: anti-pattern comment, line 370: `except Exception:` |
| SKILL_TEMPLATE.md body format | SMALL | Converted markdown headings to canonical XML tag structure |
| Archive frontend-ui-skill contract | MINIMAL | APPROVED → CLOSED, moved to `.claude/archive/` |

**Scope:** SMALL — observer-lite ran. 4 files modified + 1 archive file created.

**Deliverables:**
- All bare `except:` clauses resolved across entire library (0 remaining)
- SKILL_TEMPLATE.md matches canonical format from extension-authoring-skill
- Stale contract archived, `.claude/contracts/` clean
- All 274 tests passing, 40 zips rebuilt

### P5 Tasks 4-6: Frontmatter, Hooks Migration, Except Clauses (COMPLETE)

| Task | Scope | Changes |
|------|-------|---------|
| Task 6: Bare `except:` fixes | MINIMAL | 2 Python files: specific exception types added |
| Task 5: Hooks `decision` migration | SMALL | hooks.md: PreToolUse → `hookSpecificOutput.permissionDecision` (3 edits) |
| Task 4A: skills.md frontmatter ref | MEDIUM | 10-field table, string substitution vars, `context: fork`, dynamic context |
| Task 4B: SKILL_TEMPLATE.md | MINIMAL | YAML frontmatter with commented-out new fields |
| Task 4C: `disable-model-invocation` | MINIMAL | Added to runpod, stripe-stack, worktree-manager |
| Bonus: heal-skill allowlist | MINIMAL | S7b check with valid frontmatter key list |
| Bonus: `{"decision": undefined}` fix | MINIMAL | hooks.md:842 → `{}` (invalid JSON corrected) |

**Scope:** STANDARD — observer-full ran. 9 files modified.

**Deliverables:**
- Complete frontmatter reference in extension-authoring-skill
- Hooks migration to `hookSpecificOutput` format (PreToolUse only)
- 2 bare except clauses narrowed to specific exception types
- 3 skills marked manual-only (`disable-model-invocation: true`)
- heal-skill frontmatter validation allowlist updated
- All 274 tests passing, 40 zips rebuilt

### P5 Tasks 1-3: Core Skill Updates (COMPLETE)

| Skill | Before | After | Changes |
|-------|--------|-------|---------|
| agent-teams v1.2.0 | 331 lines | 403 lines | TeammateIdle/TaskCompleted hooks, split pane details, plan approval flow |
| subagent-teams v1.1.0 | 298 lines | 355 lines | Memory scopes, background execution, agent_type table |
| worktree-manager v1.2.0 | 405 lines | 432 lines | WorktreeCreate/WorktreeRemove hooks, native vs skill guidance |

**Also fixed:** PreToolUse observer hook now skips files outside project dir (jq-based path extraction).

**Scope:** STANDARD — observer-full ran. 9 files modified, all under 500-line limit.

**Deliverables:**
- 3 skill updates with platform-current hook events and API features
- Observer hook path exclusion fix (settings.json + settings.local.json)
- All 274 tests passing, 40 zips rebuilt

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

All P1-P11 backlog items complete. Library at 49 skills, all production-ready.

**Completed milestones:**
- [x] P9: Full library audit — 46/46 pass, all DA findings resolved
- [x] P10: Strategy cluster (5 skills) + tech debt cleanup — 49/49 pass
- [x] P11: Worked examples + metadata refresh

**Remaining low-priority items (no sprint assigned):**
- [ ] config.json `name` field inconsistency (~12 with `-skill` suffix, ~35 without) — cosmetic
- [ ] 18 config.json files missing optional `description` field
- [ ] Add reference docs to 3 empty-ref workflow skills (deal-momentum, meddic-call-prep, portfolio-deal-linker)
- [ ] Split crm-integration-skill if it grows past 500 lines again (currently 496)
- [ ] Explore new hook events: TaskCompleted, ConfigChange, Elicitation
- [ ] Strategy cluster shared reference file (reduce 5 pipeline diagram copies to 1)

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
