# Patch: demo-execution-playbook-skill

**Score:** trigger=5 tool_integration=3 output_contract=4 failure_handling=2 maintainability=5 (sum=19/25)

**Highest-leverage single change (M effort):** Add Stage 1 degrade handling (skip + flag on any failed MCP call) plus a product-spec verification call and an outcome sidecar/run log.
**Expected impact:** Prevents a single missing Clari/HubSpot record from silently producing a hollow demo brief, and makes the skill's runs observable + spec-grounded.

## Description

**Before:**
> Structured demo execution framework for AEs to drive deals forward with vertical-specific flows, live coaching, and post-demo scoring

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 172, 286-288): ""This Pearl-2 records multiple cameras simultaneously [FEATURE]—so instead of hiring 2 operators, you have 1 box doing the work [BENEFIT]."  ... Pearl actually has on-prem recording + optional on-prem Epiphan Connect."
- **Issue:** Customer-facing capability claims (multi-camera, on-prem Connect, HIPAA-friendly, dual SSD+SRT failover at 100-106) are asserted from memory; Stage 1 calls hubspot/clari/apollo but never search_product_catalog / search_product_knowledge (house rule 1) even though it lists epiphan-ai-mcp-guide as a dependency.
- **Fix:** Add a product-spec verification call in Stage 1 (search_product_knowledge) and require the demo flows to cite verified specs.

### [HIGH] failure_handling
- **Evidence** (line 75-84): "### Stage 1: Pre-Demo Intel Gathering (Parallel MCP Calls) ... 1. `hubspot_get_deal(dealId)` ... 3. `clari_search_calls(...)`"
- **Issue:** Five parallel MCP calls with no defined behavior if one fails/returns empty (e.g., no Clari call found, deal not in HubSpot); no retry/skip/alert ladder and no run log — and unlike the other four skills it has no outcome sidecar at all.
- **Fix:** Add per-call degrade rules (skip + flag missing intel), a run log to ~/.claude/skill-runs/demo-execution-playbook.jsonl, and an outcome sidecar.

### [MED] tool_integration
- **Evidence** (line 84): "5. `apollo_organizations_enrich(domain=company_domain)` -> Company size, tech stack, industry"
- **Issue:** Uses generic Apollo enrichment for company intel where an Epiphan-native path may exist, and reads contacts via hubspot_search_contacts without gating MEDDIC/EB identification through qualify_lead (house rules 3-4).
- **Fix:** Prefer Epiphan-native enrichment/qualify_lead for attendee role + ATL/BTL (EB) assignment; keep Apollo as fallback.

### [LOW] trigger_quality
- **Evidence** (line 17-24): "triggers:
  - "demo playbook"
  - "demo flow for"
  - "how should I demo to"
  - "demo checklist"
  - "live demo prep""
- **Issue:** Explicit trigger list plus keywords (29-35) — very pushy and specific; minor overlap with sales-revenue Part 3 (Demo & Discovery) and meddic-call-prep-auto.
- **Fix:** Add a one-line boundary noting sales-revenue covers lightweight demo flow while this is the full AE execution playbook.

### [LOW] output_contract
- **Evidence** (line 236, 243): "**Minimum Completion:** 5 minutes post-demo. Upload to HubSpot deal record.  ... [ ] Enter next step in HubSpot deal"
- **Issue:** Strong output contract (scorecard template + HubSpot destination), but the upload is a manual instruction rather than a hubspot_ MCP write call.
- **Fix:** Bind the scorecard upload and next-step to a HubSpot MCP write (hubspot_update_deal / note) rather than a manual step.

### [LOW] maintainability
- **Evidence** (line 109, 193, 251): "Full demo arcs ... see [reference/vertical-demo-flows.md] ... Full objection matrix ... see [reference/objection-handling-matrix.md] ... see [reference/competitive-displacement-scripts.md]"
- **Issue:** Exemplary progressive disclosure — detail pushed to three references/ files keeping SKILL.md ~382 lines; only nit is version/next-review dates hardcoded (376-377) that will silently go stale.
- **Fix:** None critical; consider dropping the manual 'Next Review' date or moving it to a maintenance log.

## Missing tool references

- search_product_catalog
- search_product_knowledge
- qualify_lead
- get_writing_style
- check_my_copy
- hubspot_update_deal

## Self-healing gap (see specs/self-healing-template.md)

No failure definition for the five Stage-1 parallel MCP calls (missing deal/Clari/enrich data is unhandled); no retry->degrade->alert->halt ladder; no run log to ~/.claude/skill-runs/demo-execution-playbook.jsonl; and uniquely among these five it emits no outcome sidecar at all, so runs are invisible to analytics.

## Overlap candidates (flag only — no removal)

- sales-revenue-skill
- meddic-call-prep-auto-skill
- challenger-sale-skill
- ae-handoff-brief-skill
