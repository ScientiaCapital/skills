# Patch: never-split-the-difference-skill

**Score:** trigger=5 tool_integration=2 output_contract=2 failure_handling=2 maintainability=4 (sum=15/25)

**Highest-leverage single change (S effort):** Route every generated email/voicemail through check_my_copy then stage as a Gmail draft.
**Expected impact:** Brings all outbound negotiation copy into brand compliance and Tim's review-before-send workflow.

## Description

**Before:**
> Chris Voss FBI negotiation framework — tactical empathy, calibrated questions, mirroring, labeling, and the Ackerman model for B2B sales and deal negotiation. Use when: negotiation, tactical empathy, calibrated questions, mirroring, labeling, accusation audit, ackerman, deal negotiation, price negotiation, never split the difference.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 256-263): ""[Name], this is Tim from Epiphan Video. [Pause] ... Not sure if it's relevant — but if it is, I'm at [number].""
- **Issue:** Multiple customer-facing artifacts (5 email templates 199-266, voicemail script, cold email 351-363) with no brand-voice gate (house rule 2) and no Gmail draft delivery mechanism.
- **Fix:** Add check_my_copy brand gate and create_draft draft-first delivery for all generated emails/voicemails.

### [MED] tool_integration
- **Evidence** (line 188-192): "## Example (selling Pearl-2 fleet, target: $48K)
- List price: $62,000 (130% anchor)"
- **Issue:** Uses illustrative Pearl-2 pricing from memory; if pricing is ever surfaced to a prospect it should come from the catalog, not a hardcoded example.
- **Fix:** Flag pricing examples as illustrative and require search_product_catalog for any real quote figure.

### [MED] output_contract
- **Evidence** (line 351-363): "### Cold Email (Accusation Audit Style)

Subject: Remote testimony at [Court System]"
- **Issue:** Outbound copy produced with no defined delivery mechanism (draft/Slack/HubSpot); conflicts with CLAUDE.md Gmail draft-first workflow.
- **Fix:** Define output as Gmail draft(s) via create_draft.

### [MED] failure_handling
- **Evidence** (line 387): "Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated."
- **Issue:** Failure semantics confined to sidecar; no retry/skip/alert ladder, no run log path.
- **Fix:** Add failure ladder + run log to ~/.claude/skill-runs/never-split-the-difference.jsonl.

### [LOW] trigger_quality
- **Evidence** (line 3): "description: "Chris Voss FBI negotiation framework — tactical empathy, calibrated questions, mirroring, labeling, and the Ackerman model ... Use when: negotiation, tactical empathy, calibrated questions, mirroring, labeling, accusation audit, ackerman, deal negotiation, price negotiation, never split the difference.""
- **Issue:** Specific, pushy, well-enumerated triggers; distinct enough from siblings (pure negotiation focus).
- **Fix:** None needed.

### [LOW] maintainability
- **Evidence** (line 1-388): "388 total lines; self-contained with tagged sections and a large <example_session> (294-364)."
- **Issue:** Under 500 lines, no drifting hardcoded IDs; example section is long but acceptable.
- **Fix:** Optionally move the court-system example to references/.

## Missing tool references

- get_writing_style
- check_my_copy
- create_draft
- search_product_catalog

## Self-healing gap (see specs/self-healing-template.md)

No failure definition beyond sidecar status; no retry->degrade->alert->halt ladder; no run log to ~/.claude/skill-runs/never-split-the-difference.jsonl. Generated emails/voicemails bypass any brand or draft-staging safeguard.

## Overlap candidates (flag only — no removal)

- challenger-sale-skill
- sales-revenue-skill
- sales-methodology-implementer-skill
