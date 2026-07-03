# Final Callable Queue Format

Extracted verbatim from `phone-verification-waterfall-skill/SKILL.md` (Stage 5 output template).

```
═══════════════════════════════════════════════════════════════════════════════
CALLABLE QUEUE — Phone Waterfall Results
Generated: {timestamp} | Success Rate: {70-80%}
═══════════════════════════════════════════════════════════════════════════════

SUMMARY:
Total Leads Pulled:        {N}
Apollo Matches:            {X} ({X%})
Clay Enrichments:          {Y} ({Y%})
Total Verified Phones:     {X+Y} ({(X+Y)%})
HubSpot Updated:           {X+Y}
ATL Contacts:              {A} ({A%})
Gray Zone:                 {G} ({G%})
BTL Contacts:              {B} ({B%})

READY TO DIAL (sorted ATL first, then ICP score + intent):

 #  │ NAME              │ TIER │ TITLE            │ COMPANY           │ PHONE        │ ICP  │ VERTICAL     │ INTENT SIGNAL
────┼──────────────────┼──────┼──────────────────┼──────────────────┼──────────────┼──────┼──────────────┼─────────────────
  1 │ Jane Smith       │ ATL  │ VP IT/AV         │ Stanford Univ    │ (650)xxx-xxx │ 93   │ Higher Ed    │ New AV role + hiring
  2 │ Mike Johnson     │ ATL  │ Dir Technology   │ Federal Courts   │ (202)xxx-xxx │ 87   │ Courts/Legal │ Extron aging out
  3 │ Sarah Chen       │ GRAY │ Manager IT       │ UCSF Medical     │ (415)xxx-xxx │ 78   │ Healthcare   │ Facility upgrade
  4 │ David Lee        │ BTL  │ AV Technician    │ Cisco Corp       │ (408)xxx-xxx │ 82   │ Corp AV      │ Meeting room reno
  5 │ ...              │ ...  │ ...              │ ...              │ ...          │ ...  │ ...          │ ...

═══════════════════════════════════════════════════════════════════════════════
DIALER QUICK LINKS:
- Download CSV:        [queue.csv]
- Import to Dialpad:   [sync button]
- Import to Aircall:   [sync button]
- By Company:          [grouped view]
- By Vertical:         [vertical view]
- By ATL/BTL Tier:     [tier view]

NEXT STEPS:
1. Prioritize ATL contacts first (decision-makers with budget authority)
2. Review GRAY zone contacts for manual budget authority verification
3. Import to your dialpad tool
4. Dial 50+ per day, log outcomes, let Sales Engagement cadences trigger

═══════════════════════════════════════════════════════════════════════════════
```
