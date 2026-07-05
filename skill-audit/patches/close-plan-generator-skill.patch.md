# Patch: close-plan-generator-skill

**Score:** trigger=4 tool_integration=3 output_contract=4 failure_handling=2 maintainability=4 (sum=17/25)

**Highest-leverage single change (M effort):** Source all product/competitive claims via search_product_knowledge and add an outcome sidecar + degrade rule for sparse Clari data.
**Expected impact:** Eliminates from-memory spec risk in a customer-facing plan and brings the skill up to the observability baseline of its siblings.

## Description

**Before:**
> Generates comprehensive close plans for Epiphan Video deals. Maps stakeholders to MEDDIC roles, identifies decision processes, assesses competitive position, and creates actionable next-best-actions with a close confidence score (0-100). Outputs ASCII report + optional mutual action plan for prospect outreach.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 114-120): "**Epiphan Competitive Advantages (by vertical):**
- Higher Ed: NDI + Kaltura/Panopto integration, multi-campus cloud ... - Live Events: Pearl Nano portability, EC20 PTZ flexibility, low latency"
- **Issue:** Product specs and competitive claims are stated from memory in the workflow (and battlecard, Stage 4) rather than pulled from search_product_catalog/search_product_knowledge — violates the no-specs-from-memory house rule for a customer-facing mutual action plan / battlecard.
- **Fix:** Require a search_product_knowledge/search_product_catalog call to source any product capability or competitive differentiator before it appears in the plan.

### [HIGH] tool_integration
- **Evidence** (line 206): "Output as Gmail draft (optional) or copy-paste ready."
- **Issue:** The Mutual Action Plan is a customer-facing outbound artifact but no Epiphan Brand voice gate (get_writing_style/check_my_copy) runs before the Gmail draft.
- **Fix:** Add check_my_copy on the mutual-action-plan body before creating the draft.

### [HIGH] failure_handling
- **Evidence** (line 362): "Bug reports: Note skill output, deal stage, which stage failed"
- **Issue:** No outcome sidecar and no defined failed/partial-run behavior — unlike the three sibling deal skills, this skill emits nothing to analytics and has no retry/degrade path when Clari/HubSpot returns sparse data (only a human 'bug report' note).
- **Fix:** Add the standard last-outcome sidecar + a 'if Clari sparse -> degrade to HubSpot notes, flag confidence as low' rule.

### [MED] tool_integration
- **Evidence** (line 62): "- **Company Context:** `apollo_organizations_enrich` (industry, headcount, location, tech stack)"
- **Issue:** Uses generic apollo_organizations_enrich for company context and never routes stakeholders through qualify_lead for ATL/BTL despite doing ATL/BTL classification (Stage 2) — Epiphan-native qualification is bypassed.
- **Fix:** Gate contact ATL/BTL through qualify_lead; keep Apollo only for firmographic gaps.

### [LOW] maintainability
- **Evidence** (line 98): "vendor evaluation? (RFP process, incumbent incumbent, incumbent defense playbook)"
- **Issue:** Duplicated word 'incumbent incumbent' — minor content-rot indicator in Stage 3.
- **Fix:** Clean up the typo.

## Missing tool references

- search_product_knowledge
- search_product_catalog
- get_writing_style
- check_my_copy
- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

No failure definition, no outcome sidecar, no retry->degrade->alert->halt ladder, and no run log to ~/.claude/skill-runs/close-plan-generator.jsonl — the weakest self-healing of the five despite good progressive disclosure.

## Overlap candidates (flag only — no removal)

- deal-momentum-analyzer
- meddic-call-prep-auto-skill
- ae-handoff-brief-skill
