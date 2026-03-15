# Example Outputs — Phone Verification Waterfall Skill

## Scenario 1: Full Success Run (Monday 6:15 AM)

**Triggers:** "verify phones" or scheduled Monday 6:15 AM

**Console Output:**
```
🔄 Phone Verification Waterfall Starting...

STAGE 1: PULL LEADS FROM HUBSPOT
─────────────────────────────────
Query: phone = NULL AND lifecyclestage != 'customer' AND excludes Golden Rules
Results: 187 contacts with missing phones
Filter Applied: -34 (customers, AE-owned, device owners, channel partners)
Ready for enrichment: 153

Breakdown by ICP Vertical:
  Higher Ed:      52 contacts (34%)
  Healthcare:     28 contacts (18%)
  Government:     25 contacts (16%)
  Corporate AV:   24 contacts (16%)
  Courts/Legal:   15 contacts (10%)
  K-12:            9 contacts ( 6%)

STAGE 2: APOLLO PHONE LOOKUP
─────────────────────────────
Enriching 153 contacts via Apollo people_match...
Batch 1 (50 contacts): 23 matches (46%)
Batch 2 (50 contacts): 25 matches (50%)
Batch 3 (53 contacts): 21 matches (40%)
─────────────────────────────────────────────
Apollo Success: 69 phones verified (45.1%)
Apollo Miss: 84 contacts (54.9%)

Phone Sources from Apollo:
  corporate_phone: 41 (59%)
  mobile_phone:    28 (41%)

STAGE 3: CLAY WATERFALL ENRICHMENT
───────────────────────────────────
Processing 84 Apollo misses via Clay...
Find Company Groups: 8 unique companies
Running enrichment: find-and-enrich-contacts-at-company
├─ Group 1 (Stanford Univ, 12 people): 7 matched (58%)
├─ Group 2 (UCSF Medical, 8 people): 4 matched (50%)
├─ Group 3 (Berkeley Lab, 7 people): 3 matched (43%)
├─ Group 4 (SF Federal Courts, 9 people): 6 matched (67%)
├─ Group 5 (Cisco Corp, 15 people): 8 matched (53%)
├─ Group 6 (Kaiser Permanente, 12 people): 6 matched (50%)
├─ Group 7 (SF State Univ, 12 people): 5 matched (42%)
├─ Group 8 (Google, 9 people): 4 matched (44%)

Clay Success: 43 phones verified (51.2% of Apollo misses)
Clay Miss: 41 contacts (48.8%)

Total phones found: 69 (Apollo) + 43 (Clay) = 112 verified (73.2% success)

STAGE 4: HUBSPOT SYNC
─────────────────────
Batch updating 112 contacts to HubSpot...
Batch 1 (100 contacts): ✓ updated successfully
Batch 2 (12 contacts): ✓ updated successfully

Fields Updated:
  phone ..................... verified number
  phone_source .............. "apollo" or "clay"
  phone_verified_at ......... 2026-03-15T06:15:32Z
  phone_waterfall_pass ...... true

All syncs complete ✓

STAGE 5: CALLABLE QUEUE GENERATION
───────────────────────────────────
Building queue: 112 contacts with verified phones
Sorting by: ICP score (primary) + Intent signals (secondary)

Sample of Top 10:
┌─────┬──────────────────┬─────────────┬──────────────┬─────────────┬──────┬──────────────┬──────────────────────┐
│  #  │ NAME             │ TITLE       │ COMPANY      │ PHONE       │ ICP  │ VERTICAL     │ INTENT SIGNAL        │
├─────┼──────────────────┼─────────────┼──────────────┼─────────────┼──────┼──────────────┼──────────────────────┤
│  1  │ Jane Smith       │ VP IT/AV    │ Stanford     │(650)555-001 │ 95   │ Higher Ed    │ Hiring AV role +10   │
│  2  │ Mike Johnson     │ Dir Tech    │ UC Berkeley  │(510)555-002 │ 94   │ Higher Ed    │ New media center +15 │
│  3  │ Sarah Chen       │ Manager AV  │ UCSF Med     │(415)555-003 │ 88   │ Healthcare   │ Facility reno +12    │
│  4  │ David Rodriguez  │ VP Ops      │ SF Fed Ct    │(415)555-004 │ 87   │ Courts/Legal │ Extron aging out +12 │
│  5  │ Elena Vasquez    │ AV Manager  │ Cisco        │(408)555-005 │ 85   │ Corp AV      │ Meeting rms reno +8  │
│  6  │ Robert Kim       │ IT Director │ Kaiser       │(510)555-006 │ 82   │ Healthcare   │ Digital health +5    │
│  7  │ Jennifer Wu      │ Dir Media   │ SF State     │(415)555-007 │ 80   │ Higher Ed    │ Streaming platform +8│
│  8  │ Marcus Johnson   │ AV Tech     │ Google       │(650)555-008 │ 78   │ Corp AV      │ Conference room +5   │
│  9  │ Patricia Brown   │ VP IT       │ Stanford     │(650)555-009 │ 77   │ Higher Ed    │ IT refresh cycle +10 │
│ 10  │ Christopher Lee  │ Manager Ops │ UC Davis     │(530)555-010 │ 76   │ Higher Ed    │ Expansion project +6 │
└─────┴──────────────────┴─────────────┴──────────────┴─────────────┴──────┴──────────────┴──────────────────────┘

Full queue: 112 contacts | Execution time: 6m 42s ✓

CALLABLE QUEUE READY ✓
═════════════════════════════════════════════════════════════════════

📊 METRICS
──────────
Total Leads Pulled:            187
Golden Rules Filtered:         -34 (-18%)
Available for Enrichment:      153
Apollo Verified:                69 (45%)
Clay Verified:                  43 (28%)
Total Verified Phones:         112 (73%)
HubSpot Synced:                112 (100%)
Queue Ready to Dial:           112

🎯 PRIORITIES
─────────────
Tier 1 (Higher Ed, ICP 90+):   18 contacts — CALL FIRST
Tier 2 (Health/Gov, ICP 80+):  34 contacts — CALL SECOND
Tier 3 (Corporate AV, ICP 70+):35 contacts — CALL THIRD
Tier 4 (Lower scores, <70):    25 contacts — CALL FOURTH

📲 NEXT STEPS
─────────────
1. Open Dialpad at 7:00 AM
2. Import CSV queue: [download link]
3. Start with Tier 1 prospects (Higher Ed)
4. Target: 50+ dials today
5. Log outcomes → trigger sales cadences

═════════════════════════════════════════════════════════════════════
✓ Success! All systems ready for dialing.
```

---

## Scenario 2: Partial Success (API Constraint)

**Context:** Clay has credit constraints or API latency

**Console Output:**
```
🔄 Phone Verification Waterfall Starting...

STAGE 1: PULL LEADS
Results: 247 contacts with missing phones
Filter: -42 (Golden Rules)
Ready: 205

STAGE 2: APOLLO LOOKUP
Apollo: 97 phones verified (47.3%)

STAGE 3: CLAY WATERFALL
⚠️ WARNING: Clay API responding slowly
Batch 1 (50 contacts): 8 matched (16%) ⏱️ 2:15
Batch 2 (50 contacts): 9 matched (18%) ⏱️ 2:45
Continuing...

⚠️ Clay taking >4 minutes for 2 batches
Remaining: 54 contacts
Estimated time if Clay: 6+ additional minutes
Total would exceed 8-minute window

📌 DECISION: Stopping Clay, returning Apollo-only results
Reason: Keep under 8-minute SLA for Monday 6:15 AM window

STAGE 4: HUBSPOT SYNC
Syncing 97 Apollo-verified phones
✓ Complete: 97 contacts updated

STAGE 5: CALLABLE QUEUE
Queue: 97 contacts (Apollo only)
Missing: 108 potential phones (from Clay misses)

═════════════════════════════════════════════════════════════════════
⚠️ PARTIAL SUCCESS

Total Verified: 97 phones (47.3%)
HubSpot Synced: 97 ✓
Ready to Dial: 97 contacts
Execution Time: 8m 02s (exceeded 8-min SLA by 2 sec)

📌 ACTION ITEMS
───────────────
1. Apollo completed successfully ✓
2. Clay API slow — check Clay status/credits
3. Consider running Clay waterfall separately Wednesday 6:15 AM
4. Check Clay dashboard: [link]

💡 OPTIMIZATION
────────────────
Next Monday, consider:
- Pre-batching Clay requests Thursday
- Checking Clay credits before Monday run
- Running Clay on Tue/Wed if anticipating slowness

📲 USE THIS QUEUE FOR MONDAY DIALS
You have 97 verified phones ready now.
Supplemental 108 phones will come Wed if Clay recovers.

═════════════════════════════════════════════════════════════════════
```

---

## Scenario 3: Error Recovery (API Failure)

**Context:** HubSpot API returns error during sync

**Console Output:**
```
🔄 Phone Verification Waterfall Starting...

STAGE 1-2: PULL & APOLLO
✓ Apollo: 72 phones verified

STAGE 3: CLAY WATERFALL
✓ Clay: 31 phones verified
✓ Total: 103 phones found

STAGE 4: HUBSPOT SYNC
Batch 1 (100 contacts): ✓ updated
Batch 2 (3 contacts): ✗ ERROR

Error Details:
  API Response: 429 Too Many Requests
  Rate Limit: 100 requests/second (you're at 105)
  Retry-After: 60 seconds

⚠️ HUBSPOT RATE LIMIT HIT
Some contacts queued for retry

RETRY STRATEGY:
Waiting 65 seconds...
Retrying Batch 2 (3 contacts)...
✓ Retry successful: 3 contacts updated

STAGE 5: CALLABLE QUEUE
Final: 103 contacts synced to HubSpot ✓
Queue Ready: 103

═════════════════════════════════════════════════════════════════════
✓ RECOVERED FROM ERROR

Total Verified: 103 phones
HubSpot Synced: 103 ✓
Queue Ready: 103 (same as before error)
Execution Time: 7m 45s (includes retry delay)

Retry handled automatically — no manual action needed.

═════════════════════════════════════════════════════════════════════
```

---

## CSV Export Format (for Dialpad/Aircall Import)

**Filename:** `callable_queue_20260315_061532.csv`

```csv
contact_id,first_name,last_name,email,company,title,phone,icp_score,vertical,intent_signals,phone_source,last_enriched
63b4a8f9e9c8d5a2,Jane,Smith,jane.smith@stanford.edu,Stanford University,VP IT/AV,(650)555-0101,95,Higher Education,Hiring AV role +10; New media center,apollo,2026-03-15T06:15:32Z
63b4a8f9e9c8d5a3,Mike,Johnson,mike.j@berkeley.edu,UC Berkeley,Director Technology,(510)555-0102,94,Higher Education,Facility expansion +12; Streaming platform,clay,2026-03-15T06:15:32Z
63b4a8f9e9c8d5a4,Sarah,Chen,s.chen@ucsf.edu,UCSF Medical,Manager AV,(415)555-0103,88,Healthcare,Facility renovation +12; Digital health,apollo,2026-03-15T06:15:32Z
...
```

---

## Dashboard Metrics (Weekly View)

After Monday 6:15 AM run completes, these metrics are logged:

```
PHONE WATERFALL — WEEKLY METRICS
═════════════════════════════════════════════════════════════════

Week of: Mar 15-21, 2026

YIELD ANALYSIS
──────────────
Contacts Pulled:        189
Golden Rules Filtered:   -38 (20%)
Available:              151
Apollo Matches:          69 (46%)
Clay Enriched:           43 (62% of Apollo misses)
Total Verified:         112 (74%)

PERFORMANCE
───────────
Apollo Success Rate:    46% (baseline 40-50% ✓)
Clay Success Rate:      62% (baseline 30-40% ✗ HIGH)
Combined Rate:          74% (target 65-70% ✓)
Execution Time:         6m 42s (target <8min ✓)
Callable Leads:         112 (target 50+ ✓)

BY VERTICAL
───────────
Higher Ed:       52 leads verified | ICP avg: 89
Healthcare:      28 leads verified | ICP avg: 78
Government:      25 leads verified | ICP avg: 81
Corporate AV:    24 leads verified | ICP avg: 79
Courts/Legal:    15 leads verified | ICP avg: 84
K-12 Schools:     9 leads verified | ICP avg: 68

INTENT SIGNALS (TOP BOOSTERS)
──────────────────────────────
Hiring AV roles:        +15 points (24 contacts detected)
Facility expansion:     +12 points (18 contacts detected)
Extron aging out:       +12 points (8 contacts detected)
Tech stack gaps:         +8 points (34 contacts detected)
Funding/acquisition:     +5 points (12 contacts detected)

TREND
─────
vs Last Week: +15 contacts callable (8% growth)
YTD Success: 71% average (trend: ↑)
Monthly Cost: Clay $180 (budget: $200)

═════════════════════════════════════════════════════════════════
```

