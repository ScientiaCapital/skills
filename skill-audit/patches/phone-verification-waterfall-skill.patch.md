# Patch: phone-verification-waterfall-skill

**Score:** trigger=5 tool_integration=3 output_contract=5 failure_handling=4 maintainability=4 (sum=21/25)

**Highest-leverage single change (M effort):** Gate classification through qualify_lead and collapse the three duplicated Golden-Rules/ATL-BTL copies into one source
**Expected impact:** Removes the highest-traffic source of ATL/BTL drift in the catalog (runs twice weekly, feeds the dial queue)

## Description

**Before:**
> Always-on callable lead pipeline for BDRs: HubSpot lead pull → Apollo phone lookup → Clay waterfall enrichment → HubSpot sync → callable queue. Ensures 50+ daily dials by maintaining verified phone inventory. Runs scheduled Mon & Wed 6:15 AM (between prospect-enrich 6:00 and prospect-refresh 6:30). Use when: 'verify phones', 'phone waterfall', 'callable leads', 'who can I call', 'dial list', 'always have someone to call', 'phone check', 'enrich phones'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 77-93): "### ATL/BTL Classification Gate (applied after Golden Rules)
Classify each contact by job title using approved ATL/BTL definitions... ATL Title Keywords... NEVER ATL..."
- **Issue:** Full Golden Rules + ATL/BTL re-implemented inline AND duplicated again in reference/golden-rules-filter.md and the Stage-1 block — three copies of the rule set in one directory — instead of gating through qualify_lead.
- **Fix:** Call qualify_lead for the Golden-Rules + ATL/BTL verdict; delete the duplicated inline copies, keep one reference doc.

### [MED] tool_integration
- **Evidence** (line 238): "**Tool:** HubSpot REST API (contacts batch update) via `hubspot_update_contact` (per-contact; no batch MCP tool) or direct HTTP"
- **Issue:** Stage 4 admits no batch MCP tool and falls back to per-contact loop / raw HTTP for 100+ contacts — a manual/slow path.
- **Fix:** Confirm whether a bulk HubSpot update tool exists in the Epiphan MCP; if not, sanction the loop and cap batch size.

### [MED] maintainability
- **Evidence** (line 316-324): "6:00 AM  → bdr-v3-prospect-enrich ... 6:15 AM  → phone-verification-waterfall-skill ... 6:30 AM  → bdr-v3-prospect-refresh"
- **Issue:** 18KB SKILL.md + 6 loose top-level docs (IMPLEMENTATION.md, INTEGRATION_MAP.md, EXAMPLE_OUTPUTS.md, README.md); schedule/task-ids restated in several files, inviting drift.
- **Fix:** Consolidate loose docs under reference/; declare schedule + task IDs once.

### [LOW] failure_handling
- **Evidence** (line 334-335): "On error: skip Clay enrichment and return Apollo-only results (better to have some phones than none) ... If Apple/Apollo API rate limits hit, queue and retry with exponential backoff"
- **Issue:** Good degrade ladder + Slack alerts on partial (405-411), but 'Apple/Apollo' typo (334) and no run log to ~/.claude/skill-runs/ (only the sidecar).
- **Fix:** Fix typo; add a run-log append.

## Missing tool references

- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Strongest of the six: Clay->Apollo-only degrade, exponential-backoff retry, >8min Slack alert, partial/error Slack templates. Still missing a durable run log at ~/.claude/skill-runs/phone-verification-waterfall.jsonl (sidecar only) and a defined halt if HubSpot sync itself fails.

## Overlap candidates (flag only — no removal)

- prospect-enrich
- callable-lead-count-skill
- sdr-dial-lists
- he-dial-queue-skill
