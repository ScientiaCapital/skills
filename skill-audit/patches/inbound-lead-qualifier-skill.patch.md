# Patch: inbound-lead-qualifier-skill

**Score:** trigger=3 tool_integration=1 output_contract=3 failure_handling=3 maintainability=3 (sum=13/25)

**Highest-leverage single change (L effort):** Convert the prompt template into a tool-wired workflow: HubSpot pull -> qualify_lead -> enrich_contact -> spec+brand gate -> gmail_create_draft
**Expected impact:** Turns an imagination-only scorer into an executable, spec-safe qualifier that actually routes and drafts

## Description

**Before:**
> Analyze inbound leads (form fills, demo requests) and score based on ICP fit, intent, and urgency. Auto-generates qualification questions, routes to right rep, and suggests personalized first touch. Use for qualifying and routing inbound leads at scale.

**After (proposed):**
> Score and route an inbound lead (form fill, demo request, content download) on ICP fit (0-40), intent (0-30), and urgency (0-30) -> priority tier + response SLA, then draft a first-touch email and route to the right AE. Use when: 'qualify this inbound lead', 'score and route [name] from [company]', 'is this demo request worth calling', 'route this form fill', 'triage inbound'. Pulls the contact from HubSpot and gates through qualify_lead.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 31-52, 199): "You are an expert at lead qualification and routing ... **ICP Fit (0-40 points)**: - Company size: 0-10 - Industry match: 0-10 ... **Assign To**: [Rep Name] (owns [territory/industry])"
- **Issue:** The entire skill is a generic prompt template — it names ZERO tools: no HubSpot/search_crm_objects to pull the lead, no qualify_lead gate, no Apollo/Clay enrichment, no Gmail draft tool. Everything (score, routing, enrichment) is done from the model's imagination on pasted-in text.
- **Fix:** Wire concrete tools: HubSpot lookup for the contact, qualify_lead for ICP/ATL-BTL/dedupe, enrich_contact for org data, gmail_create_draft for the follow-up email.

### [HIGH] tool_integration
- **Evidence** (line 154-227): "**Call Script** (within 1 hour): ```Hi [Name] ... Perfect. Let me show you exactly how we solve that...``` ... **Competitive Intel**: - Probably comparing to [Competitor] - [Competitor] weakness: [What we do better]"
- **Issue:** Customer-facing call script + email + competitive claims are generated with no search_product_catalog/search_product_knowledge spec gate and no brand voice gate (get_writing_style/check_my_copy) — violates house rules 1 and 2.
- **Fix:** Add a spec-verification gate before any product/competitor claim and a check_my_copy pass on the email template before it is drafted.

### [MED] tool_integration
- **Evidence** (line 199-206): "**Assign To**: [Rep Name] (owns [territory/industry]) ... **Why This Rep**: - Territory: [Geographic/Industry match]"
- **Issue:** Routing is abstract '[Rep Name]' with no real owner IDs; the catalog's real AEs (Phil 190030668, Lex 82625923) and Tim's BDR role are never wired in, so it can't actually route.
- **Fix:** Encode the real routing table (AE owner IDs + verticals) or hand off to ae-handoff-brief for the AE path.

### [MED] output_contract
- **Evidence** (line 59-250): "## Output Format ```markdown # Inbound Lead Analysis ...``` ... Remember: Speed to lead matters - calling within 5 minutes = 10x better conversion"
- **Issue:** Output format is fully specified but there is NO delivery mechanism — the email 'template' is text in the report, never created as a Gmail draft; contradicts the CLAUDE.md draft-first rule for outbound.
- **Fix:** Make the email template a gmail_create_draft (draft-first) and write the score/routing back to the HubSpot contact.

## Missing tool references

- qualify_lead
- search_crm_objects
- enrich_contact
- search_product_catalog
- search_product_knowledge
- get_writing_style
- check_my_copy
- gmail_create_draft

## Self-healing gap (see specs/self-healing-template.md)

Has a suppression gate (lines 252-260) and an outcome sidecar with partial/error semantics (lines 264-273), but because it calls no tools there is no failure surface defined for lookups/enrichment, no retry->degrade ladder, no alert, and no run log to skill-runs/.

## Overlap candidates (flag only — no removal)

- ae-handoff-brief
- callable-lead-count
- sales-call-prep-assistant
