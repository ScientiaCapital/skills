---
name: linkedin-sales-navigator-alt-skill
description: Detect warm outbound timing by surfacing recent job-changers, promotions, and new-in-role decision-makers at target accounts, enriched via Apollo/Clay MCP and deduped against HubSpot. Gates every prospect through Golden Rules + qualify_lead + suppression before listing. Use when: "who recently moved into [role] at [company]", "find new-in-role champions at [accounts]", "warm leads from job changes", "track promotions at [target accounts]", "who's newly hired into [title] roles this month". For point-in-time contact lookups ("find the VP of Sales at [Company]") use contact-hunter-skill instead — this skill is specifically for job-change/new-in-role timing signals, not general prospect-list building.
---

# LinkedIn Sales Navigator Alternative — Job-Change Signal Detector

<objective>
Surface warm outbound timing by detecting recent job changes, promotions, and new-in-role
decision-makers at target accounts — without a Sales Navigator subscription. This skill does
not browse LinkedIn or guess email addresses; it sources signal and contact data from live
Apollo/Clay MCP tools, then gates every candidate through HubSpot dedupe + `qualify_lead` +
Golden Rules + suppression before it's ever surfaced. New-in-role people are high-intent
targets (evaluating vendors in their first 90 days) — that timing signal, not a scraped
LinkedIn profile, is the point of this skill.
</objective>

<quick_start>
**Trigger:** "who recently moved into [role] at [accounts]", "find new-in-role champions at [company]", "warm leads from job changes", "track promotions at [target accounts]"
**Not this skill:** a plain "find [title] at [company]" lookup with no job-change angle → use `contact-hunter-skill`
**Output:** A gated, deduped list of job-change/promotion signals per target account — hot (ATL, <30-day change) vs. warm (GRAY or hiring-signal-only) — handed off for drafting/enrollment
**Dependencies:** Apollo MCP (`apollo_organizations_job_postings`, `apollo_mixed_people_api_search`, `apollo_organizations_enrich`, `apollo_people_match`), Clay MCP (`find-and-enrich-contacts-at-company`, `find-and-enrich-company`), HubSpot (`hubspot_search_contacts`, `qualify_lead`), Gmail (`create_draft`)
</quick_start>

<success_criteria>
- [ ] Target accounts / ICP defined before any tool call (explicit list or HubSpot list)
- [ ] Job-change/promotion/new-in-role signals come from Apollo and/or Clay MCP tool calls only — no manual pattern-guessing of "who's probably relevant"
- [ ] Every candidate checked against HubSpot (`hubspot_search_contacts`) for an existing record before being treated as net-new
- [ ] Every surviving candidate gated through `qualify_lead` + Golden Rules (customers, channel partners, product-only engagers excluded; AE-owned 90-day stale exception applied per CLAUDE.md) + the suppression check (see `skill-audit/specs/suppression-spec.md`)
- [ ] No "likely email address" guessing — contact details come from Apollo/Clay enrichment or are tagged "needs enrichment," never a `firstname.lastname@domain.com` guess
- [ ] Output segments Hot (ATL + recent change) vs. Warm (GRAY or hiring-signal-only); BTL/NEVER-ATL/suppressed never listed
- [ ] Next-step handoff stated (sequence-load-skill / nooks-autopilot for enrollment, or Gmail draft-first per CLAUDE.md) rather than this skill inventing campaign copy
- [ ] Outcome sidecar written
</success_criteria>

<workflow>

## Stage 1 — Define target accounts + signal window
Get the target account set from the user's request or a HubSpot list (`hubspot_search_contacts` /
existing list). Default signal window: job changes/promotions in the **last 30-60 days**. Confirm
ICP filters if given (industry, size, geography) — this scopes which accounts to check, it does not
replace the qualification gate in Stage 3.

## Stage 2 — Detect signals via Apollo/Clay (no manual guessing)
Per target account/domain, call real tools — do not infer from static title lists:
- **`apollo_organizations_job_postings`** — active hiring at the account (a hiring-signal proxy:
  growth, new-role backfill, evaluating tools for a function that's expanding).
- **`apollo_mixed_people_api_search`** — search people at the account by title/seniority to surface
  those newly in role; treat a short tenure-in-current-title as the job-change signal since Apollo
  does not expose a direct "changed jobs" filter.
- **Clay `find-and-enrich-contacts-at-company`** / **`find-and-enrich-company`** — parallel or
  fallback source, especially for accounts thin in Apollo's index.
Record per candidate: name, title, company, domain, detected signal type (new-in-role / promotion /
hiring-at-account), source tool, and tenure/date if available. This is the raw candidate list —
nothing here is qualified yet.

## Stage 3 — HubSpot dedupe + qualify_lead gate (mandatory, no bypass)
For every raw candidate, in order:
1. **Dedupe:** `hubspot_search_contacts` by email/domain — if a contact record exists, use it
   (don't treat as net-new); note existing owner/lifecyclestage.
2. **`qualify_lead`:** returns category, `power_level` (ATL/GRAY/BTL/unknown), region, junk flag.
3. **Golden Rules** (CLAUDE.md): exclude `lifecyclestage = customer` or `device_count >= 1`,
   `is_channel = true`, product-only-engager `first_conversion`, and BTL/NEVER-ATL titles.
   Apply the **AE-owned 90-day stale exception**: contacts owned by Lex Evans (82625923), Ron
   Epstein (423155215), or Phillip Sandler (190030668) are excluded unless last activity is
   >90 days ago (Ron: all geos; Lex/Phil: NA only) — surface those as `STALE AE LEAD`, don't
   auto-list them as fresh.
4. **Suppression:** check `bdr_suppressed` / `bdr_suppression_until` per the contract in
   `skill-audit/specs/suppression-spec.md` (this skill only reads/respects that gate — it does not
   create HubSpot properties or write suppression state).
5. Drop anything that fails 2-4. Tag survivors ATL / GRAY with their `qualify_lead` category.

## Stage 4 — Enrich survivors only
For the gated list only, fill in contact/company detail via **`apollo_organizations_enrich`**,
**`apollo_people_match`**, or Clay **`add-contact-data-points`** / **`add-company-data-points`**.
If a field (email, phone) can't be verified through these tools, mark the row **"needs
enrichment"** — never emit a guessed `firstname.lastname@domain` pattern.

## Stage 5 — Prioritize, segment, output
- **🔥 Hot:** ATL + job-change/promotion detected within the signal window.
- **🤝 Warm:** GRAY power level, or hiring-signal-only (no personal change detected) at an
  otherwise-qualified account.
- Group by account; flag accounts with no ATL/GRAY survivor as needing a broader search
  (`hubspot_find_contacts_by_role` equivalent) rather than lowering the bar.

```markdown
# Job-Change Signal List: [Target Account Set / Campaign Name]

**Generated**: [Date] | **Signal window**: last [N] days | **Accounts checked**: [N] | **Gated candidates**: [N]

## Search Criteria
- Target accounts / ICP: [list or filters]
- Signal types: new-in-role | promotion | hiring-at-account

## 🔥 Hot (ATL, recent change)
**[Name]** — [New Title] at [Company] ([domain])
- Signal: [new-in-role / promotion], detected [date/tenure], source: [Apollo/Clay tool]
- HubSpot: [new contact | existing, owner X] | qualify_lead: [category, power_level]
- Contact: [verified email/phone from Apollo/Clay, or "needs enrichment"]

## 🤝 Warm (GRAY or hiring-signal-only)
[same row structure]

## Excluded (for transparency, not for outreach)
- Golden Rules: [n] | Suppressed: [n] | Stale-AE surfaced: [n, see STALE AE LEAD]

## Next Step
Hand qualified rows to `sequence-load-skill` / `nooks-autopilot` for sequence enrollment, or
stage individual Gmail drafts via `gmail_create_draft` (from tkipper@epiphan.com) per Tim's
call → draft → review → send workflow. This skill does not draft campaign copy itself.
```

</workflow>

<dependencies>
## MCP tools
- **Apollo:** `apollo_organizations_job_postings`, `apollo_mixed_people_api_search`,
  `apollo_organizations_enrich`, `apollo_people_match`
- **Clay:** `find-and-enrich-contacts-at-company`, `find-and-enrich-company`, `add-contact-data-points`, `add-company-data-points`
- **HubSpot:** `hubspot_search_contacts`, `qualify_lead`
- **Gmail:** `create_draft` (draft-first staging on handoff, not built here)

## Reference (by path, not duplicated)
- `skill-audit/specs/suppression-spec.md` — suppression contract this skill reads/respects
- CLAUDE.md Golden Rules + AE 90-day stale exception + ATL/BTL classification

## Sibling skills
- `contact-hunter-skill` — point-in-time "find [title] at [company]" lookups (use instead of this skill when there's no job-change angle)
- `sequence-load-skill` / `nooks-autopilot` — actual enrollment once a candidate is gated here
- `intent-signal-aggregator-skill` — non-job-change intent signals (overlaps only on "why now" timing, not on source data)
</dependencies>

## Guardrails
- Never guess email addresses or phone numbers from a naming pattern — Apollo/Clay enrichment or "needs enrichment," nothing in between.
- Never list a candidate that hasn't passed `hubspot_search_contacts` dedupe + `qualify_lead` + Golden Rules + suppression.
- Never auto-exclude an AE-owned contact outright — apply the 90-day stale exception and surface `STALE AE LEAD` per CLAUDE.md instead of silently dropping it.
- This skill does not create HubSpot properties or write suppression state — it reads the existing gate.
- This skill does not browse LinkedIn directly; all signal comes from Apollo/Clay MCP.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-linkedin-sales-navigator-alt.json`:
```json
{"ts":"[UTC ISO8601]","skill":"linkedin-sales-navigator-alt","version":"2.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"accounts_checked":[n],"raw_candidates":[n],"gated_candidates":[n],"hot":[n],"warm":[n],
            "excluded_golden_rules":[n],"excluded_suppressed":[n],"stale_ae_surfaced":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

## Skill metadata
**Version:** 2.0 · **Author:** Tim Kipper · **Status:** active
**Chain:** `linkedin-sales-navigator-alt-skill` → `sequence-load-skill` / `nooks-autopilot` (enrollment) → `morning-brief`
**Not a replacement for:** `contact-hunter-skill` (point lookups), `lookalike-customer-finder-skill`, `champion-identifier-skill` — flagged as adjacent, not merged.
