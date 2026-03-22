# Project Context: skills

**Updated:** 2026-03-22
**Branch:** main
**Tech Stack:** Claude Code Skills Library (67 skills, Markdown/Bash, P12 autoresearch framework)

---

## Status

67 production-ready skills (2 stable, 65 active). P12 autoresearch self-improving framework complete — all 67 skills now emit outcome sidecars to `~/.claude/skill-analytics/outcomes.jsonl`. 545/545 tests passing (537 T1-T9 + 8 T10-T14). A/B variant pilot active on cold-email-sequence-generator (control vs concise).

## Recent Commits

```
a896242 chore: config.json tech debt — add 18 descriptions, normalize 36 names
ee8c7eb feat: Golden Rules 90-day stale AE exception
da4a13b fix: outcome-report.sh grep-c arithmetic bug
6ae85ba feat: P12 autoresearch self-improving skills framework
e237ae8 chore: move orphaned draft to drafts/, gitignore operational artifacts
```

## Done (This Session — Mar 22)

- [x] Audited P12 autoresearch framework (3 explore agents): 0 critical bugs, clean implementation
- [x] Fixed cold-email-sequence-generator: added `runtime_ms`, renamed `ab_variants_written` → `subject_variants_generated`, added `error` field
- [x] Fixed prospect-enrich + morning-brief: added `error` field to outcome schemas
- [x] Added outcome emission sections to all 64 remaining skills (5 parallel agents)
- [x] Handled 500-line limit: blue-ocean extracted example to reference/, 4 skills used compact format
- [x] DA post-flight caught sidecar naming inconsistency: 45 skills had `-skill` suffix, stripped for consistency with pilot convention
- [x] All 545 tests passing, 67/67 skills have outcome emission (100% coverage)

## Near-Limit Skills (Watch List)

| Skill | Lines | Notes |
|-------|-------|-------|
| crm-integration-skill | 500 | AT LIMIT — any addition requires extraction to reference/ |
| phone-verification-waterfall-skill | 499 | 1 line from limit |
| git-workflow-skill | 495 | 5 lines from limit |
| voice-ai-skill | 490 | 10 lines from limit |

## Uncommitted Work

67 SKILL.md files modified (outcome emission sections added) + 1 new file (blue-ocean reference/example-session.md). Ready to commit.

## Blockers

None. All tests pass. No observer alerts.

---

_Updated each session by END DAY workflow._
