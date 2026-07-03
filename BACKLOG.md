# Skills Library Backlog

## P1: Current Priority

- [ ] **batch-send-drafts-skill (#83)** — plan complete + DA-reviewed (~/.claude/plans/cheeky-floating-moler.md); blocked on gws CLI OAuth (`gcloud auth login` → `gws auth setup`). Carried from 2026-04-01.
- [ ] **Harvest discipline** — new skills must be created in the repo (or copied back same-day), not directly in ~/.claude/skills/ or Downloads. P14 recovered 12 unversioned skills; avoid a repeat.
- [ ] **Referenced-but-missing skills** — `sdr-email-sms-playbook`, `orlob-discovery-framework`, `weekly-kpi-report` are cited by the June SDR skills but exist only as cloud scheduled-task prompts. Export them into the repo as skills or downgrade the references to prose.

All earlier P1 items complete (see [ARCHIVE.md](./ARCHIVE.md)).

---

## P2: Recently Completed

- [x] subagent-teams-skill (in-session Task tool orchestration)
- [x] agent-capability-matrix-skill (task → agent routing)
- [x] cost-metering-skill (API cost tracking + budgets)
- [x] portfolio-artifact-skill (GTME metrics extraction)
- [x] miro-skill (Miro board interaction via MCP)
- [x] hubspot-revops-skill (HubSpot SQL analytics, lead scoring, pipeline forecasting)
- [x] Workflow-orchestrator polish (cost gate, progress rendering)
- [x] Global hooks (PostToolUse formatting)

---

## P3: Future Enhancements

- [x] Skill version tracking (completed 2026-02-07 — config.json backfill)
- [x] Auto-healing for broken skills (/heal-skill) — completed 2026-02-07
- [x] Skill usage analytics — completed 2026-02-22 (PostToolUse hook + reporting script)
- [x] Integration tests for skill activation — completed 2026-02-22 (scripts/test-skills.sh)
- [x] React + Vite SPA patterns for frontend-ui-skill — completed 2026-02-22

---

## P12: Self-Improvement Infrastructure — Future Work

- [x] **Extend outcome emit to all skills** — completed 2026-04-01 (commit 9cced08). P14 follow-up 2026-07-03: capture loop was project-scoped and lost outcomes from other sessions; fixed with user-level SessionStart sweep hook (scripts/sweep-outcomes.sh).
- [ ] **Auto-variant promotion** — when a variant has statistically significant better success rate over 2 weeks, auto-update weight split. Effort: HIGH.
- [ ] **Observer-driven prompt rewriting** — health observer proposes SKILL.md edits for underperforming skills, human approves. Effort: HIGH.
- [ ] **Dashboard UI** — web-based visualization of outcomes.jsonl + SKILL_HEALTH.md. Effort: MEDIUM. Currently CLI-only.

---

## P4: Tech Debt (from Observer/Test Findings)

- [x] **trading-signals routing orphan audit** — 4 orphaned files (swarm-consensus, chinese-llm-stack, turtle-trading, wyckoff) added to routing table. 18/18 coverage. Completed 2026-03-13.
- [ ] **Stale hardware refs cleanup** — M1/8GB references remain in agent-teams, subagent-teams, SKILLS_INDEX.md. Impact: LOW. Effort: MINIMAL.

- [x] **T5 line count violations** — 6 skills trimmed to under 500 lines. Completed 2026-02-22. Results: agent-teams (717→331), api-testing (592→261), gtm-pricing (516→110), api-design (515→403), security (515→438), worktree-manager (510→404). Content extracted to reference/ files.

---

## P5: Platform Updates (from 2026-02-22 research)

- [x] **Update agent-teams-skill** v1.2.0 — TeammateIdle/TaskCompleted hooks, split pane details, plan approval flow. Completed 2026-02-22.
- [x] **Update worktree-manager-skill** v1.2.0 — WorktreeCreate/WorktreeRemove hooks, native vs skill-managed guidance. Completed 2026-02-22.
- [x] **Update subagent-teams-skill** v1.1.0 — memory scopes, background execution, agent_type table. Completed 2026-02-22.
- [x] **Update skill frontmatter** across library for new fields (`model`, `context: fork`, `hooks`). Completed 2026-02-22. Added complete 10-field frontmatter reference to skills.md, updated SKILL_TEMPLATE.md, added `disable-model-invocation` to 3 skills, fixed heal-skill allowlist.
- [x] **Audit PreToolUse hooks** for deprecated `decision` format — migrate to `hookSpecificOutput.permissionDecision`. Completed 2026-02-22. 3 edits in hooks.md, Stop hooks correctly left unchanged.
- [x] **Add comments to bare `except:` clauses** in unsloth-training-skill reference code (2 instances). Completed 2026-02-22.

---

## P6: Observer Debt Cleanup (from 2026-02-22 session)

- [x] **Bare `except:` in data-analysis-skill** — `data-wrangling.md` lines 111, 427. Fixed: `except (ValueError, TypeError):` and `except Exception:`. Completed 2026-02-22.
- [x] **Bare `except:` in workflow-orchestrator debug-methodology.md** — Line 15 (anti-pattern comment added), line 370 (narrowed to `except Exception:`). Completed 2026-02-22.
- [x] **SKILL_TEMPLATE.md body format** — Converted from markdown headings to canonical XML tag structure. Completed 2026-02-22.
- [x] **Archive stale frontend-ui-skill contract** — Marked CLOSED, moved to `.claude/archive/`. Completed 2026-02-22.

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
- Max 6 concurrent (24GB M4)

---

> **Archive:** See [ARCHIVE.md](./ARCHIVE.md) for completed work.
