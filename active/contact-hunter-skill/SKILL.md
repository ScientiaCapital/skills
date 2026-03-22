---
name: contact-hunter-skill
description: Search and extract contact information for people or companies including names, phone numbers, emails, job titles, and LinkedIn profiles. Aggregates data from multiple sources and provides enriched contact details. Use when users need to find contact information, build prospect lists, or enrich existing contact data.
---

# Contact Hunter

<objective>
Search and extract contact information for people or companies by aggregating data from multiple sources (LinkedIn, company websites, Apollo, Hunter.io, etc.). Provides structured search queries, email pattern detection, data enrichment guidance, and export-ready contact cards with full attribution and compliance notes.
</objective>

<quick_start>
**Trigger:** "Find the VP of Sales at [Company]" or "Get contact info for [Name] at [Company]"
**Input:** Person name, company, job title, location, or LinkedIn URL
**Output:** Structured contact cards with email, phone, LinkedIn, verification steps, and export formats (CSV/JSON/vCard)
</quick_start>

<success_criteria>
- [ ] Search type identified (person, company, role, email verification, bulk enrichment)
- [ ] Structured search queries provided for LinkedIn, Google, company website
- [ ] Email pattern detected with confidence level
- [ ] Contact card populated with all available fields and source attribution
- [ ] Verification steps included (cross-reference, format validation)
- [ ] Compliance guidelines followed (public data only, GDPR/CAN-SPAM)
</success_criteria>

<workflow>

## Instructions

When a user needs to find contact information:

1. **Identify Search Type**:
   - **Person search**: Find specific individual
   - **Company search**: Find people at a company
   - **Role search**: Find people with specific job title
   - **Email verification**: Validate and enrich existing email
   - **Bulk enrichment**: Enrich list of contacts

2. **Gather Search Parameters**:
   - Person name (first, last)
   - Company name
   - Job title / role
   - Location (city, state, country)
   - Industry
   - LinkedIn URL (if available)
   - Email domain
   - Any other identifying information

3. **Search Strategy**:

   **Sources to Check** (suggest to user):
   - LinkedIn (manual search with user's account)
   - Company website (About, Team, Contact pages)
   - GitHub (for developers)
   - Twitter/X profiles
   - Professional directories
   - Public databases
   - ZoomInfo (if user has access)
   - Apollo.io (if user has access)
   - Hunter.io (if user has access)
   - RocketReach (if user has access)

   **⚠️ Important**: This skill GUIDES the search process. It doesn't directly access paid APIs. Instead, it:
   - Provides structured search queries
   - Suggests where to look
   - Helps organize found information
   - Validates and formats results

4. **Search Instructions Format**:
   ```
   🔍 CONTACT SEARCH: [Name/Company]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📋 SEARCH PARAMETERS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Target: John Smith
   Company: Acme Corp
   Title: VP of Engineering
   Location: San Francisco, CA

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 RECOMMENDED SEARCH QUERIES
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   LinkedIn:
   1. Search: "John Smith VP Engineering Acme Corp"
   2. Use company filter: "Acme Corp"
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
