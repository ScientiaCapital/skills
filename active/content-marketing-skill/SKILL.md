---
name: "content-marketing"
description: "B2B content marketing - thought leadership, SEO, LinkedIn, blog posts, case studies, and video scripts. Use when creating content strategy, writing posts, or building demand gen assets."
---

<objective>
Enable effective B2B content marketing for demand generation and thought leadership. Covers content strategy (pillars, calendars), LinkedIn optimization, SEO blog writing, case studies, video scripts, and content repurposing across platforms.
</objective>

<quick_start>
**Content types by funnel stage:**
| Content | Stage | Effort |
|---------|-------|--------|
| LinkedIn post | Top | Low |
| Blog post | Top | Low |
| Case study | Mid | Medium |
| Whitepaper | Mid | High |

**LinkedIn formula:** Hook (1 line) + Story (3-5 lines) + Lesson (2-3 lines) + CTA

**Blog SEO:** Primary keyword in title, H1, first 100 words, URL; 1,500-2,500 words
</quick_start>

<success_criteria>
Content is successful when:
- Maps to one of 3-5 content pillars
- LinkedIn posts follow hook-story-lesson structure
- Blog posts hit SEO checklist (keyword in title, H1, URL, first 100 words)
- Case studies include quantified results (metrics, not vague claims)
- Video scripts have clear hook in first 15 seconds
- Content repurposed: 1 long-form → multiple formats (LinkedIn, Twitter, email)
- Any Epiphan product spec, feature, or competitor claim is verified via `search_product_knowledge`/`search_product_catalog` — never stated from memory
- Every customer-facing draft (blog, LinkedIn, case study, video script, social copy) passes the `check_my_copy` brand-voice gate before it is marked ready to publish/send
</success_criteria>

<core_content>
B2B content strategy and creation for demand generation and thought leadership.

## Quick Reference

| Content Type | Goal | Funnel Stage | Effort |
|--------------|------|--------------|--------|
| Blog post | SEO, awareness | Top | Low |
| LinkedIn post | Engagement, brand | Top | Low |
| Case study | Social proof | Mid | Medium |
| Whitepaper | Lead gen | Mid | High |
| Video | Engagement | All | Medium |
| Webinar | Demand gen | Mid-Bottom | High |

## Content Strategy Framework

### Content Pillars

```yaml
content_pillars:
  definition: "3-5 core themes all content maps to"

  example_gtm_engineer:
    pillar_1:
      name: "AI in Sales"
      topics:
        - "LLM-powered sales automation"
        - "AI agents for outreach"
        - "Cost-optimized AI stacks"

    pillar_2:
      name: "GTM Engineering"
      topics:
        - "Building GTM infrastructure"
        - "Sales + engineering hybrid roles"
        - "Automating the revenue engine"

    pillar_3:
      name: "B2B Sales Craft"
      topics:
        - "Discovery techniques"
        - "Enterprise selling"
        - "25 years of sales lessons"
```

### Content Calendar Template

```markdown
## Monthly Content Calendar

### Week 1: [Theme]
| Day | Platform | Content Type | Topic | Status |
|-----|----------|--------------|-------|--------|
| Mon | LinkedIn | Post | | [ ] |
| Wed | Blog | Article | | [ ] |
| Fri | LinkedIn | Post | | [ ] |

### Week 2: [Theme]
| Day | Platform | Content Type | Topic | Status |
|-----|----------|--------------|-------|--------|
| Mon | LinkedIn | Post | | [ ] |
| Wed | Blog | Article | | [ ] |
| Fri | LinkedIn | Post | | [ ] |

### Monthly Goals
- [ ] 8 LinkedIn posts
- [ ] 2 Blog articles
- [ ] 1 Case study
- [ ] __ impressions target
- [ ] __ engagement target
```

## LinkedIn Content

### Post Formats That Work

**The Hook + Story + Lesson**
```
[Provocative hook - 1 line]

[Story - 3-5 lines]

[Lesson/takeaway - 2-3 lines]

[Call to action or question]
```

**The List Post**
```
[Number] things I learned about [topic]:

1. [Point] - [One line explanation]
2. [Point] - [One line explanation]
...

Which resonates most with you?
```

**The Contrarian Take**
```
Unpopular opinion: [Contrarian statement]

Here's why:

[3-4 supporting points]

Agree or disagree?
```

### LinkedIn Best Practices

```yaml
linkedin_tactics:
  posting:
    frequency: "3-5x per week"
    best_times: "7-8am, 12pm, 5-6pm (local)"
    best_days: "Tuesday-Thursday"

  formatting:
    - "First line is the hook (shows in preview)"
    - "Use line breaks liberally"
    - "Keep paragraphs to 1-2 sentences"
    - "End with engagement prompt"

  engagement:
    - "Reply to every comment within 1 hour"
    - "Comment on 10 posts before posting"
    - "Tag sparingly (only if relevant)"
    - "No links in post (kills reach)"

  hashtags:
    count: "3-5 max"
    placement: "End of post"
    mix: "1 broad, 2 niche, 2 industry"
```

### LinkedIn Post Templates

**Sharing a Win**
```
We just [achievement].

Here's what made the difference:

→ [Key factor 1]
→ [Key factor 2]
→ [Key factor 3]

The biggest lesson: [Insight]

What's working for you lately?
```

**Teaching from Experience**
```
After [X years/deals/projects] in [field], here's what I know for sure:

[Lesson 1]
↳ [Brief explanation]

[Lesson 2]
↳ [Brief explanation]

[Lesson 3]
↳ [Brief explanation]

What would you add?
```

## Blog Content

### Blog Post Structure

```markdown
## [Title - Include primary keyword]

**Meta description**: [150-160 chars with keyword]

### Introduction (100-150 words)
- Hook: Start with pain point or surprising stat
- Context: Why this matters now
- Promise: What reader will learn

### Section 1: [H2 with keyword variation]
- Key point
- Supporting evidence
- Example or data

### Section 2: [H2]
- Key point
- Supporting evidence
- Example or data

### Section 3: [H2]
- Key point
- Supporting evidence
- Example or data

### Conclusion
- Summarize key points
- Call to action
- Next step for reader

**Word count target**: 1,500-2,500 for SEO
```

### SEO Checklist

```markdown
## Blog SEO Checklist

### On-Page SEO
- [ ] Primary keyword in title (front-loaded)
- [ ] Primary keyword in URL slug
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in H1
- [ ] Secondary keywords in H2s
- [ ] Meta description (150-160 chars)
- [ ] Image alt text with keywords
- [ ] Internal links (2-3)
- [ ] External links (1-2 authoritative)

### Content Quality
- [ ] Answers search intent
- [ ] Better than top 3 results
- [ ] Includes unique data/perspective
- [ ] Readable (short paragraphs, bullets)
- [ ] Mobile-friendly formatting

### Technical
- [ ] URL is clean (/blog/keyword-topic)
- [ ] Page loads <3 seconds
- [ ] Images compressed
- [ ] Schema markup (if applicable)
```

> If the blog references any Epiphan product spec, feature, or competitor comparison, verify it via
> `search_product_knowledge`/`search_product_catalog` first (see the Verification Gate under Case Studies),
> then run `check_my_copy` on the final draft before it's marked ready to publish.

## Case Studies

### Case Study Structure

```markdown
# [Customer Name]: [Headline Result]

## The Challenge
- Company background (1-2 sentences)
- Situation before (pain points)
- Why they needed to change

## The Solution
- Why they chose us
- Implementation overview
- Key features/services used  *(verify each Epiphan feature/spec claim via `search_product_knowledge` before including — never from memory)*

## The Results
- Quantified outcomes (3-5 metrics)
- Qualitative improvements
- Timeline to results

## Customer Quote
> "[Compelling testimonial]"
> — [Name], [Title] at [Company]

## Key Takeaways
1. [Lesson others can apply]
2. [Lesson others can apply]
3. [Lesson others can apply]
```

### Verification Gate (before drafting or publishing)

Case studies and any other content that references Epiphan product specs, features, or competitor
comparisons must **never state those claims from memory**. Before the claim is used in output:
1. Call `search_product_knowledge` (or `search_product_catalog`) to confirm the spec/feature/competitor
   claim against current product data.
2. If the tool returns nothing or is unavailable, do not guess — cut the claim or flag it in the draft
   as `[UNVERIFIED — confirm before publishing]` and mark the run `partial`.
3. Once the draft is complete, run `check_my_copy` (Epiphan brand-voice gate) on the full customer-facing
   text. Only mark content "ready to publish/send" after it passes.

### Case Study Metrics to Include

```yaml
strong_metrics:
  revenue:
    - "Increased revenue by X%"
    - "Generated $X in new business"
    - "Reduced costs by $X"

  efficiency:
    - "Saved X hours per week"
    - "Reduced processing time by X%"
    - "Automated X% of manual tasks"

  performance:
    - "Improved conversion by X%"
    - "Increased win rate from X% to Y%"
    - "Shortened sales cycle by X days"

  scale:
    - "Scaled from X to Y users"
    - "Handled Xx more volume"
    - "Expanded to X new markets"
```

## Video Content

### Video Script Structure

```markdown
## [Video Title]
**Length**: [Target duration]
**Goal**: [What viewer should do/learn]

### HOOK (0:00-0:15)
[Attention-grabbing opening - question, stat, or bold claim]

### INTRO (0:15-0:30)
"Hey, I'm [Name]. Today I'm going to show you [promise]"

### MAIN CONTENT
**Point 1** (0:30-2:00)
[Key insight + example]

**Point 2** (2:00-3:30)
[Key insight + example]

**Point 3** (3:30-5:00)
[Key insight + example]

### CTA (5:00-5:30)
"If this was helpful, [subscribe/follow/download].
Next video, I'll cover [teaser]"

### B-ROLL NOTES
- [Visual to show at timestamp]
- [Screen recording needed]
- [Graphic to create]
```

> Same gate applies: verify any Epiphan spec/feature/competitor claim via `search_product_knowledge`
> before it goes in the script, and run `check_my_copy` on the finished script before it's finalized.

## Content Repurposing

### One Piece → Many Formats

```
Original: Long-form blog post (2000 words)
           ↓
├── LinkedIn carousel (10 slides)
├── Twitter/X thread (10 tweets)
├── Email newsletter summary
├── Short-form video script (2 min)
├── Podcast talking points
├── Infographic
└── Quote graphics (5-10)
```

## Integration Notes

- **Pairs with**: gtm-strategy-skill (messaging), market-research-skill (topics)
- **Product/brand gates**: `search_product_knowledge` / `search_product_catalog` (Epiphan spec + competitor
  claim verification), `check_my_copy` (brand-voice gate on customer-facing drafts) — see Verification Gate
  under Case Studies.

## Reference Files

- `reference/linkedin-templates.md` - 20+ post templates
- `reference/blog-templates.md` - Article structures by type
- `reference/seo-checklist.md` - Comprehensive SEO guide
- `reference/video-scripts.md` - Video content frameworks

## Emit Outcome Sidecar

As the final step, write to `~/.claude/skill-analytics/last-outcome-content-marketing.json`:
```json
{"ts":"[UTC ISO8601]","skill":"content-marketing","version":"1.0.0","variant":"default",
 "status":"[success|partial|error]","runtime_ms":[estimated ms from start],
 "metrics":{"content_pieces_created":[n],"platforms_targeted":[n],"repurpose_formats":[n]},
 "error":null,"session_id":"[YYYY-MM-DD]"}
```
Use status "partial" if some stages failed but results were produced. Use "error" only if no output was generated.
