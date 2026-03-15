---
name: jobs-to-be-done
description: "Jobs To Be Done (JTBD) analysis using Christensen and Ulwick's Outcome-Driven Innovation. Use when: jobs to be done, JTBD, customer jobs, outcome driven innovation, ODI, forces of progress, job map, switch interview, hiring firing, outcome statements, why customers switch."
---

<objective>
Analyze markets, products, and prospects through the Jobs To Be Done lens — the innovation framework developed by Clayton Christensen (Competing Against Luck) and operationalized by Tony Ulwick (Outcome-Driven Innovation).

**Core insight:** Customers don't buy products. They hire them to make progress in specific circumstances. Understanding the job — not the customer demographics or product features — is what predicts success.

**Dual-use skill:**
- **Sales/BDR Mode:** Use Forces of Progress and Switch Interviews to understand why prospects switch, structure discovery calls around the job map, and frame value propositions as outcome statements
- **Strategy Mode:** Use the full ODI methodology to score outcome importance vs satisfaction, identify underserved opportunities, and analyze competitive hiring/firing dynamics

When to activate: user asks about jobs to be done, JTBD analysis, customer jobs, outcome-driven innovation, forces of progress, switch interviews, or why customers switch solutions.
</objective>

<quick_start>
# Quick Start

**Trigger:** `analyze [company/product/market] using JTBD`

**Sales Mode** (discovery calls, prospect research):
1. Define the core functional job the prospect is hiring for
2. Map Forces of Progress (what's pushing them to switch?)
3. Generate Switch Interview questions for discovery calls
4. Frame your value prop as outcome statements

**Strategy Mode** (market analysis, product innovation):
1. Write the Job Statement
2. Build the Job Map (8 steps)
3. Generate 15-30 Outcome Statements
4. Score Importance vs Satisfaction (ODI algorithm)
5. Identify top underserved outcomes
6. Analyze Hiring/Firing competitive landscape

**Example:** `Analyze video conferencing for hybrid enterprise teams using JTBD`
</quick_start>

<core_concepts>
# Core Concepts

## What Is a Job?

A job is the progress a person is trying to make in a particular circumstance. Jobs are:
- **Stable over time** — the job of "getting informed about breaking news" hasn't changed in 200 years; only solutions change
- **Solution-agnostic** — no technologies, products, or methods in the job statement
- **Functional + emotional + social** — every job has all three dimensions

## The 3 Types of Jobs

| Type | Definition | Example |
|------|-----------|---------|
| **Functional** | The practical task to accomplish | "Reduce downtime during live broadcasts" |
| **Emotional** | How the person wants to feel | "Feel confident the stream won't fail mid-event" |
| **Social** | How the person wants to be perceived | "Be seen as a technically competent production team" |

## Critical Distinctions

| Concept | Definition | Example | Problem If Confused |
|---------|-----------|---------|-------------------|
| **Job** | Progress in a circumstance | "Monitor remote classroom quality" | — |
| **Need** | Contextual desire | "I need a faster encoder" | Embeds solution bias |
| **User Story** | Dev requirement | "As a user, I want alerts" | Specifies implementation |
| **Feature** | Product capability | "4K encoding at 60fps" | Describes your product, not their progress |

**The test:** If it mentions your product, a technology, or a specific method, it's NOT a job — it's a solution. Rewrite until it's solution-agnostic.
</core_concepts>

<job_statement>
# Job Statement

## Formula

```
[When ___], [I want to ___], [so I can ___]
```

- **When:** The triggering circumstance (not a persona)
- **I want to:** The functional job (solution-agnostic verb + object)
- **So I can:** The higher purpose / desired outcome

## Rules for Good Job Statements

1. No technologies, products, or brand names
2. Stable for 10+ years (if the job existed in 2010, it should read the same)
3. One core job per statement (decompose complex jobs)
4. Use active verbs: capture, deliver, ensure, coordinate, monitor

## Examples

| Domain | Job Statement |
|--------|--------------|
| Video production | When producing a live event with remote participants, I want to ensure consistent video/audio quality across all sources, so I can deliver a professional broadcast without technical disruptions |
| Sales enablement | When preparing for a discovery call with a new prospect, I want to quickly understand their current situation and pain points, so I can ask relevant questions that uncover their real needs |
| IT operations | When a critical system shows degraded performance, I want to identify the root cause and affected scope, so I can restore service before users are significantly impacted |
</job_statement>

<job_map>
# Job Map — 8 Universal Steps

Every job follows these 8 steps. Use them to structure discovery calls and identify outcome opportunities at each stage.

| Step | Definition | Discovery Question |
|------|-----------|-------------------|
| **1. Define** | Determine goals, plan approach, assess resources | "How do you decide what success looks like for [job]?" |
| **2. Locate** | Find the inputs and information needed | "Where do you go to find the [information/materials] you need?" |
| **3. Prepare** | Set up the environment, organize inputs | "What setup or preparation do you do before [executing the job]?" |
| **4. Confirm** | Verify readiness before execution | "How do you confirm everything is ready before you begin?" |
| **5. Execute** | Perform the core job activity | "Walk me through how you actually do [the job] today." |
| **6. Monitor** | Track whether the job is going well | "How do you know if things are going well or going wrong during [the job]?" |
| **7. Modify** | Make adjustments when things change | "When something goes wrong mid-[job], what do you do to correct it?" |
| **8. Conclude** | Finish, clean up, evaluate results | "How do you wrap up? How do you know if [the job] was done well?" |

**Sales application:** Walk prospects through steps 1-8 during discovery. Each step where they describe friction, workarounds, or pain is an opportunity signal.

**Strategy application:** Generate 2-4 outcome statements per step to build a comprehensive outcome set (15-30 total outcomes).
</job_map>

<outcome_statements>
# Outcome Statements

## Formula

```
[Direction] + [metric] + [object of control]
```

**Directions:** Minimize, Reduce, Increase, Maximize, Decrease, Eliminate

## Rules
- Must be measurable (contains a metric: time, likelihood, number, amount)
- Must be controllable (something the user can influence)
- Must be solution-agnostic (no product references)

## Examples

| Job Map Step | Outcome Statement | Imp | Sat |
|-------------|-------------------|-----|-----|
| Locate | Minimize the time it takes to identify the right input sources | 9 | 4 |
| Prepare | Reduce the likelihood of missing a required setup step | 8 | 5 |
| Execute | Minimize the number of manual adjustments needed during execution | 9 | 3 |
| Monitor | Increase the ability to detect problems before they affect output | 10 | 4 |
| Conclude | Minimize the time it takes to verify the job was completed correctly | 7 | 6 |

**Imp** = Importance (1-10), **Sat** = Satisfaction with current solution (1-10)

## Common Mistakes

| Mistake | Bad Example | Fixed |
|---------|------------|-------|
| Too vague | "Make it easier" | "Minimize the number of steps to configure input sources" |
| Solution-embedded | "Reduce time switching between Zoom and OBS" | "Minimize the time switching between source views" |
| Not measurable | "Improve the monitoring experience" | "Increase the likelihood of detecting quality drops within 5 seconds" |
</outcome_statements>

<forces_of_progress>
# Forces of Progress

When a customer switches solutions, four forces are at play. Two drive change, two resist it.

```
  DRIVING CHANGE                    RESISTING CHANGE
  ─────────────                     ────────────────
  ┌─────────────────┐               ┌─────────────────┐
  │  PUSH            │               │  ANXIETY          │
  │  Current pain    │──────────────▶│  Fear of new      │
  │  "This is broken"│               │  "What if it's    │
  │                  │               │   worse?"         │
  └─────────────────┘               └─────────────────┘
  ┌─────────────────┐               ┌─────────────────┐
  │  PULL            │               │  HABIT            │
  │  New attraction  │──────────────▶│  Comfort of old   │
  │  "That looks     │               │  "I know how this │
  │   better"        │               │   works"          │
  └─────────────────┘               └─────────────────┘
```

**Switch happens when:** Push + Pull > Anxiety + Habit

## BDR Quick Reference — Discovery Questions

**Push (uncover current pain):**
1. "What's the most frustrating part of how you handle [job] today?"
2. "When was the last time [current solution] let you down? What happened?"
3. "If you could wave a magic wand, what would you fix first?"

**Pull (new solution attraction):**
1. "What made you start looking at alternatives?"
2. "What would an ideal solution for [job] look like?"
3. "Who else have you looked at? What caught your eye?"

**Anxiety (reduce fear of change):**
1. "What concerns do you have about switching from [current solution]?"
2. "What would need to be true for you to feel confident making a change?"
3. "Have you tried switching before? What happened?"

**Habit (overcome inertia):**
1. "How long have you been using [current solution]?"
2. "What would your team say if you changed how they do [job]?"
3. "Is the team trained on the current system? Who would need retraining?"

**Sales insight:** If Push is weak, the prospect isn't ready — nurture, don't sell. If Anxiety is strong, your demo must directly address their specific fears.
</forces_of_progress>

<hiring_firing>
# Hiring/Firing Analysis

Customers "hire" solutions to get a job done and "fire" them when they fail. Map the competitive landscape through this lens.

## Template

| Solution Currently Hired | Hired For (what job?) | Fired For (why it fails) | Workarounds Used |
|-------------------------|----------------------|------------------------|-----------------|
| Manual spreadsheet process | Tracking inputs, flexible | Breaks at scale, error-prone | Copy-paste, double-checking |
| Legacy on-prem software | Reliability, IT control | Slow updates, poor UX | Shadow IT tools alongside |
| Competitor SaaS | Quick setup, modern UI | Missing enterprise features | Custom integrations bolted on |
| Doing nothing | Zero cost, no change risk | Job doesn't get done well | Accepting poor outcomes |

**Key questions:**
- What is the prospect currently "hiring" for this job?
- Why might they "fire" their current solution? (= your opening)
- What workarounds reveal unmet outcomes? (= your differentiation)
- Is "doing nothing" a competitor? (often the hardest to beat)

**Non-obvious insight:** Your biggest competitor is often NOT another product — it's the combination of workarounds, habits, and "good enough" that the prospect has assembled. Understand the full "hired set" before pitching.
</hiring_firing>

<switch_interview>
# Switch Interview Timeline

Map the prospect's decision journey from first thought to final decision. Based on Bob Moesta's demand-side interviewing methodology.

## The Timeline

```
First       Passive      Active       Deciding     Consuming    Satisfaction
Thought     Looking      Looking
  │            │            │            │            │            │
  ▼            ▼            ▼            ▼            ▼            ▼
"Something  "I notice    "I'm         "Comparing   "Using the   "Was it
 isn't       alternatives  actively     options,     new          worth
 working"    in passing"   searching"   getting      solution"    switching?"
                                        buy-in"
```

## Questions per Phase

**First Thought:** "When did you first realize the current way of doing [job] wasn't working? What triggered that moment?"

**Passive Looking:** "Before you started actively searching, did you notice any alternatives? Where? What caught your attention?"

**Active Looking:** "What made you shift from 'just noticing' to actively searching? What did you search for? Who did you talk to?"

**Deciding:** "How did you narrow your options? What criteria mattered most? Who else was involved in the decision?"

**Consuming:** "What was the onboarding/setup experience like? Did reality match expectations?"

**Satisfaction:** "Looking back, did the switch solve the original problem? What surprised you — good or bad?"

## Sales Application

- **Won deal debrief:** Walk the buyer through all 6 phases — you'll discover what ACTUALLY sold them (it's rarely what you think)
- **Lost deal debrief:** Find where in the timeline you lost — First Thought (no pain) vs Deciding (lost on criteria) vs Consuming (bad onboarding)
- **Discovery calls:** Use First Thought and Active Looking questions to understand where the prospect IS in their timeline right now
</switch_interview>

<opportunity_algorithm>
# Opportunity Algorithm (ODI Scoring)

Tony Ulwick's Outcome-Driven Innovation scoring identifies which outcomes are underserved (high opportunity) vs overserved (commoditized).

## Formula

```
Opportunity Score = Importance + max(Importance - Satisfaction, 0)
```

- **Importance (Imp):** 1-10, how critical is this outcome to getting the job done?
- **Satisfaction (Sat):** 1-10, how well does the current solution address this?
- **Score range:** 1-20

## Interpretation

| Score | Classification | Action |
|-------|---------------|--------|
| **>15** | **Underserved** — High importance, low satisfaction | Primary innovation target. Lead with this in sales pitches |
| **12-15** | **Appropriately served** — Balanced | Table stakes. Must match competitors, no differentiation here |
| **<12** | **Overserved** — Low importance or high satisfaction | Simplify/reduce cost. Customers may pay less for "good enough" |

## Scoring Example

| # | Outcome Statement | Imp | Sat | Score | Class |
|---|-------------------|-----|-----|-------|-------|
| 1 | Minimize time to detect quality drops during live broadcast | 10 | 3 | 17 | Underserved |
| 2 | Reduce likelihood of audio sync issues across sources | 9 | 4 | 14 | Served |
| 3 | Minimize manual adjustments needed during a live event | 9 | 3 | 15 | Underserved |
| 4 | Increase ability to switch sources without visible glitches | 8 | 6 | 10 | Overserved |
| 5 | Minimize time to set up multi-source recording | 7 | 5 | 9 | Overserved |

## JTBD Opportunity Index (0-100 Composite)

For consistency with Blue Ocean and Business Model Canvas scoring:

```python
def jtbd_opportunity_index(outcomes):
    """Normalize ODI scores to 0-100 composite index."""
    scores = [imp + max(imp - sat, 0) for imp, sat in outcomes]
    max_possible = 20  # imp=10, sat=0
    avg_normalized = sum(s / max_possible for s in scores) / len(scores)

    # Weight by number of underserved outcomes
    underserved_ratio = sum(1 for s in scores if s > 15) / len(scores)

    index = (avg_normalized * 70) + (underserved_ratio * 30)
    return round(index * 100) / 100

# Interpretation:
# 75-100: Massive opportunity — many critical underserved outcomes
# 50-74:  Solid opportunity — clear gaps to exploit
# 25-49:  Moderate — some gaps, market partially served
# 0-24:   Low opportunity — market well-served, compete on cost/convenience
```
</opportunity_algorithm>

<consumption_chain>
# Consumption Chain

Analyze friction across the full lifecycle of how customers interact with solutions for this job.

| Phase | Key Question |
|-------|-------------|
| **Awareness** | How do customers first learn a solution exists for this job? |
| **Acquisition** | How do they evaluate and purchase? What's the buying process friction? |
| **Setup** | How long from purchase to first use? What blocks quick time-to-value? |
| **Daily Use** | What does the core usage pattern look like? Where are the pain points? |
| **Supplementing** | What other tools/workarounds do they combine with this solution? |
| **Maintenance** | What upkeep, updates, or troubleshooting does the solution require? |
| **Disposal** | How do they stop using it? What's the switching cost / data lock-in? |

Each friction point in the consumption chain is a potential innovation opportunity or competitive advantage.
</consumption_chain>

<example_session>
# Example: Video Conferencing for Hybrid Enterprise Teams

## Job Statement
When coordinating a meeting with both in-room and remote participants, I want to ensure everyone can see, hear, and contribute equally, so I can run productive meetings regardless of where people are located.

## Job Map (Key Steps)

| Step | Current Reality | Friction |
|------|----------------|---------|
| Prepare | IT pre-checks room AV 30 min before | Time-consuming, still fails |
| Confirm | "Can everyone hear me?" ritual | Wastes first 5 minutes every meeting |
| Execute | Remote participants talk over each other | No spatial audio, poor camera framing |
| Monitor | No way to know if remote audio is degrading | Find out when someone says "you're breaking up" |
| Modify | Manual camera switching, volume adjusting | Presenter distracted from content |

## Top 5 Outcome Statements (Scored)

| # | Outcome | Imp | Sat | Score |
|---|---------|-----|-----|-------|
| 1 | Minimize time to detect remote participant audio/video issues | 10 | 3 | **17** |
| 2 | Reduce likelihood that in-room audio is unclear for remote participants | 9 | 4 | **14** |
| 3 | Minimize manual camera adjustments needed during meetings | 9 | 2 | **16** |
| 4 | Increase ability for remote participants to contribute equally | 10 | 4 | **16** |
| 5 | Minimize setup time required before hybrid meetings | 8 | 5 | **11** |

**JTBD Opportunity Index: 72/100** — Solid opportunity, 3 of 5 outcomes underserved.

## Forces of Progress (Prospect Switching from Legacy Room System)

| Force | Evidence |
|-------|---------|
| **Push** | "We spend $50K/year on room systems that remote workers say are terrible. CEO noticed in board meeting." |
| **Pull** | "Saw a demo where AI auto-framed speakers and mixed audio. That's what we need." |
| **Anxiety** | "We have 40 conference rooms. Ripping out existing AV is a 6-month project." |
| **Habit** | "Our AV team knows the current system inside out. They're resistant to change." |

**Verdict:** Push + Pull strong. Anxiety manageable with phased rollout. Habit requires AV team champion.

## Hiring/Firing

| Solution | Hired For | Fired For |
|----------|----------|-----------|
| Legacy room AV | Reliability, IT familiarity | Poor remote experience |
| Zoom Rooms | Easy setup, familiar UI | Limited AV quality control |
| OBS + custom rig | Maximum flexibility | Too complex, fragile |
| Nothing (laptop webcam) | Zero cost | Terrible room experience |
</example_session>

<success_criteria>
# Success Criteria

- [ ] Job Statement follows `[When], [I want to], [so I can]` — no products, technologies, or methods mentioned
- [ ] Job Map covers all 8 steps with discovery questions
- [ ] Outcome Statements use `Direction + Metric + Object` formula and are measurable
- [ ] Forces of Progress mapped with specific evidence/quotes (not generic)
- [ ] ODI Opportunity Scores calculated: `Importance + max(Importance - Satisfaction, 0)`
- [ ] Top 3 underserved outcomes identified (score > 15)
- [ ] Hiring/Firing table maps competitive landscape through job lens
- [ ] JTBD Opportunity Index calculated (0-100 composite score)
</success_criteria>
