# Project Context: skills

**Updated:** 2026-04-01
**Branch:** main
**Tech Stack:** Claude Code Skills Library (67 skills, Markdown/Bash, P12 autoresearch framework)

---

## Status

67 production-ready skills (2 stable, 65 active). P12 autoresearch self-improving framework complete — all 67 skills now emit outcome sidecars to `~/.claude/skill-analytics/outcomes.jsonl`. A/B variant pilot active on cold-email-sequence-generator (control vs concise). Skill #68 (batch-send-drafts) planned + DA-reviewed, blocked on gws CLI OAuth auth.

## Recent Commits

```
9cced08 feat: add outcome emission to all 67 skills (autoresearch expansion)
a896242 chore: config.json tech debt — add 18 descriptions, normalize 36 names
ee8c7eb feat: Golden Rules 90-day stale AE exception
da4a13b fix: outcome-report.sh grep-c arithmetic bug
6ae85ba feat: P12 autoresearch self-improving skills framework
```

## Done (This Session — Apr 1)

- [x] Researched batch Gmail draft sending — identified gap (Gmail MCP has no send capability)
- [x] Evaluated gws CLI (googleworkspace/cli) as solution — confirmed it exposes `drafts.send`
- [x] Designed batch-send-drafts-skill with Plan agent (6-stage workflow, state persistence, rate limiting)
- [x] DA Review #1: Found 3 blockers (no flock on macOS, gws not installed, Workspace OAuth risk), 4 high, 4 medium, 3 low — all mitigated in plan
- [x] DA Review #2 (final gate): Conditional pass, 2 conditions resolved (config.json schema, permissions pattern)
- [x] Installed gws CLI v0.22.5 via brew + google-cloud-sdk
- [x] Auth blocked — gws auth setup needs gcloud auth login first, session ended before completing browser OAuth flow
- [x] Plan saved to ~/.claude/plans/cheeky-floating-moler.md — ready to resume

## Next Steps

1. **Complete gws OAuth auth** — `gcloud auth login` → `gws auth setup` → `gws auth login` → test one draft send
2. **If auth works** — implement batch-send-drafts-skill per plan (Phase 1-4, ~2 hours)
3. **If auth blocked by Workspace admin** — manual OAuth via Google Cloud Console, or ask IT

## Near-Limit Skills (Watch List)

| Skill | Lines | Notes |
|-------|-------|-------|
| crm-integration-skill | 500 | AT LIMIT — any addition requires extraction to reference/ |
| phone-verification-waterfall-skill | 499 | 1 line from limit |
| git-workflow-skill | 495 | 5 lines from limit |
| voice-ai-skill | 490 | 10 lines from limit |

## Blockers

- **batch-send-drafts-skill:** gws CLI OAuth auth not yet completed (gcloud auth login needed)

---

_Updated each session by END DAY workflow._
