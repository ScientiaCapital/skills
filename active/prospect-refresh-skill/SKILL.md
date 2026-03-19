---
name: prospect-refresh
description: "Monday ICP prospect search + Gmail draft creation. Finds NET NEW prospects across all verticals using Apollo."
schedule: "0 6 30 * * 1"
timezone: "America/New_York"
---

# Prospect Refresh Skill

<objective>
Execute weekly net-new prospect search across all ICP verticals (Higher Ed, Courts, Gov, Corporate AV, Healthcare, Houses of Worship, K-12) using Apollo's People API. Deduplicate against existing HubSpot contacts. Enrich top 30 results. Create personalized Gmail drafts for each prospect. Output HTML report with drill-down links to HubSpot and Apollo records.
</objective>

<quick_start>
**Trigger:** Monday 6:30 AM ET (runs after prospect-enrich)  
**Manual Trigger:** "Run prospect refresh" or "Search new ICP prospects"  
**Dependencies:** Requires HubSpot portal 21530819, Apollo credits, Gmail tkipper@epiphan.com  
**Output:** 30 net-new prospects + 30 Gmail draft emails + HTML report with HubSpot links
</quick_start>

<success_criteria>
- [ ] Query Apollo for ICP title + vertical combinations (ATL-first targeting)
- [ ] Deduplicate against HubSpot contacts (check email, company domain, name)
- [ ] Filter Golden Rules (exclude customers, channel, device owners, etc.)
- [ ] Enrich top 30: company revenue, headcount, funding, tech stack
- [ ] Create Gmail draft for each prospect (personalized template per vertical)
- [ ] Generate HTML report with sortable columns: name, title, company, vertical, ATL/BTL, links to HubSpot/Apollo
- [ ] Include ATL/BTL tier badges and vertical ICP scores
- [ ] Report: total prospects found, dedupe rate, ATL %, top 5 companies by headcount
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

## Stage 3: Deduplicate Against HubSpot

**MCP Tool:** `search_crm_objects` (HubSpot)

**For each Apollo result, check:**

```
filterGroups: [
  {
    filters: [
      { propertyName: "email", operator: "EQ", value: apollo_result.email }
    ]
  },
  {
    filters: [
      { propertyName: "company", operator: "CONTAINS_TOKEN", value: apollo_result.organization_name }
    ]
  }
]
```

**Exclusion Logic:**
- If email exists in HubSpot → SKIP
- If company + similar name exists → SKIP
- If domain in blacklist (channel, device owners, etc.) → SKIP
- Otherwise → KEEP

**Expected Dedup Rate:** 40-60% of Apollo results removed (existing contacts)

---

## Stage 4: Apply Golden Rules + ATL/BTL Filter

**Golden Rules (Hard Exclusions):**
- Skip if company in crm_customers (customer check)
- Skip if contact tagged "Channel Partner"
- Skip if job title contains BTL keywords: Technician, Support, Intern, Admin, Engineer (non-director), Operator
- Skip if title in NEVER ATL list (Warehouse Manager, Network Admin, AV Tech, etc.)
- Keep: USA/Canada only, public company or funded (exclude bootstraps <$1M)

**ATL/BTL Classification (per CLAUDE.md):**

**ATL Tier (Always Prospect):**
- Chief (C-suite), VP, Director (IT/Tech/Facilities), Provost, Dean
- Court Administrator, Clerk of Court, City Manager, Senior Pastor

**GRAY Tier (Budget Authority >$25K Required):**
- Manager roles with Director+ reporting line
- Department Chair (context-dependent)
- Program Director (dept-level budget only)

**BTL Tier (Skip for ATL-first targeting):**
- Technician, Specialist, Coordinator, Support, Administrator
- Engineer (non-director), Operator, Instructor, Designer, Assistant
- Help Desk, Intern, Volunteer

**Output after filtering:** Typically 50-60% of dedup results (15-18 prospects per vertical)

---

## Stage 5: Enrich Top 30 Results

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

## Stage 6: Create Gmail Drafts (One per Prospect)

**MCP Tool:** `gmail_create_draft`

**Per-Vertical Email Templates (Personalized):**

**Template A — Higher Ed (ICP 90):**
```
To: prospect.email
Subject: Epiphan + [UNIVERSITY_NAME]: Hybrid Learning Infrastructure for [SCHOOL_TYPE]

Body:
Hi [FIRST_NAME],

I was researching [UNIVERSITY_NAME]'s commitment to hybrid learning and asynchronous instruction—I noticed the shift in your academic technology strategy.

We work with schools like [REFERENCE_UNIV] to solve a specific challenge: instructor burnout from manual video streaming and recording.

[COMPANY_NAME] provides:
- Live lecture capture (no manual setup)
- Auto-recordings to your LMS
- Multi-platform distribution (Zoom, Teams, Canvas)

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
- Choose template based on prospect's vertical
- Substitute [BRACKETS] with actual prospect/company data
- Do NOT send—leave as draft for manual review
- Tag draft with prospect's ATL/BTL tier + vertical ICP score

**MCP Tool Parameters:**
```
to: prospect.email
subject: [PERSONALIZED_PER_VERTICAL]
body: [TEMPLATE_WITH_SUBSTITUTIONS]
contentType: "text/plain"
```

---

## Stage 7: Generate HTML Report

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

## Stage 8: Load into HubSpot (Optional Next Step)

**Note:** This skill outputs drafts + report. **Sequence Load Skill** runs 45 min later (7:15 AM) to:
- Create HubSpot contacts from top 30
- Validate phone numbers
- Add to Apollo outreach sequence

</workflow>

---

## Skill Metadata

**Version:** 1.0  
**Last Updated:** 2026-03-19  
**Author:** Tim Kipper  
**Status:** Production  
**Integration:** Apollo + HubSpot (portal 21530819) + Gmail  
**Tier:** P1 (Core BDR Automation)  
**Triggers:** Scheduled (Monday 6:30 AM) + Manual ("Run prospect refresh")  
**Dependencies:** prospect-enrich (runs 6:00 AM), feeds into sequence-load (7:15 AM)
