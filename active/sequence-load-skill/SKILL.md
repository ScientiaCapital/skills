---
name: sequence-load
description: "Monday auto-load of weekly prospect refresh results into Apollo outreach sequences."
schedule: "0 7 15 * * 1"
timezone: "America/New_York"
---

# Sequence Load Skill

<objective>
Automatically load net-new prospects from prospect-refresh into Apollo outreach sequences. Validate Golden Rules, confirm phone numbers exist, check for duplicate enrollments, and execute batch add-to-sequence. Output enrollment report with per-prospect sequence assignment and contact IDs for HubSpot sync.
</objective>

<quick_start>
**Trigger:** Monday 7:15 AM ET (runs after prospect-refresh at 6:30 AM)  
**Manual Trigger:** "Load prospects into sequences" or "Enroll new leads"  
**Dependencies:** Requires Apollo credits, prospect-refresh output, HubSpot portal 21530819  
**Output:** Enrollment confirmation per prospect, sequence assignment, contact IDs for HubSpot creation
</quick_start>

<success_criteria>
- [ ] Read prospect-refresh output (30 net-new prospects from Gmail drafts + HTML report)
- [ ] Query HubSpot to verify prospect not already enrolled in any sequence
- [ ] Validate phone number exists (from prospect-enrich or Apollo)
- [ ] Apply Golden Rules (skip customers, channel, device owners, NEVER ATL)
- [ ] Find target Apollo sequence(s) by ICP vertical
- [ ] Get email account ID (tim@epiphan.com or primary)
- [ ] Batch add prospects to sequence (max 100 per request)
- [ ] Confirm enrollments (check Apollo contact.sequence_id)
- [ ] Create HubSpot contacts if not exist (pull contact IDs for HubSpot sync)
- [ ] Report: total enrolled, per-sequence breakdown, any failures
</success_criteria>

<workflow>

## Stage 1: Read Prospect Refresh Output

**Input Source:** prospect-refresh HTML report + Gmail drafts

**Extract from HTML Report:**
- Prospect name, email, title, company, vertical, ATL/BTL tier
- Apollo person_id, organization_id, phone
- Company revenue, headcount, funding

**Validation:**
- Email format is valid
- Phone exists (from enrichment)
- Vertical is one of: Higher Ed, Courts, Gov, Corporate AV, Healthcare, HoW, K-12

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

## Stage 3: Validate Golden Rules + Phone Exists

**Golden Rules (Hard Exclusions):**

**Skip if:**
- Email domain matches known customer domain (cross-check crm_customers)
- Contact tagged "Channel Partner" in HubSpot
- Contact tagged "Device Owner" in HubSpot
- Company in "Product Page Engagers" tag
- Title in NEVER ATL list: Warehouse Manager, Network Manager, Systems Admin, AV Technician, Graphic Design Instructor, Program Administrator, Web Designer, Classroom Support, Lab Coordinator, Maintenance, Building Engineer, Multimedia Services Manager, Video Production Specialist, Streaming Crew

**Phone Validation:**
- Phone must be non-null (from Apollo enrichment or prospect-enrich)
- Format: +1-XXX-XXX-XXXX (US) or +1-XXX-XXX-XXXX (Canada)
- If phone missing → LOG as "Phone Missing" but DO NOT ENROLL (requires phone for Apollo compliance)

**Output:** Verified prospect list (typically 80-90% after phone validation)

---

## Stage 4: Map Prospects to Target Sequences

**MCP Tool:** `apollo_emailer_campaigns_search`

**Search for sequences by vertical + template:**

| Vertical | Sequence Name Pattern | Target Sequence ID |
|----------|----------------------|------------------|
| Higher Ed | BDR_HigherEd_OutboundX | [search by name] |
| Courts | BDR_Courts_OutboundX | [search by name] |
| Government | BDR_Government_OutboundX | [search by name] |
| Corporate AV | BDR_CorporateAV_OutboundX | [search by name] |
| Healthcare | BDR_Healthcare_OutboundX | [search by name] |
| Houses of Worship | BDR_HoW_OutboundX | [search by name] |
| K-12 | BDR_K12_OutboundX | [search by name] |

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
- If none found → ERROR (cannot proceed without email account)

**Output:** email_account_id (e.g., "6633baaece5fbd01c791d7ca")

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
- Retry if rate limited

**Expected Success Rate:** 95%+ (most failures due to email validation)

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

## Skill Metadata

**Version:** 1.0  
**Last Updated:** 2026-03-19  
**Author:** Tim Kipper  
**Status:** Production  
**Integration:** Apollo + HubSpot (portal 21530819)  
**Tier:** P1 (Core BDR Automation)  
**Triggers:** Scheduled (Monday 7:15 AM) + Manual ("Load sequences")  
**Dependencies:** prospect-refresh (6:30 AM) → sequence-load (7:15 AM) → morning-brief (7:30 AM)
