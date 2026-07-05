# Patch: lookalike-customer-finder-skill

**Score:** trigger=3 tool_integration=1 output_contract=2 failure_handling=2 maintainability=2 (sum=10/25)

**Highest-leverage single change (M effort):** Wire in live MCP data sourcing (HubSpot seeds + Apollo/Clay expansion) and add Golden Rules + qualify_lead gate
**Expected impact:** Turns a static template into a real list producer and prevents surfacing existing customers/AE-owned accounts as new prospects

## Description

**Before:**
> Input your best customers and find 100+ companies that match the profile. Uses firmographic data, tech stack, growth signals, and similarity scoring to identify ideal prospects. Use when building target account lists or expanding to new markets.

**After (proposed):**
> Build a tiered target-account list by analyzing Epiphan's best customers (pulled live from HubSpot + customer-orders MCP), deriving an ICP across firmographics/tech/growth, and scoring 100+ net-new lookalike companies 0-100. Gates every surfaced company through Golden Rules + qualify_lead so existing customers/channel/AE-owned accounts are excluded. Use when: 'find companies like [customers]', 'build a lookalike list', 'who else looks like [account]', expanding into a new vertical.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 353-358): "lines 353-358 `**Recommended Tools**: - **Company Data**: Crunchbase, ZoomInfo, LinkedIn ... - **Contacts**: Apollo, RocketReach, Hunter.io ... - **Intent**: 6sense, Bombora, G2`"
- **Issue:** Names only generic/third-party tools as prose and invokes ZERO live MCP tools. Epiphan-native HubSpot/customer-orders MCP and Apollo/Clay MCP ignored — seed 'best customers' and lookalikes would be fabricated.
- **Fix:** Replace with concrete MCP calls: pull seeds from HubSpot/customer-orders MCP, expand via apollo_mixed_companies_search / Clay find-and-enrich-company.

### [HIGH] tool_integration
- **Evidence** (line 262-270): "line 262 `### Stage S — Suppression Gate` present but no Golden Rules customer/channel/AE gate and no qualify_lead anywhere"
- **Issue:** List-producing skill outputs 100+ companies plus 'Decision Maker' contacts (145-149) but only has Suppression gate — missing Golden Rules customer/channel/AE-owned exclusion; no qualify_lead. Could surface existing customers as 'net-new lookalikes'.
- **Fix:** Add Golden Rules Gate (as contact-hunter Stage G) and gate any surfaced contact through qualify_lead.

### [MED] output_contract
- **Evidence** (line 189, 320-348): "line 189 `**Export Available**: CSV with company details` and line 336 `- [ ] Enrich contact data`"
- **Issue:** Output is a Markdown report; 'Export Available: CSV' asserted but no file written and no delivery mechanism (XLSX/HubSpot list/Gmail draft). Bulk is a static placeholder template, not a produced artifact.
- **Fix:** Write a real ranked-company XLSX/CSV and optionally push to a HubSpot list.

### [MED] maintainability
- **Evidence** (line 276-399): "443 lines; lines 321-348 `Quick Start Action Plan / Week 1 ... Week 5-6` and lines 285-317 `Expected Results: Response Rate 40-50%`"
- **Issue:** ~440 lines, much of it hardcoded outreach-cadence playbook and invented benchmark rates belonging in a sequence/targeting skill. No references/ progressive disclosure.
- **Fix:** Cut weekly action-plan + benchmark tables; keep ICP+scoring+output; push detail to references/.

### [LOW] trigger_quality
- **Evidence** (line 2-3, 413-418): "line 3 `Input your best customers and find 100+ companies that match the profile`"
- **Issue:** Decent description but scope overlaps ICP/territory skills; trigger phrases buried at 413-418, generic (not tied to Epiphan verticals).
- **Fix:** Pull trigger phrases into description; tie ICP to Epiphan verticals.

## Missing tool references

- mcp__claude_ai_Epiphan_Ai__hubspot_search_companies
- qualify_lead
- mcp__claude_ai_Apollo_io__apollo_mixed_companies_search
- mcp__claude_ai_Clay__find-and-enrich-company

## Self-healing gap (see specs/self-healing-template.md)

No failure definition, no retry/degrade ladder, no run log. Only the outcome sidecar (432-441). Calls no tools, so nothing observable can fail — real gap is it never verifies data existence before producing a report.

## Overlap candidates (flag only — no removal)

- territory-planning-optimizer
- gtm-pricing-skill
- intent-signal-aggregator-skill
