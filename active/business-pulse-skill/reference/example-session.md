# Example session — business-pulse

**Prompt:** "give me the business pulse"

**Step 1 — one-shot brief**
```
weekly_brief({})
```
(Returns the bundled revenue/pipeline/BDR JSON.)

**Step 2 — one deeper cut for stage detail**
```
query_dataset({ dataset: "pipeline_open", group_by: ["stage"] })
```

**Step 3 — synthesized output (illustrative shape, NOT real numbers):**
```
BUSINESS PULSE — week ending 2026-06-14

PACE        YTD $12.1M of $19.5M target  →  62% of FY pace   [Behind ~4 pts]
REVENUE     Week $310K · MTD $1.4M · QTD $3.9M · YoY +11%
PIPELINE    $8.7M open across 214 deals
            Discovery $4.1M · Demo $1.9M · Proposal $1.5M · Commit $1.2M
WON / LOST  Won 9 ($412K) · Lost 4 ($96K) this period
BDR         Tim: 1,139 dials / 84 connects / 11 meetings · Ron: <…>
TOP MOVERS  UIUC 50-room ($123K) → Proposal · Waterloo Nexus ($40K) slipping

SO WHAT
 1. 47% of open $ is stuck in Discovery — the gap is economic-buyer contact, not activity.
    Pick the top 5 Discovery deals and thread up to a Director this week.
 2. HigherEd is carrying pace; Community College is under-penetrated vs the blue-ocean thesis —
    run greenfield-pearl-tracker for CC/Broadcast signals.
 3. Lost deals skew single-threaded — enforce "no quote on a single sub-Manager thread."
```

**Note:** vertical lines (HigherEd / CC) are *derived* (proxy/enrichment), flagged approximate —
there is no native vertical dataset dimension.
