---
name: gtm-brain-skill
description: "Relationship intelligence graph for GTM work. Reads and writes Contact/Account/Deal/Outcome nodes in Neo4j Aura. Syncs contacts/accounts from HubSpot MCP and imports call outcomes from Nooks MCP automatically. Surfaces what messaging, sequences, and personas worked across verticals. Use when: relationship graph, gtm brain, log outcome, what worked with, account map, sync from hubspot, import nooks calls, contact history, sequence performance."
version: "1.1.0"
---

<objective>
GTM Brain is a Neo4j-backed relationship graph that makes past GTM activity searchable and useful.
Every call, email, and sequence outcome is stored as graph data so future targeting uses real signal —
not guesswork — about what worked with which personas and verticals.

Graph lives at: neo4j+s://23a749c7.databases.neo4j.io (AuraDB Free — GTM Knowledge Graph)
Credentials: skills/.env (never hardcode elsewhere)
Schema reference: reference/graph-schema.md
Query patterns: reference/cypher-patterns.md
</objective>

<quick_start>
**Setup (run once per machine):**
```bash
pip3 install neo4j
set -a && source ~/Desktop/tk_projects/skills/.env && set +a
python3 ~/.claude/skills/gtm-brain-skill/scripts/brain.py init
```

**Test connection:**
```bash
set -a && source ~/Desktop/tk_projects/skills/.env && set +a
python3 ~/.claude/skills/gtm-brain-skill/scripts/brain.py ping
```

**Common intents → Stage to jump to:**

| What you say | Stage |
|-------------|-------|
| "what worked with Higher Ed IT Directors?" | Stage 3 — READ: vertical pattern |
| "show me everyone at MIT" | Stage 3 — READ: account map |
| "log call outcome for [contact]" | Stage 4 — WRITE: outcome |
| "add [contact] to the graph" | Stage 4 — WRITE: merge node |
| "which sequence wins Courts deals?" | Stage 3 — READ: sequence perf |
| "ATL coverage on open deals" | Stage 3 — READ: deal map |
| "sync [contact/company] from HubSpot" | Stage 6 — HubSpot sync |
| "import today's Nooks calls" / "sync calls" | Stage 7 — Nooks sync |
</quick_start>

<success_criteria>
- Connection ping returns `{"ok": 1, "msg": "GTM Brain connected"}`
- READ queries return ranked results with vertical/title/outcome breakdown
- WRITE operations confirm node upsert and relationship creation
- No credentials in any file other than skills/.env
- Outcome sidecar written after each session
</success_criteria>

<core_content>

## ENV Helper (prepend to every bash block)

```bash
set -a && source ~/Desktop/tk_projects/skills/.env && set +a
SCRIPT=~/.claude/skills/gtm-brain-skill/scripts/brain.py
# fallback to repo path if deployed path missing:
[ -f "$SCRIPT" ] || SCRIPT=~/Desktop/tk_projects/skills/active/gtm-brain-skill/scripts/brain.py
```

---

## Stage 1 — Connect

Always ping first to confirm Aura is awake (free instances sleep after inactivity):

```bash
set -a && source ~/Desktop/tk_projects/skills/.env && set +a
SCRIPT=~/.claude/skills/gtm-brain-skill/scripts/brain.py
[ -f "$SCRIPT" ] || SCRIPT=~/Desktop/tk_projects/skills/active/gtm-brain-skill/scripts/brain.py
python3 "$SCRIPT" ping
```

Expected: `{"ok": 1, "msg": "GTM Brain connected"}`

If it hangs 60+ seconds → Aura instance was sleeping. Wait 60 seconds and retry.

---

## Stage 2 — Intent Routing

Classify what the user wants:

| Intent | Route |
|--------|-------|
| "what worked", "who responded", "best sequence" | Stage 3 — READ |
| "account map", "everyone at [company]", "contact history" | Stage 3 — READ |
| "ATL coverage", "deal map" | Stage 3 — READ |
| "log outcome", "call result", "add [contact]" | Stage 4 — WRITE |
| "initialize", "setup schema", "first time" | Stage 5 — INIT |
| "sync from HubSpot", "add contact from HS", "pull company" | Stage 6 — HubSpot |
| "import Nooks calls", "sync today's calls", "log calls" | Stage 7 — Nooks |

---

## Stage 3 — READ Queries

Construct the correct Cypher from reference/cypher-patterns.md, then run:

```bash
python3 "$SCRIPT" run "<CYPHER_QUERY>"
```

### Pattern: What worked with vertical + title?

```bash
python3 "$SCRIPT" run "
MATCH (c:Contact {vertical: 'Higher Ed', atl_btl: 'ATL'})-[:HAD]->(o:Outcome {result: 'positive'})
RETURN c.title, o.channel, o.notes, count(*) AS wins
ORDER BY wins DESC LIMIT 10"
```

Format output as a ranked table: Title | Channel | Win count | Best notes sample.

### Pattern: Account map — all contacts + outcomes

```bash
python3 "$SCRIPT" run "
MATCH (c:Contact)-[:WORKS_AT]->(a:Account)
WHERE toLower(a.name) CONTAINS toLower('[COMPANY]')
OPTIONAL MATCH (c)-[:HAD]->(o:Outcome)
RETURN c.name, c.title, c.atl_btl,
       collect({ch: o.channel, r: o.result, n: o.notes}) AS history
ORDER BY c.atl_btl"
```

Format as: Name | Title | Tier | Last outcome.

### Pattern: Sequence performance by vertical

```bash
python3 "$SCRIPT" run "
MATCH (c:Contact {vertical: '[VERTICAL]'})-[:HAD]->(o:Outcome {result: 'positive'})-[:VIA]->(s:Sequence)
RETURN s.name, count(o) AS wins ORDER BY wins DESC LIMIT 5"
```

### Pattern: ATL coverage on open deals

```bash
python3 "$SCRIPT" run "
MATCH (d:Deal) WHERE d.stage NOT IN ['Closed Won','Closed Lost']
MATCH (c:Contact)-[:INVOLVED_IN]->(d)
WITH d, collect(c.atl_btl) AS tiers
RETURN d.name, d.stage, d.amount,
       size([t IN tiers WHERE t='ATL']) AS atl_count, size(tiers) AS total
ORDER BY atl_count ASC"
```

Flag ⚠️ for deals with 0 ATL contacts.

---

## Stage 4 — WRITE Operations

### Log a call or email outcome

When a call/sequence/email completes, write the outcome:

1. Confirm contact exists in graph (merge if not):
```bash
python3 "$SCRIPT" merge-contact \
  '{"hubspot_id":"<HS_ID>","name":"<NAME>","title":"<TITLE>","vertical":"<VERTICAL>","atl_btl":"<TIER>","email":"<EMAIL>"}'
```

2. Log the outcome:
```bash
python3 "$SCRIPT" log-outcome \
  '{"id":"outcome-<YYYYMMDD>-<HS_ID>","contact_hubspot_id":"<HS_ID>","channel":"call","result":"<positive|neutral|negative>","notes":"<what happened>","timestamp":"<ISO8601>","sequence_nooks_id":"<ID_IF_IN_SEQ>"}'
```

### Add / update account

```bash
python3 "$SCRIPT" merge-account \
  '{"hubspot_id":"<HS_ID>","name":"<NAME>","vertical":"<VERTICAL>","icp_score":<SCORE>}'
```

### Wire contact to deal

```bash
python3 "$SCRIPT" run \
  "MATCH (c:Contact {hubspot_id:'<C_ID>'}),(d:Deal {hubspot_id:'<D_ID>'}) \
   MERGE (c)-[:INVOLVED_IN {role:'champion'}]->(d)"
```

### Wire contact to account (if not already set)

```bash
python3 "$SCRIPT" run \
  "MATCH (c:Contact {hubspot_id:'<C_ID>'}),(a:Account {hubspot_id:'<A_ID>'}) \
   MERGE (c)-[:WORKS_AT]->(a)"
```

---

## Stage 5 — Schema Initialization (first time only)

```bash
set -a && source ~/Desktop/tk_projects/skills/.env && set +a
python3 "$SCRIPT" init
```

Creates: uniqueness constraints on all primary keys, indexes on vertical/atl_btl/result.
Safe to re-run (all statements use `IF NOT EXISTS`).

---

## Integration Points

**Other skills that should write outcomes to GTM Brain:**
- `epiphan-call-playbook` — after disposition is logged, call Stage 4 to log outcome
- `sdr-call-coaching` — after scoring a call, log result to graph
- `nooks-autopilot` — after warm handoff, log positive outcome

**Other skills that should read from GTM Brain:**
- `morning-brief-skill` — prepend "who responded before at this vertical" intel
- `sdr-dial-lists` — surface prior positive contacts at target accounts
- `meddic-call-prep-auto-skill` — pull contact history before a call

**Manual workflow until wired:**
Say "log outcome to GTM Brain for [contact]" after any call or email to capture the result.

---

## Stage 6 — HubSpot Sync

Pull a contact and their company from HubSpot and write both to the graph.

**Trigger:** "sync [name] from HubSpot" / "add [company] to graph" / "pull [contact] from HS"

### Step 1 — Fetch contact from HubSpot MCP

Use `hubspot_search_contacts` (Epiphan AI MCP) with the name or email:

```
mcp__claude_ai_Epiphan_Ai__hubspot_search_contacts(query="Jane Smith")
```

Extract from result: `id` (hubspot_id), `firstname`, `lastname`, `jobtitle`, `email`, `phone`, `associatedcompanyid`.

### Step 2 — Classify ATL/BTL from title

Apply the ATL/BTL Classification from CLAUDE.md:
- Match title against Universal ATL Keywords → `ATL`
- Match against BTL / NEVER ATL lists → `BTL` or `NEVER`
- Gray zone → `GRAY`

### Step 3 — Determine vertical

Use `mcp__claude_ai_Epiphan_Ai__qualify_lead` or infer from company name/domain:
Higher Ed → university/college; Courts → court/judicial; Government → city/county/state agency; Healthcare → hospital/health system; Corporate AV → enterprise/corporate.

### Step 4 — Write contact to graph

```bash
python3 "$SCRIPT" merge-contact \
  '{"hubspot_id":"<ID>","name":"<FIRST> <LAST>","title":"<JOBTITLE>","email":"<EMAIL>","phone":"<PHONE>","vertical":"<VERTICAL>","atl_btl":"<TIER>"}'
```

### Step 5 — Fetch and write company

```
mcp__claude_ai_Epiphan_Ai__hubspot_get_company(companyId="<associatedcompanyid>")
```

Extract: `id`, `name`, `domain`, vertical (same logic). Write:

```bash
python3 "$SCRIPT" merge-account \
  '{"hubspot_id":"<CO_ID>","name":"<CO_NAME>","vertical":"<VERTICAL>","domain":"<DOMAIN>","icp_score":80}'
```

Wire the relationship:

```bash
python3 "$SCRIPT" run \
  "MATCH (c:Contact {hubspot_id:'<C_ID>'}),(a:Account {hubspot_id:'<A_ID>'}) MERGE (c)-[:WORKS_AT]->(a)"
```

**Batch sync tip:** "sync everyone at [company] from HubSpot" → `hubspot_search_contacts` with company filter → loop Steps 2-5 for each contact.

---

## Stage 7 — Nooks Call Sync

Import recent Nooks call dispositions as Outcome nodes. Run after a dial session.

**Trigger:** "import today's Nooks calls" / "sync calls to graph" / "log calls from Nooks"

### Step 1 — List recent calls

```
mcp__claude_ai_Nooks__listCalls(filter_owner_id="87486452", filter_time_gte="<TODAY_ISO>")
```

Use Tim's Nooks user ID `87486452`. Returns call list with `id`, `prospectId`, `sequenceId`.

### Step 2 — Get disposition per call

For each call:
```
mcp__claude_ai_Nooks__getCallDisposition(callId="<id>")
```

### Step 3 — Map disposition → result

| Nooks disposition | Graph result |
|------------------|--------------|
| Demo Booked / Interested / Connected-Positive | `positive` |
| Voicemail / No Answer / Callback Requested | `neutral` |
| Not Interested / Wrong Person / DQ / Unsubscribed | `negative` |

### Step 4 — Resolve contact hubspot_id

```
mcp__claude_ai_Nooks__getProspect(prospectId="<id>")
```

Extract `hubspotContactId`. If contact not yet in graph → run Stage 6 sync first.

### Step 5 — Write each call as an Outcome

```bash
python3 "$SCRIPT" log-outcome \
  '{"id":"nooks-<CALL_ID>","contact_hubspot_id":"<HS_ID>","channel":"call","result":"<positive|neutral|negative>","notes":"<disposition label + any call notes>","timestamp":"<call_start_time>","sequence_nooks_id":"<SEQ_ID_IF_SET>"}'
```

Process all calls in the batch. Report: N calls imported, breakdown by result (X positive / Y neutral / Z negative).

</core_content>

## Emit Outcome Sidecar

Write to `~/.claude/skill-analytics/last-outcome-gtm-brain.json`:

```json
{
  "ts": "<ISO-8601>",
  "skill": "gtm-brain",
  "version": "1.0.0",
  "variant": "control",
  "status": "<success|partial|error>",
  "runtime_ms": <int>,
  "metrics": {
    "intent": "<read|write|init|ping>",
    "nodes_written": <int>,
    "rows_returned": <int>,
    "vertical": "<if applicable>"
  },
  "error": null,
  "session_id": "<YYYY-MM-DD>"
}
```
