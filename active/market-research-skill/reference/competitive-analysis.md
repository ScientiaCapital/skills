# Competitive Analysis Framework

## Research Process

### Step 1: Identify Competitors (15 min)

**Direct competitors:**
- Same product category
- Same target customer
- Same price tier

**Indirect competitors:**
- Different approach, same problem
- Adjacent categories
- "Do nothing" / spreadsheets

**Emerging competitors:**
- Startups in the space
- Big tech entering
- Open source alternatives

### Step 2: Gather Intelligence (30-60 min per competitor)

**Public sources:**
- Website (pricing, features, positioning)
- G2/Capterra reviews (strengths, weaknesses)
- Glassdoor (internal culture, challenges)
- LinkedIn (team size, hiring, growth)
- Crunchbase (funding, investors)
- Press releases (announcements, partnerships)

**Customer intelligence:**
- Win/loss interviews
- Prospect mentions during calls
- Industry forums / Reddit
- Social media sentiment

---

## Competitor Profile Template

```yaml
competitor:
  name: ""
  website: ""
  founded: ""
  headquarters: ""
  
funding:
  total_raised: ""
  last_round: ""
  investors: []
  
team:
  employee_count: ""
  growth_rate: ""  # YoY
  key_hires: []
  
product:
  core_offering: ""
  key_features: []
  integrations: []
  platforms: []  # web, mobile, etc.
  
pricing:
  model: ""  # per user, per seat, usage-based
  entry_price: ""
  mid_tier: ""
  enterprise: ""
  
target_market:
  segments: []
  company_size: ""
  industries: []
  geography: []
  
positioning:
  tagline: ""
  key_messages: []
  differentiation: []
  
strengths: []
weaknesses: []
threats_to_us: []
opportunities_against: []
```

---

## Analysis Frameworks

### SWOT Analysis

```
           HELPFUL              HARMFUL
         to objective        to objective
       ┌─────────────────┬─────────────────┐
INTERNAL│   STRENGTHS    │   WEAKNESSES    │
(us)    │                │                 │
       ├─────────────────┼─────────────────┤
EXTERNAL│ OPPORTUNITIES  │    THREATS      │
(them)  │                │                 │
       └─────────────────┴─────────────────┘
```

### Feature Comparison Matrix

| Feature | Us | Competitor A | Competitor B |
|---------|----|--------------| -------------|
| Feature 1 | ✅ Full | ⚠️ Partial | ❌ None |
| Feature 2 | ✅ Full | ✅ Full | ⚠️ Partial |
| Feature 3 | ⚠️ Partial | ✅ Full | ✅ Full |

### Positioning Map

```
                    HIGH PRICE
                        │
                        │
         Enterprise ────┼──── Premium
                        │
    LOW ────────────────┼──────────────── HIGH
    COMPLEXITY          │            COMPLEXITY
                        │
         Budget ────────┼──── Mid-Market
                        │
                    LOW PRICE
```

---

## Battle Card Template

### Competitor: [Name]

**In one sentence:** [What they do and for whom]

**When we see them:** [Deal stages, customer types]

**Their pitch:** [Key messages they use]

**Our response:**
- Claim: "[Their claim]"
- Reality: "[The truth]"
- Our advantage: "[Why we're better]"

**Landmines to set:**
- Ask prospect about [topic they're weak on]
- Demo [feature they don't have]
- Reference [case study that beats them]

**Traps to avoid:**
- Don't get into [area they're strong]
- Avoid [pricing comparison if they're cheaper]
- Don't mention [feature we lack]

**Win themes:**
1. [Key differentiator 1]
2. [Key differentiator 2]
3. [Key differentiator 3]

**Knockout questions:**
- "How does [competitor] handle [thing they do poorly]?"
- "What's your experience with [common complaint]?"
- "Have you seen [specific feature they lack]?"

---

## Intelligence Sources

### Review Mining

**G2 Crowd:**
- Filter by company size matching our ICP
- Focus on "What do you dislike?" section
- Note feature requests in reviews

**Capterra:**
- Sort by "most critical" reviews
- Look for patterns in complaints
- Check recency of reviews

**Glassdoor:**
- Employee complaints = product/company issues
- "Cons" section reveals internal challenges
- Interview reviews show culture

### Social Listening

**Reddit:**
```
site:reddit.com "[competitor name]" (problem OR issue OR hate OR love)
```

**Twitter/X:**
```
"[competitor name]" (frustrated OR broken OR love OR amazing)
```

**LinkedIn:**
- Follow competitor company page
- Track employee posts
- Monitor job postings (reveals strategy)

### Win/Loss Analysis

**After every competitive deal, document:**

```yaml
deal_outcome:
  result: "win" | "loss"
  competitor: ""
  deal_size: ""
  sales_cycle_days: ""
  
decision_factors:
  why_us: []
  why_them: []
  feature_gaps: []
  
process_notes:
  when_entered: ""  # early, mid, late
  champion_strength: ""
  pricing_comparison: ""
  
learnings:
  what_worked: []
  what_didnt: []
  for_next_time: []
```

---

## Competitive Response Playbook

### When They Go Negative on Us

**Response framework:**
1. Acknowledge (don't dismiss)
2. Reframe the comparison
3. Redirect to our strength
4. Provide proof point

**Example:**
> Prospect: "[Competitor] says you can't handle enterprise scale."
> Response: "Fair concern. We're built for $5-50M companies specifically - that's our sweet spot. [Competitor] is designed for $100M+ enterprises, which means complexity you don't need. Here's a reference at your exact size..."

### When They're Cheaper

**Never compete on price alone.**

1. Shift to total cost of ownership
2. Quantify implementation time/cost
3. Calculate productivity gains
4. Show hidden costs in their model

**Example:**
> "[Competitor] is $X cheaper per month, but their implementation takes 6 months vs our 6 weeks. What's 4 months of productivity worth to you?"

### When They Have a Feature We Lack

1. Validate the need (don't dismiss)
2. Explain our approach
3. Show workaround if exists
4. Share roadmap if coming

**Example:**
> "You're right, we don't have [feature] today. Here's why: [reason]. Most customers solve this by [workaround]. It's on our roadmap for [timeframe] - want me to connect you with a customer who had the same concern?"
