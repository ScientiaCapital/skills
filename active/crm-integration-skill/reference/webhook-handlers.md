# Webhook Handlers — Close CRM

Extracted verbatim from `crm-integration-skill/SKILL.md` (webhook_patterns section).

### Close Webhook (FastAPI)
```python
from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib

app = FastAPI()

@app.post("/webhooks/close")
async def close_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("Close-Sig")

    expected = hmac.new(
        CLOSE_WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(401, "Invalid signature")

    data = await request.json()
    event_type = data["event"]["event_type"]

    handlers = {
        "lead.created": handle_lead_created,
        "opportunity.status_changed": handle_opp_stage_change,
    }

    if handler := handlers.get(event_type):
        await handler(data["event"]["data"])

    return {"status": "ok"}
```

### Close Webhook Events
```
lead.created, lead.updated, lead.deleted, lead.status_changed
contact.created, contact.updated
opportunity.created, opportunity.status_changed
activity.note.created, activity.call.created, activity.email.created
unsubscribed_email.created
```
