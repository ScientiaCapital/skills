---
name: hubspot-revops-skill
description: Use when building revenue analytics on HubSpot — SQL warehouse queries,
  API enrichment pipelines, lead scoring models, pipeline forecasting, competitive
  intelligence. Triggers on "hubspot analytics", "revops dashboard", "lead scoring",
  "pipeline forecast", "ICP analysis", "hubspot SQL".
---

# HubSpot RevOps Analytics

Revenue analytics infrastructure on HubSpot API + SQL data warehouse.
Bridges CRM data → analytics → intelligence products → revenue impact.

**Scope:** HubSpot-specific analytics stack. For basic CRM CRUD, use `crm-integration-skill`. For generic dashboards, use `data-analysis-skill`.

---

## Setup Checklist

### 1. HubSpot Private App

Create at Settings → Integrations → Private Apps:

| Scope | Permission | Why |
|-------|-----------|-----|
| `crm.objects.contacts.read/write` | Read/Write | Contact enrichment |
| `crm.objects.companies.read` | Read | Company data |
| `crm.objects.deals.read/write` | Read/Write | Pipeline analytics |
| `crm.schemas.custom.read` | Read | Custom objects |
| `crm.objects.owners.read` | Read | Rep attribution |
| `timeline` | Read | Activity data |

### 2. SQL Replica Access

Discovery questions for your data warehouse:

| Question | Options |
|----------|---------|
| Where is HubSpot data replicated? | Snowflake / BigQuery / Postgres / Redshift |
| What ETL tool syncs it? | Fivetran / Airbyte / Stitch / HubSpot Data Sync |
| Sync frequency? | Real-time / Hourly / Daily |
| Schema prefix? | `hubspot.` / `raw_hubspot.` / custom |

### 3. Python Environment

```bash
pip install hubspot-api-client pandas scikit-learn requests
```

```python
# SDK initialization
from hubspot import HubSpot
client = HubSpot(access_token="pat-na1-xxxxx")

# Or raw requests
import requests
HEADERS = {"Authorization": "Bearer pat-na1-xxxxx", "Content-Type": "application/json"}
BASE = "https://api.hubapi.com"
```

---

## Core Use Cases

| # | Use Case | Input | Output | Tools |
|---|----------|-------|--------|-------|
| 1 | ICP Validation | Contact + company data | Segment conversion rates | SQL + Clay |
| 2 | Lead Scoring | Historical deals | Win probability per lead | SQL + ML + API |
| 3 | Competitive Intel | Deal close reasons | Win/loss by competitor | SQL + webhook |
| 4 | Activity Analysis | Engagement data | Activity→outcome correlation | SQL |
| 5 | Pipeline Forecast | Open deals + stage history | Weighted revenue forecast | SQL |

### Use Case Details

**UC1 — ICP Validation:** Join contacts + companies + deals in SQL, segment by industry/size/geo, compute conversion rates per segment. Feed results to Clay for enrichment writeback.

**UC2 — Lead Scoring:** Train GradientBoostingClassifier on historical won/lost deals. Features: company size, industry, engagement score, days in pipeline. Deploy scores back to HubSpot as custom property.

**UC3 — Competitive Intel:** Extract competitor mentions from deal `closed_lost_reason`. Build win/loss matrix by competitor. Trigger webhook alerts on competitive displacement patterns.

**UC4 — Activity Analysis:** Correlate email opens, meetings booked, calls logged with deal outcomes. Identify which activities actually move deals forward.

**UC5 — Pipeline Forecast:** Calculate weighted forecast using stage-specific win rates from historical data. Factor in deal age, velocity, and rep performance.

> **Reference:** See `reference/sql-analytics.md` for complete SQL templates per use case.

---

## Quick Reference: HubSpot API Endpoints

| Object | Endpoint | Key Operations |
|--------|----------|----------------|
| Contacts | `/crm/v3/objects/contacts` | Search, create, update, batch |
| Companies | `/crm/v3/objects/companies` | Search, associate to contacts |
| Deals | `/crm/v3/objects/deals` | Pipeline, stage history |
| Engagements | `/crm/v3/objects/engagements` | Emails, calls, meetings |
| Properties | `/crm/v3/properties/{object}` | Custom property CRUD |
| Associations | `/crm/v4/associations/{from}/{to}` | Object linking |
| Search | `/crm/v3/objects/{object}/search` | Filter + sort (max 10k) |

> **Reference:** See `reference/api-guide.md` for auth, SDK patterns, batch operations.

---

## Quick Reference: SQL Object Model

| HubSpot Object | SQL Table (typical) | Key Columns | Join Key |
|----------------|---------------------|-------------|----------|
| Contacts | `hubspot.contacts` | email, lifecycle_stage, lead_score | contact_id |
| Companies | `hubspot.companies` | domain, industry, employee_count | company_id |
| Deals | `hubspot.deals` | amount, stage, close_date, pipeline | deal_id |
| Deal Stages | `hubspot.deal_stage_history` | stage, timestamp, duration | deal_id |
| Engagements | `hubspot.engagements` | type, created_at, contact_id | engagement_id |
| Owners | `hubspot.owners` | email, first_name, team | owner_id |

**Join pattern:** contacts → associations → companies/deals (via association tables)

---

## Integration Points

| Skill | Relationship |
|-------|-------------|
| `crm-integration-skill` | Base CRUD patterns, auth setup |
| `data-analysis-skill` | Visualization, Streamlit dashboards |
| `sales-revenue-skill` | Pipeline metrics, MEDDIC context, forecasting |
| `research-skill` | Market/competitive research methodology |
| `cost-metering-skill` | Track API calls + Clay enrichment spend |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Exceeding 100 requests/10s rate limit | Use batch endpoints, add exponential backoff |
| Using Search API for >10k results | Switch to SQL warehouse for bulk analytics |
| Hardcoded property internal names | Fetch property definitions first: `GET /crm/v3/properties/{object}` |
| Missing association API for object links | Use v4 associations: `POST /crm/v4/associations/{from}/{to}/batch/read` |
| SQL `DATEDIFF` in Postgres | Use `AGE()` or `EXTRACT(EPOCH FROM ...)` — see dialect notes |
| Not handling HubSpot's `hs_object_id` | Always include `hs_object_id` in property requests |
| Clay enrichment without dedup | Check existing property values before writeback |
| Scoring model trained on small dataset | Need 200+ closed deals minimum for reliable ML scores |

---

## Workflow Phases

### Phase 1: Foundation
1. Set up Private App with required scopes
2. Confirm SQL replica access and schema
3. Run schema discovery queries
4. Validate data freshness (sync lag)

### Phase 2: Analytics
5. Build ICP validation queries (UC1)
6. Create pipeline velocity dashboard (UC2, UC5)
7. Set up competitive intelligence tracking (UC3)

### Phase 3: Intelligence
8. Train lead scoring model on historical deals
9. Deploy scores to HubSpot via API
10. Build enrichment pipelines (Clay → HubSpot)
11. Set up automated alerts and webhooks

> **Reference:** See `reference/enrichment-pipelines.md` for ML scoring and Clay integration.
> **Reference:** See `reference/architecture.md` for deployment patterns and cost estimates.
