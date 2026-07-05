# Patch: hubspot-revops-skill

**Score:** trigger=4 tool_integration=3 output_contract=3 failure_handling=3 maintainability=4 (sum=17/25)

**Highest-leverage single change (M effort):** Gate list-producing UC1/UC2 through qualify_lead and reconcile the Golden-Rules SQL AE-owner clause with the 90-day stale exception.
**Expected impact:** Removes a drifting second copy of ATL/BTL+AE rules and stops wrongly excluding re-engageable stale AE leads.

## Description

**Before:**
> Use when building revenue analytics on HubSpot — SQL warehouse queries,

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [MED] tool_integration
- **Evidence** (line 129-131): "-- Target only AE territories (Lex Evans, Ron Epstein, Phillip Sandler)
  AND hubspot_owner_id IN (82625923, 423155215, 190030668)"
- **Issue:** Golden-Rules SQL re-implements ATL/BTL + AE-owner exclusion in raw SQL rather than gating list-producing UC1 through qualify_lead; also reads as hard-exclude AE-owned, conflicting with CLAUDE.md 2026-03-21 90-day-stale exception.
- **Fix:** Route UC1/UC2 candidate lists through qualify_lead; keep SQL for aggregates. Update AE clause to 90-day stale-exception logic.

### [MED] output_contract
- **Evidence** (line 88-92): "| 1 | ICP Validation | ... | Segment conversion rates | SQL + Clay |"
- **Issue:** Use-case outputs abstract with no concrete delivery artifact (XLSX/HTML/HubSpot property write) named per case.
- **Fix:** Name a delivery target per UC (e.g. UC2 writes score to HubSpot property; UC5 emits XLSX/HTML forecast).

### [LOW] tool_integration
- **Evidence** (line 72-80): "from hubspot import HubSpot; client = HubSpot(access_token="pat-na1-xxxxx") ... HEADERS = {"Authorization": "Bearer pat-na1-xxxxx"}"
- **Issue:** Leads with generic raw HubSpot SDK/REST + Private App setup when line 41 states access is via Epiphan CRM MCP and no Private App is needed — Epiphan-native path buried below the generic one.
- **Fix:** Lead with Epiphan MCP tool path; demote raw SDK/Private App to appendix.

## Missing tool references

- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Partial: Common Mistakes table with rate-limit/backoff (200-210) and success|partial|error sidecar (236-245), but no explicit retry->degrade->alert->halt ladder for a failed SQL/API run and no run log to ~/.claude/skill-runs/.

## Overlap candidates (flag only — no removal)

- crm-integration-skill
- data-analysis-skill
- sales-revenue-skill
- pipeline-health-analyzer-skill
- deal-momentum-analyzer-skill
