# Close CRM — Query Language, Core Operations, Rate Limits

Extracted verbatim from `crm-integration-skill/SKILL.md` (close_patterns section).

### Query Language (for Smart Views)
```python
# Leads with no activity in 30 days
'sort:date_updated asc date_updated < "30 days ago"'

# High-value opportunities
'opportunities.value >= 50000 opportunities.status_type:active'

# Custom field filtering
'custom.cf_industry = "MEP Contractor"'

# Multiple trade types (your ICP)
'custom.cf_trades:HVAC OR custom.cf_trades:Electrical'
```

### Core Operations
```python
# Create lead with contacts
lead = close.create_lead({
    "name": "ABC Mechanical",
    "url": "https://abcmech.com",
    "contacts": [{
        "name": "John Smith",
        "title": "Owner",
        "emails": [{"email": "john@abcmech.com", "type": "office"}],
        "phones": [{"phone": "555-1234", "type": "office"}]
    }],
    "custom.cf_tier": "Gold",
    "custom.cf_source": "sales-agent"
})

# Create opportunity
opp = close._request("POST", "/opportunity/", json={
    "lead_id": lead["id"],
    "value": 50000,
    "confidence": 50,
    "status_id": "stat_xxx"  # Pipeline stage
})

# Log activity
close._request("POST", "/activity/note/", json={
    "lead_id": lead["id"],
    "note": "Initial discovery call - interested in demo"
})
```

### Rate Limit Headers (RFC-compliant)
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067200
```
