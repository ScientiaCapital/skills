# GTM Brain — Cypher Query Patterns

All queries run via:
```bash
set -a && source ~/Desktop/tk_projects/skills/.env && set +a
python3 ~/.claude/skills/gtm-brain-skill/scripts/brain.py run "<CYPHER>"
```

---

## READ Patterns

### What worked with a vertical + title?
```cypher
MATCH (c:Contact {vertical: 'Higher Ed', atl_btl: 'ATL'})-[:HAD]->(o:Outcome {result: 'positive'})
RETURN c.title, o.channel, o.notes, count(*) AS wins
ORDER BY wins DESC LIMIT 10
```

### All contacts at a company + their outcomes
```cypher
MATCH (c:Contact)-[:WORKS_AT]->(a:Account)
WHERE toLower(a.name) CONTAINS toLower('MIT')
OPTIONAL MATCH (c)-[:HAD]->(o:Outcome)
RETURN c.name, c.title, c.atl_btl, collect({channel: o.channel, result: o.result, notes: o.notes}) AS outcomes
ORDER BY c.atl_btl
```

### Best sequences by vertical
```cypher
MATCH (c:Contact {vertical: 'Courts'})-[:HAD]->(o:Outcome {result: 'positive'})-[:VIA]->(s:Sequence)
RETURN s.name, count(o) AS wins ORDER BY wins DESC LIMIT 5
```

### Deal relationship map (everyone on a deal)
```cypher
MATCH (c:Contact)-[:INVOLVED_IN]->(d:Deal {hubspot_id: $deal_id})
OPTIONAL MATCH (c)-[:HAD]->(o:Outcome)
RETURN c.name, c.title, c.atl_btl, collect({result: o.result, channel: o.channel}) AS touch_history
```

### ATL coverage for open deals
```cypher
MATCH (d:Deal) WHERE d.stage NOT IN ['Closed Won', 'Closed Lost']
MATCH (c:Contact)-[:INVOLVED_IN]->(d)
WITH d, collect(c.atl_btl) AS tiers
RETURN d.name, d.stage, d.amount,
       size([t IN tiers WHERE t = 'ATL']) AS atl_count,
       size(tiers) AS total_contacts
ORDER BY atl_count ASC
```

### Contact history (last N outcomes)
```cypher
MATCH (c:Contact {hubspot_id: $contact_id})-[:HAD]->(o:Outcome)
RETURN o.channel, o.result, o.notes, o.timestamp
ORDER BY o.timestamp DESC LIMIT 10
```

### Multi-hop: who else like my champion responded positively?
```cypher
MATCH (c:Contact {vertical: 'Higher Ed', title: 'Director of IT'})-[:HAD]->(o:Outcome {result: 'positive'})
WITH c.vertical AS v, c.title AS t, count(o) AS wins
WHERE wins >= 2
RETURN v, t, wins ORDER BY wins DESC
```

---

## WRITE Patterns

### Upsert Contact
```bash
python3 brain.py merge-contact '{"hubspot_id":"12345","name":"Jane Smith","title":"Director of IT","vertical":"Higher Ed","atl_btl":"ATL","email":"jsmith@mit.edu"}'
```

### Upsert Account + wire to Contact
```bash
python3 brain.py merge-account '{"hubspot_id":"99001","name":"MIT","vertical":"Higher Ed","icp_score":90}'
# Then wire the relationship:
python3 brain.py run "MATCH (c:Contact {hubspot_id:'12345'}),(a:Account {hubspot_id:'99001'}) MERGE (c)-[:WORKS_AT]->(a)"
```

### Log a call outcome
```bash
python3 brain.py log-outcome '{"id":"outcome-20260703-12345","contact_hubspot_id":"12345","channel":"call","result":"positive","notes":"Demo booked for July 10, interested in Pearl Mini for 3 lecture halls","timestamp":"2026-07-03T14:00:00Z"}'
```

### Attach contact to deal
```bash
python3 brain.py run "MATCH (c:Contact {hubspot_id:'12345'}),(d:Deal {hubspot_id:'deal-001'}) MERGE (c)-[:INVOLVED_IN {role:'champion'}]->(d)"
```
