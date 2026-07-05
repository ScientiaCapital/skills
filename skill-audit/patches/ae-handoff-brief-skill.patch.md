# Patch: ae-handoff-brief-skill

**Score:** trigger=5 tool_integration=3 output_contract=4 failure_handling=2 maintainability=3 (sum=17/25)

**Highest-leverage single change (M effort):** Create the missing reference/ae-handoff-template.md and add a MEDDIC-coverage degrade ladder (draft LOW-CONFIDENCE + status:partial) to Stage 7
**Expected impact:** Guarantees a consistent brief layout and a defined behavior when discovery data is thin instead of silent improvisation

## Description

**Before:**
> Auto-generate structured AE handoff briefs when Tim books a demo for Phil Sandler or Lex Evans. Packages MEDDIC scorecard, competitive intel, discovery notes, call transcripts, and next-best-action into a single document the AE can scan in 60 seconds. Increases demo-to-close rate by ensuring AEs walk in fully prepared. Use when: 'handoff to Phil', 'handoff to Lex', 'book demo for AE', 'ae brief', 'hand off [company]', 'prep handoff', 'pass to AE', 'transition [company] to Phil', 'transition [company] to Lex', 'demo booked for [company]'.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 156-166): "## Stage 4: Demo Flow Recommendation | Vertical | Lead Feature | Close Angle | | Higher Ed | Multi-room capture + CMS auto-publish | ... | Corporate AV | Meeting room capture + NDI/SRT streaming |"
- **Issue:** Product feature recommendations for the AE demo are stated from a hardcoded table (Pearl feature claims from memory) with no search_product_catalog/search_product_knowledge verification — violates house rule 1 on a customer-influencing document.
- **Fix:** Gate the demo-flow feature claims through search_product_knowledge, or cite the spec-verified epiphan-call-playbook rather than an inline table.

### [HIGH] maintainability
- **Evidence** (line 177): "## Stage 6: Output Format See `reference/ae-handoff-template.md` for full brief layout (MEDDIC scorecard table ...)."
- **Issue:** Broken reference: the skill directory contains only config.json + SKILL.md (no reference/ dir), so the cited ae-handoff-template.md does not exist — the output layout is undefined at runtime.
- **Fix:** Create reference/ae-handoff-template.md or inline the brief layout; a run will otherwise improvise the format.

### [HIGH] failure_handling
- **Evidence** (line 181-214): "### 7a. Gmail Draft to AE ... Use `gmail_create_draft` ... ## Emit Outcome Sidecar ... "status":"[success|partial|error]""
- **Issue:** Draft-first delivery is correct, but there is no defined behavior for partial failure — e.g. Clari returns no calls, deal at wrong stage (only a soft warning flag at line 89), or Apollo enrichment fails; the sidecar has partial/error fields but no rule for when to halt vs draft-anyway.
- **Fix:** Add a degrade ladder: if MEDDIC coverage < threshold or zero calls found, still draft but stamp the brief 'LOW CONFIDENCE' and set sidecar status:partial; halt only if the deal/AE can't be identified.

### [MED] tool_integration
- **Evidence** (line 131-137): "### E — Economic Buyer ... **ATL/BTL Validation (per CLAUDE.md § ATL/BTL Classification v1.0):** Map ALL known contacts to ATL/BTL tiers."
- **Issue:** ATL/BTL validation is asked for but done by hand against CLAUDE.md; qualify_lead (the ATL/BTL + dedupe source of truth) is not invoked, and the brand gate is absent on the Gmail draft to the AE.
- **Fix:** Use qualify_lead for the ATL/BTL map; run check_my_copy on the AE Gmail draft before gmail_create_draft.

## Missing tool references

- qualify_lead
- search_product_knowledge
- search_product_catalog
- get_writing_style
- check_my_copy

## Self-healing gap (see specs/self-healing-template.md)

Has an outcome sidecar (partial/error) and one soft risk flag (deal-stage warning), but no failure definition for missing calls/enrichment, no retry->degrade->alert ladder, no explicit halt condition, and no run log to ~/.claude/skill-runs/ae-handoff-brief.jsonl. The referenced output template is also missing, so a failed brief has no fallback layout.

## Overlap candidates (flag only — no removal)

- meddic-call-prep-auto-skill
- call-recording-analyzer-skill
- deal-momentum-analyzer-skill
- post-demo-automation-skill
