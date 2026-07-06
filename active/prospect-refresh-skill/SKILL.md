---
name: prospect-refresh
description: "Monday 6:30 AM (and on demand) net-new ICP prospecting across all 7 Epiphan verticals: Apollo People search (ATL-first) -> qualify_lead dedupe + Golden Rules -> Apollo/Clay firmographic enrich -> spec-verified, brand-checked Gmail drafts -> HTML report with HubSpot/Apollo drill-downs. Use when: 'run prospect refresh', 'search new ICP prospects', 'find net-new leads', 'weekly prospecting run'."
schedule: "0 6 30 * * 1"
timezone: "America/New_York"
---

# Prospect Refresh Skill

<objective>
Execute weekly net-new prospect search across all ICP verticals (Higher Ed, Courts, Gov, Corporate AV, Healthcare, Houses of Worship, K-12) using Apollo's People API. Route every candidate through the `qualify_lead` gate (dedupe + Golden Rules + ATL/BTL/GRAY + suppression — see `skill-audit/specs/suppression-spec.md`) instead of hand-rolled matching. Enrich top 30 results. Verify every product claim via `search_product_knowledge` and brand-check the copy via `check_my_copy` before a draft is created. Create personalized Gmail drafts for each surviving prospect. Output HTML report with drill-down links to HubSpot and Apollo records.
</objective>

<quick_start>
**Trigger:** Monday 6:30 AM ET (runs after prospect-enrich)  
**Manual Trigger:** "Run prospect refresh" or "Search new ICP prospects"  
**Dependencies:** Requires HubSpot portal 21530819, Apollo credits, Gmail tkipper@epiphan.com, `qualify_lead` + `search_product_knowledge`/`search_product_catalog` + `check_my_copy` (Epiphan AI)  
**Output:** 30 net-new prospects + 30 Gmail draft emails + HTML report with HubSpot links
</quick_start>

<success_criteria>
- [ ] Query Apollo for ICP title + vertical combinations (ATL-first targeting)
- [ ] `qualify_lead` called as the single gate — dedupe, Golden Rules, ATL/BTL/GRAY, suppression (see `skill-audit/specs/suppression-spec.md`); no hand-rolled keyword matching
- [ ] Enrich top 30: company revenue, headcount, funding, tech stack
- [ ] Every product/capability claim confirmed via `search_product_knowledge`/`search_product_catalog` before it appears in a draft — never stated from memory
- [ ] Every filled draft passes `check_my_copy` (Epiphan Brand) before `gmail_create_draft` is called
- [ ] Create Gmail draft for each prospect (personalized template per vertical)
- [ ] Generate HTML report with sortable columns: name, title, company, vertical, ATL/BTL, links to HubSpot/Apollo
- [ ] Include ATL/BTL tier badges and vertical ICP scores
- [ ] Report: total prospects found, dedupe rate, ATL %, top 5 companies by headcount
- [ ] Run outcome logged per `skill-audit/specs/self-healing-template.md`
</success_criteria>

<workflow>

## Stage 1: Define ICP Search Matrix

**Verticals (7 ICPs) with targeting weights:**

| Vertical | ICP Score | ATL Titles | Target Count | Budget Authority |
|----------|-----------|-----------|--------------|------------------|
| Higher Ed | 90 | CIO, VP IT, Dir. of IT Services, Provost, Dean, Dir. Academic Tech | 5 | >$50K |
| Courts | 85 | Clerk of Court, Court Administrator, Court Executive Director, Chief Judge | 4 | >$75K |
| Government | 80 | City Manager, IT Director/CIO, Director of Procurement, County Admin | 5 | >$100K |
| Corporate AV | 80 | VP Facilities, VP IT/CIO, VP Corp Communications, Dir. Facilities Ops, Dir. IT Infra | 5 | >$150K |
| Healthcare | 75 | CFO, CIO, COO, VP Operations, Director of Medical Education | 4 | >$100K |
| Houses of Worship | 70 | Senior Pastor, Executive Pastor, Finance Committee Chair, Facilities Chair | 4 | >$25K |
| K-12 | 65 | Superintendent, CTO/Dir. Tech Services, Dir. Instructional Tech, Building Principal | 3 | >$10K |

**Total Target:** 30 prospects (weighted by ICP score)

---

## Stage 2: Query Apollo via People API Search

**MCP Tool:** `apollo_mixed_people_api_search`

**Search Loop (iterate per vertical):**

```
organization_locations: ["United States", "Canada"]
person_titles: [ATL_TITLES_FOR_VERTICAL]
organization_keyword_tags: [VERTICAL_KEYWORD] # e.g., "Higher Ed", "Education"
person_seniorities: ["c_suite", "vp", "director"]
organization_num_employees_ranges: [HEADCOUNT_RANGE_FOR_VERTICAL]
page: 1
per_page: 25
```

**Example Query (Higher Ed):**
```
person_titles: ["Chief Information Officer", "CIO", "VP Information Technology", "VP of IT", "Director of IT Services", "Director of Technology", "Provost"]
organization_keyword_tags: ["Higher Education", "Education", "University", "College"]
organization_num_employees_ranges: ["51,200", "201,500", "501,1000", "1001,5000", "5001,10000"]
person_locations: ["United States", "Canada"]
```

**Output per vertical:** Up to 25 results (name, email, title, organization, location, person_id, organization_id)

---

## Stage 3: Qualify — `qualify_lead` Gate

**MCP Tool:** `qualify_lead`

Call `qualify_lead` on every Apollo result immediately after Stage 2, before any enrichment
spend or draft creation. This is the single qualification gate — do not re-derive dedupe,
Golden Rules, ATL/BTL keyword tables, or suppression logic inline. Per
`skill-audit/specs/suppression-spec.md`, `qualify_lead` returns `category`, `power_level`
(atl/gray/btl/unknown), and a `junk` flag, and is the enforcement point for suppression state
(`bdr_suppression_until` today; the proposed `bdr_suppressed`/`bdr_suppression_reason` properties
once created).

- **Dedupe (Gate A):** the gate checks each candidate against existing HubSpot contacts (email,
  company domain, name) — drop any match. (Previously a hand-rolled two-filter HubSpot search;
  now delegated so it can't drift from the canonical dedupe logic.)
- **Golden Rules:** customers, channel partners, device owners, and product-only engagers are
  excluded inside the gate call — see CLAUDE.md's Golden Rules for the canonical list; this skill
  does not restate it.
- **AE-owned / 90-day stale exception** (Lex Evans, Ron Epstein, Phillip Sandler) is evaluated by
  the gate; a stale AE lead surfaces as `STALE AE LEAD` for Tim rather than being silently dropped.
- `power_level = atl` → keep, prioritize (weighted by the Stage 1 ICP score).
- `power_level = gray` → keep, flagged for manual review (needs the vertical's budget-authority
  threshold from Stage 1, e.g. >$25K).
- `power_level = btl` or `junk = true` → drop.
- Suppressed (per the spec's fallback/release rules) → drop, note reason.
- **Geo:** USA/Canada only (per CLAUDE.md Golden Rule 5) — the gate enforces this; do not add a
  separate geo filter.

**Expected result:** 40-60% of Apollo results removed at dedupe; the ATL/GRAY-first filter
narrows further to typically 15-18 surviving prospects per vertical.

If `qualify_lead` is unavailable, do not silently fall through to hand-rolled matching — mark the
run `partial`, name the stage, and continue with whatever already-qualified prospects exist (see
Failure Handling & Outcome Logging).

---

## Stage 4: Enrich Top 30 Results

**MCP Tool:** `apollo_organizations_enrich` (for company data)

**For each retained prospect:**

```
domain: organization.domain (from Apollo result or extract from email)
```

**Enrich fields:**
- annual_revenue, headcount, founded_year
- latest_funding_amount, latest_funding_date
- website, industry, keyword_tags
- technologies (current tech stack)

**MCP Tool:** `find-and-enrich-contacts-at-company` (Clay fallback for company data)

**If Apollo org enrichment incomplete:**
```
companyIdentifier: prospect.domain
dataPoints: {
  companyDataPoints: [
    { type: "Latest Funding" },
    { type: "Tech Stack" },
    { type: "Company Customers" }
  ]
}
```

---

## Stage 5: Verification Gate + Create Gmail Drafts (One per Prospect)

**Verification Gate (required, before any draft is created):** the templates below are
skeletons, not approved copy — every one states or implies an Epiphan product capability
(e.g., "auto-recordings to your LMS", "4K Capture + Distribution", "Epiphan powers video
capture..."). Treat each bracketed capability claim as unverified until it clears this gate:

a. **Spec check** — confirm every capability/product claim for the prospect's vertical live via
   `search_product_knowledge` (or `search_product_catalog`) before it goes into a draft. Never
   state a capability from memory. If verification fails or the tool is unavailable, drop that
   line from the draft rather than guessing — don't block the whole draft on one unverified claim.
b. **Brand/voice check** — run `check_my_copy` (Epiphan Brand) on the filled body. Resolve every
   flag; never carry off-voice copy forward to `gmail_create_draft`.

**MCP Tool:** `gmail_create_draft`

**Per-Vertical Email Templates (Personalized — fill capability lines from
`search_product_knowledge`, not from the wording below):**

**Template A — Higher Ed (ICP 90):**
```
To: prospect.email
Subject: Epiphan + [UNIVERSITY_NAME]: Hybrid Learning Infrastructure for [SCHOOL_TYPE]

Body:
Hi [FIRST_NAME],

I was researching [UNIVERSITY_NAME]'s commitment to hybrid learning and asynchronous instruction—I noticed the shift in your academic technology strategy.

We work with schools like [REFERENCE_UNIV] to solve a specific challenge: instructor burnout from manual video streaming and recording.

[COMPANY_NAME] provides:
- [VERIFIED_CAPABILITY_1 — e.g. lecture capture; confirm via search_product_knowledge]
- [VERIFIED_CAPABILITY_2 — e.g. LMS distribution; confirm via search_product_knowledge]
- [VERIFIED_CAPABILITY_3 — e.g. multi-platform distribution; confirm via search_product_knowledge]

I'm not trying to sell—just want to understand if this is a priority this quarter for your department.

Are you the right person to discuss academic video infrastructure, or should I loop in [ROLE_IF_DIRECTOR]?

Best,
Tim
--
Epiphan Video
```

**Template B — Courts (ICP 85):**
```
To: prospect.email
Subject: [COURT_NAME] Remote Proceedings + Video Evidence Management

Body:
Hi [FIRST_NAME],

I was reading about [COURT_NAME]'s recent adoption of remote hearing technology. Given the volume of video evidence you're handling, I suspect you're managing multiple formats and platforms.

We partner with courts in [STATE] to centralize video evidence capture and courtroom live-streaming.

Curious: are you managing this manually today, or do you have a platform in place?

Would be worth a 15-min conversation if you're evaluating vendors this quarter.

Best,
Tim
```

**Template C — Corporate AV (ICP 80):**
```
To: prospect.email
Subject: [COMPANY] Boardroom Modernization — 4K Capture + Distribution

Body:
Hi [FIRST_NAME],

I noticed [COMPANY] is expanding your meeting rooms and conference infrastructure. Given your footprint, I'm guessing you're wrestling with:
- Inconsistent video quality across rooms
- Integration with Zoom/Teams/corporate network
- Archival and compliance

We've solved this for companies like [REFERENCE_CORP] (similar size/industry).

Worth a quick call to explore?

Best,
Tim
```

**Template D — Healthcare (ICP 75):**
```
To: prospect.email
Subject: [HOSPITAL_NAME] Medical Education + Video Evidence

Body:
Hi [FIRST_NAME],

I was researching [HOSPITAL_NAME]'s surgical training and medical education programs. I see you're ramping up simulation labs and remote mentoring.

Epiphan powers video capture and distribution for teaching hospitals doing exactly this.

Quick question: who owns your medical education video infrastructure today?

Best,
Tim
```

**Template E — Houses of Worship (ICP 70):**
```
To: prospect.email
Subject: [CHURCH_NAME] Livestream + Archive

Body:
Hi [FIRST_NAME],

I noticed [CHURCH_NAME] is offering both in-person and online services. Curious how you're handling the livestream and on-demand library today.

We work with churches your size to simplify setup and reach.

Might be worth exploring—no commitment.

Best,
Tim
```

**Template F — K-12 (ICP 65):**
```
To: prospect.email
Subject: [DISTRICT_NAME] Hybrid Learning + Board Meeting Recording

Body:
Hi [FIRST_NAME],

I was researching how [DISTRICT_NAME] is scaling hybrid learning post-pandemic. Guessing you're balancing live instruction, recordings, and board meeting transparency.

Epiphan helps districts like [REFERENCE_DISTRICT] simplify video capture across buildings.

Quick question: what's your current capture setup?

Best,
Tim
```

**Draft Creation Logic:**
1. Choose template based on prospect's vertical.
2. Substitute [BRACKETS] with actual prospect/company data; pull capability lines from
   `search_product_knowledge` (Verification Gate step a) rather than the template's placeholder wording.
3. Run `check_my_copy` on the filled body (Verification Gate step b); resolve flags.
4. Only after both gate steps pass, call `gmail_create_draft`. Do NOT send—leave as draft for manual review.
5. Tag draft with prospect's ATL/BTL tier + vertical ICP score.

**MCP Tool Parameters:**
```
to: prospect.email
subject: [PERSONALIZED_PER_VERTICAL]
body: [TEMPLATE_WITH_SUBSTITUTIONS]
contentType: "text/plain"
```

---

## Stage 6: Generate HTML Report

**Output Format:** Self-contained HTML file with:

**Report Header:**
- Execution date/time
- Total prospects found (Apollo)
- Dedupe rate %
- Final net-new count
- ATL/BTL breakdown
- Top 5 verticals by prospect count

**Sortable Table (JavaScript):**

| Name | Title | Company | Vertical | ICP | ATL/BTL | Headcount | Revenue | Gmail Draft | HubSpot Link | Apollo Link |
|---|---|---|---|---|---|---|---|---|---|---|
| Jane Smith | CIO | Higher Education Univ | Higher Ed | 90 | ATL | 8,500 | $2.1B | ✓ Draft | [link] | [link] |
| Bob Jones | Court Admin | State Supreme Court | Courts | 85 | ATL | 450 | $120M | ✓ Draft | [link] | [link] |

**Summary Section:**
- Top 5 companies by headcount
- Top 5 companies by funding (if available)
- Vertical breakdown (counts by ICP)
- ATL % vs. BTL % in results
- Recommended dial priority (ATL first, >$500M revenue second)

**Links Format:**
- HubSpot link: `https://app.hubspot.com/contacts/21530819/record/0-1/{contactId}` (placeholder until contact created)
- Apollo link: `https://app.apollo.io/search?filters...` (from Apollo result)

---

## Stage 7: Load into HubSpot (Optional Next Step)

**Note:** This skill outputs drafts + report. **Sequence Load Skill** runs 45 min later (7:15 AM) to:
- Create HubSpot contacts from top 30
- Validate phone numbers
- Add to Apollo outreach sequence

</workflow>

---

## Failure Handling & Outcome Logging

Follow `skill-audit/specs/self-healing-template.md` for the failure ladder (retry -> degrade ->
alert -> halt) and the three-way status definition (success/partial/error — always name the
failing stage for partial/error). Specific degrade paths for this skill:
- **Apollo partial/timeout on a vertical:** retry once, then skip that vertical, note it as
  degraded in the HTML report, and continue with the remaining verticals (status: `partial`).
- **Zero net-new survives Stage 3:** status `partial` (not `error`) if Apollo returned any
  results — report the raw Apollo count vs. the qualify_lead-gated count rather than reporting silence.
- **`qualify_lead` unavailable:** do not silently proceed as if the gate passed — halt draft
  creation for the affected candidates, alert Tim, and mark the run `partial` naming Stage 3.
- **Gmail quota / `gmail_create_draft` failure:** retry once, then continue drafting the rest and
  list any prospect whose draft failed in the report; don't fail the whole run for one draft.

In addition to the existing outcome sidecar below, append one run-log line to
`~/.claude/skill-runs/prospect-refresh.jsonl` per the spec's format. Distinguish an
empty-but-valid result (no net-new prospects this week — status success, `prospects_found: 0`)
from a tool error (Apollo/HubSpot/qualify_lead unreachable — status error or partial with the
failing stage named).

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-prospect-refresh.json`:
```json
{"ts":"[UTC ISO8601]","skill":"prospect-refresh","version":"1.1.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"prospects_found":[n],"drafts_created":[n],"atl_count":[n],"gray_count":[n],
            "verticals_searched":[n],"verticals_degraded":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

<dependencies>
## MCP tools
- `apollo_mixed_people_api_search` — Stage 2 ICP prospecting
- `qualify_lead` — single qualification gate: dedupe, Golden Rules, ATL/BTL/gray/junk, suppression (Stage 3)
- `apollo_organizations_enrich` / `find-and-enrich-contacts-at-company` (Clay fallback) — firmographic enrichment (Stage 4)
- `search_product_knowledge` / `search_product_catalog` — spec/capability verification gate; required before any product claim lands in a draft (Stage 5)
- `check_my_copy` (Epiphan Brand) — brand-voice gate; required on every filled draft before `gmail_create_draft` (Stage 5)
- `gmail_create_draft` — draft staging, one per prospect, never sent directly (Stage 5)

## Sibling skills referenced (reuse, don't rebuild)
- `prospect-enrich` — runs 6:00 AM, upstream of this skill
- `sequence-load` — runs 7:15 AM, downstream hand-off for qualified prospects
- `prospect-research-to-cadence` / `contact-hunter-skill` — same `qualify_lead` gate pattern
</dependencies>

## Guardrails
- Never hand-roll dedupe/Golden Rules/ATL-BTL/suppression logic inline — `qualify_lead` is the
  single gate (`skill-audit/specs/suppression-spec.md`).
- Never state an Epiphan capability, spec, or competitive claim from memory — confirm via
  `search_product_knowledge`/`search_product_catalog` before it's used in a draft.
- Never call `gmail_create_draft` for copy that hasn't passed `check_my_copy`.
- Drafts are draft-first: stage via `gmail_create_draft`, never send directly.
- If a spec or brand check can't be resolved (tool unavailable, no match), don't guess — drop the
  claim/line, note it, and continue with the rest of the run rather than blocking entirely.

---

## Skill Metadata

**Version:** 1.1.0
**Last Updated:** 2026-07-06
**Author:** Tim Kipper
**Status:** Production
**Integration:** Apollo + HubSpot (portal 21530819) + Gmail
**Tier:** P1 (Core BDR Automation)
**Triggers:** Scheduled (Monday 6:30 AM) + Manual ("Run prospect refresh")
**Dependencies:** prospect-enrich (runs 6:00 AM), feeds into sequence-load (7:15 AM)
**Changelog:** 1.1.0 — routed dedupe/Golden Rules/ATL-BTL/suppression through the `qualify_lead`
gate (was hand-rolled HubSpot filters); added a `search_product_knowledge` spec-verification +
`check_my_copy` brand gate before `gmail_create_draft`; added Failure Handling degrade paths + run log.
