# SQL Analytics Templates

SQL query templates for HubSpot data warehouse analytics. Adjust table names and schema prefix to match your ETL configuration.

---

## Schema Discovery

Run these first to understand your warehouse layout:

```sql
-- List all HubSpot tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'hubspot'
ORDER BY table_name;

-- Inspect columns for a specific table
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'hubspot'
  AND table_name = 'contacts'
ORDER BY ordinal_position;

-- Check data freshness (last sync timestamp)
SELECT MAX(_fivetran_synced) AS last_sync
FROM hubspot.contacts;
```

---

## UC1: ICP Validation

Segment contacts by company attributes, measure conversion rates per segment.

```sql
-- ICP segment conversion rates
WITH contact_company AS (
    SELECT
        c.contact_id,
        c.lifecycle_stage,
        co.industry,
        co.numberofemployees AS employee_count,
        co.annualrevenue AS annual_revenue,
        CASE
            WHEN co.numberofemployees >= 500 THEN 'Enterprise'
            WHEN co.numberofemployees >= 50  THEN 'Mid-Market'
            ELSE 'SMB'
        END AS company_segment
    FROM hubspot.contacts c
    JOIN hubspot.contact_company_associations cca
        ON c.contact_id = cca.contact_id
    JOIN hubspot.companies co
        ON cca.company_id = co.company_id
),
segment_metrics AS (
    SELECT
        company_segment,
        industry,
        COUNT(*) AS total_leads,
        COUNT(*) FILTER (WHERE lifecycle_stage = 'customer') AS customers,
        ROUND(
            100.0 * COUNT(*) FILTER (WHERE lifecycle_stage = 'customer') / NULLIF(COUNT(*), 0),
            1
        ) AS conversion_rate_pct
    FROM contact_company
    GROUP BY company_segment, industry
)
SELECT *
FROM segment_metrics
WHERE total_leads >= 10
ORDER BY conversion_rate_pct DESC;
```

---

## UC2: Pipeline Velocity

Measure time spent in each deal stage, identify bottlenecks.

```sql
-- Stage duration analysis
WITH stage_transitions AS (
    SELECT
        deal_id,
        stage_name,
        entered_at,
        LEAD(entered_at) OVER (PARTITION BY deal_id ORDER BY entered_at) AS exited_at
    FROM hubspot.deal_stage_history
),
stage_durations AS (
    SELECT
        deal_id,
        stage_name,
        -- Postgres
        EXTRACT(EPOCH FROM (exited_at - entered_at)) / 86400.0 AS days_in_stage
        -- Snowflake: DATEDIFF('day', entered_at, exited_at) AS days_in_stage
        -- BigQuery: DATE_DIFF(exited_at, entered_at, DAY) AS days_in_stage
    FROM stage_transitions
    WHERE exited_at IS NOT NULL
)
SELECT
    stage_name,
    COUNT(*) AS deals,
    ROUND(AVG(days_in_stage), 1) AS avg_days,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days_in_stage), 1) AS median_days,
    ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY days_in_stage), 1) AS p90_days
FROM stage_durations
GROUP BY stage_name
ORDER BY avg_days DESC;

-- Stage conversion rates
SELECT
    stage_name,
    COUNT(*) AS entered,
    COUNT(*) FILTER (WHERE next_stage IS NOT NULL) AS advanced,
    ROUND(100.0 * COUNT(*) FILTER (WHERE next_stage IS NOT NULL) / NULLIF(COUNT(*), 0), 1)
        AS advancement_rate_pct
FROM (
    SELECT
        deal_id,
        stage_name,
        LEAD(stage_name) OVER (PARTITION BY deal_id ORDER BY entered_at) AS next_stage
    FROM hubspot.deal_stage_history
) sub
GROUP BY stage_name
ORDER BY advancement_rate_pct;
```

---

## UC3: Competitive Win/Loss

Extract competitor mentions from closed-lost reasons, build win/loss matrix.

```sql
-- Competitor win/loss analysis (parameterized)
WITH competitor_deals AS (
    SELECT
        d.deal_id,
        d.dealname,
        d.amount,
        d.dealstage,
        d.closed_lost_reason,
        CASE
            WHEN LOWER(d.closed_lost_reason) LIKE '%[COMPETITOR_1]%' THEN '[COMPETITOR_1]'
            WHEN LOWER(d.closed_lost_reason) LIKE '%[COMPETITOR_2]%' THEN '[COMPETITOR_2]'
            WHEN LOWER(d.closed_lost_reason) LIKE '%[COMPETITOR_3]%' THEN '[COMPETITOR_3]'
            WHEN d.dealstage = 'closedlost' THEN 'Other/Unknown'
            ELSE NULL
        END AS competitor
    FROM hubspot.deals d
    WHERE d.dealstage IN ('closedwon', 'closedlost')
      AND d.closedate >= CURRENT_DATE - INTERVAL '12 months'
)
SELECT
    competitor,
    COUNT(*) FILTER (WHERE dealstage = 'closedwon') AS wins,
    COUNT(*) FILTER (WHERE dealstage = 'closedlost') AS losses,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE dealstage = 'closedwon')
        / NULLIF(COUNT(*), 0), 1
    ) AS win_rate_pct,
    ROUND(AVG(amount) FILTER (WHERE dealstage = 'closedwon'), 0) AS avg_won_deal,
    ROUND(SUM(amount) FILTER (WHERE dealstage = 'closedlost'), 0) AS revenue_lost
FROM competitor_deals
WHERE competitor IS NOT NULL
GROUP BY competitor
ORDER BY losses DESC;
```

**Usage:** Replace `[COMPETITOR_1]`, `[COMPETITOR_2]`, `[COMPETITOR_3]` with actual competitor names.

---

## UC4: Activity-to-Outcome Analysis

Correlate engagement activities with deal outcomes.

```sql
-- Activity patterns for won vs lost deals
WITH deal_activities AS (
    SELECT
        d.deal_id,
        d.dealstage,
        d.amount,
        COUNT(e.engagement_id) FILTER (WHERE e.type = 'EMAIL') AS emails_sent,
        COUNT(e.engagement_id) FILTER (WHERE e.type = 'MEETING') AS meetings_held,
        COUNT(e.engagement_id) FILTER (WHERE e.type = 'CALL') AS calls_made,
        COUNT(e.engagement_id) AS total_activities
    FROM hubspot.deals d
    LEFT JOIN hubspot.deal_contact_associations dca
        ON d.deal_id = dca.deal_id
    LEFT JOIN hubspot.engagements e
        ON dca.contact_id = e.contact_id
        AND e.created_at BETWEEN d.createdate AND COALESCE(d.closedate, CURRENT_TIMESTAMP)
    WHERE d.dealstage IN ('closedwon', 'closedlost')
    GROUP BY d.deal_id, d.dealstage, d.amount
)
SELECT
    dealstage,
    COUNT(*) AS deals,
    ROUND(AVG(emails_sent), 1) AS avg_emails,
    ROUND(AVG(meetings_held), 1) AS avg_meetings,
    ROUND(AVG(calls_made), 1) AS avg_calls,
    ROUND(AVG(total_activities), 1) AS avg_total_activities
FROM deal_activities
GROUP BY dealstage;
```

---

## UC5: Weighted Pipeline Forecast

Forecast revenue using stage-specific historical win rates.

```sql
-- Historical win rate by stage (training data)
WITH stage_outcomes AS (
    SELECT
        dsh.stage_name,
        d.dealstage AS final_outcome,
        d.amount
    FROM hubspot.deal_stage_history dsh
    JOIN hubspot.deals d ON dsh.deal_id = d.deal_id
    WHERE d.dealstage IN ('closedwon', 'closedlost')
      AND d.closedate >= CURRENT_DATE - INTERVAL '12 months'
)
SELECT
    stage_name,
    COUNT(*) AS total_deals,
    ROUND(100.0 * COUNT(*) FILTER (WHERE final_outcome = 'closedwon') / NULLIF(COUNT(*), 0), 1)
        AS historical_win_rate_pct
FROM stage_outcomes
GROUP BY stage_name
ORDER BY historical_win_rate_pct DESC;

-- Weighted forecast for open pipeline
WITH stage_win_rates AS (
    -- ... (use query above as CTE or materialized view)
    SELECT stage_name, historical_win_rate_pct / 100.0 AS win_rate
    FROM historical_stage_rates
)
SELECT
    d.pipeline,
    d.dealstage,
    o.email AS owner,
    COUNT(*) AS open_deals,
    ROUND(SUM(d.amount), 0) AS total_pipeline,
    ROUND(SUM(d.amount * COALESCE(swr.win_rate, 0.1)), 0) AS weighted_forecast
FROM hubspot.deals d
LEFT JOIN stage_win_rates swr ON d.dealstage = swr.stage_name
LEFT JOIN hubspot.owners o ON d.hubspot_owner_id = o.owner_id
WHERE d.dealstage NOT IN ('closedwon', 'closedlost')
GROUP BY d.pipeline, d.dealstage, o.email
ORDER BY weighted_forecast DESC;
```

---

## SQL Dialect Notes

| Operation | Postgres | Snowflake | BigQuery |
|-----------|----------|-----------|----------|
| Date diff (days) | `EXTRACT(EPOCH FROM (b - a)) / 86400` | `DATEDIFF('day', a, b)` | `DATE_DIFF(b, a, DAY)` |
| Current date | `CURRENT_DATE` | `CURRENT_DATE()` | `CURRENT_DATE()` |
| Interval | `INTERVAL '30 days'` | `DATEADD('day', -30, CURRENT_DATE())` | `DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)` |
| Conditional count | `COUNT(*) FILTER (WHERE ...)` | `COUNT_IF(...)` | `COUNTIF(...)` |
| Percentile | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` | `PERCENTILE_CONT(x, 0.5) OVER()` |
| String match | `LIKE '%text%'` | `ILIKE '%text%'` | `LOWER(col) LIKE '%text%'` |
| Null coalesce | `COALESCE(a, b)` | `COALESCE(a, b)` | `IFNULL(a, b)` or `COALESCE` |
