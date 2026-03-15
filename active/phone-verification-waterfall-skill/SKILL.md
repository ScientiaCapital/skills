---
name: "phone-verification-waterfall"
description: "Always-on callable lead pipeline for BDRs: HubSpot lead pull → Apollo phone lookup → Clay waterfall enrichment → HubSpot sync → callable queue. Ensures 50+ daily dials by maintaining verified phone inventory. Runs scheduled Mon & Wed 6:15 AM (between prospect-enrich 6:00 and prospect-refresh 6:30). Use when: 'verify phones', 'phone waterfall', 'callable leads', 'who can I call', 'dial list', 'always have someone to call', 'phone check', 'enrich phones'."
---

<objective>
Maintain a continuously refreshed inventory of callable leads with verified phone numbers. Automates the waterfall from HubSpot lead identification → Apollo phone verification → Clay enrichment (for Apollo misses) → HubSpot sync. Ensures Tim ALWAYS has 50+ verified dial prospects queued and ready, eliminating "nobody to call" downtime and maximizing daily dial velocity.

Built on: Lead lifecycle → phone verification → queue prioritization by ICP + intent signals.
</objective>

<quick_start>
**Standalone run (manual trigger):**
"verify phones" or "phone waterfall" or "callable leads" or "who can I call" → pulls all HubSpot leads missing phones → enriches via Apollo + Clay → writes back to HubSpot → outputs sortable callable queue

**Scheduled run:**
Every Monday & Wednesday 6:15 AM (between prospect-enrich 6:00 AM and prospect-refresh 6:30 AM) — keeps phone inventory fresh twice-weekly and allows newly refreshed leads to be phone-verified before daily calls

**Trigger phrases:**
- "verify phones"
- "phone waterfall"
- "callable leads"
- "who can I call"
- "dial list"
- "always have someone to call"
- "phone check"
- "enrich phones"
</quick_start>

<success_criteria>
- HubSpot lead pull returns 100+ contacts missing phones from all ICP verticals
- Apollo phone lookup succeeds for 40-50% of contacts (baseline)
- Clay waterfall fills 60-70% of remaining Apollo misses
- HubSpot phone field updated for 70%+ of missing numbers
- Final callable queue contains 50+ contacts sorted by ICP score + intent
- Zero contacts belong to customers (lifecycle_stage = 'customer') — Golden Rules block them
- Zero contacts owned by Account Executives (Lex, Phil, Ron, Anthony) — no AE lead theft
- Zero channel partners or existing device owners included
- Execution time under 8 minutes (HubSpot → Apollo → Clay → sync)
</success_criteria>

<workflow>

## Pipeline Stages

```
STAGE 1: PULL LEADS          STAGE 2: APOLLO PHONE      STAGE 3: CLAY WATERFALL    STAGE 4: HUBSPOT SYNC    STAGE 5: CALLABLE QUEUE
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
HubSpot Query       →     Apollo People Match    →    Clay Enrichment       →   Update Phone Field   →    Prioritized CLI
phone = null/empty  →     (Name + Email + Org)   →    (Multiple Providers)  →   (API bulk update)    →    ICP Score Sort
lifecycle_stage     →     Return: Verified #     →    Return: Verified #    →   Mark: enriched_at    →    Intent Signals
!= 'customer'       →     Success Rate: 40-50%   →    Success Rate: 30-40%  →   (Contact & Company) →    Output: CSV + Chat
No Excluded Owner   →     (No cost)              →    (Find + Enrich)        →   Log completion       →    Time-to-dial: <5s
Golden Rules Pass   →                            →                          →                        →
```

## Stage 1: Pull Leads Needing Phones

**HubSpot Query:**
```
Criteria (ALL must match):
- phone IS NULL OR phone = '' (empty string)
- lifecyclestage != 'customer'
- NOT hubspot_owner_id IN (82625923, 423155215)
  (Exclude: Lex Evans, Phil Sanders)
- NOT (hubspot_owner_id LIKE 'Ron%' OR hubspot_owner_id LIKE 'Anthony%')
  (Exclude: Ron and Anthony HubSpot owner IDs pending verification — use name-based matching as fallback until IDs confirmed)

Golden Rules Hard Gate (SKIP if ANY match):
- first_conversion contains ['Pearl', 'setup', 'Connect', 'signup']
  (Existing product engagers — not cold prospects)
- company.device_count >= 1
  (Already owns equipment — likely existing relationship)
- is_channel = true
  (Channel partners excluded)
- engagement_overview contains ['Pearl', 'trial', 'demo', 'customer']
  (Existing touchpoints)
```

**Output:** Unsorted list of 100+ contacts with:
- contact_id (HubSpot)
- first_name, last_name
- email (primary business email)
- company_name
- hs_job_title
- hubspot_owner_id, hubspot_owner_name
- company.industry, company.num_employees, company.hs_lead_status
- first_conversion (for Golden Rules check)

**Tool:** `hubspot_search_contacts` with filters applied

</Stage 1>

## Stage 2: Apollo Phone Lookup

**For each contact from Stage 1, run in parallel batches:**

```
Input:  contact_id, first_name, last_name, email, company_name
        ↓
apollo_people_match(
  first_name: "{first_name}",
  last_name: "{last_name}",
  email: "{email}",
  organization_name: "{company_name}",
  domain: "{company_domain}",
  reveal_personal_emails: false
)
        ↓
Output: phone (mobile_phone or corporate_phone, verified)
        ↓
Match rate: 40-50% success (Apollo baseline)
        ↓
NO COST — Apollo is included free
```

**Logic:**
- Apollo returns mobile_phone or corporate_phone (both acceptable for dial)
- If phone returned: tag contact `apollo_phone_source = true`
- If no phone: move to Stage 3 (Clay waterfall)
- Keep all results for final merge

**Tool:** `apollo_people_match` (batch parallel)

</Stage 2>

## Stage 3: Clay Waterfall Enrichment

**For contacts where Apollo returned NO phone, use Clay:**

**Option A: Company-level enrichment (recommended for speed)**
```
find-and-enrich-contacts-at-company(
  companyIdentifier: "{company_domain}",
  contactFilters: {
    job_title_keywords: extracted from hs_job_title,
    locations: optional if available
  },
  dataPoints: {
    contactDataPoints: [
      { type: "Email" },
      { type: "Summarize Work History" }
    ]
  }
)
```

Then for contacts found, run `add-contact-data-points` to enrich phones:
```
add-contact-data-points(
  taskId: "{from find-and-enrich response}",
  dataPoints: [
    { type: "Custom", customDataPoint: "phone number from multiple providers" }
  ],
  entityIds: [extracted contact IDs]
)
```

**Option B: Direct contact enrichment (if company approach yields few)**
```
find-and-enrich-list-of-contacts(
  contactIdentifiers: [
    {
      contactName: "{first_name} {last_name}",
      companyIdentifier: "{company_domain}"
    }
  ],
  dataPoints: {
    contactDataPoints: [
      { type: "Custom", customDataPoint: "verified phone number" }
    ]
  }
)
```

**Expected yield:**
- 30-40% of Apollo misses will get phones via Clay
- Combined success rate: 40-50% (Apollo) + 30-40% of remainder (Clay) ≈ 65-70% total

**Cost:** Clay credits consumed (monitor spend against monthly allocation)

**Tool:** `find-and-enrich-contacts-at-company` or `find-and-enrich-list-of-contacts`

</Stage 3>

## Stage 4: HubSpot Sync

**For all contacts with verified phones (Apollo + Clay combined):**

```
Batch update HubSpot contacts:
For each contact:
  UPDATE contact {contact_id}
  SET:
    phone = "{verified_phone}"
    phone_source = "apollo" OR "clay" (track origin)
    phone_verified_at = NOW()
    phone_waterfall_pass = true

Log event to company:
  ADD ACTIVITY: "Phone verified via Apollo/Clay waterfall"
  (Creates audit trail for Sales)
```

**Sync strategy:**
- Use HubSpot API in batches (500 contacts per batch)
- Tag with `phone_source` (apollo, clay, manual)
- Tag with `phone_verified_at` timestamp
- Log completion to deal/company object if linked

**Tool:** HubSpot REST API (contacts batch update) via `hubspot_contacts_update` or direct HTTP

</Stage 4>

## Stage 5: Callable Queue & Prioritization

**Build final output sorted by:**

1. **ICP Vertical Score (primary):**
   ```
   Higher Ed ..................... 90
   Courts/Legal ................... 85
   Government ..................... 80
   Corporate AV ................... 80
   Healthcare ..................... 75
   Houses of Worship .............. 70
   K-12 Schools ................... 65
   ```

2. **Intent Signals (secondary):**
   - Hiring active AV/IT roles: +15 points
   - Recent facility expansion news: +10 points
   - Tech stack shows obsolete AV (Extron, Matrox replacement signal): +12 points
   - Published RFP or procurement event: +10 points
   - Website mentions studio/control room/broadcast: +8 points
   - Recent funding/acquisition: +5 points

3. **Engagement Recency (tertiary):**
   - Touched within 30 days: top of queue
   - Touched 31-60 days: middle
   - No recent touch: bottom (but still callable)

**Final Callable Queue Format:**

```
═══════════════════════════════════════════════════════════════════════════════
CALLABLE QUEUE — Phone Waterfall Results
Generated: {timestamp} | Success Rate: {70-80%}
═══════════════════════════════════════════════════════════════════════════════

SUMMARY:
Total Leads Pulled:        {N}
Apollo Matches:            {X} ({X%})
Clay Enrichments:          {Y} ({Y%})
Total Verified Phones:     {X+Y} ({(X+Y)%})
HubSpot Updated:           {X+Y}

READY TO DIAL (sorted ICP score + intent):

 #  │ NAME              │ TITLE            │ COMPANY           │ PHONE        │ ICP  │ VERTICAL     │ INTENT SIGNAL
────┼──────────────────┼──────────────────┼──────────────────┼──────────────┼──────┼──────────────┼─────────────────
  1 │ Jane Smith       │ VP IT/AV         │ Stanford Univ    │ (650)xxx-xxx │ 93   │ Higher Ed    │ New AV role + hiring
  2 │ Mike Johnson     │ Dir Technology   │ Federal Courts   │ (202)xxx-xxx │ 87   │ Courts/Legal │ Extron aging out
  3 │ Sarah Chen       │ Manager IT       │ UCSF Medical     │ (415)xxx-xxx │ 78   │ Healthcare   │ Facility upgrade
  4 │ David Lee        │ AV Manager       │ Cisco Corp       │ (408)xxx-xxx │ 82   │ Corp AV      │ Meeting room reno
  5 │ ...              │ ...              │ ...              │ ...          │ ...  │ ...          │ ...

═══════════════════════════════════════════════════════════════════════════════
DIALER QUICK LINKS:
- Download CSV:        [queue.csv]
- Import to Dialpad:   [sync button]
- Import to Aircall:   [sync button]
- By Company:          [grouped view]
- By Vertical:         [vertical view]

NEXT STEPS:
1. Sort queue by your preferred intent weight (default: ICP score)
2. Import to your dialpad tool
3. Dial 50+ per day, log outcomes, let Sales Engagement cadences trigger

═══════════════════════════════════════════════════════════════════════════════
```

**Output formats:**
- **Chat:** Rich formatted table (above) with top 10-20 by ICP score
- **CSV download:** Full queue with all data for import to dialpad/Aircall
- **By Vertical:** Secondary view grouped by industry for vertical hunting
- **Integration:** Link to import queue to Dialpad, Aircall, or sales engagement tool

**Tool:** Assemble from Stage 4 output, sort, format, and present

</Stage 5>

## Reply-Scan Integration

**Automated queuing from reply scans (10 AM, 1 PM, 3 PM):**

When reply scans discover new leads with missing phone numbers:
- These leads are automatically queued for the next scheduled phone waterfall run (Monday or Wednesday 6:15 AM)
- Standard enrichment workflow applies (Apollo → Clay waterfall → HubSpot sync)

**Urgent high-ICP lead handling:**
- For leads scoring 80+ ICP and deemed high-priority prospects, trigger an immediate single-contact Apollo lookup
- If Apollo succeeds, append phone to contact record and add to current day's dial queue
- If Apollo fails, hold for next scheduled waterfall run (standard workflow)

**Logic:**
```
IF reply_scan_found_lead AND lead.phone IS NULL
  IF lead.icp_score >= 80 AND lead.priority = 'high'
    → TRIGGER immediate apollo_people_match(lead)
    → IF success: append phone, mark urgent_dial = true
    → ELSE: queue for next waterfall run
  ELSE
    → Queue for next scheduled waterfall (Mon or Wed 6:15 AM)
```

This ensures urgent prospects get callable status same-day while maintaining efficiency of batch enrichment for standard leads.

## Scheduled Automation

**Cron:** Every Monday & Wednesday 6:15 AM (UTC, or Tim's local timezone)

```
MONDAY MORNING SEQUENCE:
6:00 AM  → bdr-v3-prospect-enrich (refresh prospect company data)
6:15 AM  → phone-verification-waterfall-skill (verify phones on refreshed data)
6:30 AM  → bdr-v3-prospect-refresh (refresh deal velocity metrics)

WEDNESDAY MORNING SEQUENCE (mid-week refresh):
6:00 AM  → bdr-v3-prospect-enrich (refresh prospect company data)
6:15 AM  → bdr-v3-phone-waterfall-midweek (verify phones on mid-week refreshed data)
6:30 AM  → bdr-v3-prospect-refresh (refresh deal velocity metrics)
```

**Why 6:15 AM Monday & Wednesday?**
- **Monday:** Sunday evening prospect research populates HubSpot with new prospects; 6:00 AM enrich ensures firmographic data is current; 6:15 AM phone verification catches those prospects while fresh; 6:30 AM velocity refresh gives Tim complete picture before first calls
- **Wednesday:** Mid-week lead refresh captures newly added prospects from Tue-Wed research; ensures stable of callable leads remains 50+ through week; separate task (`bdr-v3-phone-waterfall-midweek`) allows independent scheduling and monitoring

**Operational notes:**
- If phone waterfall takes >8 min, send Slack alert (indicates API slowness or large backlog)
- Log success rate to dashboard (aim for 65%+ total verified)
- If Apple/Apollo API rate limits hit, queue and retry with exponential backoff
- On error: skip Clay enrichment and return Apollo-only results (better to have some phones than none)

</workflow>

<dependencies>
## Required MCP Tools

### Epiphan CRM (primary data source)
- `hubspot_search_contacts` — Pull leads with phone = null, apply Golden Rules filters
- `hubspot_get_contact` — Retrieve full contact details if needed
- `identify_company` — Check company against Epiphan customer database (device_count, channel flag)

### Apollo (phone verification stage 2)
- `apollo_people_match` — Look up person by name + email + company, return verified phone
- *(No cost — included in Apollo plan)*

### Clay (phone waterfall stage 3)
- `find-and-enrich-contacts-at-company` — Batch enrich by company + job title filters
- `add-contact-data-points` — Add custom phone data point to enrich results
- `find-and-enrich-list-of-contacts` — Enrich specific contacts by name + company
- `get-existing-search` — Poll for async enrichment results
- *(Costs Clay credits — monitor spend)*

### HubSpot API (sync stage 4)
- `hubspot_contacts_update` (batch via REST API) — Write verified phones back to HubSpot
- Or native HubSpot bulk import if preferred

## Sibling Skills & Related Tasks Referenced
- `prospect-research-to-cadence-skill` — Lead quality gates, Golden Rules filter, ICP scoring
- `sales-revenue-skill` — ICP vertical definitions, intent signal weighting
- `hubspot-revops-skill` — HubSpot bulk operations, contact filtering patterns, owner ID mapping

## Upstream & Downstream Scheduled Tasks
- `bdr-v3-prospect-enrich` — Monday 6:00 AM firmographic refresh (runs before phone waterfall)
- `bdr-v3-phone-waterfall-midweek` — Wednesday 6:15 AM mid-week phone verification run (NEW)
- `bdr-v3-prospect-refresh` — Monday 6:30 AM velocity refresh (runs after phone waterfall)

## External Dependencies
- **HubSpot API:** Contact search + bulk update
- **Apollo API:** People match (no additional cost)
- **Clay API:** Waterfall enrichment (requires active subscription + available credits)
- **Dialpad/Aircall API:** Optional integration for direct dial queue sync

## Estimated Monthly Cost
- **Apollo:** $0 (included)
- **Clay:** $150-300 depending on contacts enriched (monitor waterfall stage)
- **HubSpot:** Already in use
- **Total variable:** ~$200-300/month (Clay credits)

</dependencies>

<scheduled_automation>

**Task IDs:**
- `bdr-v3-phone-waterfall` (Monday 6:15 AM run)
- `bdr-v3-phone-waterfall-midweek` (Wednesday 6:15 AM run)

**Trigger:** Recurring, every Monday & Wednesday at 6:15 AM (user's local timezone)

**Slack Notification on Completion:**
```
✅ Phone Waterfall Complete (Mon 6:15 AM)
   Pulled:       {N} leads
   Verified:     {X+Y} phones ({%})
   HubSpot Sync: ✓
   Queue:        Ready to dial
   Leads/hour:   {rate}
```

**On Error:**
```
⚠️ Phone Waterfall Partial (Mon 6:15 AM)
   Apollo completed ({X%})
   Clay failing — check credits
   Manual action: Continue with Apollo-only queue
```

</scheduled_automation>

---

## Reference: Golden Rules Filter

**These are hard gates — if ANY condition matches, skip the contact entirely:**

| Condition | Value | Action |
|-----------|-------|--------|
| `lifecyclestage` | 'customer' | SKIP |
| `first_conversion` | contains 'Pearl' OR 'setup' OR 'Connect' | SKIP |
| Company `device_count` | >= 1 | SKIP |
| Company `is_channel` | true | SKIP |
| `hubspot_owner_id` | 82625923, 423155215 | SKIP (Lex Evans, Phil Sanders) |
| `hubspot_owner_id` | Matches 'Ron\*' OR 'Anthony\*' | SKIP (Ron & Anthony — pending ID verification) |

**Rationale:**
- Customers are in a different sales motion (success, upsell, retention)
- Product engagers are warm leads for a different sequence
- Device owners are existing relationships or renewals
- Channel partners have their own sales process
- AE-owned leads belong to Account Executives (no BDR lead theft)

</Golden Rules>

---

## Example: Phone Waterfall in Action

**Monday 6:15 AM kick-off:**

```
INPUT: HubSpot query finds 247 contacts with phone = null and meeting Golden Rules

APOLLO STAGE (2 min):
  Batched 247 into 5 parallel requests
  Success: 118 phones verified (47.8%)
  → Synced 118 to HubSpot immediately
  → Remaining: 129 needs Clay

CLAY STAGE (4 min):
  Batched 129 into company+title groups
  Ran find-and-enrich-contacts-at-company for each company
  Waterfall returned phones for 41 additional contacts (31.8%)
  → Synced 41 to HubSpot
  → Final miss: 88 (no phone found)

SYNC STAGE (30 sec):
  HubSpot batch updated 159 contacts (118 Apollo + 41 Clay)
  Tagged phone_source = 'apollo' or 'clay'
  Created audit trail entries

QUEUE STAGE (30 sec):
  Sorted 159 by ICP score (Higher Ed first, K-12 last)
  Boosted intent signal scores (hiring, facility expansion)
  Output: Callable queue ready for 50+ dials

TOTAL TIME: 7 minutes 30 seconds
CALLABLE LEADS: 159 verified phones
SUCCESS RATE: 64.4% (159/247)
```

Tim's view at 6:15 AM:
```
✅ Phone Waterfall Complete
   159 leads verified and ready to call
   Top prospect: Jane Smith (Stanford, VP IT, 93 ICP) — call now
   Your dial list is queued in Dialpad
```

