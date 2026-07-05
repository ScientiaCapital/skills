# Patch: personalization-at-scale-skill

**Score:** trigger=3 tool_integration=2 output_contract=3 failure_handling=2 maintainability=3 (sum=13/25)

**Highest-leverage single change (L effort):** Wire the named research sources to concrete tools and add a batch check_my_copy brand gate before output
**Expected impact:** Turns an aspirational explainer into an executable, on-brand skill and prevents hundreds of unverified/off-brand first lines reaching sequences

## Description

**Before:**
> Generate unique personalized first lines for hundreds of prospects using company news, LinkedIn activity, and mutual connections. Saves 10+ hours of manual research per campaign. Use when you need personalized outreach at volume.

**After (proposed):**
> Batch-generate unique, spec-verified, brand-checked personalized first lines for large prospect lists (100s) using Apollo hiring signals, Clay/company news, and LinkedIn activity — gated through qualify_lead and check_my_copy. Use when: 'personalize outreach for [N] prospects', 'generate unique first lines', 'find personalization angles for this list', 'research these companies for outreach'.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 173): "> "[Name], saw [Company] is [news event]. That kind of [change] usually creates [specific challenge you solve]...""
- **Issue:** Generates hundreds of customer-facing first lines with zero brand-voice gate (get_writing_style/check_my_copy) and no product-spec verification for Epiphan value-props. Violates house rules 1 and 2 at the highest volume of any skill in the set.
- **Fix:** Add a batchable check_my_copy pass over generated lines; pull any product-capability claim from search_product_knowledge before it enters a line.

### [HIGH] tool_integration
- **Evidence** (line 59-67): "### Research Sources
- Company news and press releases
- LinkedIn activity (posts, comments, job changes)..."
- **Issue:** Lists research sources but names NO tools — no apollo_organizations_job_postings, no Clay/web for news, no Epiphan intent tool. Describes an outcome with no wired tool chain, so it cannot run at the '300 prospects in minutes' scale it claims.
- **Fix:** Wire concrete tools per source (apollo_organizations_job_postings, apollo_organizations_enrich, Clay find-and-enrich-company, web/intent-signal-aggregator) and specify batch mechanics.

### [MED] tool_integration
- **Evidence** (line 39): "Check HubSpot via `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts` for any contact on the list before spending research time."
- **Issue:** Golden Rules gate re-implemented inline and only partially; ATL/BTL tiering used by every sibling is absent, so it can personalize BTL contacts the pipeline drops.
- **Fix:** Gate the input list through qualify_lead to inherit the same dedupe + ATL/BTL verdict.

### [MED] output_contract
- **Evidence** (line 16): "**Output:** Personalized first lines with confidence scores, grouped by personalization type, in CSV or merge-field format"
- **Issue:** CSV/merge-fields with no draft-first delivery and no named destination; lines feed 'sequence position 1' (line 227) directly.
- **Fix:** Add a draft-first staging step (or explicit CSV-for-review handoff) and name where the file lands.

### [LOW] maintainability
- **Evidence** (line 234-236): "| Response Rate | 1-3% | 8-15% | ... **Lift** | Baseline | 5-10x improvement |"
- **Issue:** Generic benchmark/best-practice filler reads as a marketing explainer, inflating the file without runnable steps.
- **Fix:** Trim explainer content to reference/; keep SKILL.md focused on the tool-wired workflow.

## Missing tool references

- qualify_lead
- check_my_copy
- get_writing_style
- search_product_knowledge
- apollo_organizations_job_postings
- apollo_organizations_enrich
- find-and-enrich-company

## Self-healing gap (see specs/self-healing-template.md)

Weakest of the six: no failure definition beyond a 'fallback strategies' section (186-194), no retry->degrade->alert ladder, no tool wiring to fail against, and no run log at ~/.claude/skill-runs/personalization-at-scale.jsonl. Sidecar is the only telemetry and presumes a workflow with no concrete tool calls.

## Overlap candidates (flag only — no removal)

- cold-email-sequence-generator-skill
- prospect-research-to-cadence
- email-template-generator-skill
- social-selling-content-generator-skill
