# Architecture

Full-stack architecture for HubSpot revenue analytics infrastructure.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ HubSpot  │ Clay MCP │ Website  │ Product  │ External APIs      │
│ CRM API  │ Enrichmt │ Analytics│ Usage    │ (ZoomInfo, etc.)   │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────┬─────────────┘
     │          │          │          │            │
     ▼          ▼          ▼          ▼            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ Fivetran │ Airbyte  │ GitHub   │ Webhooks │ Cron Jobs          │
│ (ETL)    │ (ETL)    │ Actions  │          │                    │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────┬─────────────┘
     │          │          │          │            │
     ▼          ▼          ▼          ▼            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SQL DATA WAREHOUSE                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ contacts │  │ companies│  │  deals   │  │ engagements   │  │
│  │          │  │          │  │          │  │               │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
│  Snowflake / BigQuery / Postgres / Redshift                     │
└────┬────────────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE PRODUCTS                         │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ ICP      │ Lead     │ Compet.  │ Activity │ Pipeline           │
│ Analysis │ Scoring  │ Intel    │ Analysis │ Forecast           │
│ (UC1)    │ (UC2)    │ (UC3)    │ (UC4)    │ (UC5)              │
└──────────┴──────────┴──────────┴──────────┴────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DELIVERY LAYER                             │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│ HubSpot  │ Slack    │ Streamlit│ CSV/     │ Webhook            │
│ Custom   │ Alerts   │ Dashbd   │ Reports  │ Triggers           │
│ Props    │          │          │          │                    │
└──────────┴──────────┴──────────┴──────────┴────────────────────┘
```

---

## Deployment Options

### Option A: GitHub Actions (Recommended Start)

Best for: Nightly batch processing, low cost, easy setup.

```
GitHub Actions (cron) → Python scripts → SQL warehouse + HubSpot API
```

- **Cost:** Free tier (2,000 min/month)
- **Latency:** Batch (daily/hourly)
- **Setup:** 1-2 hours

### Option B: Vercel Serverless

Best for: Webhook handlers, real-time competitive alerts.

```
HubSpot Webhooks → Vercel API Routes → Processing → Slack/HubSpot
```

- **Cost:** $0-20/month (Hobby-Pro)
- **Latency:** Real-time (<5s)
- **Setup:** 2-4 hours

### Option C: Full Stack (Production)

Best for: Complete analytics platform, multiple dashboards.

```
ETL (Fivetran) → Warehouse → dbt transforms → Streamlit dashboard
                                             → API endpoints (Vercel)
                                             → ML scoring (GitHub Actions)
```

- **Cost:** $75-200/month
- **Latency:** Near real-time to daily
- **Setup:** 1-2 weeks

---

## Cost Estimates by Tier

| Tier | Components | Monthly Cost |
|------|-----------|-------------|
| **Free** | HubSpot Free CRM + GitHub Actions + local Postgres | $0 |
| **Starter** | HubSpot Starter + Fivetran Free + Snowflake trial | ~$25 |
| **Growth** | HubSpot Pro + Fivetran Standard + Snowflake + Clay | ~$75-150 |
| **Scale** | HubSpot Enterprise + full ETL + dedicated warehouse | ~$200-500+ |

### Cost Breakdown

| Service | Free Tier | Paid |
|---------|-----------|------|
| HubSpot CRM | Free (up to 1M contacts) | $45-800/month (Starter-Enterprise) |
| Fivetran | 500k rows/month free | $120+/month |
| Snowflake | $2/credit (trial credits) | Pay per query |
| Clay | 100 credits/month free | $149+/month |
| GitHub Actions | 2,000 min/month | $0.008/min |
| Vercel | Hobby free | $20/month Pro |

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| SQL replica access denied by IT | Blocks all analytics | Start with HubSpot API + Search; escalate with ROI case |
| ETL schema changes break queries | Dashboard downtime | Pin table versions, add schema validation tests |
| HubSpot API rate limits hit | Enrichment delays | Use batch endpoints, implement exponential backoff |
| ML model drift | Inaccurate scores | Monthly retrain, track AUC-ROC, alert on score distribution shift |
| Clay enrichment overspend | Budget blowout | Set monthly caps in Clay UI, track via cost-metering-skill |
| Data freshness lag | Stale analytics | Monitor sync timestamps, alert if >24h stale |
| Political: sales team resists scoring | Low adoption | Start with shadow scoring (don't show to reps), prove with A/B test |

---

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| CRM | HubSpot (API + Private App) | Source of truth for contacts, deals, activities |
| ETL | Fivetran / Airbyte | HubSpot → Warehouse sync |
| Warehouse | Snowflake / BigQuery / Postgres | SQL analytics |
| ML | scikit-learn (GBM) | Lead scoring |
| Enrichment | Clay MCP | Contact/company enrichment |
| Automation | GitHub Actions | Nightly jobs, scoring, alerts |
| Dashboards | Streamlit / data-analysis-skill | Visualization |
| Alerts | Slack webhooks | Real-time notifications |
| Deployment | Vercel | Webhook handlers, API routes |
