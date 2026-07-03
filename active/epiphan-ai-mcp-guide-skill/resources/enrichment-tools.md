# Contact Enrichment & Lead Qualification Tools

## `enrich_contact` — Find Phone & Email

Finds mobile phone number and work email for a contact using multi-source lookup.

**Input:**
- `firstName` (required)
- `lastName` (required)
- `companyName` (required)
- `linkedinUrl` (optional — improves accuracy)

**Returns:** Mobile phone + work email with source attribution

**How it works (3-tier lookup):**
1. **Clay cache** (instant) — checks if already enriched previously
2. **HubSpot contacts DB** (instant) — checks existing CRM records
3. **Clay API** (30-90 seconds) — live enrichment if not cached

**Tips:**
- Provide LinkedIn URL for best accuracy
- First call for a new contact may take 30-90 seconds (Clay API polling)
- Subsequent calls for the same contact are instant (cached)

---

## `qualify_lead` — Lead Qualification

Analyzes a HubSpot contact and determines lead quality, classification, and generates outreach.

**Input:**
- `contactId` (string — HubSpot contact ID, required)
- `writeToHubspot` (boolean, optional — default false)

**Returns:**
- **Junk detection:** Is this spam, competitor, or personal email?
- **ICP classification:** How well does this lead match our Ideal Customer Profile (AI-powered embedding analysis)
- **Region routing:** NA / EMEA / APAC assignment
- **Outreach email:** Personalized draft email for first contact

**If `writeToHubspot: true`:**
- Updates the contact's lifecycle stage in HubSpot
- Creates a qualification note with the analysis results
- Visible to the entire sales team

**When to use:**
- New inbound leads that need triaging
- Batch qualification of contact lists
- Before assigning leads to reps — routes to correct region automatically

---

## `generate_image` — Data Visualization

Creates Economist-style data charts and infographics from data.

**Input:**
- Data as JSON or text description
- Chart type preference (optional)

**Supported types:** bar, line, pie, area, heatmap, dashboard, infographic, executive slides

**Returns:** S3 URL to the generated image

**Important:** Always provide actual data (JSON array, table, numbers). Don't just describe what you want — include the data to visualize.

---

## Device Analytics

### `analytics_get_device` — Pearl Device Lookup
**Input:** `serialNumber` (string)
**Returns:** Product model, lifetime hours, idle %, recording locations, linked CRM customer

### `analytics_search_by_email` — Fleet by Registrant Email
**Input:** `email` (string — the email used to register devices)
**Returns:** All Pearl devices registered to that email, with registrant summary and device stats
