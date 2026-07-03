# Sales Intelligence Tools Reference

## Company Identification & Briefing

### `sales_brief` — Complete Customer Briefing
The most useful pre-call tool. One call returns everything.

**Input:** `companyName` (text) — fuzzy matching, approximate name works
**Returns:**
- Company info (CRM + HubSpot cross-referenced)
- Revenue history (last 12 months)
- Top 5 products purchased
- Open deals with stages
- Key contacts (up to 5)
- Recent notes and activity

### `identify_company` — Fuzzy Company Match
Match spoken/misspelled company names against CRM + HubSpot.

**Input:** `name` (text — even from speech transcription)
**Returns:** Best matches with confidence scores and cross-linked IDs
**Example:** "be an age photo" -> finds "B&H Photo"

---

## Call Intelligence (Clari)

### `get_call_history` — Search Calls by Name, Company, or Email
**Best tool for finding calls.** Searches PostgreSQL `clari_calls` table (7K+ calls with AI summaries).

**Input:**
- `search` — company name, contact name, or call title (e.g. "Tufts University", "Jesse Anderson")
- `rep_email` — filter by sales rep email (optional)
- `attendee_email` — filter by external attendee email (optional)
- `days` — look back N days (default: 30)
- `limit` — max results (default: 5)

**How it works:**
- If `search` provided → searches PostgreSQL by title/account_name/participant_names/summary (instant)
- If only email provided → falls back to Clari API

**Example:** "How did the Tufts call go?" → finds "Tufts University / Epiphan" call with full summary + action items.

### `clari_search_calls` — Direct Clari API Search (MCP)
**Input:** `repEmail`, `attendeeEmail`, `daysBack`, `status`
**Returns:** Call list with participants and Clari review URLs
**Note:** Only filters by email — use `get_call_history` with `search` for name-based lookup.

### `clari_get_call` — Full Call Details
**Input:** `callId` (string), optional `includeTranscript` (default: false)
**Returns:** Summary, metrics, action items, optionally full transcript

### `clari_get_call_summary` — Quick Call Summary
**Input:** `callId` (string)
**Returns:** Summary + action items only (lightweight, fast)

---

## Stripe Cloud Usage

### `stripe_usage_insights` — Epiphan Cloud Usage Analysis
Analyzes Connect/Unify metered usage from Stripe EU.

**Input:** `companyName` or `domain` (optional — omit for all customers)
**Returns:**
- Usage hours (Connect + Unify) vs contract limits
- Growth signals (increasing usage)
- Renewal alerts (>80% of contract)
- Churn risk (declining usage)
- Cross-sell opportunities

**Examples:**
- "Which customers are approaching usage limits?"
- "Cloud usage for PLI"
- "Upsell opportunities based on Stripe data"

---

## Engagement History

### `activity_get_timeline` — Contact/Company/Rep Timeline
**Input:**
- `type`: "contact", "company", or "owner" (sales rep)
- `id`: HubSpot ID for the entity
- `daysBack`: how far back (default: 90 days)
- `activityTypes`: filter by type (calls, emails, notes, tasks, meetings)

**Returns:** Chronological timeline, newest first:
- Calls with outcome: Connected / Voicemail / No Answer
- Emails with direction: sent / received
- Notes, tasks, meetings with details

---

## Handoff & Qualification

### `ae_handoff` — BDR to AE Handoff Package
Generates complete handoff by aggregating all sources.

**Input:**
- `companyName` OR `hubspotCompanyId` (required)
- `contactEmail` (optional — primary contact)
- `createNote` (boolean — writes to HubSpot if true)

**Returns:**
- Bottom Line summary
- Pre-call tasks for AE
- Intel from: sales_brief + device history + Clari calls + engagement timeline + LLM analysis

**CAUTION:** `createNote: true` creates a HubSpot note visible to the entire sales team. Use deliberately.

### `qualify_lead` — Lead Qualification
**Input:** `contactId` (HubSpot contact ID), optional `writeToHubspot`
**Returns:**
- Junk detection (spam, competitor, personal email)
- ICP classification (AI-powered)
- Region routing (NA / EMEA / APAC)
- Personalized outreach email draft

If `writeToHubspot: true`: updates lifecycle stage + creates qualification note.

---

## Upcoming Meetings

### `get_upcoming_meetings` — Calendar Check
Returns upcoming meetings from connected calendar.
Useful for checking what calls are scheduled before preparing briefs.
