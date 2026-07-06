---
name: contact-hunter-skill
description: Find and enrich contact information for specific people or companies using HubSpot, Apollo, and Clay MCP tools. Applies Golden Rules qualification gates before returning results. Use when you need to find contacts at target accounts with verified emails and phones for BDR outreach.
---

# Contact Hunter

<objective>
Find, enrich, and qualify contact information for specific people or companies using live MCP tool calls to HubSpot, Apollo, and Clay. Returns contact cards with email, phone, title, ATL/BTL tier, and suppression status — ready for the BDR dial list, a Gmail draft, or sequence load.
</objective>

<quick_start>
**Trigger:** "Find the VP of Sales at [Company]" or "Get contact info for [Name] at [Company]" or "Hunt contacts at [Company]"
**Input:** Person name, company, job title, location, or LinkedIn URL
**Output:** Qualified contact cards with email, phone, LinkedIn, ATL/BTL tier, suppression status, HubSpot record link, and a staged Gmail draft per contact
**MCP Tools:** `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts`, `mcp__claude_ai_Apollo_io__apollo_contacts_search`, `mcp__claude_ai_Clay__find-and-enrich-contacts-at-company`, `qualify_lead`, `mcp__claude_ai_Gmail__create_draft`
</quick_start>

<success_criteria>
- [ ] Golden Rules pre-filter applied (Stage G) before enrichment spend
- [ ] HubSpot searched first (check if contact already exists)
- [ ] Apollo waterfall run if HubSpot returns no result
- [ ] Clay enrichment run for phone/LinkedIn if Apollo has email only
- [ ] `qualify_lead` called as the single gate — Golden Rules, dedupe, ATL/BTL/gray/junk, suppression (see `skill-audit/specs/suppression-spec.md`)
- [ ] Contact card output with HubSpot record URL
- [ ] Gmail draft staged for each surfaced (non-suppressed, non-BTL-excluded) contact
- [ ] Run outcome logged per `skill-audit/specs/self-healing-template.md`
</success_criteria>

<workflow>

## Stage G — Golden Rules Pre-Filter (run BEFORE any search)

Cheap disqualification on already-known properties, before spending enrichment credits:

1. **Customers:** `lifecyclestage = customer` OR `device_count >= 1` → **EXCLUDE**
2. **Channel Partners:** `is_channel = true` → **EXCLUDE**
3. **AE-Owned (Active):** `hubspot_owner_id` IN `[82625923, 423155215, 190030668]` AND last activity < 90 days → **EXCLUDE**
4. **Geo Gate:** Non-USA/Canada contacts → **EXCLUDE** (unless explicitly requested)

If the target company is already a customer, stop and notify Tim. Do not enrich.

## Stage 1: Search HubSpot First

**MCP Tool:** `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts`

```
Search by: company name OR person name OR email domain
Filter: USA/Canada only, NOT lifecyclestage=customer, NOT is_channel=true
Return: contactId, firstName, lastName, email, phone, jobtitle, hubspot_owner_id,
        lifecyclestage, device_count, bdr_suppression_until, last_activity_date
```

If contact found in HubSpot → jump to Stage 3 (qualify_lead gate).
If not found → continue to Stage 2.

## Stage 2: Apollo Enrichment Waterfall

**MCP Tool:** `mcp__claude_ai_Apollo_io__apollo_contacts_search`

```
Search by: person_title OR organization_name
Filters: country IN [US, CA], seniority IN [director, vp, c_suite, owner]
Limit: 10 results
```

If Apollo has email but no phone → run Clay enrichment:

**MCP Tool:** `mcp__claude_ai_Clay__find-and-enrich-contacts-at-company`

```
company: [company name]
title_keywords: [from search parameters]
enrich_phone: true
```

## Stage 3: Qualify — `qualify_lead` Gate

Call `qualify_lead` on every candidate before it's included in output. This is the single
qualification gate — do not re-derive Golden Rules, ATL/BTL keyword tables, or suppression
logic inline. Per `skill-audit/specs/suppression-spec.md`, `qualify_lead` returns `category`,
`power_level` (atl/btl/gray/unknown), and a `junk` flag, and is the enforcement point for
suppression state.

- `power_level = atl` → include, prioritize
- `power_level = gray` → include, flagged for manual review
- `power_level = btl` or `junk = true` → exclude from output
- Suppressed (per the spec's fallback/release rules) → exclude, note reason

## Stage 4: Output Contact Cards

For each contact that passed Stages G, 1–2, and the qualify_lead gate, output:

```
┌─────────────────────────────────────────────────────┐
│ JOHN SMITH  [ATL — VP]                              │
│ VP of Engineering @ Acme Corp                       │
├─────────────────────────────────────────────────────┤
│ Email:    john.smith@acme.com   (Apollo, verified)  │
│ Phone:    +1 (415) 555-0123     (Clay waterfall)    │
│ LinkedIn: linkedin.com/in/johnsmith                 │
│ Location: San Francisco, CA                         │
├─────────────────────────────────────────────────────┤
│ HubSpot:  https://app.hubspot.com/contacts/21530819/│
│           record/0-1/{contactId}                    │
│ Owner:    Unowned (eligible for BDR outreach)       │
│ Suppressed: No                                      │
└─────────────────────────────────────────────────────┘
```

**Bulk output** (CSV format for sequence-load):
```
First,Last,Title,Company,Email,Phone,LinkedIn,ATL_Tier,HubSpot_ID
John,Smith,VP Engineering,Acme Corp,john.smith@acme.com,+14155550123,linkedin.com/in/johnsmith,ATL,{id}
```

**Summary line after each hunt:**
`Found: [N] contacts | [A] ATL | [G] Gray | [B] BTL | [X] excluded by Golden Rules | [S] suppressed`

## Stage 5: Gmail Draft Handoff

Per CLAUDE.md's "always create Gmail drafts" workflow: for each ATL/GRAY contact that passed
Stage 3, stage a draft via `mcp__claude_ai_Gmail__create_draft` (send-from `tkipper@epiphan.com`)
rather than sending directly — or, for bulk hunts feeding a sequence, hand the qualified CSV off
to `sequence-load-skill` instead of drafting one-by-one. Never draft for a BTL/junk/suppressed
contact.

---

**Compliance:** All data sourced from HubSpot (existing CRM records), Apollo (public professional data), or Clay (verified enrichment). No scraping. Follow CAN-SPAM for outreach.

## Failure Handling & Outcome Logging

Follow `skill-audit/specs/self-healing-template.md` for the failure ladder (retry → degrade →
alert → halt) and the three-way status definition (success/partial/error — always name the
failing stage for partial/error). In addition to the existing outcome sidecar below, append one
run-log line to `~/.claude/skill-runs/contact-hunter-skill.jsonl` per the spec's format.
Distinguish an empty-but-valid result (no contacts matched — status success, records_out: 0)
from a tool error (HubSpot/Apollo/Clay/qualify_lead unreachable — status error or partial with
the failing stage named).

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-contact-hunter.json`:
```json
{"ts":"[UTC ISO8601]","skill":"contact-hunter","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"contacts_searched":[n],"contacts_found":[n],"phones_found":[n],"emails_found":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

</workflow>

<dependencies>
## MCP tools
- `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts` — HubSpot lookup (Stage 1)
- `mcp__claude_ai_Apollo_io__apollo_contacts_search` — Apollo waterfall (Stage 2)
- `mcp__claude_ai_Clay__find-and-enrich-contacts-at-company` — phone/LinkedIn enrichment (Stage 2)
- `qualify_lead` — single qualification gate: Golden Rules, dedupe, ATL/BTL/gray/junk, suppression (Stage 3)
- `mcp__claude_ai_Gmail__create_draft` — draft staging (Stage 5)

## Sibling skills referenced (reuse, don't rebuild)
- `sequence-load-skill` — bulk hand-off target for qualified CSV output
- `phone-verification-waterfall-skill` — deeper phone verification if Clay leaves a gap
</dependencies>

## Guardrails
- No scraping, no email-pattern guessing, no Google-dorking — Apollo/Clay enrichment only (see Compliance line).
- Never hand-roll Golden Rules/ATL-BTL/suppression logic inline — `qualify_lead` is the single gate (`skill-audit/specs/suppression-spec.md`).
- Never draft or send to a BTL, junk, or suppressed contact.
- If the target company is already a customer, stop and notify Tim — do not enrich further.

## Skill metadata
**Version:** 1.0.0 · **Author:** Tim Kipper · **Status:** Active · **Tier:** P1 (Core BDR Automation)
