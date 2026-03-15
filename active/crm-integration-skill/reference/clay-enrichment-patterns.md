# Clay MCP Waterfall Enrichment Pattern

**Use Clay MCP for:**
- Phone verification (aggregates 50+ data providers)
- Missing email addresses after Apollo
- Work history and professional background
- Thought leadership / LinkedIn activity
- Company tech stack, funding, headcount enrichment

**Waterfall Strategy:**
```
1. Apollo (free, fast, limited match rate)
   └─ If missing phones/emails → 2. Clay MCP (credits, comprehensive)
   └─ If missing company data → 2. Clay MCP (credits, comprehensive)
```

**Clay MCP Workflow Pattern:**

```python
# Step 1: Find company and create enrichment task
task_id = find_and_enrich_company(
    companyIdentifier="company.com",  # domain or LinkedIn URL
    companyDataPoints=[
        {type: "Tech Stack"},
        {type: "Latest Funding"},
        {type: "Headcount Growth"}
    ]
)
# Returns: taskId for polling

# Step 2: Queue contact enrichment jobs
add_contact_data_points(
    taskId=task_id,
    dataPoints=[
        {type: "Email"},
        {type: "Summarize Work History"},
        {type: "Find Thought Leadership"}
    ]
)

# Step 3: Poll for results (asynchronous enrichment)
results = get_existing_search(taskId=task_id)
# Returns: { state: "in-progress" | "completed", value: {...} }

# Step 4: Write enriched data back to HubSpot
if results['state'] == 'completed':
    hubspot_api.update_contact(
        contact_id=contact['id'],
        {
            'phone': results['value']['phone'],
            'email': results['value']['email'],
            'work_history': results['value']['work_history']
        }
    )
```

**MCP Tool Prefix:**
```
mcp__claude_ai_Clay__find-and-enrich-company
mcp__claude_ai_Clay__find-and-enrich-contacts-at-company
mcp__claude_ai_Clay__add-contact-data-points
mcp__claude_ai_Clay__add-company-data-points
mcp__claude_ai_Clay__get-existing-search
```

**Cost Considerations:**
- **Apollo:** Free for basic enrichment, rate-limited (good for initial screening)
- **Clay:** Credits-based pricing (~$150-300/month for typical BDR team)
  - Waterfall approach: Apollo first (zero cost) → Clay fallback (pay only for misses)
  - Budget ~5-10 Clay credits per contact for full enrichment (phone + email + work history)

**Integration with HubSpot RevOps:**
→ See `hubspot-revops-skill` for ICP Validation (UC1) with Clay enrichment
→ See `phone-verification-waterfall-skill` for Golden Rules filtering + Clay waterfall

---

## Environment Variables

```bash
# Close CRM
export CLOSE_API_KEY="api_xxx"
export CLOSE_WEBHOOK_SECRET="whsec_xxx"

# HubSpot
export HUBSPOT_ACCESS_TOKEN="pat-xxx"

# Salesforce
export SF_CLIENT_ID="xxx"
export SF_USERNAME="user@company.com"
export SF_PRIVATE_KEY_PATH="./salesforce.key"
export SF_INSTANCE_URL="https://yourorg.my.salesforce.com"
```

```bash
# Install dependencies
pip install httpx pyjwt hubspot-api-client python-dotenv
```

---

## Example Session

**User:** "I need to push enriched leads from my sales-agent to Close CRM"

**Claude:**
1. Here's the pattern for pushing enriched data to Close:
```python
async def push_to_close(close_client, enriched_data: dict) -> str:
    lead_data = {
        "name": enriched_data["company_name"],
        "url": enriched_data.get("website"),
        "custom.cf_tier": enriched_data["tier"],
        "custom.cf_source": "sales-agent",
        "contacts": [{
            "name": c["name"],
            "title": c.get("title"),
            "emails": [{"email": c["email"]}] if c.get("email") else []
        } for c in enriched_data.get("contacts", [])]
    }

    result = close_client.create_lead(lead_data)
    return result["id"]
```

2. Make sure you have these custom fields in Close:
   - `cf_tier` (choices: Gold, Silver, Bronze)
   - `cf_source` (choices: sales-agent, inbound, referral)

3. Rate limit: 100 requests per 10 seconds. Add `asyncio.sleep(0.1)` between requests for bulk imports.
