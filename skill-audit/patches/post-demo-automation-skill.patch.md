# Patch: post-demo-automation-skill

**Score:** trigger=4 tool_integration=2 output_contract=4 failure_handling=3 maintainability=2 (sum=15/25)

**Highest-leverage single change (M effort):** Verify every product/competitor claim through search_product_knowledge and add a check_my_copy brand gate before any recap/objection email draft.
**Expected impact:** Stops inaccurate spec claims from reaching prospects within 2 hours of a demo — the highest-blast-radius customer-facing gap in the set.

## Description

**Before:**
> Automates post-demo follow-up sequence for Epiphan AEs: demo recap emails, internal debrief notes, meeting scheduling, stakeholder expansion, and 5-touch momentum plans.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 256,281): "- "We have Extron SMP" -> Position Pearl as upgrade (SMP discontinued; Pearl has cloud, AI) ... - Takeaway 1: "Pearl's direct API integration cuts transcoding time — your faculty time-to-publish drops from 4 hours to 15 min""
- **Issue:** Recap emails and objection responses assert product specs and competitor claims from memory (SMP discontinued, Pearl cloud/AI, transcoding/time-to-publish numbers) — customer-facing copy that violates the no-specs-from-memory house rule and could ship inaccurate claims.
- **Fix:** Require search_product_knowledge/search_product_catalog to verify any capability, integration, or competitor claim before it enters the draft.

### [HIGH] tool_integration
- **Evidence** (line 230): "- **Gmail** (gmail_create_draft) — compose recap email"
- **Issue:** Recap, objection-response, loop-in, and 5-touch emails are all customer-facing but no Epiphan Brand voice gate (get_writing_style/check_my_copy) runs before drafting.
- **Fix:** Add a check_my_copy brand pass on each generated email body before gmail_create_draft.

### [HIGH] maintainability
- **Evidence** (line 66,196): "## Workflow: 5-Stage Post-Demo Automation ... ### Stage 7: Deal Stage Automation"
- **Issue:** File is 410 lines with all vertical templates, objection libraries, three worked examples, and config inline and no references/ progressive disclosure — exceeds the ~500-line lean-context guidance in spirit and is the least maintainable of the five; title also says '5-Stage' but there are 7 stages (line 196), an internal inconsistency.
- **Fix:** Move vertical templates, objection library, and the three examples to references/ files and fix the stage count.

### [MED] tool_integration
- **Evidence** (line 157-159): "1. **Research via Apollo:** - Identify 2-3 likely stakeholders ... Pull titles, emails, LinkedIn profiles"
- **Issue:** Stakeholder expansion pulls new contacts via Apollo but never routes them through qualify_lead for dedupe/ATL-BTL before drafting loop-in emails — risk of drafting to a dup or a customer/partner-excluded contact per Golden Rules.
- **Fix:** Gate all Apollo-discovered contacts through qualify_lead before Stage 5 outreach drafts.

### [MED] failure_handling
- **Evidence** (line 407-410): "## Version History
- **v1.0** (April 2026): Initial release with 5-stage automation"
- **Issue:** No outcome sidecar emitted (all three sibling deal skills emit one) — no analytics/log of run status, so failed/partial runs are invisible. Troubleshooting section (line 370) handles inputs but there is no status ladder or run log.
- **Fix:** Add the standard last-outcome-post-demo-automation.json sidecar and a run log.

## Missing tool references

- search_product_knowledge
- search_product_catalog
- get_writing_style
- check_my_copy
- qualify_lead

## Self-healing gap (see specs/self-healing-template.md)

Has good human-facing escalation (Day 14 BDR handoff, troubleshooting) but no machine self-healing: no outcome sidecar, no status ladder, no run log to ~/.claude/skill-runs/post-demo-automation.jsonl.

## Overlap candidates (flag only — no removal)

- close-plan-generator
- meddic-call-prep-auto-skill
- deal-momentum-analyzer
