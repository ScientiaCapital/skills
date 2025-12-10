# Domain Warming Protocol

## Domain Setup

```python
# Module: cold-reach/domains
# - GoDaddy/Namecheap API for bulk domain buying
# - Cloudflare API for SPF, DKIM, DMARC
# - Auto-provision 3 mailboxes per domain
```

**DNS Records Required:**
- SPF: `v=spf1 include:_spf.google.com ~all`
- DKIM: Generated per domain
- DMARC: `v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com`

## Warming Schedule

| Day | Daily Volume | Activity |
|-----|--------------|----------|
| 1-7 | 2-5 emails | Reply to warm emails only |
| 8-14 | 5-15 emails | Mix 70% warm + 30% cold |
| 15-21 | 15-30 emails | Monitor spam rates closely |
| 22-30 | 30-50 emails | Full capacity if <2% spam |

## Health Metrics

| Metric | Target | Action if Exceeded |
|--------|--------|-------------------|
| Bounce rate | <3% | Clean list, verify emails |
| Spam rate | <0.3% | Pause warming, check content |
| Open rate | >40% | Adjust subject lines |
| Reply rate | >5% | Good - continue |

## Sequence Engine

```python
class SequenceEngine:
    async def execute_sequence(self, lead: Lead, sequence: Sequence):
        for step in sequence.steps:
            # Check for reply before sending
            if await self._has_reply(lead):
                await self._route_to_agent(lead, 'ANALYZER')
                return

            # Personalize and send
            message = await self._personalize(step.template, lead)
            await self._send(lead.email, message)

            # Wait for configured delay
            await asyncio.sleep(step.delay_hours * 3600)
```

## Deliverability Checklist

- [ ] Domain age > 30 days before cold outreach
- [ ] SPF, DKIM, DMARC all configured
- [ ] Warming period completed (30 days)
- [ ] Email verification for all leads
- [ ] Unsubscribe link in all emails
- [ ] Physical address in footer
- [ ] Daily volume < 50/mailbox
