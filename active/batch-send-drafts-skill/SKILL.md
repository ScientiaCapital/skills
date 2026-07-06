---
name: batch-send-drafts
description: "Review and batch-send staged Gmail BDR outreach drafts. Lists all queued drafts, shows a prioritized review table (recipient / subject / vertical), and generates one-click Gmail send links so Tim can flush the outreach queue in under 2 minutes. Trigger: send staged drafts, flush draft queue, batch send drafts, review my drafts, what drafts do I have."
version: "1.0.0"
---

<objective>
Surface all staged Gmail outreach drafts for review, group them by vertical/priority, and produce a one-click send link per draft — so Tim can review and flush the entire queue without hunting through Gmail. The Gmail MCP has no send tool; the bottleneck is knowing WHICH to send and in what order, not the click itself.
</objective>

<quick_start>
**Trigger:** "send staged drafts" / "flush draft queue" / "batch send drafts" / "review my drafts"
**From address:** tkipper@epiphan.com (always filter to this sender)
**Output:** Numbered review table + one Gmail link per draft → Tim clicks Send in browser
**MCP tools:** `list_drafts` → `search_threads` (for recipient enrichment if needed) → `qualify_lead` (per-recipient ATL/BTL, canonical source — see `skill-audit/specs/suppression-spec.md`)
</quick_start>

<success_criteria>
- [ ] All drafts from tkipper@epiphan.com fetched and displayed
- [ ] Table shows: # / Recipient / Subject / Vertical / Touch # / Draft Age
- [ ] Drafts prioritized: ATL contacts first, then by age (oldest first)
- [ ] One-click Gmail link per draft: `https://mail.google.com/mail/u/0/#drafts`
- [ ] Tim approves subset → links open, Tim sends in browser (one tab per draft)
- [ ] Outcome sidecar written with count queued / count confirmed for send
</success_criteria>

<workflow>

## Stage 1: Fetch all staged drafts

**MCP tool:** `mcp__claude_ai_Gmail__list_drafts`

Call with no filter first to get the full list. If the result is large (>50 drafts), call `mcp__claude_ai_Gmail__search_threads` with query `from:tkipper@epiphan.com in:drafts` to narrow to BDR outreach.

For each draft, extract:
- `id` — the Gmail draft ID (used to build the send link)
- `message.payload.headers` — scan for `To`, `Subject`
- `message.internalDate` or `message.payload.headers.Date` — draft age
- `message.snippet` — first 100 chars of body (vertical clue)

If `list_drafts` returns minimal header data, call `mcp__claude_ai_Gmail__get_thread` on the `threadId` of each draft to get full headers.

**Error/empty handling:**
- `list_drafts` errors (auth failure, timeout, etc.) → report the error to Tim verbatim and **halt** — do not proceed to Stage 2 with partial data.
- `list_drafts` succeeds with 0 drafts → report "No staged drafts found" and **halt** cleanly (this is a `success` status, not `error`).
- Append a line to `~/.claude/skill-runs/batch-send-drafts.jsonl` at both start and end of run (`{ts, status, drafts_found}`) so runs are auditable beyond the analytics sidecar.

## Stage 2: Enrich + classify

For each draft:

**Vertical detection** (from subject line + snippet, no extra API calls):
- `edu` / `university` / `college` / `higher ed` → Higher Ed
- `court` / `judicial` / `clerk` → Courts
- `city` / `county` / `government` / `municipality` → Government
- `hospital` / `health` / `medical` / `surgical` → Healthcare
- `church` / `worship` / `pastor` → Worship
- everything else → Corporate / Other

**ATL signal** — call `qualify_lead(recipient_email, name/title if parseable from headers)` per
recipient to resolve `power_level`. Do not substring-match titles inline; the canonical ATL/BTL
taxonomy lives in `qualify_lead` (see `skill-audit/specs/suppression-spec.md`), and a hand-rolled
keyword subset drifts from it.
- `power_level == atl` → ATL ★
- `power_level == gray` or `unknown` (or `qualify_lead` unreachable) → GRAY (ranked after ATL, before BTL)
- `power_level == btl` → BTL (ranked last; still shown — a draft already staged is never auto-dropped here)
- `junk == true` on the returned category → flag 🚫 in the table; Tim decides whether to still send

**Touch number** (from subject line patterns):
- `RE:` prefix or `[2]` / `[3]` / `FU` / `follow` → follow-up touch
- No prefix → Touch 1 (cold)

**Draft age:** days since `internalDate`. Flag drafts >7 days old with ⚠️ (stale, recipient context may have changed).

## Stage 3: Present review table

Sort order: ATL first → then by draft age DESC (oldest first, they've been waiting longest).

Present as a clean numbered table:

```
STAGED OUTREACH DRAFTS — <date> (<N> total)
──────────────────────────────────────────────────────────────────
 #  Recipient                Subject                    Vertical    Age   ATL?
──────────────────────────────────────────────────────────────────
 1  Dr. Smith (dean@u.edu)   [Pearl Mini] Lecture cap…  Higher Ed   3d    ★
 2  J. Johnson (jj@city.gov) Following up on Nexus…     Gov         1d    ★
 3  T. Nguyen (t@hosp.org)   Epiphan for OR suites…     Healthcare  5d ⚠️ ?
 4  …
──────────────────────────────────────────────────────────────────
<N> drafts ready. Which to send? (e.g. "all", "1-3", "1 3 5", "skip 3")
```

Ask Tim: **"Which drafts to send?"**

Accepted responses:
- `all` → confirm full list
- `1-4` → range
- `1 3 5` → specific numbers
- `skip 2` → all except
- draft number alone → just that one
- `none` / `cancel` → exit without sending

## Stage 4: Generate send links

For each confirmed draft, build the Gmail URL:

```
https://mail.google.com/mail/u/0/#drafts/<DRAFT_ID>
```

where `<DRAFT_ID>` is the `id` from the `list_drafts` response.

**Output format:**

```
READY TO SEND — open each link, review, click Send:

 1. Dr. Smith — [Pearl Mini] Lecture cap…
    → https://mail.google.com/mail/u/0/#drafts/18f3a...

 2. J. Johnson — Following up on Nexus…
    → https://mail.google.com/mail/u/0/#drafts/18f4b...

 3. T. Nguyen — Epiphan for OR suites…
    → https://mail.google.com/mail/u/0/#drafts/18f5c...

Open all <N> in tabs? Run: ! open -a "Google Chrome" "<url1>" "<url2>" ...
(Or cmd+click each link above.)
```

Also offer the one-liner `open` command so Tim can pop all selected drafts into Chrome tabs simultaneously:

```bash
! open -a "Google Chrome" "https://mail.google.com/mail/u/0/#drafts/ID1" "https://mail.google.com/mail/u/0/#drafts/ID2" ...
```

> **Why not auto-send?** The Gmail MCP exposes list/create/label but no send tool. A GCP project + Gmail API OAuth would enable programmatic send — flag in BACKLOG if Tim wants full automation later.

## Stage 5: Emit outcome sidecar

Write `~/.claude/skill-analytics/last-outcome-batch-send-drafts.json`:
```json
{
  "ts": "[UTC ISO8601]",
  "skill": "batch-send-drafts",
  "version": "1.0.0",
  "variant": "default",
  "status": "[success|partial|error]",
  "runtime_ms": "[est ms]",
  "metrics": {
    "drafts_found": "[n]",
    "drafts_confirmed_for_send": "[n]",
    "atl_count": "[n]",
    "stale_count": "[n]",
    "verticals": {"higher_ed": 0, "courts": 0, "gov": 0, "healthcare": 0, "other": 0}
  },
  "error": null,
  "session_id": "[YYYY-MM-DD]"
}
```

</workflow>

---

## Known limitation + upgrade path

**Current:** Tim clicks Send in browser (one tab per draft, ~5 sec each).
**Full automation requires:** GCP project → Gmail API enabled → `gws auth setup --project <id> --login` → then `gws mail send <draft_id>` per draft. See BACKLOG.md.

## Skill metadata
**Version:** 1.0.0 · **Status:** v1 (review + link; manual send) · **Author:** Tim Kipper
**Integration:** Gmail MCP (list_drafts, search_threads, get_thread) + `qualify_lead` (ATL/BTL classification, per suppression-spec.md)
**Tier:** P1 (BDR Core) · **Triggers:** Manual ("send staged drafts", "flush draft queue")
**Feeds:** outreach pipeline; complements morning-brief (draft count awareness)
