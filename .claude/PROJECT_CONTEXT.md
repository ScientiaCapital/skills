# Project Context: skills

**Updated:** 2026-07-03 (end of day)
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

## Done (This Session — Jul 3, P16)

- [x] gtm-brain-skill: Neo4j AuraDB graph skill (87th skill); schema initialized live; write/read smoke test passed
- [x] SKILL_TEST_MATRIX: 49 ⏳ → 0 ⏳; 5 trigger conflicts found and resolved; 86/86 validated
- [x] 5 config.json trigger conflicts resolved (pipeline health, discovery call, discovery questions, email template, stalled deals)
- [x] sdr-email-sms-playbook: soft close phrase bank added (15 phrases); title corrected to Sr. BDR

## Next Steps (pick up here tomorrow)

1. **GTM Brain — start feeding it:** after first dial session, say "import today's Nooks calls" → graph auto-populates. After a few weeks "what worked with Higher Ed IT Directors?" returns real signal.
2. **GTM Brain — read wire-up:** add Stage 6/7 read queries into morning-brief-skill and sdr-dial-lists (surface "who responded before at this account").
3. **batch-send-drafts full automation:** create GCP project at console.cloud.google.com → `gws auth setup --project <id> --login`
4. **Late July (~2026-07-25):** remove Vasil ramping caveats (sdr-call-coaching/sdr-dial-lists); confirm Nyasha Nooks mailbox; confirm he-dial-queue SDR roster

## Near-Limit Skills (Watch List)

git-workflow 495 • morning-brief ~490 • voice-ai 490 • data-analysis 487 • business-model-canvas 478 • unsloth-training 477 • linkedin-sales-navigator-alt 472 • post-demo-automation 409 (extract Stage 3/5 before next edit)

## Blockers

- he-dial-queue: SDR-2..4 roster not confirmed (HOLD on Edgar per Tim 2026-06-09)
- Nyasha Chigwedere: no Nooks mailbox → auto-email enrollment held

---

_Updated each session by END DAY workflow._
