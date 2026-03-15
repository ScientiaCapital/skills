# Implementation Guide — Phone Verification Waterfall Skill

## Quick Setup (5 minutes)

### 1. Verify API Connections
Before activating the skill, confirm these are working:

```bash
# Test HubSpot
curl -H "Authorization: Bearer $HUBSPOT_API_KEY" \
  https://api.hubapi.com/crm/v3/objects/contacts?limit=1

# Test Apollo
python3 << 'PY'
import requests
resp = requests.get('https://api.apollo.io/v1/contacts?api_key=' + APOLLO_KEY)
print(resp.status_code)
PY

# Test Clay (if available)
# Clay uses direct UI + MCP, no direct API test needed
```

### 2. Confirm HubSpot Owner IDs
The skill references these AE IDs for exclusion:
- 82625923 (Lex Finkle)
- 423155215 (Phil Hutchins)
- Ron* (pattern)
- Anthony* (pattern)

**Verify these are correct:**
```bash
# In HubSpot, go to Settings → Users & Teams
# Look up: Lex, Phil, Ron, Anthony
# Copy their owner_id values
# Update config.json excluded_contact_filters if different
```

### 3. Test on Small Batch
Before running Monday 6:15 AM, test with a small prospect batch:

```
Trigger: "verify phones" (manual trigger)
Filter by company: "Stanford University" (known Higher Ed prospect)
Expected: 10-20 contacts pulled, 6-8 phones verified
Duration: Should complete in <2 minutes for 20 contacts
```

### 4. Schedule Monday 6:15 AM Run
Add to your scheduling system (Zapier, cron, Claude task, etc.):

```bash
# Scheduled task
Task ID: phone-waterfall-monday-6-15am
Cron: 15 6 * * 1 (Mon 6:15 AM)
Command: trigger_skill("phone-verification-waterfall")
Notify: Post results to Slack #tim-bdr or #sales
```

---

## Operational Checklist

### Weekly (Before Monday 6:15 AM)
- [ ] Confirm Clay has available credits (check Clay dashboard)
- [ ] Verify HubSpot sync is working (no API rate limit issues)
- [ ] Check that prospect-enrich-skill ran successfully at 6:00 AM

### Monthly (End of month)
- [ ] Review phone verification rate (aim: 65%+)
- [ ] Check Clay credit usage vs allocation
- [ ] Update Golden Rules filter if new AEs hired or policies changed

### Quarterly
- [ ] Audit first_conversion keywords (add new product names)
- [ ] Review ICP vertical scores (adjust if strategy shifts)
- [ ] Check for new channel partners to exclude

---

## Troubleshooting

### Low Phone Verification Rate (<50%)
**Symptom:** Fewer phones verified than expected
**Causes:**
1. Apollo API quota exhausted → check Apollo dashboard
2. Clay not configured → verify Clay MCP connection
3. Many contacts from newer companies → Clay needs more time to index

**Fix:**
- Run Apollo-only (skip Clay) if Clay credits are low
- Increase batch size for Clay enrichment (takes longer but more complete)
- Check Clay account status

### HubSpot Sync Failing
**Symptom:** Phones verified but not appearing in HubSpot
**Causes:**
1. API rate limit hit → queue and retry
2. Invalid phone format → check phone regex validation
3. Insufficient HubSpot API permissions → check API key scope

**Fix:**
- Check HubSpot error logs for rate limit messages
- Validate phone format before sync (US: (XXX) XXX-XXXX or +1-XXX-XXX-XXXX)
- Verify API key has contacts:write permission

### Execution Takes >10 Minutes
**Symptom:** Skill takes too long to run
**Causes:**
1. Large batch of contacts (>500) → split into weeks
2. Clay enrichment slow → Clay API latency
3. HubSpot sync timeout → retry needed

**Fix:**
- Increase schedule frequency (run Wed instead of just Mon)
- Reduce batch size if API rate limits
- Add retry logic with exponential backoff

---

## Integration Points

### Downstream: Sales Engagement Cadences
Once contacts have phones, they're ready for:
- Dialpad integration (import CSV queue)
- Aircall integration (direct sync)
- Sales engagement platform (Apollo sequences, HubSpot workflows)

**Example:** prospect-research-to-cadence-skill can now target these contacts with verified phones for immediate outreach.

### Upstream: Prospect Sourcing
Relies on:
- prospect-enrich-skill (6:00 AM) — refreshes company data
- HubSpot data quality — accurate email + first_conversion values

**Example:** If prospect-enrich-skill fails at 6:00 AM, phone waterfall runs on stale data.

### Sibling: Prospect Refresh
prospect-refresh-skill (6:30 AM) can use phone verification results to:
- Update deal velocity metrics (phones available for dialing)
- Trigger automated outreach workflows
- Calculate BDR capacity (dial capacity vs actual dials)

---

## Performance Targets

| Metric | Target | Current | Notes |
|--------|--------|---------|-------|
| Total leads pulled | 100+ | — | Should find 100-250 cold prospects |
| Apollo success rate | 40-50% | — | Baseline expectation |
| Clay waterfall rate | 30-40% of Apollo misses | — | Depends on Clay credit availability |
| Combined verified rate | 65-70% | — | (Apollo) + (Clay of remainder) |
| Execution time | <8 minutes | — | Includes HubSpot sync |
| Callable leads ready | 50+ | — | Minimum for daily dials (50+/day) |

---

## Examples

### Example 1: Successful Run (Monday 6:15 AM)
```
📊 Phone Waterfall Results
├─ Leads Pulled: 187 (HubSpot)
├─ Golden Rules Filtered: -34 (customers, AE-owned, device owners)
├─ Ready for Enrichment: 153
│
├─ Apollo Lookup: 73 verified (47.7%)
├─ Clay Waterfall: 34 verified (22.2% of remainder)
├─ Total Verified: 107 (69.9%)
│
├─ HubSpot Synced: 107 ✓
├─ Execution Time: 6m 42s
│
└─ 🎯 CALLABLE QUEUE READY
   Top prospect: Jane Smith (Stanford, VP IT, 93 ICP)
   Import to Dialpad: [link]
   Full CSV: [download]
```

### Example 2: Partial Success (API Constraint)
```
⚠️ Phone Waterfall Partial
├─ Leads Pulled: 247
├─ Apollo Success: 118 (47.8%) ✓
├─ Clay API Slow: 41 verified (16.6%) — took 5m+ (Clay latency)
├─ Total Verified: 159 (64.4%)
│
└─ ℹ️ ACTION: Clay enrichment slow
   Continue with Apollo-only queue
   Retry Clay waterfall Tuesday morning
   Check Clay API status
```

### Example 3: Dry Run (New Contact Batch)
```
ℹ️ Phone Waterfall Test Run
├─ Company: Stanford University
├─ Leads Pulled: 18 (test batch)
├─ Apollo: 8 verified (44%)
├─ Clay: 3 verified (27% of remainder)
├─ Total: 11 verified (61%) ✓
│
└─ Ready for production Monday
   Success rate matches expectations
   No API issues detected
```

---

## Support & Debugging

### Enable Verbose Logging
For troubleshooting, request verbose mode:
```
Trigger: "verify phones with debug"
Output: includes Apollo request/response details, Clay waterfall logs, HubSpot sync status
```

### Check Scheduled Task Status
```bash
# View all scheduled tasks
list_scheduled_tasks()

# Get phone-waterfall-specific history
get_scheduled_task_runs(task_id="phone-waterfall-monday-6-15am", limit=10)
```

### Manual Re-run
If Monday 6:15 AM run fails, manually trigger:
```
"verify phones" or "phone waterfall"
Runs immediately with same config
Overwrites any previous Monday results
```

---

## Next Steps

1. **Confirm API connections** (Step 1 above)
2. **Verify AE owner IDs** (Step 2 above)
3. **Test on small batch** (Step 3 above)
4. **Schedule Monday run** (Step 4 above)
5. **Monitor first week** — check results, adjust as needed

Questions? See SKILL.md for full reference or reach out to Tim.

