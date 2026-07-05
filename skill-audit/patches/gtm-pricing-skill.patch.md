# Patch: gtm-pricing-skill

**Score:** trigger=3 tool_integration=3 output_contract=3 failure_handling=2 maintainability=5 (sum=16/25)

**Highest-leverage single change (S effort):** Add enumerated trigger phrases plus one-line pointers to qualify_lead / search_product_catalog for the Epiphan-specific cases
**Expected impact:** Cuts activation collisions with research-skill and stops duplicating native ICP/pricing tooling

## Description

**Before:**
> B2B go-to-market strategy, pricing models, ICP development, positioning, and competitive intelligence. Use when planning GTM strategy, setting pricing, defining ICP, or evaluating opportunities.

**After (proposed):**
> Generic B2B go-to-market frameworks: ICP scoring rubric, April Dunford positioning, value-based/tiered pricing, and opportunity scoring. Use when: build an ICP, write a positioning statement, design pricing tiers, set list price, feature gating, score an opportunity, competitive battle card, GTM launch checklist. For Epiphan account/competitor research use research-skill; for live lead ICP scoring use qualify_lead.

## Findings & fixes

### [MED] trigger_quality
- **Evidence** (line 3): "description: "B2B go-to-market strategy, pricing models, ICP development, positioning, and competitive intelligence. Use when planning GTM strategy, setting pricing, defining ICP, or evaluating opportunities.""
- **Issue:** No enumerated 'Use when:' trigger-phrase list; 'competitive intelligence' + 'ICP development' collide with research-skill and territory-planning, risking mis-activation.
- **Fix:** Add explicit trigger phrases and disambiguate scope (generic frameworks, not Epiphan account research).

### [MED] tool_integration
- **Evidence** (line 98): "See `reference/gtm.md` for full YAML ICP worksheet templates and an example ICP (MEP contractors)."
- **Issue:** Pure static-framework skill with zero tool calls; ICP scoring and competitive pricing duplicate Epiphan-native qualify_lead and search_product_catalog without referencing them — violates 'Epiphan-native preferred'.
- **Fix:** Point ICP scoring to qualify_lead and competitive/price benchmarking to search_product_catalog when target is an Epiphan opportunity.

### [LOW] output_contract
- **Evidence** (line 112-119): "**Positioning Statement Template:**
```
For [target customer segment] who [key need/pain],"
- **Issue:** Defines output templates but no delivery mechanism (doc, artifact, HubSpot) for where the strategy lands.
- **Fix:** Specify a deliverable target (doc-coauthoring handoff or HTML one-pager).

### [LOW] failure_handling
- **Evidence** (line 343): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** Only failure handling is the sidecar status field; no defined behavior when inputs (value/competitor data) are missing.
- **Fix:** Add a degrade rule: proceed with documented assumptions and flag confidence when value data is unavailable.

## Missing tool references

- qualify_lead
- search_product_catalog

## Self-healing gap (see specs/self-healing-template.md)

No failure definition, no retry/degrade/alert ladder, and no run log — only the pass/partial/error sidecar status. Acceptable for a knowledge skill but no explicit 'insufficient input' degrade path.

## Overlap candidates (flag only — no removal)

- research-skill
- territory-planning-optimizer
- blue-ocean-strategy-skill
- business-model-canvas-skill
