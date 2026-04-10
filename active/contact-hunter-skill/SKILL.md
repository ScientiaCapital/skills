---
name: contact-hunter-skill
description: Find and enrich contact information for specific people or companies using HubSpot, Apollo, and Clay MCP tools. Applies Golden Rules qualification gates before returning results. Use when you need to find contacts at target accounts with verified emails and phones for BDR outreach.
---

# Contact Hunter

<objective>
Find, enrich, and qualify contact information for specific people or companies using live MCP tool calls to HubSpot, Apollo, and Clay. Returns contact cards with email, phone, title, ATL/BTL tier, and suppression status — ready for the BDR dial list or sequence load.
</objective>

<quick_start>
**Trigger:** "Find the VP of Sales at [Company]" or "Get contact info for [Name] at [Company]" or "Hunt contacts at [Company]"
**Input:** Person name, company, job title, location, or LinkedIn URL
**Output:** Qualified contact cards with email, phone, LinkedIn, ATL/BTL tier, suppression status, and HubSpot record link
**MCP Tools:** `mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts`, `mcp__claude_ai_Apollo_io__apollo_contacts_search`, `mcp__claude_ai_Clay__find-and-enrich-contacts-at-company`
</quick_start>

<success_criteria>
- [ ] Golden Rules filter applied — customers, channel partners, AE-owned <90d, non-NA excluded
- [ ] HubSpot searched first (check if contact already exists)
- [ ] Apollo waterfall run if HubSpot returns no result
- [ ] Clay enrichment run for phone/LinkedIn if Apollo has email only
- [ ] ATL/BTL tier assigned per title keyword
- [ ] bdr_suppression_until checked — suppressed contacts excluded
- [ ] Contact card output with HubSpot record URL
</success_criteria>

<workflow>

## Stage G — Golden Rules Gate (run BEFORE any search)

Disqualify any contact or company matching these criteria before spending enrichment credits:

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

If contact found in HubSpot → jump to Stage 3 (ATL/BTL classification).
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

## Stage 3: ATL/BTL Classification

Assign tier using CLAUDE.md ATL/BTL keyword rules:
- **ATL**: Chief, VP, President, Director, Dean, Superintendent, Provost → prioritize
- **NEVER ATL**: AV Technician, Network Manager, Systems Administrator → skip
- **GRAY**: Manager + reports to Director + budget >$25K → surface for manual review

## Stage 4: Suppression Check

Before including any contact in output:
- Check `bdr_suppression_until` property
- **EXCLUDE** if `bdr_suppression_until` IS SET AND > TODAY
- **INCLUDE** if property IS NOT SET or date < TODAY

## Stage 5: Output Contact Cards

For each contact that passed Stages G–4, output:

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

---

**Compliance:** All data sourced from HubSpot (existing CRM records), Apollo (public professional data), or Clay (verified enrichment). No scraping. Follow CAN-SPAM for outreach.
   3. Use title filter: "VP of Engineering"
   4. Location: "San Francisco Bay Area"

   Google:
   1. "John Smith" "VP of Engineering" "Acme Corp"
   2. "John Smith" "Acme Corp" email
   3. site:linkedin.com/in "John Smith" "Acme"
   4. site:acme.com "John Smith"

   Company Website:
   1. Check: https://acme.com/about
   2. Check: https://acme.com/team
   3. Check: https://acme.com/leadership
   4. Check: https://acme.com/contact

   Email Pattern Guessing:
   Common patterns at acme.com:
   • john.smith@acme.com
   • john@acme.com
   • jsmith@acme.com
   • j.smith@acme.com
   • smithj@acme.com

   GitHub (for technical roles):
   • Search: "John Smith Acme"
   • Look for company in bio

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📝 DATA COLLECTION TEMPLATE
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Once you find the information, fill this template:

   Full Name: [First Last]
   Job Title: [Exact title]
   Company: [Company name]
   Email: [email@domain.com]
   Phone: [(xxx) xxx-xxxx]
   LinkedIn: [linkedin.com/in/username]
   Location: [City, State/Country]
   Department: [Engineering, Sales, etc.]

   Additional Info:
   • Reports to: [Manager name]
   • Team size: [Number]
   • Start date: [When they joined]
   • Previous companies: [List]
   • Education: [Degree, School]

   Data Sources:
   • [LinkedIn profile URL]
   • [Company website URL]
   • [Other sources]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ VERIFICATION STEPS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   1. Cross-reference multiple sources
   2. Check LinkedIn profile matches company
   3. Verify email format matches company pattern
   4. Validate phone number format
   5. Confirm job title is current
   6. Check for recent company changes

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ⚠️ COMPLIANCE & ETHICS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   • Only use publicly available information
   • Respect privacy and GDPR regulations
   • Don't scrape private databases
   • Honor do-not-contact preferences
   • Use for legitimate business purposes only
   • Keep CAN-SPAM compliance for cold outreach
   ```

5. **Organize Results**:

   **Individual Contact Card**:
   ```
   ┌─────────────────────────────────────────┐
   │ JOHN SMITH                              │
   │ VP of Engineering @ Acme Corp           │
   ├─────────────────────────────────────────┤
   │ 📧 john.smith@acme.com                  │
   │ 📱 (415) 555-0123                       │
   │ 💼 linkedin.com/in/johnsmith            │
   │ 📍 San Francisco, CA                    │
   ├─────────────────────────────────────────┤
   │ Department: Engineering                 │
   │ Reports to: Sarah Chen (CTO)            │
   │ Team size: ~45 engineers                │
   │ Tenure: 2+ years at Acme                │
   ├─────────────────────────────────────────┤
   │ 🔍 Sources:                             │
   │ • LinkedIn (verified)                   │
   │ • Company website                       │
   │ • Verified: 2024-01-15                  │
   └─────────────────────────────────────────┘
   ```

   **Bulk Results** (CSV/Excel format):
   ```csv
   Name,Title,Company,Email,Phone,LinkedIn,Location,Source,Verified
   John Smith,VP Engineering,Acme Corp,john.smith@acme.com,(415) 555-0123,linkedin.com/in/johnsmith,San Francisco,LinkedIn,2024-01-15
   Jane Doe,Director Marketing,Acme Corp,jane.doe@acme.com,(415) 555-0124,linkedin.com/in/janedoe,San Francisco,Company Website,2024-01-15
   ```

6. **Email Pattern Detection**:

   When searching company contacts, detect email patterns:
   ```
   🔍 DETECTED EMAIL PATTERN: Acme Corp

   Confirmed Emails Found:
   • john.smith@acme.com
   • sarah.chen@acme.com
   • michael.jones@acme.com

   Detected Pattern: firstname.lastname@acme.com

   Confidence: 95%

   Alternative Patterns (if primary fails):
   • firstname@acme.com
   • firstnamelastname@acme.com
   • f.lastname@acme.com

   To Verify Unknown Email:
   1. Use email verification tool
   2. Check for bounce/invalid
   3. Look for SMTP response
   4. Verify on LinkedIn
   ```

7. **Data Enrichment**:

   For existing contacts, enrich with:
   - Current job title
   - Company changes
   - Updated contact info
   - Social profiles
   - Company information
   - Reporting structure
   - Recent activity/posts

8. **Export Formats**:

   - **CSV**: For CRM import
   - **JSON**: For API integration
   - **vCard**: For contact managers
   - **Salesforce CSV**: Pre-formatted for SFDC
   - **HubSpot CSV**: Pre-formatted for HubSpot

## Search Strategies

**For Company Employees**:
```
site:linkedin.com/in "[Company Name]"
OR
site:[company-domain.com] "team" OR "about" OR "leadership"
```

**For Specific Roles**:
```
"[Job Title]" "[Company]" email
OR
"[Job Title]" site:linkedin.com "[Company]"
```

**For Email Validation**:
- Check company website for email format
- Use email verification services
- Look for pattern in existing emails
- Test with email finder tools

**For Phone Numbers**:
- Company website contact page
- LinkedIn profile (sometimes public)
- Professional directories
- Industry associations

## Example Triggers

- "Find the VP of Sales at Acme Corp"
- "Get contact info for John Smith at Microsoft"
- "Find engineering managers at Stripe"
- "Enrich this list of contacts with emails"
- "What's the email pattern at Google?"
- "Find the marketing team at HubSpot"

## Compliance Guidelines

**What's Allowed**:
- Publicly available information
- Business contact information
- LinkedIn public profiles
- Company websites
- Professional directories
- Published contact lists

**What's NOT Allowed**:
- Scraping private databases
- Purchasing questionable contact lists
- Bypassing email verification
- Ignoring opt-out requests
- Violating GDPR/CCPA
- Harassing contacts

**Best Practices**:
- Always cite data sources
- Respect privacy preferences
- Use for legitimate business purposes
- Keep data up to date
- Provide opt-out mechanisms
- Follow CAN-SPAM for outreach
- Comply with data protection laws

## Output Quality

Ensure contact information:
- Includes all available fields
- Cites data sources
- Has confidence/verification level
- Follows data privacy laws
- Is formatted consistently
- Includes contact preferences
- Notes data freshness
- Provides context (tenure, role, team)
- Flags any uncertainties
- Suggests verification steps

Provide structured, ethically-sourced contact information with full transparency.

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
