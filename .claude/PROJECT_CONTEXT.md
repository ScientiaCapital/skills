# Project Context: skills

**Updated:** 2026-07-03
**Branch:** main
**Tech Stack:** Claude Code Skills Library (82 skills, Markdown/Bash, P12 autoresearch framework)

---

## Status

82 production-ready skills (2 stable, 80 active) after P14 harvest. Repo was dormant Apr 9 → Jul 3 while 12 skills were built outside version control (~/.claude/skills + Downloads); all now committed and normalized. P12 analytics capture repaired (user-level SessionStart sweep hook). Full quality audit done — all RED findings remediated, 657/657 tests passing.

## Naming Exceptions (do not "fix")

`nooks-autopilot`, `sdr-dial-lists`, `sdr-call-coaching`, `epiphan-call-playbook` deliberately lack the `-skill` suffix — directory name = deployed skill name = what live scheduled tasks invoke. Renaming breaks automation.

## Done (This Session — Jul 3, P14)

- [x] Harvested 12 unversioned skills into active/ (9 deployed-only + 3 June SDR skills from Downloads/epiphan-mcp-guide)
- [x] Normalized all 12: config.json, XML sections, ≤500 lines (3 parallel agents)
- [x] Analytics repair: sweep-outcomes.sh + user-level SessionStart hook; 5 June sidecars backfilled; first SKILL_HEALTH.md generated
- [x] Docs refreshed to 82: README, CLAUDE.md, PLANNING (P13+P14), BACKLOG, SKILLS_INDEX, DEPENDENCY_GRAPH, SKILL_TEST_MATRIX (39→82 rows)
- [x] Hygiene: 18 root artifacts → work-artifacts/ (gitignored), 3 stale zips deleted, 3 config name fixes
- [x] Full audit + remediation: 4 nonexistent MCP tools fixed across 6 skills, March ramp targets → dynamic month lookup (3 skills), Stage S gate added to he-dial-queue, 11 stale ~/.agents/skills duplicates deleted, crm-integration + phone-verification-waterfall trimmed (500→411/437)
- [x] Observer reports refreshed (QUALITY/ARCH/SKILL_HEALTH/P14_AUDIT — 2026-07-03)

## Next Steps

1. **batch-send-drafts-skill (#83)** — still blocked on gws OAuth (`gcloud auth login` → `gws auth setup`); plan at ~/.claude/plans/cheeky-floating-moler.md
2. **Late July:** review Vasil ramping caveats (sdr-call-coaching/sdr-dial-lists); confirm Nyasha's Nooks mailbox; confirm he-dial-queue SDR roster
3. **Export cloud-only skills** — sdr-email-sms-playbook, orlob-discovery-framework, weekly-kpi-report exist only as scheduled-task prompts; bring into repo
4. **SKILL_TEST_MATRIX:** 45 skills pending activation re-validation

## Near-Limit Skills (Watch List)

git-workflow 495 • morning-brief ~490 • voice-ai 490 • data-analysis 487 • business-model-canvas 478 • unsloth-training 477 • linkedin-sales-navigator-alt 472 • post-demo-automation 409 (extract Stage 3/5 before next edit)

## Blockers

- batch-send-drafts: gws CLI OAuth not completed

---

_Updated each session by END DAY workflow._
