# Patch: pipeline-health-analyzer-skill

**Score:** trigger=2 tool_integration=1 output_contract=3 failure_handling=2 maintainability=3 (sum=11/25)

**Highest-leverage single change (L effort):** Wire the skill to the Epiphan CRM MCP (search_crm_objects/ask_agent) for data instead of a manual CSV, and add gmail_create_draft + brand gate for the re-engagement email.
**Expected impact:** Turns a manual analyst worksheet into an automated, draft-first skill and removes the biggest collision/generic-tool gap.

## Description

**Before:**
> Analyze pipeline health, identify stalled deals, predict close probability, and suggest actions to move deals forward. Improves forecast accuracy and prevents revenue leakage. Use when deals get stuck or forecast accuracy is poor.

**After (proposed):**
> Portfolio-level pipeline forecast + health rollup: stage-by-stage conversion vs benchmark, risk-adjusted forecast (commit/best/worst scenarios), probability calibration, and a pipeline report card. Pulls deals from HubSpot (Epiphan CRM MCP) or a CSV export. Use when: 'analyze pipeline health', 'risk-adjusted forecast', 'forecast accuracy', 'which stage do deals stall in', 'pipeline report card', 'scenario planning'. For per-deal momentum scoring use deal-momentum-analyzer; for kill/recover triage use dead-deal-recovery.

## Findings & fixes

### [HIGH] trigger_quality
- **Evidence** (line 3): "Use when deals get stuck or forecast accuracy is poor."
- **Issue:** Description is generic, non-pushy, enumerates no distinct trigger phrases in the frontmatter, and its scope ('identify stalled deals, predict close probability, suggest actions') is near-identical to deal-momentum-analyzer and dead-deal-recovery — high collision, no clear ownership boundary.
- **Fix:** Rewrite description to enumerate specific phrases and stake a distinct claim (forecast/rollup analytics vs per-deal momentum).

### [HIGH] tool_integration
- **Evidence** (line 14): "**Input:** Pipeline export (CSV with deal data) or CRM access"
- **Issue:** Skill relies on a manual CSV export and names zero MCP tools anywhere in the workflow — HubSpot data is available natively via the Epiphan CRM MCP, so this is generic/manual where an Epiphan-native automated pull exists.
- **Fix:** Replace CSV input with search_crm_objects/ask_agent pulls (as deal-momentum-analyzer does); make CSV a fallback only.

### [HIGH] tool_integration
- **Evidence** (line 101-108): "**Re-engagement Email**:
Subject: [Company] - Quick check-in

Hi [Name], I haven't heard back since our [last interaction]"
- **Issue:** Emits a customer-facing re-engagement email inline with no brand voice gate (get_writing_style/check_my_copy) and no draft-delivery mechanism (no gmail_create_draft) — output is copy-paste text, not a draft-first outbound artifact.
- **Fix:** Generate via gmail_create_draft after a check_my_copy brand gate.

### [MED] tool_integration
- **Evidence** (line 37): "4. **Stakeholder Coverage** - Number and level of contacts"
- **Issue:** 'Level of contacts' scoring never routes through qualify_lead for ATL/BTL, unlike its sibling skills — inconsistent stakeholder classification.
- **Fix:** Gate stakeholder-level assessment through qualify_lead.

### [MED] failure_handling
- **Evidence** (line 253): "As the final step, write to `~/.claude/skill-analytics/last-outcome-pipeline-health-analyzer.json`"
- **Issue:** Only failure handling is the analytics sidecar; no defined behavior when the CSV is malformed/missing or CRM access fails, no retry/degrade/alert path.
- **Fix:** Add explicit 'if input missing -> request export / fall back to CRM pull; if both fail -> alert and halt' ladder.

## Missing tool references

- search_crm_objects
- ask_agent
- qualify_lead
- gmail_create_draft
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

No failure definition and no retry->degrade->alert->halt ladder; the only persistence is the analytics sidecar (line 253), with no run log to ~/.claude/skill-runs/pipeline-health-analyzer.jsonl and no automated data source (CSV is manual).

## Overlap candidates (flag only — no removal)

- deal-momentum-analyzer
- dead-deal-recovery
- sales-forecast-builder
