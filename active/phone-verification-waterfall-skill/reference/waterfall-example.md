# Example: Phone Waterfall in Action

Extracted verbatim from `phone-verification-waterfall-skill/SKILL.md`.

**Monday 6:15 AM kick-off:**
```
INPUT: HubSpot query finds 247 contacts with phone = null and meeting Golden Rules
APOLLO STAGE (2 min):
  Batched 247 into 5 parallel requests
  Success: 118 phones verified (47.8%)
  → Synced 118 to HubSpot immediately
  → Remaining: 129 needs Clay
CLAY STAGE (4 min):
  Batched 129 into company+title groups
  Ran find-and-enrich-contacts-at-company for each company
  Waterfall returned phones for 41 additional contacts (31.8%)
  → Synced 41 to HubSpot
  → Final miss: 88 (no phone found)
SYNC STAGE (30 sec):
  HubSpot batch updated 159 contacts (118 Apollo + 41 Clay)
  Tagged phone_source = 'apollo' or 'clay'
QUEUE STAGE (30 sec):
  Sorted 159 by ICP score (Higher Ed first, K-12 last)
  Output: Callable queue ready for 50+ dials
TOTAL TIME: 7 min 30 sec | CALLABLE: 159 verified | SUCCESS: 64.4%
```
