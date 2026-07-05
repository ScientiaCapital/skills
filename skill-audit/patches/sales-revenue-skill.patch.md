# Patch: sales-revenue-skill

**Score:** trigger=4 tool_integration=3 output_contract=2 failure_handling=2 maintainability=3 (sum=14/25)

**Highest-leverage single change (M effort):** Insert qualify_lead as the mandatory pre-sequence dedupe/ATL-BTL gate and centralize the hardcoded owner IDs/ICP scores to one declared block.
**Expected impact:** Removes drift risk on AE IDs and makes qualification authoritative instead of a re-implemented inline table.

## Description

**Before:**
> Epiphan Video B2B sales - video capture/streaming lead qualification, pipeline metrics, MEDDIC discovery, and demo execution for Pearl devices, EC20 PTZ, and Epiphan Connect. Use for lead scoring, cold outreach to Higher Ed/Government/Corporate AV, and pipeline reviews.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 93-94): "| ENRICHER | Contact discovery — ATL-first ... | Apollo MCP | ... |  | WRITER | Personalized Apollo sequences ... | Apollo MCP |"
- **Issue:** Enrichment/scoring routes through Apollo + Clay + a manual Golden-Rules query rather than qualify_lead as the dedupe/ATL-BTL source of truth (house rule 3); ATL/BTL logic is re-implemented inline (67-70) instead of gating through qualify_lead.
- **Fix:** Add qualify_lead as the mandatory dedupe/qualification gate before any sequence enrollment; keep the inline ATL/BTL table only as a fallback.

### [HIGH] tool_integration
- **Evidence** (line 273-274): "| "Too expensive" | Acknowledge -> "Compared to Extron SMP or Blackmagic?" -> Show Total Cost of Ownership (Pearl-2 vs legacy + integration) |  ... Pearl = portable, NDI + SRT, Kaltura native integration"
- **Issue:** Customer-facing objection responses assert Pearl specs (NDI+SRT, Kaltura native, TCO) from memory with no search_product_catalog / search_product_knowledge gate (house rule 1).
- **Fix:** Require product-knowledge lookup before emitting spec/competitive claims in objection scripts and demo content.

### [MED] tool_integration
- **Evidence** (line 98-112): "1. **Short and specific** - Under 100 words ... 4. **Personalization** - Company name + vertical signal ... | Step | Timing | Purpose | Example |"
- **Issue:** Generates cold-email + Apollo sequence copy with no brand-voice gate (get_writing_style/check_my_copy, house rule 2) and prefers Apollo sequences generically without the Gmail draft-first staging CLAUDE.md mandates for call lists.
- **Fix:** Add a brand gate on all generated copy and clarify draft-first (Gmail) vs Apollo-sequence paths.

### [MED] output_contract
- **Evidence** (line 354): "**Action:** Before adding to Apollo sequence, query Epiphan CRM MCP to validate lead state."
- **Issue:** The skill spans many outputs (scores, emails, pipeline reviews, demo scripts) but never pins a single delivery contract (draft vs XLSX vs HubSpot list); outbound is 'add to Apollo sequence' without draft-first review.
- **Fix:** Define per-mode output contracts and default outbound to Gmail draft-first before sequence enrollment.

### [MED] failure_handling
- **Evidence** (line 373): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** No retry/skip/alert ladder for failed MCP calls (Apollo/Clay/CRM) and no run log beyond the sidecar.
- **Fix:** Add a degrade ladder for MCP failures and a run log to ~/.claude/skill-runs/sales-revenue.jsonl.

### [MED] maintainability
- **Evidence** (line 352): "hubspot_owner_id IN ('82625923', '423155215', '190030668')` — AEs: Lex Evans, Ron Epstein, Phillip Sandler"
- **Issue:** Owner IDs, AE names, ICP scores, and product lists are hardcoded and duplicated from CLAUDE.md across the file (61, 337, 340, 352), so they will drift when CLAUDE.md changes; skill is also long and multi-domain (374 lines, three reference/ files).
- **Fix:** Declare owner IDs / AE roster / ICP scores once (or reference CLAUDE.md § authoritatively) instead of re-listing inline.

### [LOW] trigger_quality
- **Evidence** (line 3): "description: "Epiphan Video B2B sales - video capture/streaming lead qualification, pipeline metrics, MEDDIC discovery, and demo execution ... Use for lead scoring, cold outreach to Higher Ed/Government/Corporate AV, and pipeline reviews.""
- **Issue:** Specific and Epiphan-scoped, but it is a mega-skill spanning outreach + revops + discovery + demo, so it collides with demo-execution-playbook (demo), sales-methodology-implementer (MEDDIC), and cold-email-sequence-generator (cold email).
- **Fix:** Tighten description to position this as the umbrella BDR sales skill and cross-reference the specialized siblings to reduce trigger contention.

## Missing tool references

- qualify_lead
- search_product_catalog
- search_product_knowledge
- get_writing_style
- check_my_copy
- create_draft

## Self-healing gap (see specs/self-healing-template.md)

No failure definition beyond sidecar status; no retry->degrade->alert->halt ladder for Apollo/Clay/CRM MCP failures; no run log to ~/.claude/skill-runs/sales-revenue.jsonl. Qualification relies on an inline Golden-Rules query rather than qualify_lead, so a CRM outage silently degrades to memory-based classification with no alert.

## Overlap candidates (flag only — no removal)

- demo-execution-playbook-skill
- sales-methodology-implementer-skill
- meddic-call-prep-auto-skill
- cold-email-sequence-generator-skill
- challenger-sale-skill
- never-split-the-difference-skill
