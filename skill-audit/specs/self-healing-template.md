# Self-Healing Template (proposal — not applied to any skill by this audit)

Standard block every BDR skill should adopt. Skills reference this file; the logic is not duplicated per-skill.

## 1. Failure definition

A run is one of:
- **success** — all stages completed, data pulled live, output delivered.
- **partial** — at least one stage degraded (a source was empty/unavailable, a spec/brand check was skipped, a delivery step failed) but output was still produced. Must say *which* stage degraded and why.
- **error** — no usable output was produced at all (auth failure, empty required input, unhandled exception).

Every skill's Emit Outcome Sidecar step must map to one of these three and name the failing stage — "error" or "partial" with no reason is not acceptable.

## 2. Fallback ladder

For every external call (HubSpot, Apollo, Clay, Clari, Nooks, Gmail, Google Calendar):

1. **Retry once** with backoff on transient errors (rate limit, timeout).
2. **Degrade**: fall back to a lesser but still-correct source (e.g. Apollo fails → Clay-only; Clari transcript unfetchable → score from call summary only) and mark output partial.
3. **Alert**: on repeated failure or when a mandatory gate can't be evaluated (e.g. qualify_lead unavailable for a list-producing skill), send Tim a Slack DM — do not silently proceed as if the gate passed.
4. **Halt**: if the skill cannot produce a safe/correct output at all (e.g. can't identify the deal/contact), stop and write the error state rather than guessing.

## 3. Run log convention

Every skill appends one JSON line per run to `~/.claude/skill-runs/{skill-name}.jsonl`:

```json
{"ts":"<UTC ISO8601>","skill":"<name>","version":"<semver>","rep":"<owner>","inputs_hash":"<sha256 of key inputs>","status":"success|partial|error","error":"<string|null>","records_in":0,"records_out":0}
```

This is in addition to — not instead of — the existing `~/.claude/skill-analytics/last-outcome-{skill}.json` sidecar. The sidecar is a snapshot of the *last* run; the run log is the trendable history the drift-detection substrate needs. Most audited skills (see `report.html` leaderboard) have the sidecar but not the run log — that is the single most common self-healing gap in this catalog.

## 4. Version consistency

The sidecar's `"version"` field must match the SKILL.md frontmatter `version:`. (Found drifting in `gtm-brain-skill`: sidecar hardcodes `1.0.0` while frontmatter says `1.1.0`.) Reference the frontmatter value; do not hardcode it a second time in the sidecar template.
