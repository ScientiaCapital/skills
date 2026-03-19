# Sequence Audit — Apollo Removal Pattern

When friday-sequence-audit identifies contacts that should be removed from sequences, it MUST call the Apollo API to actually remove them — not just recommend removal.

## Removal Triggers

1. **Email bounced**: Contact's email bounced in sequence
2. **AE drift**: Contact reassigned to AE owner (82625923, 423155215, 190030668)
3. **NEVER ATL title**: Contact has a title on the NEVER ATL list
4. **Customer conversion**: Contact's lifecycle_stage changed to 'customer'
5. **Meeting booked**: Contact has a meeting scheduled with an AE

## Apollo Removal API Call

```
Tool: apollo_emailer_campaigns_remove_or_stop_contact_ids
Parameters:
  contact_ids: [array of Apollo contact IDs to remove]
  emailer_campaign_ids: [array of sequence IDs containing these contacts]
  mode: "remove"  # or "stop" with stop_reason for tracking
  stop_reason: "Friday audit: [bounce|AE drift|NEVER ATL|customer|meeting booked]"
```

## Pre-Removal Checklist

1. Confirm contact exists in Apollo: `apollo_contacts_search(q_keywords=contact_email)`
2. Confirm sequence membership: `apollo_emailer_campaigns_search(q_name=sequence_name)`
3. Execute removal: `apollo_emailer_campaigns_remove_or_stop_contact_ids(...)`
4. Log removal in Supabase: Insert disposition event with event_type='MANUAL_UPDATE'

## Post-Removal Verification

After batch removal, re-query sequences to confirm contacts are gone.
Report: "Removed X contacts from Y sequences (Z bounces, W AE drift, V NEVER ATL)"
