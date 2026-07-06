---
name: challenger-sale
description: "The Challenger Sale methodology — Teach-Tailor-Take Control framework for B2B sales. Use when: challenger sale, commercial teaching, constructive tension, reframe, teach tailor take control, insight selling, commercial insight, challenger rep."
---

<objective>
Challenger selling: win deals by teaching prospects something new about their business, tailoring the message to their stakeholders, and taking control of the conversation. Based on Dixon & Adamson's research of 6,000+ sales reps.

**Dual-use skill:**
- **BDR/Sales Mode:** Build commercial insights for outreach, tailor messages to stakeholders, handle objections with constructive tension
- **Strategy Mode:** Develop teaching pitches for entire verticals, build reframe narratives, design commercial teaching choreography

When to activate: user asks about challenger sale, commercial teaching, insight selling, teach-tailor-take control, constructive tension, or reframing customer thinking.

**Not to be confused with `sales-methodology-implementer-skill`:** that skill is the multi-framework playbook selector (MEDDIC, Challenger, SPIN, etc. — "which methodology fits this deal"). This skill is the single-methodology deep-dive: it builds the actual Teach/Tailor/Take-Control content once Challenger has been chosen.
</objective>

<quick_start>
# Quick Start

**Three modes:**

- `Teach`: Build a commercial insight for [prospect/vertical]
- `Tailor`: Adapt insight for [stakeholder role] at [company]
- `Take Control`: Handle [objection] with constructive tension

**Example:** `Build a Challenger teaching pitch for higher-ed AV directors`
</quick_start>

<success_criteria>
# Success Criteria

- [ ] Commercial insight passes the "So What?" test — prospect learns something new about their OWN business
- [ ] Message is tailored to specific stakeholder type (economic buyer vs champion vs user vs blocker)
- [ ] Objection handling uses reframe (not retreat or discount)
- [ ] Teaching pitch follows the 6-step choreography (Warmer > Reframe > Rational Drowning > Emotional Impact > New Way > Your Solution)
- [ ] Insight leads to YOUR unique capabilities (not generic advice anyone could give)
- [ ] Every product/spec/competitive claim (Step 6, LMS/integration lists, competitive reframes) is confirmed via `search_product_catalog` / `search_product_knowledge` — never asserted from memory
- [ ] Every generated email/pitch passes `check_my_copy` before it's finalized or staged as a Gmail draft
</success_criteria>

<core_concepts>
# Core Concepts

## The 5 Rep Profiles (CEB Research — 6,000+ Reps)

| Profile | % of Star Performers | Approach |
|---------|---------------------|----------|
| **Challenger** | 39% | Teaches, tailors, takes control |
| Hard Worker | 17% | Always going above and beyond |
| Relationship Builder | 7% | Builds strong personal advocacy |
| Lone Wolf | 25% | Follows own instincts, breaks rules |
| Reactive Problem Solver | 12% | Reliably resolves service issues |

**Key insight:** In complex B2B sales, Relationship Builders are the WORST performers (only 7% of stars). Challengers dominate because customers value insights over relationships.

## The 3 Challenger Skills

1. **Teach** for differentiation — lead with insights, not products
2. **Tailor** for resonance — adapt the message to the stakeholder
3. **Take Control** of the sale — assert on value, not price
</core_concepts>

<teach_framework>
# Commercial Teaching Pitch — 6-Step Choreography

## Step 1: The Warmer
Demonstrate you understand their world. NO product mentions.
- "Universities running 50+ lecture halls face a specific challenge with hybrid delivery..."
- "Courts managing remote testimony are discovering that consumer video tools create compliance gaps..."

## Step 2: The Reframe
Introduce an insight that challenges their current assumption.
- Pattern: "Most [personas] believe [common assumption]. But [data/evidence] shows [surprising reality]."
- "Most teams think their biggest cost is hardware. But what we hear from AV teams managing large deployments is that the majority of total cost is actually staff time — troubleshooting, re-recording, and fielding complaints."

## Step 3: Rational Drowning
Data and evidence that makes the problem undeniable. Stack 2-3 proof points.
- Industry stats, peer benchmarks, cost calculations
- "That's $X per year in staff time" / "Y% of events experience quality issues"

## Step 4: Emotional Impact
Connect to what this means for THEM personally (not the organization).
- "Your team is the one getting the call at 8 PM when the stream drops during the board meeting."
- "When lecture capture fails mid-semester, it's your department that takes the heat."

## Step 5: A New Way
Show how to solve the problem. Still NOT your product — describe the approach/architecture.
- "The solution is hardware-based encoding that eliminates the software layer entirely..."
- "What leading institutions are doing is separating capture from distribution..."

## Step 6: Your Solution
NOW — and only now — connect your capabilities to the New Way.

**Spec Verification Gate (required before this step):** Before naming a product, capability,
spec, integration, or competitive comparison, call `search_product_catalog` (pricing/specs/features)
and/or `search_product_knowledge` (deep technical RAG) to confirm it. **Never state Pearl/Epiphan
specs, LMS/integration lists, or competitor comparisons from memory** — they go stale and create
liability if wrong. If verification comes back empty or the tool is unavailable, do not assert the
claim: mark it `[unverified — needs spec check]` in the output and flag it to Tim rather than guessing.
- "This is exactly what Pearl was designed for — appliance-based encoding with..." *(only after the capability above is confirmed via `search_product_catalog`/`search_product_knowledge`)*

## Template

```
WARMER:    "[Persona] dealing with [situation] face [specific challenge]..."
REFRAME:   "Most believe [assumption]. But [evidence] shows [surprise]."
DROWNING:  "[Stat 1]. [Stat 2]. That's [quantified impact]."
EMOTIONAL: "Your team is the one that [personal consequence]."
NEW WAY:   "What leading [peers] are doing is [approach]..."
SOLUTION:  "This is exactly what [product] was built for — [capability]."
```
</teach_framework>

<tailor_framework>
# Stakeholder Tailoring Matrix

| Stakeholder | Cares About | Language | Insight Angle | CTA Style |
|-------------|------------|----------|---------------|-----------|
| **Economic Buyer** (CFO/VP) | ROI, risk reduction, strategic alignment | Business outcomes, $ | "Cost of inaction is $X/year" | Executive briefing |
| **Champion** (Director/Mgr) | Solving their pain, career impact | Operational metrics | "Here's what your peers are doing" | Working session |
| **End User** (Technician) | Will it work? Integration? Workflow? | Technical specs | "Here's what you're missing in your stack" | Technical demo |
| **Blocker** (IT/Procurement) | Risk, compliance, vendor lock-in | Standards, SLAs, security | "Here's how to de-risk this" | Reference call |

## Tailoring Rules

1. Same insight, different framing for each stakeholder
2. **Economic buyer:** Lead with business impact, end with ROI
3. **Champion:** Lead with peer comparison, end with their career win
4. **User:** Lead with technical proof, end with workflow improvement
5. **Blocker:** Lead with risk mitigation, end with standards compliance
</tailor_framework>

<take_control>
# Constructive Tension Techniques

## The Assertive Redirect (when asked for discount)
> "I understand budget is a concern. Before we talk pricing, let me make sure we agree on the value. You mentioned [pain point] costs your team [X]. If we solve that, we're talking about [Y] in savings. Does that math work for you?"

## The Pocket Veto Counter (when deal stalls at consensus)
> "It sounds like there might be different priorities across your team. In our experience, the most effective approach is to align on the problem first. Would it help if I put together a brief for [economic buyer] that quantifies the impact?"

## The Respectful Challenge (when prospect is wrong)
> "I hear that. And I've seen other teams take that approach. What I've also seen is [counter-evidence]. Would you be open to looking at it from a different angle?"

## Price Anchoring Sequence

1. Quantify the problem FIRST (rational drowning)
2. Establish the cost of doing nothing
3. THEN present price as a fraction of the problem cost
4. Never defend price — redirect to value gap
</take_control>

<email_templates>
# Email Templates — Challenger Style

**Brand Gate (required before any email is finalized or sent):** Run `check_my_copy` (and
`get_writing_style` for voice reference) on every generated email/pitch before it's used. Fix
anything flagged — off-voice copy does not go out. This runs immediately before delivery, i.e.
after the Reframe/insight content is drafted and after specs are verified (Spec Verification Gate,
`<teach_framework>` Step 6), but before the message is staged.

**Delivery contract:** Output is draft-first, per CLAUDE.md's Gmail workflow (call → open draft →
review/edit → send). Stage every generated email as a Gmail draft via `create_draft` — never send
directly, and never treat inline chat text as the final deliverable.

## Cold Email (under 100 words)

```
Subject: [Specific challenge] at [Company]

[Name],

Most [role/vertical] teams assume [common assumption].

But [surprising data point] — meaning [quantified impact for their org].

[One sentence about the new approach leading organizations are taking].

Worth a 15-minute conversation to see if this applies to [Company]?

[Signature]
```

## Follow-up — The Reframe Nudge

```
Subject: Re: [Original subject]

[Name],

Wanted to share one more data point — [peer organization] was in a similar
position and found that [specific outcome after changing approach].

Would it make sense to compare notes?
```
</email_templates>

<integration_points>
# Integration Points

## Strategy Skill Cluster — First Principles Pipeline

```
JTBD (What job?) → Blue Ocean (Where's the space?) → BMC (How to deliver?)
                                    ↓
              Challenger (What insight reframes their thinking?)
                                    ↓
              NSTTD (How to communicate with tactical empathy)
                                    ↓
                        OUTPUT: Email / Call / Deck
```

**JTBD:** The Reframe IS the underserved outcome the prospect doesn't know they have. Use JTBD outcome scoring to identify the insight.

**Blue Ocean:** Commercial insights often point to ERRC factors (Create/Raise) — what the industry doesn't offer yet.

**BMC:** Tailoring maps directly to Customer Segments and Value Propositions blocks.

**NSTTD:** "Take Control" is amplified by tactical empathy, calibrated questions, and the FM DJ voice. Use accusation audits before delivering tough reframes.

## Email Writing Principles (First Principles Lens)

1. **JTBD:** Lead with the prospect's job, not your product
2. **Challenger:** Deliver a commercial insight that reframes their assumption
3. **NSTTD:** Use tactical empathy to lower defenses
4. **EE lens:** Be precise, concise, technically grounded — no fluff
5. Max 100 words for cold outreach
</integration_points>

<example_session>
## Example: Higher Ed Lecture Capture — Commercial Teaching Pitch

**User:** Build a Challenger teaching pitch for a Higher Ed AV Director evaluating lecture capture for 50+ classrooms

### Step 1: The Warmer
You're managing AV across dozens of classrooms — maybe multiple buildings or campuses — with faculty who just want to walk in and teach. Meanwhile, students expect every lecture recorded reliably, and your team is the one on the hook when something doesn't capture. The pressure to deliver consistent hybrid delivery at scale is real, and it only grows each semester.

### Step 2: The Reframe
Most institutions think their biggest lecture capture cost is hardware. But what we consistently hear from AV teams managing 50+ rooms is that the majority of total cost is staff time — troubleshooting software encoders, rebooting crashed PCs, and re-recording failed sessions. The hardware line item is the visible cost; the invisible cost is your team's hours.

### Step 3: Rational Drowning
Walk them through the math using THEIR numbers (ask during discovery or estimate conservatively):
- "How often do your software encoders crash or fail to record?" (typical range we hear: 5-15% of sessions)
- "How long does it take your team to troubleshoot each incident?" (typical: 30-60 min)
- At 50 rooms × 4 sessions/day × 180 teaching days: ~36,000 sessions/year
- Even at a conservative 5% failure rate = ~1,800 incidents requiring some response
- Not all are hands-on, but ask: "How many of those does your team physically respond to?"
- Multiply their answer × their avg troubleshooting time × their loaded labor rate
- **Key:** Let THEM fill in the numbers. The math is more powerful when it's their data, not yours. Never cite research you can't produce.

### Step 4: Emotional Impact
Your AV team is the one getting the call at 8 AM Monday when Professor Chen's Friday lecture didn't record. The faculty member isn't calling the software vendor — they're calling your team. And when a semester's worth of recordings is spotty, it's your department's credibility on the line with the Provost, not the vendor's.

### Step 5: A New Way
What leading R1 universities are doing is eliminating the software layer entirely — moving to appliance-based capture that records regardless of what happens to the campus network or the classroom PC. No software agent on the podium machine means no OS updates breaking the encoder, no antivirus quarantining the capture process, no PC reboots mid-lecture.

### Step 6: Your Solution
*(Spec Verification Gate: call `search_product_catalog("Pearl-2 local recording network offline LMS buffering")` — or `search_product_knowledge` for deeper technical detail — before writing this step. Confirm the local-record-on-network-drop behavior and LMS buffering claim against the returned result; do not proceed on the paragraph below until it's confirmed or corrected.)*

This is exactly what Pearl-2 was built for — a dedicated hardware encoder that captures, streams, and records simultaneously with zero PC dependency. When the network drops, it keeps recording locally. When the LMS goes down, it buffers and uploads later. Faculty walk in, press one button (or it auto-starts on schedule), and the lecture is captured. Your team manages 50+ rooms from a single web dashboard instead of remoting into 50 PCs.

### Stakeholder Tailoring

| Stakeholder | Reframe Angle | Key Metric | CTA |
|-------------|--------------|------------|-----|
| **VP Academic Affairs** | "Cost of failed recordings = student complaints + accreditation risk" | Staff hours lost, failure rate | Executive briefing |
| **AV Director** | "Your team is troubleshooting problems that shouldn't exist" | Staff hours recovered, single-pane management | Working session |
| **IT Security** | "No software agent = no attack surface, no OS patches to manage" | Zero endpoint footprint, HTTPS only | Reference call |
| **Procurement** | "Compare 5-year TCO: hardware appliance vs software + PC refresh" | TCO comparison worksheet | Formal quote |

### Competitive Reframe
*(Spec Verification Gate: confirm the Panopto/Kaltura/YuJa/Canvas integration list via `search_product_catalog` before using this reframe — competitive integration claims are exactly what goes stale.)*

When prospect says "We're also talking to Panopto/Echo360/Kaltura":
> "Those are strong platforms for content management. The question is what sits in the classroom doing the capture. Most CMS platforms rely on a software agent running on a PC — that's the layer where failures happen. Pearl integrates with Panopto, Kaltura, YuJa, and Canvas natively. The difference is what happens when the PC freezes mid-lecture."

### LMS Integration Note
*(Spec Verification Gate: this is the highest-stakes claim in the pitch — Higher Ed buyers ask it first and will check it. Call `search_product_catalog` / `search_product_knowledge` for the current integration list before stating it; do not repeat the list below from memory once specs may have changed.)*

First question every Higher Ed buyer asks: "Does it work with our LMS?"
Pearl-2 integrates with Canvas, Blackboard, Moodle, Kaltura, Panopto, YuJa, and Echo360 via LTI/REST/RTMP. Lead with this in the Warmer if you know their stack.

### Cold Email (Challenger Style)

```
Subject: Lecture capture at [University]

[Name],

Most AV teams managing 50+ classrooms tell us the same thing — their
biggest lecture capture cost isn't hardware. It's staff time
troubleshooting software crashes and re-recording failed sessions.

The pattern we see at R1 institutions: they're removing the software
layer entirely and moving to appliance-based capture.

Worth 15 minutes to compare notes on what's working?

[Signature]
```

*(Brand Gate: run `check_my_copy` on the draft above before staging it. Then stage it as a Gmail
draft via `create_draft` — do not send directly, and do not treat the block above as the final
deliverable until both steps have run.)*
</example_session>

<anti_patterns>
# Anti-Patterns

- **Leading with product features** — Challengers teach about the PROBLEM, not the solution
- **Generic insights** — "Digital transformation is important" is NOT a commercial insight
- **Retreating on price** — Challengers redirect to value, never discount without removing scope
- **Same pitch for every stakeholder** — Tailoring is not optional
- **Being aggressive** — Constructive tension is NOT confrontation. It's respectful disagreement backed by evidence
- **Skipping the Warmer** — You earn the right to challenge by first proving you understand their world
- **Stating specs from memory** — Any Pearl/Epiphan spec, integration list, or competitive claim not confirmed via `search_product_catalog`/`search_product_knowledge` this run is a guess, not an insight
- **Skipping the Brand Gate** — Never stage or send an email that hasn't passed `check_my_copy`
</anti_patterns>

<dependencies>
## MCP tools
- `search_product_catalog` — pricing/specs/features verification (fast, catalog + RAG fallback) — required before any Step 6 / competitive / LMS claim
- `search_product_knowledge` — deep technical RAG for claims `search_product_catalog` can't resolve
- `check_my_copy` / `get_writing_style` — brand-voice gate, required before any email/pitch is finalized
- `create_draft` (Gmail) — stages the finished, gated email as a draft (draft-first, never direct send)

## Sibling skills referenced
- `sales-methodology-implementer-skill` — picks the methodology; this skill executes Challenger once chosen
- `epiphan-ai-mcp-guide-skill` — reference for product-tool usage patterns
</dependencies>

## Guardrails
- Never assert a product spec, integration list, or competitive comparison from memory — the Spec
  Verification Gate (`search_product_catalog` / `search_product_knowledge`) runs before Step 6, the
  Competitive Reframe, and the LMS Integration Note, every time.
- Never finalize or stage an email without the Brand Gate (`check_my_copy`) passing first.
- Emails are draft-first: stage via `create_draft`, never send directly.
- **Failure ladder** (see `skill-audit/specs/self-healing-template.md`): if a spec/brand check can't
  be evaluated (tool unavailable, no match), retry once; if it still can't be resolved, degrade —
  mark the claim/copy `[unverified]` and produce a partial result rather than guessing; do not
  silently proceed as if the gate passed. If no usable pitch/email can be produced at all, halt and
  report "error" rather than emitting unverified content.

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-challenger-sale.json`:
```json
{"ts":"[UTC ISO8601]","skill":"challenger-sale","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"insights_generated":[n],"reframes_created":[n],"stakeholders_tailored":[n],
            "specs_verified":[n],"specs_unverified":[n],"copy_gate_passed":[true|false]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced — including any spec left
`[unverified]` or copy that failed `check_my_copy` and had to be regenerated. Use "error" only if no
output was generated. Also append one line to `~/.claude/skill-runs/challenger-sale.jsonl`:
`{"ts":"<UTC ISO8601>","skill":"challenger-sale","version":"1.0.0","status":"success|partial|error","error":"<string|null>","records_in":0,"records_out":0}`
per the run-log convention in `skill-audit/specs/self-healing-template.md`.
