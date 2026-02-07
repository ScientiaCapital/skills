# Enrichment Pipelines

Automated data enrichment workflows: Clay → HubSpot writeback, ML lead scoring, competitive alerts.

---

## Clay → HubSpot Writeback

Use Clay MCP to enrich contacts, then write results back to HubSpot custom properties.

### Pattern: Enrich + Writeback

```python
import os
import requests
from hubspot import HubSpot
from hubspot.crm.contacts import BatchInputSimplePublicObjectBatchInput
import time

client = HubSpot(access_token=os.environ["HUBSPOT_ACCESS_TOKEN"])

def enrich_and_writeback(contact_ids: list[str], enrichment_data: dict):
    """
    Write Clay enrichment results back to HubSpot.

    Args:
        contact_ids: HubSpot contact IDs to update
        enrichment_data: Dict mapping contact_id -> enrichment properties
    """
    updates = []
    for cid in contact_ids:
        if cid in enrichment_data:
            data = enrichment_data[cid]
            updates.append({
                "id": cid,
                "properties": {
                    "icp_segment": data.get("icp_tier", ""),
                    "enrichment_source": "clay",
                    "last_enriched_at": data.get("enriched_at", ""),
                    "company_tech_stack": data.get("tech_stack", ""),
                    "estimated_arr": str(data.get("estimated_arr", "")),
                }
            })

    # Batch update in chunks of 100
    for i in range(0, len(updates), 100):
        batch = updates[i:i + 100]
        client.crm.contacts.batch_api.update(
            BatchInputSimplePublicObjectBatchInput(inputs=batch)
        )
        time.sleep(1)  # Rate limit buffer

    return len(updates)
```

### Deduplication Check

Always check existing values before overwriting:

```python
def needs_enrichment(contact: dict, max_age_days: int = 30) -> bool:
    """Check if contact needs re-enrichment."""
    props = contact.get("properties", {})

    # Never enriched
    if not props.get("last_enriched_at"):
        return True

    # Stale enrichment
    from datetime import datetime, timedelta
    last = datetime.fromisoformat(props["last_enriched_at"])
    if datetime.now() - last > timedelta(days=max_age_days):
        return True

    return False
```

---

## ML Lead Scoring Pipeline

### Step 1: Extract Training Data (SQL)

```sql
-- Training dataset: closed deals with features
SELECT
    c.contact_id,
    co.numberofemployees AS employee_count,
    co.industry,
    co.annualrevenue AS annual_revenue,
    COUNT(e.engagement_id) AS total_engagements,
    COUNT(e.engagement_id) FILTER (WHERE e.type = 'EMAIL') AS email_count,
    COUNT(e.engagement_id) FILTER (WHERE e.type = 'MEETING') AS meeting_count,
    EXTRACT(EPOCH FROM (d.closedate - d.createdate)) / 86400.0 AS days_in_pipeline,
    CASE WHEN d.dealstage = 'closedwon' THEN 1 ELSE 0 END AS won
FROM hubspot.contacts c
JOIN hubspot.contact_company_associations cca ON c.contact_id = cca.contact_id
JOIN hubspot.companies co ON cca.company_id = co.company_id
JOIN hubspot.deal_contact_associations dca ON c.contact_id = dca.contact_id
JOIN hubspot.deals d ON dca.deal_id = d.deal_id
LEFT JOIN hubspot.engagements e ON c.contact_id = e.contact_id
WHERE d.dealstage IN ('closedwon', 'closedlost')
  AND d.closedate >= CURRENT_DATE - INTERVAL '18 months'
GROUP BY c.contact_id, co.numberofemployees, co.industry,
         co.annualrevenue, d.closedate, d.createdate, d.dealstage;
```

### Step 2: Train Model

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load training data
df = pd.read_csv("training_data.csv")  # or pd.read_sql(query, conn)

# Feature engineering
le = LabelEncoder()
df["industry_encoded"] = le.fit_transform(df["industry"].fillna("Unknown"))

features = [
    "employee_count", "annual_revenue", "industry_encoded",
    "total_engagements", "email_count", "meeting_count", "days_in_pipeline"
]
X = df[features].fillna(0)
y = df["won"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train GBM
model = GradientBoostingClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.1,
    min_samples_leaf=10,
    random_state=42
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
print(classification_report(y_test, y_pred))
print(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.3f}")

# Feature importance
for feat, imp in sorted(zip(features, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat}: {imp:.3f}")

# Save model
joblib.dump(model, "lead_scoring_model.pkl")
joblib.dump(le, "industry_encoder.pkl")
```

**Minimum data requirements:**
- 200+ closed deals (won + lost combined)
- AUC-ROC > 0.70 for production deployment
- Retrain monthly or when win rate shifts >5%

### Step 3: Score and Deploy

```python
import joblib

model = joblib.load("lead_scoring_model.pkl")
le = joblib.load("industry_encoder.pkl")

def score_contact(contact: dict) -> int:
    """Score a single contact (0-100)."""
    features = pd.DataFrame([{
        "employee_count": contact.get("employee_count", 0),
        "annual_revenue": contact.get("annual_revenue", 0),
        "industry_encoded": le.transform([contact.get("industry", "Unknown")])[0],
        "total_engagements": contact.get("total_engagements", 0),
        "email_count": contact.get("email_count", 0),
        "meeting_count": contact.get("meeting_count", 0),
        "days_in_pipeline": contact.get("days_in_pipeline", 0),
    }])
    probability = model.predict_proba(features)[0][1]
    return int(probability * 100)

def deploy_scores(scored_contacts: list[dict]):
    """Write ML scores to HubSpot."""
    updates = [
        {"id": c["contact_id"], "properties": {"lead_score_ml": str(c["score"])}}
        for c in scored_contacts
    ]
    # Use batch_update_with_backoff from api-guide.md
    batch_update_with_backoff(client, updates)
```

---

## Competitive Displacement Workflow

Automated alerting when deals are lost to specific competitors.

```python
def handle_deal_closed_lost(deal_id: str):
    """Analyze closed-lost deal for competitive intel."""
    deal = client.crm.deals.basic_api.get_by_id(
        deal_id,
        properties=["dealname", "amount", "closed_lost_reason", "hubspot_owner_id"]
    )
    reason = (deal.properties.get("closed_lost_reason") or "").lower()

    competitors = ["[COMPETITOR_1]", "[COMPETITOR_2]", "[COMPETITOR_3]"]
    detected = [c for c in competitors if c.lower() in reason]

    if detected:
        alert = {
            "deal": deal.properties["dealname"],
            "amount": deal.properties.get("amount", "unknown"),
            "competitor": detected[0],
            "reason": deal.properties.get("closed_lost_reason"),
            "owner": deal.properties.get("hubspot_owner_id"),
        }
        send_slack_alert(alert)  # Implement with your Slack webhook
        log_competitive_loss(alert)  # Store for trend analysis

    return detected
```

---

## Nightly Enrichment Job

GitHub Actions cron for automated enrichment:

```yaml
# .github/workflows/hubspot-enrichment.yml
name: Nightly HubSpot Enrichment
on:
  schedule:
    - cron: '0 6 * * *'  # 6am UTC daily
  workflow_dispatch:

jobs:
  enrich:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install hubspot-api-client pandas scikit-learn requests

      - name: Run enrichment
        env:
          HUBSPOT_ACCESS_TOKEN: ${{ secrets.HUBSPOT_ACCESS_TOKEN }}
        run: python scripts/nightly_enrichment.py

      - name: Run scoring
        env:
          HUBSPOT_ACCESS_TOKEN: ${{ secrets.HUBSPOT_ACCESS_TOKEN }}
        run: python scripts/score_pipeline.py
```

---

## Cost Tracking

Track enrichment spend to avoid surprise bills:

| Service | Unit | Cost | Monthly Cap |
|---------|------|------|-------------|
| Clay enrichments | per contact | ~$0.02-0.10 | Set in Clay UI |
| HubSpot API | per request | Free (rate limited) | N/A |
| ML scoring compute | per batch | ~$0.001 | Negligible |
| Warehouse queries | per TB scanned | Varies by provider | Set in warehouse |

```python
# Simple cost tracker
import json
from datetime import date

def log_enrichment_cost(contacts_enriched: int, cost_per_contact: float = 0.05):
    """Log enrichment cost for budget tracking."""
    cost_file = f"costs/{date.today().isoformat()}.json"
    entry = {
        "date": date.today().isoformat(),
        "contacts_enriched": contacts_enriched,
        "cost_per_contact": cost_per_contact,
        "total_cost": round(contacts_enriched * cost_per_contact, 2),
        "service": "clay_enrichment"
    }
    # Append to daily log
    with open(cost_file, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

> **Integration:** Feed cost data to `cost-metering-skill` for unified budget tracking.
