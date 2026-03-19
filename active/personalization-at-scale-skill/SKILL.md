---
name: personalization-at-scale-skill
description: Generate unique personalized first lines for hundreds of prospects using company news, LinkedIn activity, and mutual connections. Saves 10+ hours of manual research per campaign. Use when you need personalized outreach at volume.
---

# Personalization at Scale

<objective>
Generate hundreds of unique, researched first lines in minutes instead of hours. Takes a prospect list and finds personalization angles from company news, LinkedIn activity, funding rounds, hiring signals, and mutual connections to make cold outreach feel warm.
</objective>

<quick_start>
**Trigger:** "Personalize outreach for [N] prospects" or "Generate unique first lines for my prospect list"
**Input:** CSV or list with First Name, Last Name, Title, Company, LinkedIn URL
**Output:** Personalized first lines with confidence scores, grouped by personalization type, in CSV or merge-field format
</quick_start>

<success_criteria>
- [ ] 70%+ prospects have unique, specific personalization found
- [ ] Each first line is recent (within 30-60 days), role-relevant, and couldn't be copy/pasted to another prospect
- [ ] Confidence scores assigned (High/Medium/Low) to every first line
- [ ] Fallback strategies provided for prospects with no personalization found
- [ ] Output ready for export to outreach tool (CSV merge fields)
</success_criteria>

<workflow>

## Instructions

You are an expert sales development researcher who specializes in finding personalization angles for outbound prospecting at scale.

### Research Sources
- Company news and press releases
- LinkedIn activity (posts, comments, job changes)
- Funding announcements and rounds
- Product launches, hiring patterns, tech stack changes
- Conference attendance, podcast/webinar appearances
- Blog posts and thought leadership
- Mutual connections, shared interests/alma mater
- Recent promotions or role changes

### Personalization Styles
1. **Congratulations** - Recent achievement or announcement
2. **Observation** - Noticed something specific about their company/role
3. **Shared Interest** - Common connection, interest, or experience
4. **Insight** - Industry trend relevant to their situation
5. **Question** - Ask about their approach to a challenge
6. **Compliment** - Genuine praise for their work/content
7. **Problem Call-Out** - Identify a pain point they're likely experiencing

### Quality Standards

**Good Personalization**:
- Specific and unique to them (couldn't copy/paste to anyone else)
- Recent (within last 30-60 days ideally)
- Relevant to their role or business
- Natural and conversational (not creepy-stalker)
- Easy to verify (they can remember this happening)

**Avoid**:
- Generic compliments ("I love your company!")
- Fake personalization ("I was on your website...")
- Stale information (from 6+ months ago)
- Information they'd be uncomfortable you know
- Obvious automation ("I saw your recent LinkedIn post" x 100)

### Output Format

```markdown
# Personalization at Scale: [Campaign Name]

**Campaign**: [Campaign name/description]
**Prospect Count**: [Number]
**Target Persona**: [Job title/role]
**Industry**: [Industry or vertical]
**Research Date**: [Date]
**Personalization Success Rate**: [X]% (prospects with unique personalization found)

---

## Campaign Summary

**Personalization Breakdown**:
- [X] prospects: Company news/press mention
- [X] prospects: Recent LinkedIn activity
- [X] prospects: Funding or growth signals
- [X] prospects: Mutual connections
- [X] prospects: Hiring/tech stack signals
- [X] prospects: Recent job change
- [X] prospects: Content/thought leadership
- [X] prospects: No personalization found (fallback needed)

**Time Saved**: Manual ~5 min/prospect vs AI ~10 sec/prospect = [X] hours saved

---

## Personalized First Lines

### Prospect #1: [Name]

**Details**: [First Last] | [Title] | [Company] | [LinkedIn URL]

**Personalization Found**:
- **Type**: [Congratulations/Observation/Shared/etc.]
- **Source**: [LinkedIn post / Company news / Funding round / etc.]
- **Date**: [When this happened]
- **Context**: [Brief description of what you found]

**Option 1 (Direct)**:
> "Hi [First Name], congrats on [specific achievement]! I noticed [additional observation]. [Transition to value prop]"

**Option 2 (Question)**:
> "[First Name], I saw [specific thing]. Curious - are you [question related to their situation]?"

**Option 3 (Insight)**:
> "Hi [First Name], given [their situation/news], I imagine [relevant challenge]. [Transition to value prop]"

**Confidence Score**: [High/Medium/Low]
- High: Recent, specific, highly relevant
- Medium: Relevant but older, or less specific
- Low: Generic personalization, may not resonate

---

### Prospect #2: [Name]

[Repeat structure for each prospect]

---

## Personalization by Type

### Congratulations
Prospects with recent achievements, funding, promotions, or launches. First line pattern:
> "Congrats on [specific event]! With that kind of [growth/change], [likely pain point you solve]..."

### Observations
Prospects who posted content, made comments, or showed LinkedIn activity. First line pattern:
> "Loved your take on [topic]. The point about [specific thing] really resonated - we see that with [similar companies]..."

### Mutual Connections
Prospects with 1st or 2nd degree connections you can reference. First line pattern:
> "Hi [Name], I noticed we're both connected with [Mutual Connection]. [Context]. Thought I should reach out about [topic]..."

### Company News
Companies with recent press mentions, launches, or announcements. First line pattern:
> "[Name], saw [Company] is [news event]. That kind of [change] usually creates [specific challenge you solve]..."

### Hiring Signals
Companies with job postings indicating growth, tech changes, or priorities. First line pattern:
> "Noticed you're hiring [X+ roles]. Scaling that fast usually creates [specific problem you solve]..."

### Thought Leadership
Prospects on podcasts, webinars, published blogs, or conference speaking. First line pattern:
> "Really enjoyed your [content type] on [topic]. Your point about [specific insight] was spot-on..."

---

## No Personalization Found — Fallback Strategies

**Role-Based**: "Hi [Name], most [job titles] I talk to are dealing with [common pain point]. Is that on your radar?"

**Company-Stage**: "Hi [Name], companies at [their stage/size] typically face [challenge]. How are you handling [specific aspect]?"

**Industry**: "Hi [Name], with [industry trend], I imagine [company] is thinking about [related topic]..."

**Competitor Reference**: "Hi [Name], we work with [competitor 1], [competitor 2], and [competitor 3] to solve [problem]. Worth a conversation?"
```

---

## Usage Instructions

### Step 1: Upload Prospect List

Provide a CSV or list with at least:
- First Name, Last Name, Job Title, Company Name
- LinkedIn URL (if available), Email (if available)

Optional: Company website, Industry, Company size, Location

### Step 2: Specify Preferences

**Personalization Style** (pick 1-3): Congratulations | Observations | Mutual connections | Company news | Hiring signals | Thought leadership

**Tone**: Professional | Casual | Direct | Consultative

**Avoid**: Anything older than [X] days | Personal information | Sensitive topics

### Step 3: Review & Customize

- Review first 10 personalizations and adjust tone if needed
- Flag any that feel "off"
- Add company-specific context and modify CTAs

### Step 4: Export & Use

**Formats**: CSV with personalization columns | Merge fields for Outreach/Salesloft | Individual email drafts

**Workflow**: Generate → Upload as custom fields → Use in sequence position 1 → Track response rates by type → Double down on what works

---

## Performance Benchmarks

| Metric | Generic Cold Email | With Personalization |
|--------|-------------------|---------------------|
| Response Rate | 1-3% | 8-15% |
| Lift | Baseline | 5-10x improvement |

**Time**: Manual 5-10 min/prospect vs AI 10-30 sec/prospect = 8-16 hours saved per 100 prospects

**Quality Threshold**: Aim for 70%+ with unique personalization. Below 50% = consider different prospect list.

---

### Best Practices

1. **Mix Personalization Types**: Don't just use LinkedIn posts for everyone
2. **Keep It Natural**: Should sound like you'd say it in person
3. **Update Regularly**: Refresh every 30 days as news/activity changes
4. **Track What Works**: Note which types get best response by persona
5. **Quality Over Quantity**: 100 well-personalized > 500 generic
6. **Don't Be Creepy**: If it feels stalker-ish, skip it
7. **Don't Fake It**: "I was on your website" when you clearly weren't
8. **Always Verify**: Spot-check first 10 personalizations manually

### Common Use Cases

**Trigger Phrases**:
- "Personalize outreach for 300 prospects"
- "Generate unique first lines for my prospect list"
- "Find personalization angles for these LinkedIn profiles"
- "Research these 500 companies and prospects"

**Response Approach**:
1. Ingest prospect list (CSV or manual input)
2. Research each prospect across multiple sources
3. Identify best personalization angle per prospect
4. Generate 2-3 first line options per prospect
5. Provide confidence scores and fallback options
6. Export in requested format

Remember: Good personalization should feel like you actually researched them, because you (or AI) did!

</workflow>
