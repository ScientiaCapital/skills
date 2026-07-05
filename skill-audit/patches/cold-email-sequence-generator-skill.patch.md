# Patch: cold-email-sequence-generator-skill

**Score:** trigger=3 tool_integration=1 output_contract=2 failure_handling=2 maintainability=2 (sum=10/25)

**Highest-leverage single change (M effort):** Add a customer-facing gate: qualify_lead on the list + search_product_knowledge on every claim + check_my_copy on every string, then emit Gmail drafts instead of chat text.
**Expected impact:** Removes hallucinated-spec risk and off-brand copy, and makes output sendable in Tim's draft->review->send flow.

## Description

**Before:**
> Generate personalized cold email sequences (7-14 emails) with A/B test subject lines, follow-up timing recommendations, and integrated social proof. Creates multi-touch campaigns optimized for response rates. Use when users need outbound email campaigns, sales sequences, or lead generation emails.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 89): "We've helped [similar company 1] and [similar company 2] [achieve specific outcome] without [common objection]."
- **Issue:** Zero Epiphan-native tool calls anywhere. No search_product_catalog/search_product_knowledge for spec/claim verification, no qualify_lead dedupe gate on the target list, no Epiphan Brand get_writing_style/check_my_copy before generating customer-facing copy. Entire skill is a static template library.
- **Fix:** Add a pre-generation gate: qualify_lead on the audience list, search_product_knowledge for any product claim, check_my_copy on every drafted subject/body before output.

### [HIGH] output_contract
- **Evidence** (line 15): "**Output:** Full email sequence with subject lines (A/B), body copy, timing, personalization variables, and performance benchmarks"
- **Issue:** Output is raw markdown text only. No delivery mechanism — no Gmail draft creation via create_draft, which CLAUDE.md mandates for all outreach ('ALWAYS create Gmail drafts'). Not draft-first.
- **Fix:** Terminal stage should call mcp__claude_ai_Gmail__create_draft per email from tkipper@epiphan.com so Tim reviews in Gmail.

### [MED] maintainability
- **Evidence** (line 274-275): "</workflow>
</output>"
- **Issue:** Malformed XML: closing </output> at line 275 has no matching opening tag. Dangling tag corrupts any structural parse.
- **Fix:** Delete the stray </output> line.

### [MED] trigger_quality
- **Evidence** (line 3): "Use when users need outbound email campaigns, sales sequences, or lead generation emails."
- **Issue:** Generic B2B framing with no Epiphan/BDR anchor collides directly with sdr-email-sms-playbook. No disambiguation.
- **Fix:** Scope description to generic/non-Epiphan use OR fold into sdr-email-sms-playbook; add pointer.

### [MED] failure_handling
- **Evidence** (line 267): "{"ts":"[UTC ISO8601]","skill":"cold-email-sequence-generator","version":"1.1.0","
- **Issue:** Sidecar has status field but no defined failed/partial behavior, no retry->degrade ladder, no run log jsonl. success_criteria are content checks not run-state checks.
- **Fix:** Add explicit partial/error criteria (spec verification fails -> mark partial, skip claim) and a run log line.

## Missing tool references

- mcp__claude_ai_Gmail__create_draft
- search_product_knowledge
- Epiphan Brand get_writing_style
- Epiphan Brand check_my_copy
- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

No failure definition beyond a status enum, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs/{skill}.jsonl — only the analytics sidecar.

## Overlap candidates (flag only — no removal)

- sdr-email-sms-playbook-skill
- email-template-generator-skill
- personalization-at-scale-skill
