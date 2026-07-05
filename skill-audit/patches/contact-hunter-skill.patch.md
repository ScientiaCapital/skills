# Patch: contact-hunter-skill

**Score:** trigger=4 tool_integration=3 output_contract=2 failure_handling=2 maintainability=1 (sum=12/25)

**Highest-leverage single change (S effort):** Delete orphaned legacy body (123-357) and route qualification through qualify_lead
**Expected impact:** Removes contradictory instructions that could make the skill guess emails/scrape against policy; single source of truth for ATL/BTL and dedupe

## Description

**Before:**
> Find and enrich contact information for specific people or companies using HubSpot, Apollo, and Clay MCP tools. Applies Golden Rules qualification gates before returning results. Use when you need to find contacts at target accounts with verified emails and phones for BDR outreach.

*(trigger_quality > 3 — no description rewrite proposed)*

## Findings & fixes

### [HIGH] maintainability
- **Evidence** (line 122-369): "line 122 `**Compliance:** ...No scraping. Follow CAN-SPAM for outreach.` immediately followed by line 123 `   3. Use title filter: "VP of Engineering"` ... line 126 `   Google:` ... line 138 `   Email Pattern Guessing:`"
- **Issue:** File contains TWO contradictory bodies stitched together: a clean MCP-first workflow (1-122) and a legacy manual/Google-dork/email-guessing version (123-357). The tail defines a second contact-card format (204-223), a second CSV schema (226-230), duplicate trigger lists (306-313) and duplicate compliance sections (315-340) that conflict with the Golden-Rules-gated top half.
- **Fix:** Delete lines 123-357 (orphaned legacy body). Keep the MCP workflow ending at line 122, then the outcome sidecar block.

### [HIGH] maintainability
- **Evidence** (line 368-369): "line 369 `</output>` and line 368 `</workflow>`"
- **Issue:** Dangling closing tags — orphaned `</output>` with no matching open, evidence of a bad merge/paste.
- **Fix:** Remove the stray `</output>` tag.

### [HIGH] tool_integration
- **Evidence** (line 16, 42-74): "line 16 `**MCP Tools:** ...hubspot_search_contacts, apollo_contacts_search, ...Clay__find-and-enrich-contacts-at-company`"
- **Issue:** Does not route through qualify_lead — the CLAUDE.md dedupe/ATL-BTL source of truth. Golden Rules and ATL/BTL are re-implemented inline (Stage G, Stage 3) risking drift from canonical logic.
- **Fix:** Insert qualify_lead as the gate after HubSpot search; drive ATL/BTL and dedupe from its verdict.

### [MED] tool_integration
- **Evidence** (line 138-144, 232-257): "lines 138-144 `Email Pattern Guessing: ... john.smith@acme.com` and line 232 `Email Pattern Detection`"
- **Issue:** Legacy tail promotes email-pattern guessing/Google dorking — a manual method Apollo/Clay automates and the top half explicitly forbids ('No scraping', line 122).
- **Fix:** Remove; rely on Apollo/Clay verified enrichment only.

### [MED] output_contract
- **Evidence** (line 15, 90-118): "line 15 `Output: Qualified contact cards ... and HubSpot record link` and line 111 `**Bulk output** (CSV format for sequence-load)`"
- **Issue:** No delivery mechanism — no Gmail draft-first stage despite CLAUDE.md 'ALWAYS create Gmail drafts for every lead.' Two competing card formats (95-108 vs 204-223) make the contract ambiguous.
- **Fix:** Pick one card format; add draft-staging handoff (or hand to sequence-load-skill).

### [MED] failure_handling
- **Evidence** (line 358-367): "line 367 `Use status "partial" if some stages failed ... "error" only if no output`"
- **Issue:** Only failure signal is the outcome sidecar status. No retry/skip ladder on empty/error waterfall tiers, no run log.
- **Fix:** Add 'no result -> next tier -> all empty = zero-with-reason' ladder and run-log append.

## Missing tool references

- qualify_lead
- mcp__claude_ai_Gmail__create_draft

## Self-healing gap (see specs/self-healing-template.md)

Has outcome sidecar (partial/error) but no per-stage failure DEFINITION, no retry->degrade->alert->halt ladder, and no run log to ~/.claude/skill-runs/contact-hunter.jsonl. Empty-result vs tool-error not distinguished.

## Overlap candidates (flag only — no removal)

- linkedin-sales-navigator-alt-skill
- phone-verification-waterfall-skill
- prospect-enrich-skill
