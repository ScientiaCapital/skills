# Patch: sdr-email-sms-playbook-skill

**Score:** trigger=5 tool_integration=3 output_contract=4 failure_handling=3 maintainability=4 (sum=19/25)

**Highest-leverage single change (S effort):** Insert a spec/brand verification gate (search_product_knowledge + check_my_copy) between template fill and Gmail draft creation.
**Expected impact:** Keeps the strong Epiphan cadence but stops unverified competitor/product claims and off-voice copy from reaching prospects.

## Description

**Before:**
> 5-touch email/SMS cadence for Epiphan BDR outreach. Full templates for Higher Ed, Courts, Gov, Healthcare by touch. Companion to epiphan-call-playbook (phone). Writing rules, subject line patterns, and SMS guidelines. Use when: email playbook, email template, outreach email, sdr email, cold email template, sms outreach, follow up email, 5 touch cadence.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 344-346): "- **vMix/OBS are software** — unreliable for mission-critical unattended
  recording; Pearl is dedicated hardware built for one job."
- **Issue:** Product/competitor specs stated from memory (Pearl = dedicated hardware, Extron SMP EOL, Matrox exited encoder market). No search_product_catalog/search_product_knowledge to verify before they land in customer-facing email copy. Violates house rule 1.
- **Fix:** Add a spec-verification step: any product/competitor claim woven into a touch must be confirmed via search_product_knowledge first.

### [MED] tool_integration
- **Evidence** (line 22-23): "Enroll into the 5-touch cadence (Nooks handles enrollment; this skill is
   the CONTENT for each step)."
- **Issue:** No brand gate. Rule 2 requires get_writing_style/check_my_copy before customer-facing strings; skill has detailed Writing Rules but never runs the Epiphan Brand tools.
- **Fix:** Add check_my_copy pass on each drafted touch before Gmail draft creation.

### [LOW] output_contract
- **Evidence** (line 26-27): "Create Gmail drafts for review before send (Tim's workflow: draft ->
   review/edit -> send)."
- **Issue:** Draft-first delivery specified in prose but the Gmail MCP tool (create_draft) is never named, so no explicit tool contract for HOW drafts are staged.
- **Fix:** Name mcp__claude_ai_Gmail__create_draft explicitly as the delivery step, one draft per touch.

## Missing tool references

- search_product_knowledge
- search_product_catalog
- Epiphan Brand check_my_copy
- mcp__claude_ai_Gmail__create_draft

## Self-healing gap (see specs/self-healing-template.md)

Sidecar defines an error status with guidance ('Set status to error ... if the cadence could not be built') — better than most — but still no retry->degrade->alert ladder and no run log to ~/.claude/skill-runs/{skill}.jsonl.

## Overlap candidates (flag only — no removal)

- cold-email-sequence-generator-skill
- email-template-generator-skill
- epiphan-call-playbook
- sms-text-optimizer
