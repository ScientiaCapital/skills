# Patch: business-pulse-skill

**Score:** trigger=4 tool_integration=4 output_contract=3 failure_handling=1 maintainability=4 (sum=16/25)

**Highest-leverage single change (S effort):** Add outcome sidecar + empty-data guard (flag 'no live data', never fabricate) and one concrete delivery target.
**Expected impact:** Makes failed/degraded runs observable and gives the skill a headless delivery path like siblings.

## Description

**Before:**
> Live firm-wide sales pulse from the Epiphan CRM — revenue vs pace, pipeline by stage, won/lost, BDR activity, with coaching takeaways. Use when: business pulse, how are we doing, pipeline health, revenue pace, weekly numbers, standup brief, are we on track, sales snapshot.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] failure_handling
- **Evidence** (line 87-92): "success_criteria: "[ ] Pulled LIVE data via weekly_brief / query_dataset this run — no stale or fabricated numbers""
- **Issue:** No failure/partial behavior; if weekly_brief errors/empties there is no degrade path, no alert, and — unlike its siblings — NO outcome sidecar at all, so a failed run is invisible to the analytics sweep.
- **Fix:** Add sidecar (last-outcome-business-pulse.json) + empty-data guard (flag 'no live data', never fabricate).

### [MED] output_contract
- **Evidence** (line 48,52-67): "3. **Synthesize** into the output shape below — never just dump JSON."
- **Issue:** Output SHAPE well-specified but no delivery mechanism (no Slack DM/HTML/file) — renders inline text only, nowhere for a scheduled/standup consumer to receive it.
- **Fix:** Add explicit delivery target (Slack DM to Tim or saved HTML).

### [LOW] tool_integration
- **Evidence** (line 35-40): "weekly_brief({ bdr_owner_ids: ["93367782","93782443","94135434"] }) ... (IDs + Nooks mapping live in epiphan-ai-mcp-guide-skill golden defaults.)"
- **Issue:** Epiphan-native tools used correctly, but owner IDs inlined here AND said to live in epiphan-ai-mcp-guide-skill — two drifting sources of truth.
- **Fix:** Reference golden-defaults IDs by pointer only.

## Missing tool references

- (sidecar writer) last-outcome-business-pulse.json

## Self-healing gap (see specs/self-healing-template.md)

Largest gap of the five: no failure definition, no retry/degrade/alert ladder, no outcome sidecar or run log at all — a broken weekly_brief pull yields fabrication risk or a silent no-op with zero telemetry.

## Overlap candidates (flag only — no removal)

- weekly-kpi-report-skill
- morning-brief-skill
- pipeline-health-analyzer-skill
- sales-revenue-skill
