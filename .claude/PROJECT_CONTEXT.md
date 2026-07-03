# Project Context: skills

**Updated:** 2026-07-03
**Branch:** main
**Tech Stack:** Claude Code Skills Library (86 skills, Markdown/Bash, P12 autoresearch framework)

---

## Status

86 production-ready skills (2 stable, 84 active) after P14+P15. P15 added 4 skills: batch-send-drafts (Gmail draft review/send helper), orlob-discovery-framework (5-step discovery + per-vertical root causes), sdr-email-sms-playbook (5-touch email/SMS cadence), weekly-kpi-report (Friday 5:30 PM scorecard). template-skill stub deleted from deployed. 689/689 tests passing.

## Naming Exceptions (do not "fix")

`nooks-autopilot`, `sdr-dial-lists`, `sdr-call-coaching`, `epiphan-call-playbook` deliberately lack the `-skill` suffix — directory name = deployed skill name = what live scheduled tasks invoke. Renaming breaks automation.

## Done (This Session — Jul 3, P15)

- [x] batch-send-drafts-skill: Gmail draft review + one-click send links (gws OAuth blocked → Python-free design)
- [x] orlob-discovery-framework-skill: 5-step framework + reference/epiphan-root-causes.md (7 verticals)
- [x] sdr-email-sms-playbook-skill: 5-touch email/SMS cadence, full templates for Higher Ed / Courts / Gov / Healthcare
- [x] weekly-kpi-report-skill: Friday 5:30 PM CST per-rep scorecards, Nooks + HubSpot, Slack DM to Tim
- [x] template-skill stub deleted from ~/.claude/skills/
- [x] All docs updated to 86 (README, CLAUDE.md, SKILLS_INDEX, SKILL_TEST_MATRIX)
- [x] 689 tests passing, deployed + zips rebuilt

## Next Steps

1. **Late July:** review Vasil ramping caveats (sdr-call-coaching/sdr-dial-lists ~2026-07-25); confirm Nyasha's Nooks mailbox; confirm he-dial-queue SDR roster
2. **batch-send-drafts full automation:** create GCP project at console.cloud.google.com → `gws auth setup --project <id> --login` → upgrade skill to programmatic send
3. **SKILL_TEST_MATRIX:** 49 skills pending activation re-validation
4. **Next sprint (P16):** TBD — user has questions

## Near-Limit Skills (Watch List)

git-workflow 495 • morning-brief ~490 • voice-ai 490 • data-analysis 487 • business-model-canvas 478 • unsloth-training 477 • linkedin-sales-navigator-alt 472 • post-demo-automation 409 (extract Stage 3/5 before next edit)

## Blockers

- he-dial-queue: SDR-2..4 roster not confirmed (HOLD on Edgar per Tim 2026-06-09)
- Nyasha Chigwedere: no Nooks mailbox → auto-email enrollment held

---

_Updated each session by END DAY workflow._
