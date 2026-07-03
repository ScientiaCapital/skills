# Runnable Tool Examples

Copy-adapt these. All read-only unless noted. Defaults assume FY2026 (start 2025-11-01),
$19.5M target, BDR IDs 87486452 (Tim) / 423155215 (Ron).

## Account prep
```
sales_brief({ company: "NC State University" })
// → company info, revenue history, top products, open deals, key contacts, recent notes (one call)

crm_search_customers({ query: "Cornell" })
hubspot_search_companies({ query: "ncsu.edu", searchBy: "domain" })
```

## Weekly numbers (the standup brief)
```
weekly_brief({})                       // last Sunday, all defaults
weekly_brief({ week_ending: "2026-06-14" })
weekly_brief({ ae_names: ["Phil Sandler","Lex Evans"] })
```

## Custom pipeline cuts
```
// Open pipeline as an owner×stage matrix
query_dataset({ dataset: "pipeline_open", group_by: ["owner","stage"] })

// Revenue by month, FY-to-date
query_dataset({ dataset: "revenue", group_by: ["period_month"],
                date_from: "2025-11-01", date_to: "2026-11-01" })

// Won vs lost this quarter
query_dataset({ dataset: "deals_closed", group_by: ["outcome"],
                date_from: "2026-05-01", date_to: "2026-08-01" })

// BDR activity
query_dataset({ dataset: "rep_activity", group_by: ["owner"],
                filters: { owner_ids: ["87486452","423155215"] } })

// ⚠️ Vertical breakdown is NOT a native dim. Proxy via source/pipeline/country, or enrich
//    account-by-account. Label any vertical split as derived/approximate.
```

## A rep's book of deals
```
hubspot_search_deals({ collaborator_owner_id: "87486452", year: 2026, limit: 50 })
// → synced-Postgres rows incl. stage_label + collaborator_owner_ids
hubspot_search_deals({ query: "UIUC", limit: 10 })
```

## Calls (count by duration, not disposition — see caveats)
```
clari_search_calls({ repEmail: "psandler@epiphan.com", daysBack: 90, limit: 50 })
clari_search_calls({ attendeeEmail: "buyer@university.edu", daysBack: 180 })
clari_get_call_summary({ /* callId from search */ })
```

## Product truth (never quote specs from memory)
```
search_product_catalog({ query: "NDI encoder", category: "encoder" })
search_product_knowledge({ query: "Pearl Nexus simultaneous channels" })
// Verified 2026-06-20: Pearl-2 = max 6 full-HD channels; Pearl Nexus = recommend 2 (max 3).
```

## Contacts & qualification
```
hubspot_search_contacts({ query: "media services", searchBy: "name" })
qualify_lead({ /* lead payload */ })
get_upcoming_meetings({})
```

## Handoff (when a BTL champion is warm and you need the AE)
```
ae_handoff({ /* account + champion + signal */ })
```

## Writes — confirm first (these change the CRM)
```
hubspot_create_contact_note(...)   hubspot_set_lifecycle_stage(...)   hubspot_create_deal(...)
```
