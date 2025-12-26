---
name: crm-integration-skill
description: |
  Unified CRM integration patterns for Close CRM, HubSpot, and Salesforce. Covers API
  authentication, CRUD operations, pipeline management, activity logging, webhooks,
  bulk operations, and cross-CRM sync patterns. Optimized for GTM automation workflows.
  Triggers: "Close CRM", "HubSpot", "Salesforce", "CRM API", "lead sync", "deal sync",
  "activity logging", "CRM webhook", "pipeline automation", "contact enrichment",
  "CRM migration", "bulk import", "custom fields", "CRM integration".
---

# CRM Integration Skill

Unified patterns for Close CRM, HubSpot, and Salesforce API integrations.

## Quick Reference

| CRM | Auth Method | Rate Limits | Best For |
|-----|-------------|-------------|----------|
| **Close** | API Key | 100 req/10s | SMB sales teams, simplicity |
| **HubSpot** | OAuth 2.0 / Private App | 100 req/10s (free) | Marketing + Sales alignment |
| **Salesforce** | OAuth 2.0 (JWT) | 100k req/day (Enterprise) | Enterprise, complex workflows |

| Domain | Key Operations | Reference File |
|--------|---------------|----------------|
| **Authentication** | API keys, OAuth flows, token refresh | `reference/auth-patterns.md` |
| **Core CRUD** | Contacts, companies, deals, activities | `reference/crud-operations.md` |
| **Automation** | Webhooks, sequences, workflows | `reference/automation.md` |
| **Sync Patterns** | Cross-CRM sync, deduplication, migration | `reference/sync-patterns.md` |

---

## Part 1: Authentication

### Close CRM (Your Daily Driver)

```python
import httpx
from typing import Optional

class CloseClient:
    """Close CRM API client with rate limiting."""
    
    BASE_URL = "https://api.close.com/api/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            auth=(api_key, ""),  # Basic auth, password empty
            timeout=30.0,
            headers={"Content-Type": "application/json"}
        )
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        response = self.client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        return response.json()
```

**Rate Limits:** 100 requests per 10 seconds (burst), 6000/minute sustained

### HubSpot

```python
class HubSpotClient:
    """HubSpot API client using Private App token."""
    
    BASE_URL = "https://api.hubapi.com"
    
    def __init__(self, access_token: str):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        response = self.client.request(method, endpoint, **kwargs)
        if response.status_code == 429:
            # Rate limited - check Retry-After header
            retry_after = int(response.headers.get("Retry-After", 10))
            raise RateLimitError(retry_after)
        response.raise_for_status()
        return response.json()
```

**Rate Limits by Tier:**
| Tier | Limits | Cost |
|------|--------|------|
| Free | 100 req/10s | $0 |
| Starter | 100 req/10s | $45/mo |
| Pro | 150 req/10s | $800/mo |
| Enterprise | 200 req/10s | $3,600/mo |

### Salesforce

```python
import jwt
from datetime import datetime, timedelta

class SalesforceClient:
    """Salesforce API client using JWT Bearer flow (server-to-server)."""
    
    def __init__(
        self, 
        client_id: str,
        username: str,
        private_key: str,
        instance_url: str,
        is_sandbox: bool = False
    ):
        self.client_id = client_id
        self.username = username
        self.private_key = private_key
        self.instance_url = instance_url
        self.auth_url = (
            "https://test.salesforce.com" if is_sandbox 
            else "https://login.salesforce.com"
        )
        self.access_token: Optional[str] = None
        self._authenticate()
    
    def _authenticate(self):
        """JWT Bearer token flow."""
        now = datetime.utcnow()
        payload = {
            "iss": self.client_id,
            "sub": self.username,
            "aud": self.auth_url,
            "exp": int((now + timedelta(minutes=3)).timestamp())
        }
        assertion = jwt.encode(payload, self.private_key, algorithm="RS256")
        
        response = httpx.post(
            f"{self.auth_url}/services/oauth2/token",
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": assertion
            }
        )
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
```

**API Versions:** Use latest stable (v59.0 as of 2024). Check `/services/data/` for versions.

---

## Part 2: Core CRUD Operations

### Entity Mapping

| Concept | Close | HubSpot | Salesforce |
|---------|-------|---------|------------|
| Company | `lead` | `company` | `Account` |
| Person | `contact` | `contact` | `Contact` / `Lead` |
| Deal | `opportunity` | `deal` | `Opportunity` |
| Activity | `activity` | `engagement` | `Task` / `Event` |
| Custom Field | `custom.cf_xxx` | `properties` | `CustomField__c` |

### Close CRM Operations

```python
# --- LEADS (Companies) ---
def create_lead(self, data: dict) -> dict:
    """Create a lead (company) in Close."""
    return self._request("POST", "/lead/", json=data)

def search_leads(self, query: str, limit: int = 100) -> list:
    """Search leads using Close query language."""
    return self._request(
        "POST", "/data/search/",
        json={
            "query": {"type": "query_string", "value": query},
            "results_limit": limit
        }
    )["data"]

# --- CONTACTS ---
def create_contact(self, lead_id: str, data: dict) -> dict:
    """Create contact under a lead."""
    data["lead_id"] = lead_id
    return self._request("POST", "/contact/", json=data)

# --- OPPORTUNITIES (Deals) ---
def create_opportunity(self, lead_id: str, data: dict) -> dict:
    """Create opportunity under a lead."""
    data["lead_id"] = lead_id
    return self._request("POST", "/opportunity/", json=data)

def update_opportunity_status(self, opp_id: str, status_id: str) -> dict:
    """Move opportunity to new pipeline stage."""
    return self._request(
        "PUT", f"/opportunity/{opp_id}/",
        json={"status_id": status_id}
    )

# --- ACTIVITIES ---
def log_activity(self, lead_id: str, activity_type: str, note: str) -> dict:
    """Log a note or activity."""
    return self._request(
        "POST", "/activity/note/",
        json={"lead_id": lead_id, "note": note}
    )

def log_call(self, lead_id: str, direction: str, duration: int, note: str) -> dict:
    """Log a call activity."""
    return self._request(
        "POST", "/activity/call/",
        json={
            "lead_id": lead_id,
            "direction": direction,  # "outbound" or "inbound"
            "duration": duration,
            "note": note
        }
    )
```

### HubSpot Operations

```python
# --- CONTACTS ---
def create_contact(self, properties: dict) -> dict:
    """Create a contact in HubSpot."""
    return self._request(
        "POST", "/crm/v3/objects/contacts",
        json={"properties": properties}
    )

def search_contacts(self, filters: list, limit: int = 100) -> list:
    """Search contacts with filters."""
    return self._request(
        "POST", "/crm/v3/objects/contacts/search",
        json={
            "filterGroups": [{"filters": filters}],
            "limit": limit
        }
    )["results"]

# --- COMPANIES ---
def create_company(self, properties: dict) -> dict:
    return self._request(
        "POST", "/crm/v3/objects/companies",
        json={"properties": properties}
    )

# --- DEALS ---
def create_deal(self, properties: dict, associations: list = None) -> dict:
    """Create deal with optional associations."""
    payload = {"properties": properties}
    if associations:
        payload["associations"] = associations
    return self._request("POST", "/crm/v3/objects/deals", json=payload)

def update_deal_stage(self, deal_id: str, stage: str) -> dict:
    return self._request(
        "PATCH", f"/crm/v3/objects/deals/{deal_id}",
        json={"properties": {"dealstage": stage}}
    )

# --- ENGAGEMENTS (Activities) ---
def log_note(self, contact_id: str, body: str) -> dict:
    """Log a note engagement."""
    return self._request(
        "POST", "/crm/v3/objects/notes",
        json={
            "properties": {"hs_note_body": body},
            "associations": [{
                "to": {"id": contact_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 202}]
            }]
        }
    )
```

### Salesforce Operations

```python
# --- ACCOUNTS ---
def create_account(self, data: dict) -> dict:
    """Create an Account (company)."""
    return self._request(
        "POST", "/services/data/v59.0/sobjects/Account/",
        json=data
    )

# --- CONTACTS ---
def create_contact(self, data: dict) -> dict:
    return self._request(
        "POST", "/services/data/v59.0/sobjects/Contact/",
        json=data
    )

# --- OPPORTUNITIES ---
def create_opportunity(self, data: dict) -> dict:
    """Create opportunity. Required: Name, StageName, CloseDate."""
    return self._request(
        "POST", "/services/data/v59.0/sobjects/Opportunity/",
        json=data
    )

# --- SOQL QUERIES ---
def query(self, soql: str) -> list:
    """Execute SOQL query."""
    response = self._request(
        "GET", "/services/data/v59.0/query/",
        params={"q": soql}
    )
    return response["records"]

# Example queries:
# "SELECT Id, Name, Email FROM Contact WHERE Email LIKE '%@coperniq.com'"
# "SELECT Id, Name, Amount, StageName FROM Opportunity WHERE IsClosed = false"

# --- TASKS (Activities) ---
def create_task(self, data: dict) -> dict:
    """Create a task/activity."""
    return self._request(
        "POST", "/services/data/v59.0/sobjects/Task/",
        json=data
    )
```

---

## Part 3: Pipeline Management

### Pipeline Stage Mapping

| Stage | Close Status | HubSpot Stage | Salesforce Stage |
|-------|--------------|---------------|------------------|
| New Lead | `Lead` | `appointmentscheduled` | `Prospecting` |
| Qualified | `Contacted` | `qualifiedtobuy` | `Qualification` |
| Demo Scheduled | `Opportunity` | `presentationscheduled` | `Needs Analysis` |
| Proposal | `Proposal` | `decisionmakerboughtin` | `Proposal/Price Quote` |
| Negotiation | `Negotiation` | `contractsent` | `Negotiation/Review` |
| Closed Won | `Won` | `closedwon` | `Closed Won` |
| Closed Lost | `Lost` | `closedlost` | `Closed Lost` |

### Pipeline Automation Pattern

```python
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class DealStage(Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    DEMO = "demo"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"

@dataclass
class DealUpdate:
    deal_id: str
    new_stage: DealStage
    notes: str = ""
    close_date: datetime = None

class PipelineManager:
    """Unified pipeline manager across CRMs."""
    
    STAGE_MAPPING = {
        "close": {
            DealStage.NEW: "stat_xxx",  # Replace with actual status IDs
            DealStage.QUALIFIED: "stat_yyy",
            # ...
        },
        "hubspot": {
            DealStage.NEW: "appointmentscheduled",
            DealStage.QUALIFIED: "qualifiedtobuy",
            # ...
        },
        "salesforce": {
            DealStage.NEW: "Prospecting",
            DealStage.QUALIFIED: "Qualification",
            # ...
        }
    }
    
    def update_stage(self, crm: str, update: DealUpdate):
        """Update deal stage in specified CRM."""
        stage_value = self.STAGE_MAPPING[crm][update.new_stage]
        
        if crm == "close":
            self.close_client.update_opportunity_status(
                update.deal_id, stage_value
            )
        elif crm == "hubspot":
            self.hubspot_client.update_deal_stage(
                update.deal_id, stage_value
            )
        elif crm == "salesforce":
            self.sf_client._request(
                "PATCH", 
                f"/services/data/v59.0/sobjects/Opportunity/{update.deal_id}",
                json={"StageName": stage_value}
            )
```

---

## Part 4: Webhooks & Real-Time Sync

### Close Webhooks

```python
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()

CLOSE_WEBHOOK_SECRET = "your_webhook_secret"

@app.post("/webhooks/close")
async def close_webhook(request: Request):
    """Handle Close CRM webhooks."""
    body = await request.body()
    signature = request.headers.get("Close-Sig")
    
    # Verify signature
    expected = hmac.new(
        CLOSE_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(401, "Invalid signature")
    
    data = await request.json()
    event = data["event"]
    
    # Route by event type
    handlers = {
        "lead.created": handle_lead_created,
        "lead.updated": handle_lead_updated,
        "opportunity.status_changed": handle_opp_stage_change,
        "activity.created": handle_activity_created,
    }
    
    handler = handlers.get(event["event_type"])
    if handler:
        await handler(event["data"])
    
    return {"status": "ok"}
```

### HubSpot Webhooks

```python
@app.post("/webhooks/hubspot")
async def hubspot_webhook(request: Request):
    """Handle HubSpot webhooks."""
    # HubSpot sends array of events
    events = await request.json()
    
    for event in events:
        object_type = event["objectType"]  # contact, deal, company
        change_type = event["subscriptionType"]  # creation, propertyChange, deletion
        object_id = event["objectId"]
        
        if change_type == "deal.propertyChange":
            if event["propertyName"] == "dealstage":
                await sync_deal_stage_to_close(
                    object_id, 
                    event["propertyValue"]
                )
    
    return {"status": "ok"}
```

### Salesforce Platform Events (Streaming)

```python
from aiosfstream import SalesforceStreamingClient

async def listen_salesforce_events():
    """Listen to Salesforce Platform Events via Streaming API."""
    async with SalesforceStreamingClient(
        consumer_key=SF_CLIENT_ID,
        consumer_secret=SF_CLIENT_SECRET,
        username=SF_USERNAME,
        password=SF_PASSWORD + SF_SECURITY_TOKEN
    ) as client:
        
        await client.subscribe("/data/OpportunityChangeEvent")
        
        async for message in client:
            change = message["payload"]
            if "StageName" in change.get("ChangeEventHeader", {}).get("changedFields", []):
                await sync_to_close(change)
```

---

## Part 5: Bulk Operations

### Close Bulk Import

```python
async def bulk_import_leads(self, leads: list[dict], batch_size: int = 100):
    """Bulk import leads to Close with rate limiting."""
    for i in range(0, len(leads), batch_size):
        batch = leads[i:i + batch_size]
        
        for lead in batch:
            try:
                self.create_lead(lead)
            except Exception as e:
                logger.error(f"Failed to import lead: {e}")
        
        # Rate limit: 100 req/10s = 10 req/s
        await asyncio.sleep(10)  # Wait between batches
```

### HubSpot Batch API

```python
def batch_create_contacts(self, contacts: list[dict]) -> dict:
    """Create up to 100 contacts in one request."""
    return self._request(
        "POST", "/crm/v3/objects/contacts/batch/create",
        json={"inputs": [{"properties": c} for c in contacts]}
    )

def batch_update_deals(self, updates: list[dict]) -> dict:
    """Update up to 100 deals in one request."""
    return self._request(
        "POST", "/crm/v3/objects/deals/batch/update",
        json={"inputs": updates}
    )
```

### Salesforce Composite API

```python
def composite_create(self, records: list[dict]) -> dict:
    """Create up to 200 records in one call."""
    return self._request(
        "POST", "/services/data/v59.0/composite/sobjects",
        json={
            "allOrNone": False,
            "records": records
        }
    )

# Example:
records = [
    {"attributes": {"type": "Contact"}, "Email": "a@example.com", "LastName": "Smith"},
    {"attributes": {"type": "Contact"}, "Email": "b@example.com", "LastName": "Jones"},
]
```

---

## Part 6: Cross-CRM Sync Patterns

### Bidirectional Sync Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Close     │────▶│  Sync Layer  │◀────│  HubSpot    │
│  (Primary)  │◀────│  (Postgres)  │────▶│  (Marketing)│
└─────────────┘     └──────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │ Salesforce  │
                    │ (Enterprise)│
                    └─────────────┘
```

### Sync Record Schema

```sql
CREATE TABLE crm_sync_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,  -- contact, deal, company
    
    -- CRM IDs
    close_id VARCHAR(100),
    hubspot_id VARCHAR(100),
    salesforce_id VARCHAR(100),
    
    -- Canonical data (source of truth)
    email VARCHAR(255),
    company_name VARCHAR(255),
    
    -- Sync metadata
    last_synced_at TIMESTAMPTZ,
    sync_source VARCHAR(50),  -- which CRM triggered last sync
    sync_hash VARCHAR(64),    -- detect changes
    
    UNIQUE(close_id),
    UNIQUE(hubspot_id),
    UNIQUE(salesforce_id)
);

CREATE INDEX idx_sync_email ON crm_sync_records(email);
```

### Conflict Resolution Strategy

```python
from enum import Enum
from datetime import datetime

class ConflictStrategy(Enum):
    CLOSE_WINS = "close"      # Close is source of truth (your daily driver)
    LAST_WRITE_WINS = "lww"   # Most recent update wins
    MERGE = "merge"           # Merge non-conflicting fields

class SyncEngine:
    def __init__(self, strategy: ConflictStrategy = ConflictStrategy.CLOSE_WINS):
        self.strategy = strategy
    
    def resolve_conflict(
        self, 
        close_record: dict, 
        hubspot_record: dict,
        salesforce_record: dict
    ) -> dict:
        """Resolve conflicts between CRM records."""
        
        if self.strategy == ConflictStrategy.CLOSE_WINS:
            # Start with Close data, fill gaps from others
            merged = close_record.copy()
            for key in hubspot_record:
                if key not in merged or not merged[key]:
                    merged[key] = hubspot_record[key]
            return merged
        
        elif self.strategy == ConflictStrategy.LAST_WRITE_WINS:
            # Compare updated_at timestamps
            records = [
                (close_record, close_record.get("date_updated")),
                (hubspot_record, hubspot_record.get("hs_lastmodifieddate")),
                (salesforce_record, salesforce_record.get("SystemModstamp")),
            ]
            return max(records, key=lambda x: x[1] or datetime.min)[0]
```

### Deduplication

```python
from fuzzywuzzy import fuzz

def find_duplicates(contacts: list[dict], threshold: int = 85) -> list[tuple]:
    """Find potential duplicate contacts."""
    duplicates = []
    
    for i, c1 in enumerate(contacts):
        for c2 in contacts[i+1:]:
            # Email exact match
            if c1.get("email") and c1["email"] == c2.get("email"):
                duplicates.append((c1, c2, 100, "email"))
                continue
            
            # Fuzzy name + company match
            name_score = fuzz.token_sort_ratio(
                c1.get("name", ""), c2.get("name", "")
            )
            company_score = fuzz.token_sort_ratio(
                c1.get("company", ""), c2.get("company", "")
            )
            
            combined = (name_score + company_score) / 2
            if combined >= threshold:
                duplicates.append((c1, c2, combined, "fuzzy"))
    
    return duplicates
```

---

## Part 7: Custom Fields

### Close Custom Fields

```python
def get_custom_fields(self) -> list:
    """Get all custom fields in Close."""
    return self._request("GET", "/custom_field/lead/")["data"]

def create_custom_field(self, name: str, field_type: str) -> dict:
    """Create a custom field. Types: text, dropdown, date, number, etc."""
    return self._request(
        "POST", "/custom_field/lead/",
        json={"name": name, "type": field_type}
    )

# Accessing custom field values
# lead["custom"]["cf_xxxxxx"] = "value"
```

### HubSpot Properties

```python
def create_property(self, object_type: str, name: str, field_type: str) -> dict:
    """Create a custom property."""
    return self._request(
        "POST", f"/crm/v3/properties/{object_type}",
        json={
            "name": name,
            "label": name.replace("_", " ").title(),
            "type": field_type,  # string, number, date, enumeration
            "fieldType": "text",
            "groupName": "contactinformation"
        }
    )
```

### Salesforce Custom Fields

```python
# Custom fields in Salesforce end with __c
# Access via: record["My_Custom_Field__c"]

# Creating custom fields requires Metadata API
# Usually done via Setup UI or Salesforce CLI:
# sf project deploy start --source-dir force-app/main/default/objects/Contact/fields/
```

---

## Cost Comparison

| Feature | Close | HubSpot | Salesforce |
|---------|-------|---------|------------|
| **Starting Price** | $49/user/mo | Free (limited) | $25/user/mo |
| **API Access** | All plans | Starter+ ($45+) | All plans |
| **Webhooks** | All plans | Pro+ ($800+) | All plans |
| **Bulk API** | All plans | All plans | Enterprise+ |
| **Custom Objects** | Yes | Enterprise+ | All plans |

**Tim's Recommendation:** Close for primary sales work (simplest API, best value). HubSpot for marketing alignment. Salesforce only if enterprise requires it.

---

## Integration with Your Stack

| Project | CRM Integration Use |
|---------|-------------------|
| **sales-agent** | Push enriched leads to Close |
| **dealer-scraper-mvp** | Bulk import leads to Close |
| **cold-reach** | Log email activities to CRM |
| **ThetaRoom** | Could sync trading signals to Salesforce for institutional clients |

## Reference Files

- `reference/auth-patterns.md` - Detailed OAuth flows, token refresh, security
- `reference/crud-operations.md` - Complete API examples for all entities
- `reference/automation.md` - Webhook setup, sequences, workflows
- `reference/sync-patterns.md` - Cross-CRM sync, migration scripts
- `reference/close-deep-dive.md` - Close-specific power features (Smart Views, workflows)

---

## Quick Start

```bash
# Install dependencies
pip install httpx pyjwt python-dotenv fuzzywuzzy

# Environment variables
export CLOSE_API_KEY="api_xxx"
export HUBSPOT_ACCESS_TOKEN="pat-xxx"
export SF_CLIENT_ID="xxx"
export SF_PRIVATE_KEY_PATH="./salesforce.key"
export SF_USERNAME="user@company.com"
```

```python
# Quick usage
from crm_clients import CloseClient, HubSpotClient, SalesforceClient

close = CloseClient(os.environ["CLOSE_API_KEY"])
leads = close.search_leads("company:Coperniq")
```
