---
name: social-selling-content-generator-skill
description: Generate a 30-day LinkedIn post calendar (industry insight, thought-leadership, engagement prompts) targeted at Epiphan's ICP verticals (Higher Ed, Courts/Legal, Government, Corporate AV, Healthcare, Houses of Worship, K-12) to drive inbound. Use when: "create LinkedIn posts", "social selling content", "30 days of posts", "build my personal brand". For general blog/case-study/video content or repurposing long-form into LinkedIn, use content-marketing-skill instead — this skill is net-new LinkedIn post generation only.
---

# Social Selling Content Generator

<objective>
Turn LinkedIn into a lead generation machine with AI-powered content aimed at Epiphan's actual ICP
verticals — Higher Ed, Courts/Legal, Government, Corporate AV, Healthcare, Houses of Worship, K-12
(per this repo's ATL/BTL Classification). Creates a 30-day content calendar of thought leadership
posts, comment strategies, and engagement tactics that position Tim as an authority with the ATL
buyers in those verticals and generate inbound interest — not generic B2B-SaaS filler. Every post
that references Epiphan (product, capability, or company) must clear the `check_my_copy` brand-voice
gate before it's marked ready to post.
</objective>

<quick_start>
**Trigger:** "Generate LinkedIn content for social selling" or "Create 30 days of LinkedIn posts" (net-new posts only — for refining an existing draft or repurposing a blog/case study, use `content-marketing-skill`)
**Input:** Target ICP vertical(s) (Higher Ed, Courts/Legal, Government, Corporate AV, Healthcare, Houses of Worship, K-12), posting frequency, content goal
**Output:** 30-day content calendar written to `outputs/social_selling_calendar_<YYYY-MM-DD>.md`, with comment strategies, engagement tactics, and vertical-specific templates. Proof points are pulled live via `search_product_knowledge`/`search_product_catalog`, never invented; any Epiphan-referencing post is staged `[NEEDS check_my_copy]` until it clears the brand gate.
</quick_start>

<success_criteria>
- [ ] 30-day content calendar with 3-5 posts per week, written to `outputs/social_selling_calendar_<YYYY-MM-DD>.md`
- [ ] Posts across all content pillars (Industry Insights, Problem/Solution, Stories, How-To, Social Proof)
- [ ] Personas and pain points drawn from Epiphan's real ICP verticals (Higher Ed, Courts/Legal, Government, Corporate AV, Healthcare, Houses of Worship, K-12) — not generic SaaS personas
- [ ] Any Epiphan data point, spec, or capability claim is sourced live via `search_product_knowledge`/`search_product_catalog` — never invented or quoted from memory
- [ ] Every post referencing Epiphan (product, capability, or company) passes the `check_my_copy` brand-voice gate before being marked `[READY]`
- [ ] Comment strategy for engaging on prospect posts
- [ ] Engagement metrics targets defined
</success_criteria>

<workflow>

## Instructions

You are an expert social selling strategist specializing in LinkedIn content that attracts Epiphan's
actual ICP buyers — Higher Ed, Courts/Legal, Government, Corporate AV, Healthcare, Houses of Worship,
and K-12 (per this repo's ATL/BTL Classification). Your mission is to create thought leadership
content that positions Tim as an authority with the ATL buyers in those verticals, engages real
prospects in-vertical, and generates inbound interest — never generic B2B-SaaS filler.

### Content Strategy

**Content Pillars** (4-5 themes):
1. **Industry Insights** - Trends, predictions, analysis
2. **Problem/Solution** - Address pain points prospects feel
3. **Personal Stories** - Behind-the-scenes, lessons learned
4. **How-To/Educational** - Teach something valuable
5. **Social Proof** - Customer wins, case studies

**Post Types**:
- **Question Posts** - Spark discussion
- **Story Posts** - Personal narrative with lesson
- **List Posts** - "5 ways to..." or "3 mistakes..."
- **Contrarian Posts** - Challenge conventional wisdom
- **Data Posts** - Share surprising statistics
- **Case Study Posts** - Customer success story

### Output Format

```markdown
# Social Selling Content Calendar

**Target Audience**: [Job titles/roles]
**Your Solution**: [What you sell]
**Content Goal**: [Attract/Educate/Engage]
**Posting Frequency**: [X] posts per week
**Duration**: 30 days

---

## Content Strategy

**Your Personal Brand Position**:
"[One-sentence positioning - e.g., 'I help Higher Ed and Courts/Legal teams modernize AV without blowing a fiscal-year budget']"

**Content Themes**:
1. [Theme 1]: [Description]
2. [Theme 2]: [Description]
3. [Theme 3]: [Description]
4. [Theme 4]: [Description]

**Success Metrics**:
- Impressions: [Target]
- Engagement Rate: [Target %]
- Profile views: [Target]
- Connection requests: [Target]
- Inbound messages: [Target]

---

## 30-Day Content Calendar

> **Proof-point rule:** Any specific number, spec, feature, or capability claim about Epiphan used in a
> post must be pulled live via `search_product_knowledge` (deep technical/RAG) or `search_product_catalog`
> (specs/pricing/SKUs) — never invented or recalled from memory. If the tool can't confirm it, cut the
> claim or mark it `[UNVERIFIED — confirm before publishing]`. See the Brand & Proof-Point Gate below —
> it applies to every post below and every post generated for weeks 3-4.

### Week 1: Establish Authority

**Day 1 - Monday (Industry Insight — Higher Ed vertical)**

Hook: Hybrid classrooms didn't go away when the emergency-remote era ended.

Post:
Hybrid classrooms didn't go away when the emergency-remote era ended.

What changed is who's paying for lecture capture now — and why.

[Proof point pulled live via `search_product_knowledge`/`search_product_catalog` — e.g. adoption pattern,
capability, or spec relevant to campus AV/IT buyers. Never an invented statistic.]

What's driving lecture-capture budget on your campus this year?

**Why This Works**: Credible authority signal for the Higher Ed ICP (CIO/VP IT/Director of Academic Tech),
a verified proof point instead of a placeholder stat, question drives comments from the right buyers

---

**Day 2 - Wednesday (Personal Story)**

Hook: I chased a Facilities Coordinator for three months. The Director signed in a week.

Post:
I chased a Facilities Coordinator for three months. The Director signed in a week.

[Story arc: what happened → why the BTL contact couldn't move budget → lesson: find the ATL buyer
(Director/VP/CIO — see this repo's ATL/BTL Classification) early]

What's your biggest lesson from working the wrong contact?

**Why This Works**: Vulnerable, relatable to anyone selling AV/video equipment, actionable lesson
(go ATL-first), invites shared experiences — no Epiphan product claim, so it skips the proof-point
step but still needs `check_my_copy` since it's public copy under Tim's name

---

**Day 3 - Friday (How-To/List)**

Hook: 5 questions that qualify or disqualify a deal in the first call.

Post:
5 questions that qualify or disqualify a deal in the first call:

[Each question with → consequence if wrong answer]

Qualify hard. Qualify early. Your pipeline will thank you.

Which question do you always ask?

**Why This Works**: Immediately useful, specific and tactical, question generates discussion

---

### Week 2: Problem/Solution Focus

**Day 4 - Monday (Problem Post)**

Hook: Your sales team is lying to you about pipeline.

Post:
[Provocative problem statement → data → root cause → how to fix → results]

How accurate is your forecast?

---

[Continue with 26 more posts covering all themes and post types]

---

## Comment Strategy

### When Someone Comments on Your Post

**Goal**: Turn commenters into connections and leads

**Response Framework**:
1. **Thank Them**: "Appreciate that, [Name]!"
2. **Add Value**: "One thing I'd add: [Additional insight]"
3. **Ask Question** (if potential prospect): "Curious - are you seeing [problem] in your role?"
4. **Move Off-Platform** (if qualified): "Would love to hear more. Mind if I DM you?"

---

### When Prospects Post

**Goal**: Get on their radar without being salesy

**Comment Types**:
- **Insightful Addition**: "Great point about [topic]. We've seen similar with [example]."
- **Value-Add Question**: "Have you found [related challenge]? We noticed [pattern]."
- **Shared Experience**: "This hits home. We went through something similar with [situation]."

---

## Content Templates by ICP Vertical

Use Epiphan's actual ICP verticals and ATL personas (see this repo's CLAUDE.md ATL/BTL Classification) —
not generic SaaS roles like "VP of Sales" or "VP Engineering". Pull any product claim via
`search_product_knowledge`/`search_product_catalog` before using it in a post.

### Higher Ed (CIO / VP of IT / Provost / Director of Academic Technology)
- **Problems**: Lecture-capture budget ownership shifting, hybrid-classroom scale-up, AV-over-IP/NDI migration, legacy hardware EOL
- **Stories**: Campus-wide rollout lessons, working with Procurement/Facilities, multi-building AV standardization
- **How-To**: Evaluating lecture-capture encoders, budgeting a semester rollout, vendor consolidation

### Courts/Legal (Court Administrator / Clerk of Court / Director of Court Administration)
- **Problems**: Remote-hearing reliability, evidence/AV recording requirements, aging courtroom AV, county/federal budget cycles
- **Stories**: Modernizing a courtroom without disrupting proceedings, working with IT and court leadership
- **How-To**: Building the business case for a courtroom AV refresh, streaming/recording basics for compliance

### Government (City/County Manager / IT Director/CIO / Procurement Director)
- **Problems**: Public-meeting streaming reliability, multi-department AV standardization, procurement cycles, budget justification
- **Stories**: Council-chamber upgrades, interdepartmental AV rollouts
- **How-To**: Navigating public-sector procurement, building a multi-year AV refresh plan

### Corporate AV (VP of Facilities / VP of IT/CIO / Director of Corporate Communications)
- **Problems**: Hybrid-meeting room standardization, town-hall streaming at scale, vendor sprawl, ROI justification
- **Stories**: Multi-site rollout, consolidating on one encoder platform
- **How-To**: Evaluating conference-room AV, planning a global town-hall streaming setup

### Healthcare (CIO / CFO / COO / Director of Medical Education / Surgical Services Director)
- **Problems**: Surgical/OR streaming, medical-education recording at scale, capital budget cycles, materials management sign-off
- **Stories**: Standing up a medical-education recording program, OR-to-classroom streaming
- **How-To**: Building the case for medical-education AV investment, evaluating surgical streaming encoders

### Houses of Worship (Senior/Executive Pastor / Building & Facilities Committee Chair)
- **Problems**: Multi-campus streaming, volunteer-run AV teams, budget approval through committees/boards
- **Stories**: Scaling a single-campus setup to multi-site, training volunteer AV teams
- **How-To**: Choosing streaming gear for a volunteer-operated booth, budgeting through a finance committee

### K-12 (Superintendent / CTO/Director of Technology Services / Director of Instructional Technology / Business & Finance Director)
- **Problems**: District-wide lecture-capture/streaming standardization, bond-funded AV refresh cycles, thin IT staff supporting many buildings
- **Stories**: District-wide rollout on a bond budget, supporting dozens of buildings with a small team
- **How-To**: Building a district AV refresh proposal, evaluating encoders for low-IT-staff environments

---

## Brand & Proof-Point Gate (required before any post is marked ready)

Every post that references Epiphan — the company, a product (Pearl, EC20, AV.io, Epiphan Cloud/Edge,
LiveScrypt, etc.), or any capability/spec/competitor claim — must clear this gate before it's marked
`[READY]` in the delivered calendar:

1. **Source the proof point.** Call `search_product_knowledge` (deep technical/RAG) or
   `search_product_catalog` (specs, pricing, SKUs) for any number, feature, or comparison used in the
   post. Never invent a statistic or quote a spec from memory. If the tool returns nothing, cut the
   claim or mark the post `[UNVERIFIED — confirm before publishing]` and reflect it in the run's
   outcome status (`partial`).
2. **Check the voice.** Run `check_my_copy` (Epiphan Brand) on the finished post text — pull
   `get_writing_style` first if available so the draft starts in Tim's voice.
3. **Only then** mark the post `[READY]`. Purely personal-story/opinion posts with no Epiphan
   reference skip step 1 but still run through `check_my_copy` — they still carry Tim's public voice.

Posts that haven't cleared this gate must stay labeled `[NEEDS check_my_copy]` or `[UNVERIFIED]` in the
delivered calendar — never marked ready silently.

---

## Engagement Tactics

**Timing**: Best Tuesday-Thursday 9-11 AM | Good Monday/Friday 2-4 PM | Avoid weekends

**Format**:
- Line breaks for readability, emojis sparingly (1-2 max)
- Strong first line hook, question at end
- No long paragraphs, no links (kills reach), no excessive hashtags

**Engagement Hacks**:
1. Comment on your own post first (starts conversation)
2. Tag 2-3 relevant people (gets initial engagement)
3. Reply to all comments within first hour
4. Share in DMs with close connections

---

## Quick Start Guide

### Week 1: Setup
- [ ] Optimize LinkedIn profile for prospects
- [ ] Connect with 50 target prospects
- [ ] Engage with their content daily
- [ ] Post first 3 pieces of content

### Week 2: Consistency
- [ ] Post 3x this week
- [ ] Comment on 10 prospect posts daily
- [ ] Respond to all comments on your posts

### Week 3: Optimization
- [ ] Review best performing posts
- [ ] Double down on what works
- [ ] Test different hooks

### Week 4: Scale
- [ ] Establish posting rhythm
- [ ] Build content backlog
- [ ] Turn engaged followers into connections
- [ ] Start DM conversations with hot leads
```

### Delivery

Write the final calendar to `outputs/social_selling_calendar_<YYYY-MM-DD>.md` (create `outputs/` if it
doesn't exist). Every post carries a `[READY]` / `[NEEDS check_my_copy]` / `[UNVERIFIED]` tag from the
Brand & Proof-Point Gate above. Tim reviews and copies `[READY]` posts to LinkedIn manually — this skill
does not post directly to LinkedIn, and the Gmail-draft staging workflow in this repo's CLAUDE.md applies
to email touches, not LinkedIn content.

### Best Practices

1. **Post Consistently**: 3-5x per week minimum
2. **Engage More Than You Post**: Comment 10x for every 1 post
3. **Be Authentically You**: Don't copy others' voice
4. **Provide Value First**: Don't pitch in posts
5. **Track What Works**: Double down on high-engagement themes
6. **Move Conversations Off-Platform**: DM → Call → Meeting
7. **Play Long Game**: Takes 3-6 months to build momentum

Remember: Social selling is about being helpful at scale!

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-social-selling-content-generator.json`:
```json
{"ts":"[UTC ISO8601]","skill":"social-selling-content-generator","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"posts_generated":[n],"content_types":[n],"comment_strategies":[n],"weeks_of_content":[n],
            "posts_passed_brand_gate":[n],"posts_unverified":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced (including any post left
`[UNVERIFIED]` or `[NEEDS check_my_copy]`). Use "error" only if no output was generated.

</workflow>

<dependencies>
## MCP tools
- **Epiphan Brand:** `check_my_copy` (required gate on any Epiphan-referencing post before it's marked
  `[READY]`), `get_writing_style` (optional — pulls Tim's voice before drafting)
- **Epiphan AI:** `search_product_knowledge` (deep technical/RAG proof points), `search_product_catalog`
  (specs, pricing, SKUs) — source of truth for any claim made about Epiphan in a post

## Sibling skills (overlap — reuse, don't duplicate)
- `content-marketing-skill` — blog/case-study/video content, general content strategy, and repurposing
  long-form into LinkedIn/Twitter/email. If the ask is refining an existing draft or repurposing other
  content, hand off to that skill instead of regenerating a calendar here.
- `linkedin-sales-navigator-alt-skill` — LinkedIn prospect list building/tracking, not content generation.
</dependencies>

## Guardrails
- Never state an Epiphan product spec, feature, or competitor claim from memory — always verify via
  `search_product_knowledge`/`search_product_catalog` first, and cut or flag `[UNVERIFIED]` claims the
  tools can't confirm.
- Never mark a post `[READY]` if it references Epiphan and hasn't passed `check_my_copy`.
- Personas and pain points must come from Epiphan's real ICP verticals (Higher Ed, Courts/Legal,
  Government, Corporate AV, Healthcare, Houses of Worship, K-12) — not generic SaaS/tech-sales roles.
- This skill generates net-new posts only; for refining an existing draft or repurposing other content,
  hand off to `content-marketing-skill`.

## Skill metadata
**Version:** 1.0 · **Author:** Tim Kipper · **Status:** active
