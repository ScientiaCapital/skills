# Patch: linkedin-sales-navigator-alt-skill

**Score:** trigger=2 tool_integration=1 output_contract=2 failure_handling=1 maintainability=1 (sum=7/25)

**Highest-leverage single change (L effort):** Replace manual pattern-guessing with Apollo/Clay MCP + HubSpot dedupe/qualify_lead gate, and narrow the trigger to job-change detection
**Expected impact:** Eliminates policy-risky email guessing and the largest trigger collision in the prospecting cluster; produces qualified, deduped output

## Description

**Before:**
> Build targeted prospect lists by analyzing LinkedIn profiles, extracting job titles, companies, locations, and recent activity. Identifies decision-makers, tracks job changes for warm outreach, and enriches contact data. Use when users need to find prospects, build lead lists, or track decision-maker movements.

**After (proposed):**
> Detect warm outbound timing by surfacing recent job-changers, promotions, and new-in-role decision-makers at target accounts, enriched via Apollo/Clay MCP and deduped against HubSpot. Gates every prospect through Golden Rules + qualify_lead + suppression before listing. Use when: 'who recently moved into [role]', 'find new-in-role champions at [accounts]', 'warm leads from job changes'. For point contact lookups use contact-hunter-skill instead.

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 300-317): "lines 301-306 `**Email Discovery Methods**: 1. **Pattern Matching** ... 2. **Hunter.io / RocketReach** ... 4. **Domain Search**: Try common patterns` and line 307 `**Phone Number Sources**: ... ZoomInfo / Apollo (paid tools)`"
- **Issue:** Zero live MCP tools; relies on manual email-pattern guessing and generic third-party tools where Epiphan-native Apollo/Clay MCP + hubspot_search_contacts exist. No qualify_lead, no Golden Rules, no suppression gate on a list-producing outbound skill.
- **Fix:** Rebuild around apollo_contacts_search / Clay + hubspot_search_contacts; gate every prospect through qualify_lead + Golden Rules + suppression.

### [HIGH] tool_integration
- **Evidence** (line 30, 79-91): "line 30 `This skill only works with publicly available information and respects LinkedIn's Terms of Service` with no CRM dedupe anywhere in 472 lines"
- **Issue:** Produces prospect lists and 'likely email addresses' with no HubSpot dedupe — will surface existing customers/AE-owned contacts as net-new. Contradicts CLAUDE.md Golden Rules.
- **Fix:** Add mandatory HubSpot dedupe + Golden Rules gate before any prospect is listed.

### [HIGH] maintainability
- **Evidence** (line 94-459): "472 lines; lines 343-373 campaign templates, 376-393 `Research Notes / Seasonal Factors`, 429-437 `Best Practices`"
- **Issue:** Longest of the six (472 lines), nearly all static template + generic best-practices prose with no references/ progressive disclosure.
- **Fix:** Collapse to a lean workflow (ICP -> MCP search -> qualify -> output); move template/examples to references/.

### [HIGH] trigger_quality
- **Evidence** (line 3, 441-447): "line 3 `Build targeted prospect lists by analyzing LinkedIn profiles ... tracks job changes for warm outreach`"
- **Issue:** Heavy collision: 'find [title] at [company]' (line 13) overlaps contact-hunter's 'Find the VP of Sales at [Company]'; job-change tracking overlaps intent-signal-aggregator. Name references Sales Navigator, a tool it can't access, inflating scope.
- **Fix:** Narrow to job-change/warm-lead detection and cross-reference contact-hunter for point lookups; or merge.

### [MED] output_contract
- **Evidence** (line 14, 94-427): "line 14 `Output: Prioritized prospect list with contact details, personalization notes, and segmented campaign strategies`"
- **Issue:** Output is a ~330-line Markdown template with placeholder tables; no concrete artifact written and no Gmail draft-first staging despite outbound intent.
- **Fix:** Define a real deliverable and draft-first staging (or hand to sequence-load-skill).

## Missing tool references

- mcp__claude_ai_Apollo_io__apollo_contacts_search
- mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts
- qualify_lead
- mcp__claude_ai_Clay__find-and-enrich-contacts-at-company
- mcp__claude_ai_Gmail__create_draft

## Self-healing gap (see specs/self-healing-template.md)

No failure definition, no retry->degrade->alert->halt ladder, no run log. Only the outcome sidecar (463-470). Calls no tools, so no observable failure surface; no verification a prospect exists before emitting a 'likely email'.

## Overlap candidates (flag only — no removal)

- contact-hunter-skill
- lookalike-customer-finder-skill
- intent-signal-aggregator-skill
- champion-identifier-skill
