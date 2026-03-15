# Golden Rules Filter — Reference

Used by phone-verification-waterfall-skill and prospect-research-to-cadence-skill to exclude contacts who don't fit the BDR cold prospect motion.

## Filter Logic

**SKIP the contact if ANY of these conditions are TRUE:**

### 1. Lifecycle Stage
- `lifecyclestage = 'customer'`
- **Reason:** Customers are in a different motion (success, upsell). BDR focus is cold prospects only.

### 2. First Conversion (Product Engagement)
- `first_conversion` contains ANY of: `'Pearl'`, `'setup'`, `'Connect'`, `'signup'`
- **Reason:** Contact has already engaged with Epiphan product or setup process. Warm lead, not cold.

### 3. Device Ownership
- Company `device_count >= 1` (in Epiphan CRM)
- **Reason:** Company already owns at least one Pearl device. Likely existing relationship, renewal candidate, not cold prospect.

### 4. Channel Partner Flag
- Company `is_channel = true`
- **Reason:** Channel partners (resellers, integrators) have a separate sales process. BDR should not prospect these.

### 5. Account Executive Ownership
- Contact `hubspot_owner_id` IN (`'82625923'`, `'423155215'`)
  - 82625923 = Lex Finkle (AE)
  - 423155215 = Phil Hutchins (AE)
- **Reason:** These leads are owned by Account Executives. No BDR lead theft.

### 6. Other Account Executive Ownership (Pending Verification)
- Contact `hubspot_owner_id` matches pattern `'Ron*'` OR `'Anthony*'`
- **Reason:** Likely Account Executives (Ron, Anthony). Verify exact IDs and add to filter when confirmed.

---

## HubSpot Query Template

```sql
SELECT contact_id, first_name, last_name, email, company_name, hs_job_title, hubspot_owner_id
FROM contacts
WHERE
  phone IS NULL
  AND phone != ''
  AND lifecyclestage != 'customer'
  AND hubspot_owner_id NOT IN ('82625923', '423155215')
  AND first_conversion NOT LIKE '%Pearl%'
  AND first_conversion NOT LIKE '%setup%'
  AND first_conversion NOT LIKE '%Connect%'
  AND first_conversion NOT LIKE '%signup%'
  AND (
    SELECT device_count FROM companies WHERE company_id = contacts.company_id
  ) < 1
  AND (
    SELECT is_channel FROM companies WHERE company_id = contacts.company_id
  ) = false
ORDER BY contact_created_at DESC
LIMIT 500;
```

---

## Implementation in Skills

### prospect-research-to-cadence-skill
- Applied at Stage 1 (Research) before enrichment starts
- Skips golden rules violators early to avoid wasted API calls

### phone-verification-waterfall-skill
- Applied at Stage 1 (Pull Leads) before phone lookup
- Ensures no customer/owned/engaged leads enter the phone waterfall

---

## Maintenance

**Add new AE IDs as they hire:**
- File a task in hubspot-revops-skill to update this filter when new AEs join
- Update both skills immediately (no caching)

**Update first_conversion keywords:**
- If new product names or engagement signals emerge, add them
- Example: If "Connect Pro" launches, add `'Connect Pro'` to the filter

**Channel partner updates:**
- Quarterly review of `is_channel = true` flag in HubSpot
- Coordinate with sales ops if new partners are added

