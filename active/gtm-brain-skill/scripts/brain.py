#!/usr/bin/env python3
"""
GTM Brain — Neo4j query runner.
Usage: python3 neo4j.py <command> [cypher] [params_json]
Commands: ping | init | run | merge-contact | merge-account | merge-deal | log-outcome
Reads NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE from environment.
"""
import os, sys, json
from neo4j import GraphDatabase

URI  = os.environ['NEO4J_URI']
AUTH = (os.environ['NEO4J_USERNAME'], os.environ['NEO4J_PASSWORD'])
DB   = os.environ['NEO4J_DATABASE']

def get_driver():
    return GraphDatabase.driver(URI, auth=AUTH)

def run_query(cypher, params=None):
    with get_driver() as driver:
        with driver.session(database=DB) as session:
            result = session.run(cypher, params or {})
            return [dict(r) for r in result]

def ping():
    rows = run_query("RETURN 1 AS ok, 'GTM Brain connected' AS msg")
    print(json.dumps(rows[0]))

def init_schema():
    """Create uniqueness constraints and indexes."""
    stmts = [
        "CREATE CONSTRAINT contact_id IF NOT EXISTS FOR (c:Contact) REQUIRE c.hubspot_id IS UNIQUE",
        "CREATE CONSTRAINT account_id IF NOT EXISTS FOR (a:Account) REQUIRE a.hubspot_id IS UNIQUE",
        "CREATE CONSTRAINT deal_id    IF NOT EXISTS FOR (d:Deal)    REQUIRE d.hubspot_id IS UNIQUE",
        "CREATE CONSTRAINT outcome_id IF NOT EXISTS FOR (o:Outcome) REQUIRE o.id IS UNIQUE",
        "CREATE CONSTRAINT sequence_id IF NOT EXISTS FOR (s:Sequence) REQUIRE s.nooks_id IS UNIQUE",
        "CREATE INDEX contact_vertical IF NOT EXISTS FOR (c:Contact) ON (c.vertical)",
        "CREATE INDEX contact_atl      IF NOT EXISTS FOR (c:Contact) ON (c.atl_btl)",
        "CREATE INDEX outcome_result   IF NOT EXISTS FOR (o:Outcome) ON (o.result)",
    ]
    with get_driver() as driver:
        with driver.session(database=DB) as session:
            for s in stmts:
                session.run(s)
    print(json.dumps({"status": "schema initialized", "statements": len(stmts)}))

def merge_contact(props):
    """Upsert a Contact node. props must include hubspot_id."""
    cypher = """
    MERGE (c:Contact {hubspot_id: $hubspot_id})
    SET c += $props
    RETURN c.hubspot_id AS id, c.name AS name
    """
    rows = run_query(cypher, {"hubspot_id": props["hubspot_id"], "props": props})
    print(json.dumps(rows[0] if rows else {}))

def merge_account(props):
    cypher = """
    MERGE (a:Account {hubspot_id: $hubspot_id})
    SET a += $props
    RETURN a.hubspot_id AS id, a.name AS name
    """
    rows = run_query(cypher, {"hubspot_id": props["hubspot_id"], "props": props})
    print(json.dumps(rows[0] if rows else {}))

def merge_deal(props):
    cypher = """
    MERGE (d:Deal {hubspot_id: $hubspot_id})
    SET d += $props
    RETURN d.hubspot_id AS id, d.name AS name
    """
    rows = run_query(cypher, {"hubspot_id": props["hubspot_id"], "props": props})
    print(json.dumps(rows[0] if rows else {}))

def log_outcome(props):
    """
    Write an Outcome node and link it to Contact (and optionally Sequence).
    props: {id, contact_hubspot_id, channel, result, notes, timestamp, sequence_nooks_id?}
    """
    cypher = """
    MERGE (o:Outcome {id: $id})
    SET o.channel   = $channel,
        o.result    = $result,
        o.notes     = $notes,
        o.timestamp = $timestamp
    WITH o
    MATCH (c:Contact {hubspot_id: $contact_id})
    MERGE (c)-[:HAD]->(o)
    RETURN o.id AS outcome_id, c.name AS contact
    """
    params = {
        "id":         props["id"],
        "channel":    props.get("channel", "unknown"),
        "result":     props.get("result", "neutral"),
        "notes":      props.get("notes", ""),
        "timestamp":  props.get("timestamp", ""),
        "contact_id": props["contact_hubspot_id"],
    }
    rows = run_query(cypher, params)

    # Optionally link to Sequence
    if props.get("sequence_nooks_id"):
        seq_cypher = """
        MERGE (s:Sequence {nooks_id: $nooks_id})
        SET s.name = $seq_name
        WITH s
        MATCH (o:Outcome {id: $outcome_id})
        MERGE (o)-[:VIA]->(s)
        """
        run_query(seq_cypher, {
            "nooks_id":   props["sequence_nooks_id"],
            "seq_name":   props.get("sequence_name", ""),
            "outcome_id": props["id"],
        })

    print(json.dumps(rows[0] if rows else {}))

def run_cypher(cypher, params=None):
    rows = run_query(cypher, params)
    print(json.dumps(rows, default=str))

# ── CLI dispatch ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ping"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}

    dispatch = {
        "ping":          lambda: ping(),
        "init":          lambda: init_schema(),
        "run":           lambda: run_cypher(arg, params),
        "merge-contact": lambda: merge_contact(json.loads(arg)),
        "merge-account": lambda: merge_account(json.loads(arg)),
        "merge-deal":    lambda: merge_deal(json.loads(arg)),
        "log-outcome":   lambda: log_outcome(json.loads(arg)),
    }
    fn = dispatch.get(cmd)
    if fn:
        fn()
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
