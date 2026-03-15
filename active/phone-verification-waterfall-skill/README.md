# Phone Verification Waterfall Skill

**Ensure Tim always has 50+ verified phone numbers queued for daily dials.**

This skill automatically pulls cold prospects from HubSpot, verifies phone numbers via Apollo + Clay waterfall enrichment, syncs back to HubSpot, and outputs a prioritized callable queue sorted by ICP score.

## Quick Start (30 seconds)

**Trigger phrases:**
- "verify phones"
- "phone waterfall"
- "callable leads"
- "who can I call"
- "dial list"
- "phone check"

**Expected output:** CSV of 50-100+ leads with verified phones, sorted by ICP (Higher Ed first, K-12 last)

**Scheduled:** Every Monday 6:15 AM (between prospect-enrich at 6:00 and prospect-refresh at 6:30)

## What It Does

1. **Pull leads** from HubSpot (contacts with phone = null, excluding customers/AE-owned/existing devices)
2. **Apollo lookup** → 40-50% get verified phones (free, no cost)
3. **Clay waterfall** → 30-40% of Apollo misses get phones (paid credits, ~$150-300/month)
4. **HubSpot sync** → Write verified numbers back to contact phone field
5. **Callable queue** → Sort by ICP score + intent signals, output CSV for Dialpad/Aircall

## Key Metrics

| Metric | Target |
|--------|--------|
| Callable leads | 50+ |
| Phone verification rate | 65-70% |
| Execution time | <8 min |
| Cost/month | $150-300 (Clay only) |

## Documentation

- **SKILL.md** — Full skill definition (use when triggering manually)
- **config.json** — Skill metadata, triggers, MCP tools, scheduling
- **IMPLEMENTATION.md** — Setup checklist, troubleshooting, examples
- **INTEGRATION_MAP.md** — Architecture, dependencies, data flow
- **EXAMPLE_OUTPUTS.md** — Real console output from 3 scenarios (success, partial, error)
- **golden-rules-filter.md** — Reusable exclusion logic (also used by prospect-research-to-cadence-skill)

## Integration

**Upstream (requires):**
- prospect-enrich-skill (runs at 6:00 AM, refreshes company data)
- HubSpot data quality (accurate emails, first_conversion tracking)

**Downstream (feeds):**
- Dialpad/Aircall (import CSV queue for dialing)
- Sales engagement platforms (trigger cadences on enriched leads)
- Tim's daily 7 AM dial start (50+ ready-to-call leads)

## Golden Rules (Hard Filters)

These contacts are ALWAYS skipped:
- Customers (lifecycle_stage = 'customer')
- Product engagers (first_conversion contains 'Pearl', 'setup', 'Connect', 'signup')
- Existing device owners (company.device_count >= 1)
- Channel partners (is_channel = true)
- Account Executive leads (owned by Lex, Phil, Ron, Anthony)

## Setup Checklist

- [ ] Verify HubSpot API connection
- [ ] Verify Apollo API connection
- [ ] Verify Clay API connection
- [ ] Confirm AE owner IDs (Lex, Phil, Ron, Anthony)
- [ ] Test on small batch (Stanford University, ~20 contacts)
- [ ] Schedule cron: `15 6 * * 1` (Monday 6:15 AM)
- [ ] Add Slack notification to #sales
- [ ] Brief Tim on Monday morning workflow
- [ ] Go live

See IMPLEMENTATION.md for detailed setup steps.

## Performance Targets

**Yield:**
- Leads pulled: 100-250
- Apollo success: 40-50%
- Clay waterfall: 30-40% (of Apollo misses)
- Total verified: 65-70%

**Callable:**
- Queue size: 50+ minimum
- Top tier (ICP 80+): ~30-40 leads
- Mid tier (ICP 60-79): ~20-30 leads

**Timing:**
- Monday 6:15 AM run completes by 6:23 AM (8-min window)
- Results ready for Tim's 7 AM dial start
- CSV exported to Dialpad automatically

## Cost & Resources

- **Apollo:** $0 (included in existing subscription)
- **Clay:** ~$150-300/month (depends on contacts enriched)
- **HubSpot:** Already in use
- **Execution:** <8 min weekly (automated, unattended)

## Common Issues

**Low phone verification rate (<50%)?**
- Check Apollo API quota
- Check Clay credit balance
- Check HubSpot contact quality (emails, company data)

**Execution takes >10 min?**
- API rate limits hit
- Check HubSpot/Apollo/Clay status pages
- Run smaller batch or split across days

**HubSpot sync failing?**
- Check API rate limit errors
- Validate phone number format
- Check API key permissions

See IMPLEMENTATION.md troubleshooting section for full details.

## Next Steps

1. Read IMPLEMENTATION.md (Setup section)
2. Follow the 8-step activation checklist
3. Test on small batch (5 min)
4. Go live Monday 6:15 AM
5. Monitor Slack notifications

---

**Contact:** Tim Knottenbelt (BDR/Application Engineer, Epiphan Video)  
**Created:** 2026-03-15  
**Version:** 1.0.0

