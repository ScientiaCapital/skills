# Coperniq Messaging Guide

## ICP Definition

**Target:** Multi-trade contractors (MEP+E), $5-50M revenue

**Pain Points:**
- Too complex for Jobber, not ready for ServiceTitan
- Projects in one system, service calls in another
- Trucks and equipment tracked in spreadsheets
- No single platform handles multiple trades

## Cold Email Templates

### Option A (Tight - Recommended)

> Tim from Coperniq. At $5-50M with multiple trades, you're in no-man's land: too complex for Jobber, not ready to bet the business on ServiceTitan.
>
> So you're gluing it together with spreadsheets. That's not a you problem - it's a market gap.
>
> We built for that gap. 10 minutes?

### Option B (Problem-Forward)

> Quick question: how many different systems is your team using to manage jobs right now?
>
> Most MEP contractors I talk to are at 3-4 minimum. One for projects, one for service, spreadsheets for equipment...
>
> We built a single platform that handles all of it. Worth 10 minutes to see if it fits?

## SMS Sequence

**Step 1 (Day 0):**
> Tim w/ Coperniq. Quick q: how many different systems does your team use to run jobs? We help multi-trade shops consolidate. 5 mins?

**Step 2 (Day 3):**
> Following up - most contractors your size are stuck between tools that are too simple or too bloated. We built for the middle. Worth a look?

**Step 3 (Day 7):**
> Honest q: what's the most broken part of your current setup? Might have a solution.

**Step 4 (Day 10 - Final):**
> Last text. If you're not stuck juggling systems, ignore this. If you are - 10 mins: [link]

## Reply Intent Classification

```python
INTENT_CATEGORIES = {
    'INTERESTED': ['call me', 'tell me more', 'sounds good', 'let\'s talk'],
    'OBJECTION': ['we already', 'not right now', 'too busy', 'using X'],
    'UNSUBSCRIBE': ['stop', 'remove', 'unsubscribe', 'no more'],
    'INFO_REQUEST': ['pricing', 'how does', 'what is', 'demo'],
    'REFERRAL': ['talk to', 'reach out to', 'contact']
}

async def route_reply(reply: str, intent: str):
    routes = {
        'INTERESTED': 'sales_agent.schedule_call',
        'OBJECTION': 'nurture_sequence.add',
        'UNSUBSCRIBE': 'cold_reach.stop_sequence',
        'INFO_REQUEST': 'sales_agent.send_info',
        'REFERRAL': 'enricher.find_contact'
    }
    await routes[intent](reply)
```

## Call Summary Format

When summarizing sales calls, capture:

1. **Software Stack:** What systems do they currently use?
2. **Interest Level:** What features/problems resonated?
3. **Team Size:** Field vs office headcount
4. **Goals:** What are they trying to achieve?
5. **Pain Points:** What's broken today?
6. **Failed Implementations:** Previous software attempts that didn't work
