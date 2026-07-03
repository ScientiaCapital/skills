---
name: orlob-discovery-framework
description: "Chris Orlob's 5-step discovery framework applied to Epiphan — business problem → cause analysis → negative impact → future state → close. Per-vertical root causes, calibrated question bank, MEDDIC integration, and the 0-3 discovery scoring rubric used by sdr-call-coaching. Use when: discovery framework, orlob discovery, discovery questions, cause analysis, business problem discovery, how to run discovery."
version: "1.0.0"
---

<objective>
Run buyer-centric discovery on Epiphan sales calls using Chris Orlob's 5-step
framework. The goal is to peel past the surface feature request to a business
problem the buyer owns, trace it to a root cause Epiphan products actually fix,
quantify the negative impact, paint the future state, and close to a concrete
next step — capturing MEDDIC along the way. This skill is the reference that
`sdr-call-coaching` scores against and that `epiphan-call-playbook` and
`sdr-dial-lists` draw calibrated questions from.
</objective>

<quick_start>
The 5 steps, in order, every discovery call:

1. **Business Problem** — what's the actual problem behind the ask? (not the feature)
2. **Cause Analysis** — what's *driving* that problem? (root cause, see `reference/epiphan-root-causes.md`)
3. **Negative Impact** — what does it cost them? (quantified: time, money, students, cases, congregants)
4. **Future State** — what does "fixed" look like, in their words?
5. **Close** — lock a specific next step with a date and an owner.

Tim's proven opener for Step 1/2 (works across verticals):
> "Where do you tend to lose the most time — capture, switching sources, or getting recordings out the door?"

Never feature-dump. Ask, listen, confirm the pain back, *then* connect a product.
</quick_start>

<success_criteria>
A discovery call ran well if, by the end, you can write down:
- The **business problem** in the buyer's own words (not "they want a Pearl Mini").
- The **root cause** driving it, confirmed back to the buyer (matched to `reference/epiphan-root-causes.md`).
- A **quantified negative impact** (a number the buyer said out loud, or agreed to).
- The buyer's **future state** — what success looks like to *them*.
- A **committed next step**: date, owner, and what happens (demo, technical call, POC).
- MEDDIC coverage: at minimum Identify Pain + Metrics, plus whatever Economic Buyer /
  Decision Process / Champion signals surfaced.

Scores 3/3 on the discovery dimension of `sdr-call-coaching` when cause analysis
surfaced a root cause the buyer owns (see Scoring Rubric below).
</success_criteria>

<core_content>

## The 5-Step Framework

Discovery is a funnel, not a checklist. Each step earns the right to the next.
You cannot quantify impact (Step 3) on a problem you haven't diagnosed (Step 2),
and you can't diagnose a problem the buyer hasn't admitted is a problem (Step 1).
Move down only when the buyer has agreed with you at the current step.

```
Step 1  Business Problem   →  "So the real issue is X, not just needing new gear?"
Step 2  Cause Analysis     →  "And what's driving X — is it A, B, or C?"
Step 3  Negative Impact    →  "When X happens, what does it cost you?"
Step 4  Future State       →  "If X were solved, what changes for you?"
Step 5  Close              →  "Makes sense to get [next step] on the calendar?"
```

---

## Step 1: Surface the Business Problem

Get past the feature request ("I need a lecture-capture box") to the business
problem behind it ("faculty stopped recording and students are complaining").
Buyers open with solutions; your job is to walk them back to the problem.

**Epiphan example (Higher Ed):**
Buyer says: "We're looking at replacing our capture appliances." You: "Before we
talk boxes — what made replacing them a priority *now*? What's not working with
what you have?" → surfaces "usage dropped below half and the provost is asking why."

**What good looks like:** the buyer describes a business outcome at risk (adoption,
uptime, compliance, the record, the service) — not a spec.

**Calibrated questions (ask at least one open one before any product talk):**
- "What made this a priority now — what changed?"
- "Where do you tend to lose the most time — capture, switching sources, or getting recordings out the door?" *(Tim's proven line)*
- "If nothing changed here, what happens six months from now?"
- "How do you currently handle [the workflow they mentioned]?" *(Voss calibrated)*

**Do NOT:** pitch a product, name a SKU, or list specs. You're diagnosing.

---

## Step 2: Cause Analysis

The most-skipped, highest-value step. Take the stated problem and find the
*root cause* — because the root cause is what Epiphan actually fixes, and naming
it is what makes the buyer trust you diagnosed correctly. Use
`reference/epiphan-root-causes.md` to match the buyer's symptom to a known cause
for their vertical, then confirm it back.

**Epiphan example (Higher Ed):**
Problem: "faculty stopped recording." Cause-analysis: "What's making it hard for
them — is it the setup per room, the different source types, or that nobody's
around when something fails?" Buyer: "Honestly, one guy supports 50 rooms." →
root cause = **AV-staffing crunch** (from the reference file).

**Calibrated questions:**
- "What's driving that — is it A, B, or C?" *(offer the vertical's known causes)*
- "What happens when [the failure] occurs — who gets the call?" *(Voss calibrated)*
- "Walk me through the last time this broke — where exactly did it fall apart?"
- "Is that a people problem, a gear problem, or a workflow problem?"

**Do NOT:** accept the symptom as the cause. "Recordings are inconsistent" is a
symptom; "one tech covers 50 rooms so nobody's there on a failure" is a cause.
See `reference/epiphan-root-causes.md` for the symptom→cause map per vertical.

---

## Step 3: Negative Impact (Quantified)

Turn the root cause into a number the buyer says out loud. Cost of inaction is
what creates urgency and justifies budget. Push gently for quantification —
time, money, headcount, students touched, cases delayed, congregants reached.

**Epiphan example (Higher Ed):**
> "If a faculty member stops recording because it's too hard, how many students
> does that touch?" → buyer: "A big lecture is 300 kids." Now the AV-staffing
> crunch has a number attached, and the problem is worth solving.

**Calibrated questions:**
- "If a faculty member stops recording because it's too hard, how many students does that touch?" *(Tim's proven impact line)*
- "How many hours a week does your team spend firefighting this?"
- "What does a failed [service / proceeding / all-hands] cost you — not just dollars, reputation too?"
- "How often does this happen — weekly, every event, once a semester?"

**Do NOT:** move to solution while the impact is still vague. If the buyer won't
quantify, the problem may not be painful enough to buy against — note that.

---

## Step 4: Future State

Have the buyer describe what "solved" looks like *in their words*. This gives you
their Decision Criteria for free and makes the eventual demo a confirmation of
their own vision rather than a feature tour.

**Epiphan example (Corporate AV):**
> "If hybrid all-hands just worked every time — nobody sweating the stream —
> what would that free your team up to do?" → buyer describes the win, and you've
> got their success criteria and an emotional stake in it.

**Calibrated questions:**
- "If this were solved, what changes for you day-to-day?"
- "What would need to be true for you to consider this a win?" *(Voss calibrated)*
- "A year from now, if this worked, what does your team stop worrying about?"
- "Who else feels the relief when this is fixed?" *(surfaces stakeholders → MEDDIC)*

**Do NOT:** describe *your* future state ("with Pearl you'll be able to…"). Let
them paint it; you map the product to their picture at demo time.

---

## Step 5: Close to Next Step

Every discovery call ends with a committed next step — a date, an owner, and what
happens. "I'll send some info" is not a close. Tie the next step to the problem
and impact you just uncovered so it feels like progress, not a sales push.

**Epiphan example:**
> "Based on the staffing crunch and the 300-student exposure, the fastest way to
> know if this fits is a 30-minute demo with the actual room sources. Does Thursday
> or next Tuesday work, and should your AV lead be on it?"

**Calibrated questions / closes:**
- "What's the best next step from your side to figure out if this is a fit?" *(let them propose — Voss)*
- "Makes sense to get a technical demo on the calendar — Thursday or Tuesday?"
- "Who else should be in the room when we show this?" *(Decision Process + Champion)*
- "What would stop this from moving forward?" *(surfaces blockers early)*

**Do NOT:** end open-ended. No date + no owner = no next step.

---

## Calibrated Question Bank (by step)

Grouped for quick pull into `sdr-dial-lists` and `epiphan-call-playbook`. Voss
calibrated forms ("How do you…", "What happens when…", "What would need to be
true for…") are noted; they keep the buyer talking and non-defensive.

| Step | Pull-ready questions |
|---|---|
| 1 Business Problem | "What made this a priority now?" · "Where do you lose the most time — capture, switching, or publishing?" · "How do you currently handle that?" |
| 2 Cause Analysis | "What's driving that — A, B, or C?" · "What happens when it breaks — who gets the call?" · "People, gear, or workflow problem?" |
| 3 Negative Impact | "How many [students/cases/congregants] does that touch?" · "How many hours a week firefighting this?" · "How often does it happen?" |
| 4 Future State | "What changes for you if this is solved?" · "What would need to be true for this to be a win?" · "Who else feels the relief?" |
| 5 Close | "What's the best next step from your side?" · "Demo Thursday or Tuesday?" · "Who else should be in the room?" |

Per-vertical calibrated questions and root causes: `reference/epiphan-root-causes.md`.

---

## MEDDIC Integration Points

Capture MEDDIC *during* discovery — don't run a separate interrogation. Each Orlob
step naturally surfaces MEDDIC elements:

| Orlob step | MEDDIC captured |
|---|---|
| 1 Business Problem | **I**dentify Pain (the problem itself) |
| 2 Cause Analysis | **I**dentify Pain (root cause), early **M**etrics signal |
| 3 Negative Impact | **M**etrics (quantified cost of inaction) |
| 4 Future State | **D**ecision **C**riteria (their definition of "solved"), **C**hampion (who wants it) |
| 5 Close | **D**ecision **P**rocess (next steps, who's involved), **E**conomic **B**uyer (who signs), **C**hampion |

For deeper Economic Buyer validation and ATL/BTL classification, hand off to
`meddic-call-prep-auto-skill`. A BTL-only call means you found Pain but not the
Economic Buyer — note it and use Step 5 to ask who owns the budget.

---

## Scoring Rubric (for sdr-call-coaching)

The discovery dimension is scored 0-3. This is the authoritative rubric that
`sdr-call-coaching` grades against:

- **3** — Peeled past the surface to a business problem the buyer owns; asked
  calibrated/open diagnostic questions; surfaced a **root cause** (Step 2) and
  confirmed it back; ideally quantified impact (Step 3). Cause analysis happened.
- **2** — Identified a real pain point but stayed at **symptom level** — never
  traced it to a root cause. Some good questions, but no diagnosis.
- **1** — Asked some questions, but all **surface-level**; no business problem
  surfaced, no cause analysis.
- **0** — Pure **feature dump**. Pitched product with no discovery.

**Coaching tie-in:** when scoring below 3, name the specific Orlob move missed —
e.g. *"cause analysis — never asked what's driving the AV-staffing crunch"* or
*"skipped impact — got the problem but never quantified what it costs them."*

---

## Common Mistakes

- **Feature dump (score 0):** leading with SKUs and specs before diagnosing.
  The buyer's opening solution-request is bait — walk them back to the problem.
- **Staying at symptom level (score 2):** accepting "recordings are inconsistent"
  as the problem and moving to solution. That's a symptom; find the cause.
- **Skipping cause analysis (Step 2):** jumping from problem straight to impact
  or demo. Step 2 is where you earn trust and where the *right* product surfaces.
- **Unquantified impact (Step 3):** "that sounds frustrating" is not a number.
  No number = no urgency = a deal that stalls.
- **Painting the buyer's future state for them (Step 4):** "with Pearl you'll…"
  Let them describe success; you map to it at demo.
- **Open-ended close (Step 5):** "I'll follow up" with no date/owner. Every call
  ends with a committed next step.

</core_content>

## Emit Outcome Sidecar

After running discovery guidance on a call, emit an outcome sidecar so the
analytics pipeline can track skill health. Write to the path below (outside the
repo — required so the PreToolUse observer hook allows the write):

```bash
cat > ~/.claude/skill-analytics/last-outcome-orlob-discovery-framework.json <<'JSON'
{
  "ts": "<ISO8601 timestamp>",
  "skill": "orlob-discovery-framework",
  "version": "1.0.0",
  "variant": "control",
  "status": "success",
  "runtime_ms": <int>,
  "metrics": {
    "discovery_score": <0-3>,
    "root_cause_identified": <true|false>,
    "impact_quantified": <true|false>,
    "next_step_committed": <true|false>,
    "vertical": "<higher-ed|courts|government|healthcare|corporate-av|how|k12>"
  },
  "error": null,
  "session_id": "<session id>"
}
JSON
```

Set `status` to `"partial"` if discovery ran but no root cause was surfaced
(score ≤ 2), and `"error"` with an `error` message if the skill could not run.
