# Patch: prospect-refresh-skill

**Score:** trigger=3 tool_integration=2 output_contract=4 failure_handling=2 maintainability=2 (sum=13/25)

**Highest-leverage single change (M effort):** Insert a spec-verification (search_product_knowledge) + brand-check (check_my_copy) gate before gmail_create_draft, and dedupe via qualify_lead
**Expected impact:** Stops 30 drafts/run from shipping memory-stated product claims and off-brand copy; removes hand-rolled dedupe drift

## Description

**Before:**
> Monday ICP prospect search + Gmail draft creation. Finds NET NEW prospects across all verticals using Apollo.

**After (proposed):**
> Monday 6:30 AM (and on demand) net-new ICP prospecting across all 7 Epiphan verticals: Apollo People search (ATL-first) -> qualify_lead dedupe + Golden Rules -> Apollo/Clay firmographic enrich -> spec-verified, brand-checked Gmail drafts -> HTML report with HubSpot/Apollo drill-downs. Use when: 'run prospect refresh', 'search new ICP prospects', 'find net-new leads', 'weekly prospecting run'.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 193-206): "Subject: Epiphan + [UNIVERSITY_NAME]: Hybrid Learning Infrastructure...
[COMPANY_NAME] provides:
- Live lecture capture (no manual setup)
- Auto-recordings to your LMS
- Multi-platform distribution (Zoom, Teams, Canvas)"
- **Issue:** Six hardcoded email templates state Epiphan product capabilities from memory ('auto-recordings to your LMS', '4K Capture + Distribution'). Violates house rule 1 (specs from search_product_catalog/search_product_knowledge) and house rule 2 (no brand-voice gate).
- **Fix:** Call search_product_knowledge for the vertical's capabilities and check_my_copy/get_writing_style on the drafted body before drafting; treat templates as skeletons filled from verified data.

### [HIGH] tool_integration
- **Evidence** (line 84-98): "**For each Apollo result, check:**
...propertyName: "email", operator: "EQ"... propertyName: "company", operator: "CONTAINS_TOKEN""
- **Issue:** Dedupe is a hand-rolled two-filter HubSpot search, not qualify_lead. Stage 4 Golden Rules also re-stated in prose diverging from the CLAUDE.md canonical list.
- **Fix:** Replace Stage 3 dedupe + Stage 4 gating with qualify_lead.

### [MED] output_contract
- **Evidence** (line 315): "- Do NOT send—leave as draft for manual review"
- **Issue:** Draft-first is correct, but 30 Gmail drafts are created before any human sees the product claims — with unverified specs this ships wrong claims into 30 drafts/run.
- **Fix:** Move spec-verification + brand check ahead of gmail_create_draft.

### [MED] maintainability
- **Evidence** (line 190-310): "**Template A — Higher Ed (ICP 90):** ... **Template F — K-12 (ICP 65):**"
- **Issue:** ~120 lines of inline templates + a 7-row ICP matrix hardcoded in a 13KB SKILL.md. Templates duplicate reference/email-templates.md used by prospect-research-to-cadence, so edits must happen twice.
- **Fix:** Move templates to a shared reference/ file; declare the ICP score table once (repeated in 4 siblings).

### [MED] failure_handling
- **Evidence** (line 362): "**Note:** This skill outputs drafts + report. **Sequence Load Skill** runs 45 min later (7:15 AM)"
- **Issue:** No behavior for partial Apollo failure, Gmail quota exhaustion, or zero net-new. Sidecar exists but no retry/alert ladder or run log.
- **Fix:** Add a degrade path and a run log.

## Missing tool references

- qualify_lead
- search_product_knowledge
- search_product_catalog
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

No failure definition for zero-net-new, Apollo timeout, or Gmail quota; no retry->degrade->alert ladder; no run log at ~/.claude/skill-runs/prospect-refresh.jsonl. Sidecar records outcome but cannot drive recovery.

## Overlap candidates (flag only — no removal)

- prospect-research-to-cadence
- prospect-enrich
- cold-email-sequence-generator-skill
- sequence-load
