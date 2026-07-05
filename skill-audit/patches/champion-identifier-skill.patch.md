# Patch: champion-identifier-skill

**Score:** trigger=4 tool_integration=2 output_contract=3 failure_handling=2 maintainability=4 (sum=15/25)

**Highest-leverage single change (M effort):** Ground champion candidates in real HubSpot/Apollo contact data and derive ATL/BTL via qualify_lead instead of free-form 0-60 scoring
**Expected impact:** Stops fabricating people and scores; ties influence/ATL to canonical logic so recommendations are actionable

## Description

**Before:**
> Analyze LinkedIn profiles in target accounts to identify potential internal champions. Evaluates role, career path, mutual connections, interests, and suggests personalization approach. Use when you need to find who will champion your solution internally.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] tool_integration
- **Evidence** (line 1-242): "line 3 `Analyze LinkedIn profiles in target accounts to identify potential internal champions` — no MCP tool referenced anywhere in 242 lines"
- **Issue:** Invokes zero live tools. Champion scoring, org chart, and 'Account Mapping (DMU)' (152-159) produced from inference alone — no hubspot_search_contacts for real contacts/owners, no qualify_lead for ATL/BTL, no Apollo/Clay to confirm titles. Candidates and scores are effectively fabricated.
- **Fix:** Pull real account contacts via hubspot_search_contacts + Apollo; derive ATL/BTL/influence from qualify_lead.

### [MED] tool_integration
- **Evidence** (line 225-229): "line 227 `5. Document champion interactions in CRM` (prose, not a tool call)"
- **Issue:** CRM documentation is a manual suggestion, not wired to a HubSpot write/note. ATL/BTL implied by 'Start at Director/VP level' (225) but never gated through canonical qualify_lead / ATL-BTL logic.
- **Fix:** Add qualify_lead ATL/BTL gate on candidates; optionally a HubSpot note write for the chosen champion.

### [MED] failure_handling
- **Evidence** (line 231-240): "lines 233-240 outcome sidecar with `"atl_count":[n]`"
- **Issue:** Sidecar tracks atl_count implying ATL classification is expected, but body never defines how ATL is determined nor what to do when all candidates score <30. No retry/degrade/run-log.
- **Fix:** Define 'no champion found' degrade path; source atl_count from qualify_lead.

### [LOW] output_contract
- **Evidence** (line 15, 61-190): "line 15 `Output: Ranked champion candidates with scores (0-60), outreach templates, org chart, and multi-threading strategy`"
- **Issue:** Format is well-specified (cards, DMU table, coverage map) but no delivery mechanism — outreach templates (100-110) are terminal text, not staged as Gmail drafts per draft-first workflow.
- **Fix:** Stage outreach templates as Gmail drafts via create_draft for top 1-2 candidates.

### [LOW] trigger_quality
- **Evidence** (line 13): "line 13 `**Trigger:** "Find potential champions at [Company]" or "Who should I connect with at [Company] to champion our tool?"`"
- **Issue:** Specific, mostly collision-free, but 'who should I connect with at [Company]' brushes contact-hunter/linkedin-alt point-lookup phrasing.
- **Fix:** Emphasize the champion/advocacy angle to disambiguate.

## Missing tool references

- mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts
- qualify_lead
- mcp__claude_ai_Apollo_io__apollo_contacts_search
- mcp__claude_ai_Gmail__create_draft

## Self-healing gap (see specs/self-healing-template.md)

Outcome sidecar present (partial/error) but no failure definition, no retry->degrade->alert->halt ladder, no run log to ~/.claude/skill-runs/champion-identifier.jsonl. No handling for 'no candidate above threshold'.

## Overlap candidates (flag only — no removal)

- linkedin-sales-navigator-alt-skill
- contact-hunter-skill
- meddic-call-prep-auto-skill
