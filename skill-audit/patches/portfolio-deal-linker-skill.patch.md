# Patch: portfolio-deal-linker-skill

**Score:** trigger=4 tool_integration=4 output_contract=4 failure_handling=3 maintainability=3 (sum=18/25)

**Highest-leverage single change (S effort):** Renumber the duplicate 'Stage 4' and add last-run.json corruption/missing recovery (default trailing-24h window + flag).
**Expected impact:** Removes step-index ambiguity and prevents an undefined attribution window on first/corrupted runs.

## Description

**Before:**
> Auto-update GTME portfolio when HubSpot deals close. Links deal outcomes (won/lost, revenue, cycle time) to the skills, automations, and outreach that influenced them — building VP BD transition evidence automatically. Runs daily at 7am CST or on-demand. Use when: 'portfolio update', 'deal closed', 'link deal to portfolio', 'gtme evidence', 'what did I influence', 'career evidence', 'transition tracker'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] maintainability
- **Evidence** (line 130,193): "## Stage 4: Update Portfolio Files (line 130) ... ## Stage 4: Comp Plan Attainment Tracker (line 193)"
- **Issue:** Two different stages both numbered 'Stage 4' — ambiguous step index; can't tell which runs when.
- **Fix:** Renumber Comp Plan Attainment Tracker to Stage 5 and cascade references.

### [MED] failure_handling
- **Evidence** (line 272-281): ""status":"[success|partial|error]" ... Use status "partial" if some stages failed ... "error" only if no output was generated."
- **Issue:** Status defined but no behavior when the incremental mechanism fails — if last-run.json (line 51) is missing/corrupt the attribution window is undefined; no alert/retry.
- **Fix:** Define last-run.json recovery (default trailing-24h + flag) and retry/skip for failed hubspot_search_deals; log to ~/.claude/skill-runs/.

### [LOW] tool_integration
- **Evidence** (line 53): "Exclude channel deals (`is_channel = true`) and owned by AE IDs '82625923','423155215','190030668' (Lex Evans, Ron Epstein, Phillip Sandler)"
- **Issue:** Re-hardcodes AE owner-ID exclusion inline (a 4th copy across the catalog) instead of referencing canonical Golden Rules; also reads as hard-exclude, ignoring the 90-day stale exception.
- **Fix:** Reference CLAUDE.md Golden Rules owner list once; note stale-AE exception.

## Missing tool references

- qualify_lead (dedupe when matching attributed contacts)

## Self-healing gap (see specs/self-healing-template.md)

Has incremental state (last-run.json, 51) and success|partial|error sidecar (272-281), but no recovery when last-run.json is missing/corrupt, no retry->degrade->alert ladder for a failed HubSpot pull, no run log to ~/.claude/skill-runs/portfolio-deal-linker.jsonl.

## Overlap candidates (flag only — no removal)

- portfolio-artifact-skill
- deal-momentum-analyzer-skill
- weekly-kpi-report-skill
