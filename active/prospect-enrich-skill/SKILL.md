---
name: prospect-enrich
description: "Mon-Fri 6:00 AM — Daily batch enrichment of phoneless contacts using Apollo + Clay. DEMO REQUEST first, then ATL-first priority. Golden Rules + ATL/BTL Classification Gate. Feeds into phone-waterfall and prospect-refresh."
schedule: "0 6 * * 1-5"
timezone: "America/New_York"
---

# Prospect Enrich Skill

<objective>
Enrich HubSpot contacts missing phone numbers using Apollo and Clay APIs. Apply DEMO REQUEST priority (hand-raisers first), then ATL-first prioritization and Golden Rules (exclude customers, channel, device owners, AE-owned contacts). Output branded HTML report sorted by tier and ready for phone-waterfall and prospect-refresh tasks.
</objective>

<quick_start>
**Trigger:** Mon-Fri 6:00 AM ET
**Manual Trigger:** "Run prospect enrich" or "Enrich phoneless contacts"
**Dependencies:** Requires HubSpot portal 21530819 access, Apollo credits, Clay credits
**Output:** Branded HTML report + enriched contacts synced to HubSpot with tier tags
</quick_start>

<success_criteria>
- [ ] Query HubSpot for all contacts with phone = null (geo: USA/Canada only)
- [ ] Filter out Golden Rule exclusions (customers, channel, device owners, AE-owned, product-page engagers)
- [ ] Identify DEMO REQUEST contacts (first_conversion contains demo/pricing keywords) — enrich FIRST
- [ ] Classify remaining by ATL/BTL tier (see CLAUDE.md ATL/BTL Decision-Maker rules)
- [ ] Batch enrich via Apollo (apollo_people_bulk_match or apollo:enrich-lead)
- [ ] For Apollo misses: send to Clay waterfall (find-and-enrich-contacts-at-company)
- [ ] Sync enriched phone numbers back to HubSpot with tier tags
- [ ] Include company enrichment (domain, revenue, headcount) for ATL-tier contacts
- [ ] Generate branded HTML report with tier sections and Epiphan colors
- [ ] Report: total contacts processed, phone match rate %, ATL/BTL breakdown, credits used
</success_criteria>

<workflow>

## Stage 1: Pull Phoneless Contacts from HubSpot

**MCP Tool:** `search_crm_objects` (HubSpot)

```
objectType: "contacts"
filterGroups: [{
  filters: [
    { propertyName: "phone", operator: "NOT_HAS_PROPERTY" },
    { propertyName: "hs_lead_status", operator: "IN", values: ["Subscriber", "Qualified Lead", "Inbound Lead", "Marketing Qualified Lead", "Sales Qualified Lead"] }
  ]
}]
properties: [
  "firstname", "lastname", "email", "company", "jobtitle", "phone",
  "first_conversion", "lifecyclestage", "hubspot_owner_id",
  "device_count", "engagement_overview", "is_channel"
]
limit: 100
```

**Output:** List of contacts with name, email, company, title, first_conversion; no phone.

---

## Stage 2: Apply Golden Rules Filter

**Golden Rules (Hard Exclusions — apply BEFORE enrichment to save credits):**

- **EXCLUDE:** `lifecyclestage = 'customer'` (existing customer)
- **EXCLUDE:** `device_count >= 1` (device owner)
- **EXCLUDE:** `engagement_overview` contains product usage (product-only engager)
- **EXCLUDE:** `is_channel = true` (channel partner)
- **EXCLUDE:** `hubspot_owner_id IN (82625923, 423155215)` — AE-owned contacts (do not prospect)
- **EXCLUDE:** `first_conversion ILIKE '%setup%'` — product setup forms only (not sales interest)
- **Keep:** Geo filter to USA/Canada only

**⚠️ CRITICAL — DO NOT EXCLUDE these first_conversion values:**
- `'Pearl family demo'`, `'Demo signup'`, `'demo request'`
- `'General contact us'`, `'pricing'`
- `'Pearl'`, `'Connect'`, `'signup'`

These are **HIGH-INTENT demo requests** — active hand-raisers. Tag them as **DEMO REQUEST** tier and enrich BEFORE all other tiers.

**Output:** Filtered list (typically 60-70% of input after Golden Rules)

---

## Stage 3: ATL/BTL Classification Gate (MANDATORY)

**Apply BEFORE enrichment to set processing priority order.**

**Reference:** CLAUDE.md § ATL/BTL Decision-Maker Classification v1.0

### Tier 1: DEMO REQUEST (Enrich FIRST — Highest Priority)
Any contact whose `first_conversion` contains:
- `'Demo signup'`, `'Pearl family demo'`, `'demo request'`
- `'General contact us'`, `'pricing'`

These are active hand-raisers — enrich immediately **regardless of job title**.

### Tier 2: ATL (Enrich Second — Budget Authority)
Chief (CIO, CTO, CFO, COO) • Vice President (VP, AVP, SVP, EVP) • President • Provost • Vice Provost • Superintendent • Director (of IT, Technology, Facilities, Academic Technology, Procurement, Materials Mgmt, Medical Education, Court Administration) • Dean • Court Administrator • Clerk of Court (Federal) • City Manager • County Manager • Senior Pastor • Executive Pastor

### Tier 3: GRAY (Enrich Third — Flag for Tim's Review)
- Manager (AV/Facilities/IT) — ATL only if reports to Director+ AND has delegated budget authority >$25K
- Department Chair — ATL at small institutions; BTL at large universities
- Director of Educational Technology — depends on reporting line (Provost = ATL; IT VP = maybe BTL)
- Program Director — ATL only if department-level budget holder; BTL if coordination role

### Tier 4: BTL (Enrich Last — Deprioritize)
Technician • Specialist • Coordinator • Support • Administrator (Systems/Network/Database) • Engineer (AV/Network/Systems) • Operator • Instructor/Professor/Faculty • Designer (Learning/Instructional/Graphic) • Assistant • Clerk (non-Court Admin) • Volunteer • Intern • Student • Resident • Help Desk

### NEVER ENRICH (Hard Skip — Do NOT Spend Apollo/Clay Credits)
Warehouse Manager • Network Manager • Systems Administrator • AV Technician • Graphic Design Instructor • Program Administrator • Web Designer • Classroom Support • Lab Coordinator • Maintenance • Building Engineer • Multimedia Services Manager • Video Production Specialist • Streaming Crew

**Classification Logic:**
```
if first_conversion matches DEMO_KEYWORDS:
  tier = "DEMO REQUEST"  # Enrich first, regardless of title
elif title in NEVER_ENRICH:
  tier = "NEVER"  # Hard skip — do not spend credits
elif title in ATL:
  tier = "ATL"
elif title in GRAY:
  tier = "GRAY"  # Flag for Tim's manual review
else:
  tier = "BTL"

# Processing order: DEMO REQUEST → ATL → GRAY → BTL (skip NEVER)
```

---

## Stage 4: Batch Enrich via Apollo

**Process contacts in tier priority order: DEMO REQUEST → ATL → GRAY → BTL**

**MCP Tool:** `apollo_people_bulk_match` (or `apollo:enrich-lead` skill)

```
details: [
  {
    id: contact.id,
    first_name: contact.firstname,
    last_name: contact.lastname,
    email: contact.email,
    organization_name: contact.company,
    domain: extract domain from email or company website
  }
  ... (up to 10 per batch)
]
reveal_personal_emails: false
```

**Expected Enrichment:**
- phone (direct, mobile, corporate)
- current_role_min_months_since_start_date (tenure for seniority signal)
- person_seniorities (c_suite, vp, director, manager, etc.)

**Match Rate Target:** 65-75% of batch should get phone.

---

## Stage 5: Waterfall Misses to Clay

**For Apollo non-matches:** Send to Clay `find-and-enrich-contacts-at-company`

**MCP Tool:** `find-and-enrich-contacts-at-company`

```
companyIdentifier: contact.company (domain preferred)
contactFilters: {
  job_title_keywords: [extract broad role from contact.jobtitle],
  locations: ["United States", "Canada"]
}
dataPoints: {
  contactDataPoints: [{ type: "Email" }],
  companyDataPoints: [{ type: "Latest Funding" }, { type: "Tech Stack" }]
}
```

**Clay Enrichment:** Return matching contacts at company with email + company data.

---

## Stage 6: Sync Back to HubSpot

**For each enriched contact:**

1. **Update HubSpot contact** via `manage_crm_objects` (updateRequest):
   - phone (direct or mobile from Apollo/Clay)
   - hs_analytics_num_page_views (engagement signal)
   - Tag in notes: `[DEMO REQUEST]`, `[ATL]`, `[GRAY]`, or `[BTL]`

2. **Enrich company data** if not already set:
   - MCP Tool: `apollo_organizations_enrich`
   - Update HubSpot company: revenue, headcount, founded_date

---

## Stage 7: Generate Branded HTML Report

**Output:** HTML file saved to workspace as `bdr-v3-prospect-enrich-YYYY-MM-DD.html`

**Styling:**
- Epiphan brand colors: `#1a1a2e` (dark), `#e94560` (accent), `#0f3460` (primary)
- Clean, professional layout
- Mobile-responsive design

**Report Sections:**

**Summary Metrics Table:**
| Metric | Value |
|--------|-------|
| Total phoneless pool | X |
| After Golden Rules filter | Y (Z% removed) |
| DEMO REQUEST tier | D |
| ATL tier | A |
| GRAY tier | G |
| BTL tier | B |
| NEVER tier (skipped) | N |
| Phones found (Apollo) | PA (PA% of processed) |
| Phones found (Clay) | PC (PC% of non-Apollo) |
| Total enriched | PA + PC (success %) |
| Apollo credits used | C |

**Section 1: DEMO REQUEST Contacts (Green highlight)**
Sorted first — these are hand-raisers with highest conversion potential.

| Contact | Email | Title | Company | Phone | First Conversion | Revenue | Action |
|---------|-------|-------|---------|-------|-----------------|---------|--------|
| ... | ... | ... | ... | ... | Demo signup | ... | Priority dial |

**Section 2: ATL Contacts (Blue highlight)**
Budget decision-makers — second priority.

**Section 3: GRAY Contacts (Yellow highlight)**
Flagged for Tim's manual review — budget authority uncertain.

**Section 4: BTL Contacts (Gray)**
No budget authority — lowest enrichment priority.

**Section 5: NEVER ENRICH Skipped List**
Contacts that matched NEVER ENRICH titles — credits NOT spent.

**Section 6: Key Insights + Recommended Actions**
- Top companies by ATL density
- Highest-value DEMO REQUESTs
- Recommended next steps

**Next Steps:** Results feed into `phone-verification-waterfall-skill` for phoneless re-check and `prospect-refresh-skill` for net-new ICP search.

</workflow>

---

## Skill Metadata

**Version:** 1.1
**Last Updated:** 2026-03-19
**Author:** Tim Kipper
**Status:** Production
**Integration:** HubSpot (portal 21530819) + Apollo + Clay
**Tier:** P1 (Core BDR Automation)
**Triggers:** Scheduled (Mon-Fri 6:00 AM) + Manual ("Run prospect enrich")
**Changelog:**
- v1.1 (2026-03-19): Added DEMO REQUEST tier (highest priority), AE owner exclusion (IDs 82625923, 423155215), first_conversion filter logic, HTML report output with Epiphan brand colors. Schedule expanded Mon-Fri (was Mon only).
- v1.0 (2026-03-19): Initial release with ATL/BTL classification, Apollo + Clay waterfall.
