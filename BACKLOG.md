# Skills Library Backlog

## P1: Current Priority

All P1 items complete (see [ARCHIVE.md](./ARCHIVE.md)).

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

## P4: Tech Debt (from Observer/Test Findings)

- [x] **T5 line count violations** — 6 skills trimmed to under 500 lines. Completed 2026-02-22. Results: agent-teams (717→331), api-testing (592→261), gtm-pricing (516→110), api-design (515→403), security (515→438), worktree-manager (510→404). Content extracted to reference/ files.

---

## P5: Platform Updates (from 2026-02-22 research)

- [x] **Update agent-teams-skill** v1.2.0 — TeammateIdle/TaskCompleted hooks, split pane details, plan approval flow. Completed 2026-02-22.
- [x] **Update worktree-manager-skill** v1.2.0 — WorktreeCreate/WorktreeRemove hooks, native vs skill-managed guidance. Completed 2026-02-22.
- [x] **Update subagent-teams-skill** v1.1.0 — memory scopes, background execution, agent_type table. Completed 2026-02-22.
- [ ] **Update skill frontmatter** across library for new fields (`model`, `context: fork`, `hooks`). Effort: MEDIUM, Impact: LOW.
- [ ] **Audit PreToolUse hooks** for deprecated `decision` format — migrate to `hookSpecificOutput.permissionDecision`. Effort: SMALL, Impact: LOW.
- [ ] **Add comments to bare `except:` clauses** in unsloth-training-skill reference code (2 instances). Effort: MINIMAL, Impact: LOW.

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
