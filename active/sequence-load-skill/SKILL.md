---
name: sequence-load
description: "Monday 7:15 AM (and on demand) enrollment of prospect-refresh net-new leads into Apollo sequences: qualify_lead final gate + HubSpot/Apollo dedupe + phone validation -> vertical->sequence mapping -> batch add-to-sequence -> HubSpot contact sync -> enrollment report. Use when: 'load prospects into sequences', 'enroll new leads', 'run sequence load'."
schedule: "0 7 15 * * 1"
timezone: "America/New_York"
---

# Sequence Load Skill

<objective>
Automatically load net-new prospects from prospect-refresh into Apollo outreach sequences. Read a structured handoff (not a scraped report), re-gate every survivor through `qualify_lead` as the final authoritative go/no-go, confirm phone numbers exist, check for duplicate enrollments, and execute batch add-to-sequence. Output enrollment report with per-prospect sequence assignment and contact IDs for HubSpot sync.
</objective>

<quick_start>
**Trigger:** Monday 7:15 AM ET (runs after prospect-refresh at 6:30 AM)  
**Manual Trigger:** "Load prospects into sequences" or "Enroll new leads"  
**Dependencies:** Requires Apollo credits, prospect-refresh's structured handoff, HubSpot portal 21530819, `qualify_lead` (Epiphan AI)  
**Output:** Enrollment confirmation per prospect, sequence assignment, contact IDs for HubSpot creation
</quick_start>

<config>
**Vertical → Sequence Mapping** (declared once here; Stage 4 resolves the live `sequence_id` dynamically via `apollo_emailer_campaigns_search` each run — never hardcode a sequence ID or email-account ID inline in a stage):

| Vertical | Sequence Name Pattern |
|----------|----------------------|
| Higher Ed | BDR_HigherEd_OutboundX |
| Courts | BDR_Courts_OutboundX |
| Government | BDR_Government_OutboundX |
| Corporate AV | BDR_CorporateAV_OutboundX |
| Healthcare | BDR_Healthcare_OutboundX |
| Houses of Worship | BDR_HoW_OutboundX |
| K-12 | BDR_K12_OutboundX |

Fallback sequence: `BDR_Outbound_General` if a vertical-specific match isn't found.
</config>

<success_criteria>
- [ ] Read prospect-refresh's structured handoff (net-new prospects; JSON/CSV or direct MCP query — not HTML scraping)
- [ ] Query HubSpot to verify prospect not already enrolled in any sequence
- [ ] Validate phone number exists (from prospect-enrich or Apollo)
- [ ] Call `qualify_lead` on every survivor as the final, authoritative enrollment gate (do not re-derive Golden Rules / NEVER-ATL prose here)
- [ ] Find target Apollo sequence(s) by ICP vertical (config table above; resolved dynamically)
- [ ] Get email account ID (tim@epiphan.com or primary)
- [ ] Batch add prospects to sequence (max 100 per request)
- [ ] Confirm enrollments (check Apollo contact.sequence_id)
- [ ] Create HubSpot contacts if not exist (pull contact IDs for HubSpot sync)
- [ ] Report: total enrolled, per-sequence breakdown, any failures
- [ ] Halt + alert (not just log) on a Stage 6 email-account resolution failure or a Stage 7 sub-threshold batch success
</success_criteria>

<workflow>

## Stage 1: Read Prospect Refresh's Structured Handoff

**Input Source:** a structured handoff from prospect-refresh — NOT the HTML report. Consume one of, in preference order:
1. A shared HubSpot list of net-new refresh candidates (direct MCP query via `search_crm_objects`), or
2. A structured JSON/CSV file prospect-refresh emits alongside its HTML report (e.g. `~/.claude/skill-state/prospect-refresh-handoff.json`, outside the repo per the sidecar-path convention), containing one record per prospect.

The HTML report remains prospect-refresh's human-facing deliverable for Tim's review (drill-down links, sortable table) — it is not this skill's machine input. Re-parsing that HTML is exactly the silent-break risk this stage used to carry: any report-format change (a renamed column, restyled table) would break this skill without either skill raising an error. **Note:** emitting the structured handoff is prospect-refresh's responsibility — if `active/prospect-refresh-skill/SKILL.md` doesn't yet write one, that's a fix for that skill's own file, not this one; until then, degrade to the direct HubSpot list query (option 1) rather than falling back to HTML scraping.

**Expected fields per record:**
- Prospect name, email, title, company, vertical, ATL/BTL tier
- Apollo person_id, organization_id, phone
- Company revenue, headcount, funding

**Validation:**
- Email format is valid
- Phone exists (from enrichment)
- Vertical is one of: Higher Ed, Courts, Gov, Corporate AV, Healthcare, HoW, K-12

**If the structured handoff is missing or empty:** don't guess or silently skip — alert Tim and halt this run (see Failure Handling below) rather than falling back to scraping the HTML report.

**Output:** Structured list of 30 prospects (or fewer if filtering applied)

---

## Stage 2: Deduplicate Against HubSpot + Apollo

**Step A: Check HubSpot for existing contact**

**MCP Tool:** `search_crm_objects` (HubSpot)

```
objectType: "contacts"
filterGroups: [{
  filters: [
    { propertyName: "email", operator: "EQ", value: prospect.email }
  ]
}]
properties: ["email", "phone", "hs_lead_status"]
```

**Decision Logic:**
- If contact exists + NOT in "Sequenced" or "Active Sequence" status → REUSE contact (get contact ID)
- If contact exists + in sequence → SKIP (avoid re-enrollment)
- If contact does not exist → PROCEED to Stage 3 (create new)

**Step B: Check Apollo for duplicate enrollments**

**MCP Tool:** `apollo_contacts_search`

```
q_keywords: prospect.email
per_page: 10
```

**Decision Logic:**
- If Apollo contact exists + already in a sequence → SKIP
- If Apollo contact exists + no sequence → PROCEED (re-enroll)
- If Apollo contact does not exist → PROCEED to Stage 3 (create new)

**Dedup Output:** List of unique prospects (typically 60-70% of input after dedup)

---

## Stage 3: Final Enrollment Gate — `qualify_lead` + Phone Exists

This is the **last checkpoint** before a contact enters a live Apollo sequence, so it must be authoritative rather than a second, drifting copy of Golden Rules / NEVER-ATL prose.

**MCP Tool:** `qualify_lead` (Epiphan AI) — call on every survivor of Stage 2 dedupe.

**Decision Logic (treat the verdict as authoritative — do not re-derive it):**
- `junk == true` → SKIP (do not enroll)
- `category` flags a disqualification (customer match, channel partner, device-owner, product-only engager) → SKIP
- `power_level == btl` with a NEVER-ATL title → SKIP
- `power_level == atl` or `gray` (gray-zone $25K budget-authority rule already applied by `qualify_lead`) → PROCEED

**Why re-gate here instead of trusting upstream:** prospect-refresh already calls `qualify_lead` once at candidate-sourcing time (its own Stage 3), but ~45 minutes pass before this skill runs, and HubSpot/CRM state can change in that window (a contact converts to customer, gets suppressed, gets tagged channel). Don't skip this call as "already checked upstream" — a stale verdict here is exactly how a disqualified lead reaches a live sequence.

**Phone Validation:**
- Phone must be non-null (from Apollo enrichment or prospect-enrich)
- Format: +1-XXX-XXX-XXXX (US) or +1-XXX-XXX-XXXX (Canada)
- If phone missing → LOG as "Phone Missing" but DO NOT ENROLL (requires phone for Apollo compliance)

**Output:** Verified prospect list (typically 80-90% after phone validation)

---

### Stage S — Suppression Gate

Before sequence enrollment, exclude suppressed contacts:
- **EXCLUDE** if `bdr_suppression_until` IS SET AND `bdr_suppression_until` > TODAY
- **INCLUDE** if `bdr_suppression_until` IS NOT SET (never suppressed)
- **INCLUDE** if `bdr_suppression_until` < TODAY (cooling period expired)

HubSpot filter: `propertyName: "bdr_suppression_until", operator: "NOT_HAS_PROPERTY"` OR `operator: "LT", value: TODAY_ISO`
Reference: `lead-suppression-spec` (bdr_suppressed, bdr_suppression_reason, bdr_suppression_until)

---

## Stage 4: Map Prospects to Target Sequences

**MCP Tool:** `apollo_emailer_campaigns_search`

**Search for sequences by vertical + template**, using the mapping declared once in `<config>` above (do not re-hardcode the vertical→sequence-name table per stage; resolve the actual `sequence_id` fresh each run by name search, since renames/new sequences shouldn't require an edit here).

**Query Logic:**
```
per_page: 100
# Search returns: id, name, status, num_contacts, num_enrolled
```

**Sequence Selection Rule:**
- Map prospect.vertical to sequence_name_pattern
- Choose sequence with LOWEST current enrollment (load balancing)
- Fallback: default "BDR_Outbound_General" if vertical-specific not found

**Output:** Prospect + sequence_id mapping

---

## Stage 5: Create Apollo Contacts (If New)

**MCP Tool:** `apollo_contacts_search`

**For new prospects (not found in Stage 2):**

```
per_page: 10
q_keywords: prospect.email
```

**If not found, create contact via:**

**MCP Tool:** `apollo_contacts_create`

```
email: prospect.email
first_name: prospect.first_name
last_name: prospect.last_name
title: prospect.title
organization_name: prospect.company
phone: prospect.phone (if available)
label_names: [prospect.vertical, "BDR_Prospect", "2026_Q1"]
```

**Output:** New Apollo contact ID (apollo_contact_id)

---

## Stage 6: Get Email Account ID

**MCP Tool:** `apollo_email_accounts_index`

**Query all linked email accounts:**

```
# Returns: [{ id, email, status, daily_send_limit, ... }]
```

**Selection Logic:**
- Look for email containing "epiphan" or "tkipper"
- Use primary email account if multiple
- If none found → **HALT the run and alert Tim** (do not proceed without a resolvable email account; this is not a per-prospect failure to log and continue past — nothing can be enrolled without it). Mark the run `error` and name Stage 6 as the failing stage in the outcome sidecar.

**Output:** email_account_id (the id string returned by `apollo_email_accounts_index` — resolve it fresh each run, never hardcode a specific account id)

---

## Stage 7: Batch Add to Sequences

**MCP Tool:** `apollo_emailer_campaigns_add_contact_ids`

**For each sequence (group prospects by sequence_id):**

```
id: sequence_id (from Stage 4 mapping)
emailer_campaign_id: sequence_id (same as id)
send_email_from_email_account_id: email_account_id (from Stage 6)
contact_ids: [contact_id_1, contact_id_2, ..., contact_id_N] (max 100 per batch)
sequence_active_in_other_campaigns: true (allow multi-sequence enrollment)
sequence_unverified_email: false (require verified emails)
status: "active" (start sequence immediately)
```

**Batch Logic:**
- Group prospects by target sequence
- Send 100 contacts max per API call
- Retry once if rate limited, then move to the next batch and log the failed one

**Expected Success Rate:** 95%+ (most failures due to email validation)

**Batch-level halt/alert (beyond per-prospect logging):** if success rate for the whole run falls below 70%, or an entire batch (not just scattered individual prospects) fails, don't just log it and continue quietly — alert Tim with the failing batch/sequence and mark the run `partial`, naming Stage 7 as the degraded stage.

---

## Stage 8: Confirm Enrollments

**MCP Tool:** `apollo_contacts_search`

**For each enrolled contact, verify enrollment:**

```
q_keywords: contact.email
per_page: 1
```

**Check response:**
- contact.sequences (should contain sequence_id from Stage 7)
- contact.last_sequence_enrollment_date (should be "today")
- contact.status (should be "active")

**Log Enrollment:**
```
✓ jane@acme.com → BDR_HigherEd_Outbound (sequence_id: abc123)
✗ bob@example.com → Phone validation failed
✗ carol@company.com → Already enrolled in BDR_Corporate_AV
```

---

## Stage 9: Create HubSpot Contacts (Sync)

**For newly created Apollo contacts, create HubSpot counterparts:**

**MCP Tool:** `manage_crm_objects` (HubSpot createRequest)

```
objectType: "contacts"
properties: {
  firstname: prospect.first_name,
  lastname: prospect.last_name,
  email: prospect.email,
  phone: prospect.phone,
  jobtitle: prospect.title,
  company: prospect.company_name,
  lifecyclestage: "subscriber",
  hs_lead_status: "open",
  custom_apollo_contact_id: apollo_contact_id,
  custom_apollo_sequence: sequence_name,
  custom_atl_btl_tier: prospect.atl_btl_tier,
  custom_prospect_vertical: prospect.vertical,
  custom_prospect_icp_score: prospect.icp_score
}
associations: [
  {
    targetObjectId: company_id, # Find or create company in HubSpot
    targetObjectType: "companies"
  }
]
```

**Company Association Logic:**
- Search HubSpot for company by domain
- If found: use company_id from existing record
- If not found: create company via manage_crm_objects

**Output:** Created contact IDs (to link Gmail drafts)

---

## Stage 10: Output Enrollment Report

**Format:** Markdown table + summary stats

**Enrollment Table:**

| Prospect | Email | Phone | Vertical | Sequence | Apollo ID | HubSpot ID | Status |
|----------|-------|-------|----------|----------|-----------|-----------|--------|
| Jane Smith | jane@acme.com | +1-555-0123 | Higher Ed | BDR_HigherEd_1 | apollo-123 | hs-456 | ✓ Enrolled |
| Bob Jones | bob@example.com | null | Courts | - | - | - | ✗ Phone missing |
| Carol White | carol@corp.com | +1-555-0124 | Corp AV | BDR_CorporateAV_1 | apollo-789 | hs-012 | ✓ Enrolled |

**Summary Stats:**
- Total prospects processed: X
- Successfully enrolled: Y (Y% of X)
- Phone validation failures: Z
- Duplicate/already enrolled: W
- HubSpot synced: Y (new contacts)
- Per-sequence breakdown:
  - BDR_HigherEd_1: 5 enrolled
  - BDR_Courts_1: 4 enrolled
  - BDR_CorporateAV_1: 5 enrolled
  - etc.

**Next Steps:** Prospects now enrolled in Apollo sequences. Gmail drafts (from prospect-refresh) ready for manual review + send-from-draft workflow.

</workflow>

---

## Failure Handling & Outcome Logging

Follow `skill-audit/specs/self-healing-template.md` for the failure ladder (retry -> degrade ->
alert -> halt) and the three-way status definition (success/partial/error — always name the
failing stage for partial/error). Specific to this skill:
- **Stage 1 handoff missing/empty:** halt, alert Tim, status `error`, name Stage 1 — never fall
  back to scraping the HTML report.
- **Stage 3 `qualify_lead` unavailable:** alert and halt rather than proceeding as if the gate
  passed (per the spec's fallback ladder, item 3) — do not fall back to inline Golden Rules prose.
- **Stage 6 no resolvable email account:** halt, alert Tim, status `error`.
- **Stage 7 batch success below 70% or a whole batch failing:** alert Tim, status `partial`,
  name Stage 7.
- Append one line per run to `~/.claude/skill-runs/sequence-load.jsonl` (in addition to the
  outcome sidecar below) per the spec's run-log convention, so failures are trendable rather than
  visible only in the latest snapshot.

---

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-sequence-load.json`:
```json
{"ts":"[UTC ISO8601]","skill":"sequence-load","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"contacts_loaded":[n],"sequences_updated":[n],"duplicates_skipped":[n],"phone_validation_failures":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.

---

<dependencies>
## MCP tools
- **Epiphan AI:** `qualify_lead` — final, authoritative enrollment gate (Stage 3)
- **HubSpot:** `search_crm_objects` (dedupe, Stage 2; sequence handoff query, Stage 1), `manage_crm_objects` (contact/company create, Stage 9)
- **Apollo:** `apollo_contacts_search` (dedupe + Stage 5 lookup), `apollo_contacts_create` (Stage 5), `apollo_emailer_campaigns_search` (Stage 4), `apollo_email_accounts_index` (Stage 6), `apollo_emailer_campaigns_add_contact_ids` (Stage 7)

## Sibling skills referenced (reuse, don't rebuild)
- `prospect-refresh` — upstream source of net-new prospects; hands off a structured list (not this skill's input via HTML scraping).
- `prospect-enrich` / `phone-verification-waterfall` — phone enrichment referenced in Stage 3.
- `lead-suppression-spec` — Stage S suppression gate.
</dependencies>

---

## Skill Metadata

**Version:** 1.0
**Last Updated:** 2026-03-19
**Author:** Tim Kipper
**Status:** Production
**Integration:** Apollo + HubSpot (portal 21530819)
**Tier:** P1 (Core BDR Automation)
**Triggers:** Scheduled (Monday 7:15 AM) + Manual ("Load sequences")
**Dependencies:** prospect-refresh (6:30 AM, structured handoff) → sequence-load (7:15 AM, `qualify_lead` final gate) → morning-brief (7:30 AM)
