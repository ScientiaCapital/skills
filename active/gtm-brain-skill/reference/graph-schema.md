# GTM Brain — Graph Schema

## Nodes

| Label | Key Property | Other Properties |
|-------|-------------|-----------------|
| `Contact` | `hubspot_id` | name, title, email, phone, vertical, atl_btl |
| `Account` | `hubspot_id` | name, vertical, icp_score, domain |
| `Deal` | `hubspot_id` | name, stage, amount, owner_id, created_date |
| `Outcome` | `id` | channel (call/email/sequence/meeting), result (positive/neutral/negative), notes, timestamp |
| `Sequence` | `nooks_id` | name, vertical, step_count |

## Relationships

```
(Contact)-[:WORKS_AT]->(Account)
(Contact)-[:INVOLVED_IN {role}]->(Deal)
(Contact)-[:HAD]->(Outcome)
(Outcome)-[:VIA]->(Sequence)
(Deal)-[:WITH]->(Account)
```

## Vertical Values (match ATL/BTL gate)

`Higher Ed` · `Courts` · `Government` · `Healthcare` · `Corporate AV` · `Houses of Worship` · `K-12`

## ATL/BTL Values

`ATL` · `GRAY` · `BTL` · `NEVER`

## Result Values

`positive` — demo booked, replied with interest, moved stage
`neutral` — left voicemail, opened email, no reply yet
`negative` — DQ'd, wrong person, hard no, unsubscribed

## Channel Values

`call` · `email` · `sms` · `sequence` · `meeting` · `linkedin`

## Constraints & Indexes (created by `neo4j.py init`)

- Uniqueness: Contact.hubspot_id, Account.hubspot_id, Deal.hubspot_id, Outcome.id, Sequence.nooks_id
- Index: Contact.vertical, Contact.atl_btl, Outcome.result
