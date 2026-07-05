# Lead Suppression Spec (proposal — specifies only; does not write to HubSpot)

One global suppression rule, referenced by every list-producing skill instead of being re-implemented per skill. This audit found suppression/dedupe logic hand-rolled independently in at least 12 skills (contact-hunter, sdr-dial-lists, he-dial-queue, callable-lead-count, phone-verification-waterfall, prospect-enrich, prospect-refresh, prospect-research-to-cadence, sequence-load, morning-brief, deal-momentum-analyzer, close-plan-generator, and others) — each a slightly different subset of CLAUDE.md's Golden Rules / ATL-BTL taxonomy, guaranteed to drift.

## State of record

HubSpot contact properties (proposed, not yet created):
- `bdr_suppressed` (boolean)
- `bdr_suppression_reason` (enum: `no_email` | `no_phone` | `dismissed` | `bad_fit` | `do_not_contact`)
- `bdr_suppressed_date` (date)

## Fallback

When HubSpot write access is unavailable: append to `~/.claude/skill-state/suppression.jsonl`; reconcile to HubSpot on the next authorized run. Never let a missing write capability silently skip suppression — degrade to the fallback file, don't skip the check.

## Release condition

Suppression lifts on a NEW engagement signal only:
- Form fill (HubSpot `first_conversion` timestamp newer than `bdr_suppressed_date`)
- Email reply (Gmail thread activity from the contact after suppression date)
- Meeting booked (HubSpot meeting engagement after suppression date)
- Device registration (Epiphan device-analytics activity after suppression date)
- Intent/page-visit signal (via whatever intent tooling is wired, e.g. intent-signal-aggregator-skill)

No other event (time elapsed, list refresh, manual re-run) lifts suppression.

## Enforcement point

**`qualify_lead` is the single gate.** Every list-producing or dial-list-building skill calls `qualify_lead` immediately after its initial candidate pull (Gate A: dedupe), before any ATL/BTL tiering, enrichment spend, or draft creation. Skills should stop hand-rolling Golden Rules / NEVER-ATL keyword tables inline — that logic re-derives (and drifts from) what `qualify_lead` already returns (`category`, `power_level`, junk flag per the `nooks-autopilot` reference implementation).

**IMPORTANT:** Creating the HubSpot properties above and writing suppression state are actions Tim must approve separately. This spec only defines the contract; the audit does not create properties or write to HubSpot.
