# Patch: meddic-call-prep-auto-skill

**Score:** trigger=5 tool_integration=3 output_contract=3 failure_handling=4 maintainability=3 (sum=18/25)

**Highest-leverage single change (S effort):** Add a spec/competitor live-verification gate before emitting the displacement table, and route suppression through qualify_lead.
**Expected impact:** Eliminates confidently-wrong competitor claims in briefs and aligns dedupe with the single source of truth.

## Description

**Before:**
> Auto-generate MEDDIC-structured call prep scripts from prospect context. Pulls HubSpot deal + contact data, Apollo enrichment, CRM activity history, and calendar context to build a complete demo/discovery brief in 60 seconds. Use when: 'call prep', 'prep me for', 'demo prep', 'discovery prep', 'meddic brief', 'prep [company]', 'get me ready for [company]'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 118-124): "| Vertical | Primary Competitor | Displacement Angle |
| Higher Ed | Extron SMP (discontinued) | Extron EOL -> Pearl migration path |"
- **Issue:** Competitive displacement angles + competitor EOL status stated from a hardcoded memory table with no live verification. House rule 1 requires competitor/product specs via search_product_catalog/search_product_knowledge; sibling epiphan-call-playbook gates the same 'Extron SMP discontinued' claim behind live verification.
- **Fix:** Add a spec-verification gate requiring search_product_catalog/search_product_knowledge before emitting any displacement claim; treat the table as fallback only.

### [MED] tool_integration
- **Evidence** (line 132-136): "**Golden Rules check:** If ANY of these are true, STOP and skip this prep: - lifecyclestage = 'customer' ... - hubspot_owner_id IN ('82625923', '423155215', '190030668')"
- **Issue:** Golden-Rules + ATL/BTL dedupe done inline via raw HubSpot/CRM reads rather than gating through qualify_lead, the declared dedupe/ATL-BTL source of truth (house rule 3).
- **Fix:** Route suppression + ATL/BTL classification through qualify_lead where available; keep inline logic as fallback.

### [MED] output_contract
- **Evidence** (line 179-254): "## Stage 3: Output Format ... CALL PREP: [Company Name]"
- **Issue:** Output is a terminal ASCII brief with no defined delivery mechanism (no Gmail draft/Slack/saved HTML). No durable artifact survives the chat session.
- **Fix:** Add optional Gmail draft (create_draft to tkipper@epiphan.com) or saved HTML.

### [LOW] maintainability
- **Evidence** (line 152-155): "- **NEVER an EB:** Warehouse Manager, Network Manager, Systems Administrator, AV Technician ..."
- **Issue:** Full ATL/BTL keyword lists + owner IDs duplicated verbatim from CLAUDE.md; drift risk when canonical classification changes.
- **Fix:** Reference CLAUDE.md ATL/BTL section (as line 151 already does) instead of re-inlining the lists.

## Missing tool references

- search_product_catalog
- search_product_knowledge
- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Has outcome sidecar with success/partial/error (lines 287-296) and a Golden-Rules STOP, but no retry->degrade->alert->halt ladder for failed MCP pulls (Clari/Apollo down) and no run log to ~/.claude/skill-runs/{skill}.jsonl.

## Overlap candidates (flag only — no removal)

- sales-call-prep-assistant
- orlob-discovery-framework
- epiphan-call-playbook
