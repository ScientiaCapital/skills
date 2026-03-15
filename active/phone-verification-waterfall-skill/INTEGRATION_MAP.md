# Integration Map — Phone Verification Waterfall Skill

## Monday Morning Sales Stack

The phone-verification-waterfall-skill runs as part of Tim's automated Monday morning prep sequence:

```
MONDAY 6:00 AM  ┌─ prospect-enrich-skill
                │  └─ Refreshes company firmographics + tech stack
                │
MONDAY 6:15 AM  ├─ phone-verification-waterfall-skill (THIS SKILL)
                │  └─ Verifies phones on newly enriched prospects
                │  └─ Populates callable queue for daily dials
                │
MONDAY 6:30 AM  └─ prospect-refresh-skill
                   └─ Refreshes deal velocity + pipeline metrics
```

**Why this order?**
1. Enrich company data first (broader research)
2. Then verify phones on those enriched prospects (narrow to callable)
3. Then refresh deal metrics (pipeline visibility)

---

## Skill Dependencies

### Reads From
- **prospect-research-to-cadence-skill** — Golden Rules filter logic, ICP scoring, first_conversion keywords
- **sales-revenue-skill** — ICP vertical definitions, intent signal weighting, revenue metrics
- **hubspot-revops-skill** — HubSpot bulk operations, contact filtering patterns, API rate limit handling

### Data Sources
- **HubSpot:** Contacts, company data, ownership
- **Epiphan CRM:** Device counts, channel flags, customer status
- **Apollo:** Phone number verification (no cost)
- **Clay:** Waterfall enrichment for Apollo misses (costs credits)

### Feeds Into
- **prospect-research-to-cadence-skill** — Can now target verified phone contacts for outreach sequences
- **Sales engagement tools** — Dialpad, Aircall, Apollo sequences (via CSV export or API)
- **Tim's daily dialing** — Callable queue ready by 6:30 AM for 7 AM start

---

## Information Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ SUNDAY 11 PM: Research prospect batch                           │
│ (prospect-research-to-cadence-skill creates new leads)          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ MONDAY 6:00 AM: prospect-enrich-skill                           │
│ └─ Refresh company data for all HubSpot contacts               │
│ └─ Firmographics, tech stack, news signals                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ MONDAY 6:15 AM: phone-verification-waterfall-skill (THIS)      │
│ ├─ Pull leads where phone = null                               │
│ ├─ Apollo phone lookup (Apollo people_match)                   │
│ ├─ Clay waterfall for Apollo misses                            │
│ ├─ HubSpot sync: write verified phones                         │
│ └─ Output: Callable queue sorted by ICP + intent               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ MONDAY 6:30 AM: prospect-refresh-skill                          │
│ └─ Refresh deal velocity, pipeline metrics                     │
│ └─ Update contact engagement scores                            │
│ └─ Prepare dashboard for 7 AM call start                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────────┐
│ MONDAY 7:00 AM: Tim's Dial Day Starts                           │
│ ├─ Callable queue ready in Dialpad/Aircall                     │
│ ├─ 50+ verified phone numbers ready to dial                    │
│ ├─ ICP scores guide priority (Higher Ed first)                 │
│ └─ Log dials → trigger sales engagement cadences               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Dependencies

### Required from HubSpot (Input)
```
Contacts table:
├─ contact_id (primary key)
├─ first_name, last_name
├─ email (business email)
├─ phone (should be NULL/empty for this to be included)
├─ hs_job_title
├─ hubspot_owner_id
├─ lifecyclestage
├─ first_conversion (product engagement tracking)
│
Companies table (joined):
├─ company_id
├─ industry
├─ num_employees
├─ hs_lead_status
```

### Required from Epiphan CRM (Validation)
```
For Golden Rules check:
├─ company.device_count (exclude if >= 1)
├─ company.is_channel (exclude if true)
├─ customer status (exclude if customer)
```

### Updated Back to HubSpot (Output)
```
Contacts table (batch update):
├─ phone (Apollo or Clay verified number)
├─ phone_source ("apollo" or "clay")
├─ phone_verified_at (timestamp)
├─ phone_waterfall_pass (boolean)
│
Companies table (optional):
└─ last_phone_waterfall_run (timestamp for audit)
```

---

## API Rate Limits & Costs

### Apollo (No Additional Cost)
- **Included in plan** — no cost for people_match API calls
- **Rate limit:** 100 requests/second (usually hit 40-50/sec in this workflow)
- **Timeout:** 30 seconds per request
- **Retry strategy:** Exponential backoff if rate limited

### Clay (Credits-based)
- **Cost:** ~$0.01-0.05 per contact enriched (varies by data provider)
- **Monthly allocation:** Tim has $200-300 monthly Clay credits
- **Waterfall efficiency:** Only enriches ~40% of contacts (Apollo misses), so credits stretch
- **Monitoring:** Check Clay dashboard monthly; pause enrichment if credits near limit

### HubSpot (Included in Existing Plan)
- **Contact search:** 500 calls/second (this skill uses ~1/sec)
- **Contact update (batch):** Unlimited, batched into 100 per request
- **No rate limit issues expected** for this workflow scale

---

## Failure Modes & Fallbacks

### If Apollo API Unavailable
- **Impact:** ~40-50% of contacts won't get phones
- **Fallback:** Skip Apollo, go directly to Clay waterfall
- **Output:** Reduced phone verification rate (~30-40%), but still usable
- **Action:** Alert Tim, continue with Clay-only results

### If Clay API Unavailable or Out of Credits
- **Impact:** ~30-40% of remaining Apollo misses won't get phones
- **Fallback:** Return Apollo-only results (still 40-50% of total)
- **Output:** Lower verification rate, still 50+ callable leads likely
- **Action:** Check Clay credit balance, schedule waterfall retry for Wednesday

### If HubSpot API Rate Limit Hit
- **Impact:** Sync writes fail partway through
- **Fallback:** Queue batch for retry with exponential backoff
- **Output:** Some contacts updated, others queued for next attempt
- **Action:** Retry logic built-in, monitor error logs

### If Lead Batch Is Unexpectedly Large (>500)
- **Impact:** Execution exceeds 8-minute window
- **Fallback:** Process top 300 by lead score, queue remainder for Wednesday
- **Output:** Partial success, queue for follow-up
- **Action:** Monitor HubSpot contact growth, increase frequency if needed

---

## Monitoring & Alerts

### Slack Notifications (on completion)
```
✅ Phone Waterfall Complete (Mon 6:15 AM)
   Pulled:       {N} leads | Apollo: {X%} | Clay: {Y%}
   Verified:     {X+Y} phones ({%})
   HubSpot Sync: ✓ | Execution: {time}s
   Callable:     Ready to dial
```

### Slack Alerts (on error)
```
⚠️ Phone Waterfall Partial (Mon 6:15 AM)
   Apollo: ✓ completed ({X%})
   Clay: ✗ API error — check credits
   Sync: ✓ synced Apollo results
   Action: Retry Clay Wednesday morning
   Dashboard: [link to error logs]
```

### Manual Monitoring
- **Weekly:** Check success rate in HubSpot (65%+ target)
- **Monthly:** Review Clay credit spend vs allocation
- **Monthly:** Audit Golden Rules filter (new AEs, products, exclusions)

---

## Integration Checklist

Before Monday 6:15 AM first run:

- [ ] HubSpot API key configured and has contacts:write permission
- [ ] Apollo API key configured
- [ ] Clay API configured (if using waterfall enrichment)
- [ ] Verify AE owner IDs are correct (Lex, Phil, Ron, Anthony)
- [ ] Test Apollo on 5 sample contacts
- [ ] Test Clay waterfall on 5 sample contacts
- [ ] Verify HubSpot phone field update works
- [ ] Schedule cron job: `15 6 * * 1` (Monday 6:15 AM)
- [ ] Add Slack notification to #sales channel
- [ ] Brief Tim on Monday morning workflow
- [ ] Test full flow on sample company batch

---

## Roadmap & Future Enhancements

### Short-term (v1.1)
- Add mobile vs. corporate phone preference (Tim prefers mobile for dials)
- Integrate with Dialpad API for direct queue sync (instead of CSV export)
- Add Clay waterfall retry logic (automatically retry Wednesday if Clay fails Monday)

### Medium-term (v1.2)
- Predictive phone scoring (historical dial success rates by source)
- Multi-language contact detection (non-English prospects)
- Competitor detection (flag Extron/Matrox device owners as high-signal)

### Long-term (v2.0)
- Real-time phone verification (trigger on new HubSpot contact creation)
- Phone number validation & formatting (international number support)
- Dial outcome feedback loop (log dials → improve ICP/intent scoring)

