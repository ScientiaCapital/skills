# HubSpot API Guide

## Authentication

### Private App Token (Recommended)

```python
# Option 1: Official SDK
from hubspot import HubSpot
client = HubSpot(access_token="pat-na1-xxxxx")

# Option 2: Raw requests
import requests

HUBSPOT_TOKEN = os.environ["HUBSPOT_ACCESS_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_TOKEN}",
    "Content-Type": "application/json"
}
BASE_URL = "https://api.hubapi.com"
```

### Required Scopes by Use Case

| Use Case | Scopes Needed |
|----------|---------------|
| Read contacts/companies | `crm.objects.contacts.read`, `crm.objects.companies.read` |
| Enrich contacts (writeback) | `crm.objects.contacts.write` |
| Deal analytics | `crm.objects.deals.read` |
| Score writeback | `crm.objects.deals.write`, `crm.objects.contacts.write` |
| Custom properties | `crm.schemas.custom.read`, `crm.schemas.custom.write` |
| Engagement data | `timeline` |

---

## CRUD Operations

### Contacts

```python
# SDK — Search contacts
from hubspot.crm.contacts import PublicObjectSearchRequest

search = PublicObjectSearchRequest(
    filter_groups=[{
        "filters": [{
            "propertyName": "lifecyclestage",
            "operator": "EQ",
            "value": "customer"
        }]
    }],
    properties=["email", "firstname", "lastname", "company", "hs_lead_status"],
    limit=100
)
results = client.crm.contacts.search_api.do_search(search)

# SDK — Update contact
from hubspot.crm.contacts import SimplePublicObjectInput

update = SimplePublicObjectInput(properties={
    "hs_lead_status": "QUALIFIED",
    "lead_score_ml": "87"  # custom property
})
client.crm.contacts.basic_api.update(contact_id="12345", simple_public_object_input=update)
```

### Companies

```python
# SDK — Get company by domain
search = PublicObjectSearchRequest(
    filter_groups=[{
        "filters": [{
            "propertyName": "domain",
            "operator": "EQ",
            "value": "example.com"
        }]
    }],
    properties=["name", "domain", "industry", "numberofemployees", "annualrevenue"]
)
results = client.crm.companies.search_api.do_search(search)
```

### Deals

```python
# SDK — Search deals by stage
search = PublicObjectSearchRequest(
    filter_groups=[{
        "filters": [{
            "propertyName": "dealstage",
            "operator": "EQ",
            "value": "closedwon"
        }]
    }],
    properties=["dealname", "amount", "closedate", "dealstage", "pipeline"],
    sorts=[{"propertyName": "closedate", "direction": "DESCENDING"}],
    limit=100
)
results = client.crm.deals.search_api.do_search(search)
```

---

## Custom Properties

Create custom properties for storing analytics results:

```python
# Create a custom contact property for ML lead score
from hubspot.crm.properties import PropertyCreate

prop = PropertyCreate(
    name="lead_score_ml",
    label="ML Lead Score",
    type="number",
    field_type="number",
    group_name="contactinformation",
    description="Machine learning lead score (0-100)"
)
client.crm.properties.core_api.create(object_type="contacts", property_create=prop)
```

**Common custom properties for RevOps:**

| Property | Object | Type | Purpose |
|----------|--------|------|---------|
| `lead_score_ml` | Contact | number | ML-generated score (0-100) |
| `icp_segment` | Company | enumeration | ICP tier (A/B/C/D) |
| `competitor_displaced` | Deal | string | Which competitor was displaced |
| `enrichment_source` | Contact | string | Clay / ZoomInfo / manual |
| `last_enriched_at` | Contact | datetime | Enrichment freshness |

---

## Batch Operations

HubSpot rate limit: **100 requests per 10 seconds** (private apps).

```python
# Batch update contacts (up to 100 per call)
from hubspot.crm.contacts import BatchInputSimplePublicObjectBatchInput

batch = BatchInputSimplePublicObjectBatchInput(inputs=[
    {"id": "101", "properties": {"lead_score_ml": "92"}},
    {"id": "102", "properties": {"lead_score_ml": "45"}},
    {"id": "103", "properties": {"lead_score_ml": "78"}},
])
client.crm.contacts.batch_api.update(batch)
```

**Rate limit handling:**

```python
import time

def batch_update_with_backoff(client, updates, batch_size=100):
    """Update contacts in rate-limit-friendly batches."""
    for i in range(0, len(updates), batch_size):
        batch = updates[i:i + batch_size]
        try:
            client.crm.contacts.batch_api.update(
                BatchInputSimplePublicObjectBatchInput(inputs=batch)
            )
        except Exception as e:
            if "429" in str(e):
                time.sleep(11)  # Wait for rate limit window
                client.crm.contacts.batch_api.update(
                    BatchInputSimplePublicObjectBatchInput(inputs=batch)
                )
            else:
                raise
        time.sleep(0.5)  # Stay under 100 req/10s
```

---

## Association API (v4)

Link objects together (contact→company, deal→contact, etc.):

```python
# Read associations: which contacts are on a deal
response = requests.post(
    f"{BASE_URL}/crm/v4/associations/deals/contacts/batch/read",
    headers=HEADERS,
    json={"inputs": [{"id": "deal_123"}]}
)

# Create association: link contact to company
response = requests.put(
    f"{BASE_URL}/crm/v4/objects/contacts/{contact_id}/associations/companies/{company_id}",
    headers=HEADERS,
    json=[{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 1}]
)
```

**Common association type IDs:**

| From | To | Type ID |
|------|-----|---------|
| Contact | Company | 1 |
| Deal | Contact | 3 |
| Deal | Company | 5 |
| Contact | Deal | 4 |

---

## Webhook Subscriptions

Set up real-time alerts for competitive intelligence:

```python
# Create webhook subscription (via HubSpot UI or API)
# Settings → Integrations → Private Apps → Webhooks

# Webhook payload handler (Flask example)
from flask import Flask, request
app = Flask(__name__)

@app.route("/hubspot-webhook", methods=["POST"])
def handle_webhook():
    events = request.json
    for event in events:
        if event["propertyName"] == "dealstage":
            if event["propertyValue"] == "closedlost":
                # Trigger competitive analysis
                analyze_lost_deal(event["objectId"])
    return "", 200
```

**Subscribable events:**
- `contact.propertyChange` — lifecycle stage changes
- `deal.propertyChange` — stage transitions, amount changes
- `deal.creation` — new deals entering pipeline
- `deal.deletion` — deals removed from pipeline
