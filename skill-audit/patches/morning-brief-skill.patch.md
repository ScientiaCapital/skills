# Patch: morning-brief-skill

**Score:** trigger=3 tool_integration=2 output_contract=4 failure_handling=2 maintainability=3 (sum=14/25)

**Highest-leverage single change (M effort):** Insert qualify_lead dedupe/ATL gate between Stage 2 and 3, and add product-spec + brand check before Gmail draft creation.
**Expected impact:** Eliminates duplicate/stale-tier leads and prevents from-memory product claims in outbound drafts.

## Description

**Before:**
> Daily briefing with calendar, CRM priority dial list, deal momentum summary, and Gmail drafts for each lead.

**After (proposed):**
> Tim's daily BDR morning brief (M–F 7:30 AM ET). Trigger: 'show morning brief','today's dial list','morning brief', or scheduled run. Pulls today's Google Calendar, a qualify_lead-gated ATL-first dial list from HubSpot (portal 21530819), deal-momentum scores, last-7-day Clari summaries, and creates a draft-only Gmail per lead; filters Supabase cooldown + HubSpot suppression. Emits single-page HTML brief. Consumes callable-lead-count inventory; does NOT re-run sdr-dial-list sourcing or business-pulse firm-wide reporting.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 74-96): "objectType: "contacts" ... sorts:[{propertyName:"custom_atl_btl_tier",direction:"ASCENDING"}]"
- **Issue:** Dial list produced directly from search_crm_objects with hand-rolled ATL/BTL sort on a custom field — never gates through qualify_lead, the dedupe/ATL-BTL source of truth. Dupe + stale-tier risk.
- **Fix:** Route Stage-2 candidates through qualify_lead before Stage 3.

### [HIGH] tool_integration
- **Evidence** (line 287,291,320): ""positive feedback on the Pearl Nano demo." ... "Canvas integration setup" ... "the Pearl Mini setup on 3/12""
- **Issue:** Customer-facing Gmail drafts name products from memory — no search_product_catalog/search_product_knowledge, no brand gate (get_writing_style/check_my_copy).
- **Fix:** Add spec-verification + check_my_copy pass in Stage 7 before create_draft.

### [MED] trigger_quality
- **Evidence** (line 3): "description: "Daily briefing with calendar, CRM priority dial list, deal momentum summary, and Gmail drafts for each lead.""
- **Issue:** Frontmatter description is a flat capability sentence — no enumerated trigger phrases, not 'pushy'. Manual triggers ('Show morning brief','Today's dial list') live only in quick_start line 15-16, not in the router-matched description.
- **Fix:** Move enumerated trigger phrases into description; state de-collision vs sdr-dial-lists/callable-lead-count/business-pulse.

### [MED] failure_handling
- **Evidence** (line 465-472): "Stage 11: Emit Outcome Sidecar ... "status":"[success|partial|error]""
- **Issue:** Sidecar carries status enum but no per-stage partial/error definition, no retry/skip/alert ladder, no run log.
- **Fix:** Add failure matrix (Supabase/Calendar/Clari down -> degrade+flag); log to ~/.claude/skill-runs/morning-brief.jsonl.

## Missing tool references

- qualify_lead
- search_product_catalog
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Has success|partial|error sidecar (465-472) but no per-stage failure definition, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs/morning-brief.jsonl. Dead Clari/Supabase/Calendar dependency has undefined behavior.

## Overlap candidates (flag only — no removal)

- sdr-dial-lists
- callable-lead-count-skill
- business-pulse-skill
- deal-momentum-analyzer-skill
