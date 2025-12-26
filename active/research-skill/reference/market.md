# Market Research Reference

Comprehensive guide for company research, competitive analysis, and lead intelligence.

---

## Company Profile Template

### Basic Information

```yaml
company:
  name: ""
  website: ""
  linkedin: ""
  founded: ""
  headquarters: ""

industry:
  primary: ""  # e.g., "Electrical Contractor"
  secondary: []  # e.g., ["HVAC", "Plumbing"]
  naics_codes: []

size:
  employees_total: 0
  employees_field: 0
  employees_office: 0
  trucks_vehicles: 0
  revenue_estimate: ""  # "$5-10M", "$10-25M", "$25-50M", "$50M+"
  growth_stage: ""  # "startup", "growth", "mature", "declining"
```

### Operations Profile

```yaml
operations:
  service_area:
    states: []
    major_metros: []
    radius_miles: 0

  service_types:
    - type: "commercial"
      percentage: 0
    - type: "residential"
      percentage: 0
    - type: "service_calls"
      percentage: 0
    - type: "new_construction"
      percentage: 0

  trades_offered:
    - name: ""
      team_size: 0
      revenue_percentage: 0

  certifications: []
  licenses: []
```

### Technology Stack

```yaml
software:
  crm:
    name: ""
    satisfaction: ""  # "happy", "neutral", "frustrated"
    years_using: 0

  project_management:
    name: ""
    satisfaction: ""
    years_using: 0

  accounting:
    name: ""
    satisfaction: ""
    years_using: 0

  field_service:
    name: ""
    satisfaction: ""
    years_using: 0

  other_tools:
    - name: ""
      purpose: ""

  known_integrations: []

  gaps_identified:
    - area: ""
      current_workaround: ""  # Often "spreadsheets" or "paper"
```

### Pain Points & Signals

```yaml
pain_points:
  operational:
    - description: ""
      severity: ""  # "high", "medium", "low"
      evidence: ""  # Where you found this

  technology:
    - description: ""
      severity: ""
      evidence: ""

  growth:
    - description: ""
      severity: ""
      evidence: ""

failed_implementations:
  - software: ""
    timeframe: ""
    reason_failed: ""
    lessons_learned: ""
```

### Decision Makers

```yaml
decision_makers:
  - name: ""
    title: ""
    linkedin: ""
    email: ""
    phone: ""
    role_in_decision: ""  # "champion", "decision_maker", "influencer", "blocker"
    communication_style: ""
    notes: ""

buying_committee:
  - role: "Economic Buyer"
    person: ""
  - role: "Technical Evaluator"
    person: ""
  - role: "End User Champion"
    person: ""
```

### Sales Intelligence

```yaml
sales_intel:
  icp_fit_score: 0  # 0-100
  tier: ""  # "GOLD", "SILVER", "BRONZE"

  timing_signals:
    - signal: ""
      date_detected: ""
      implication: ""

  competitive_situation:
    actively_evaluating: []
    incumbent_satisfaction: ""
    budget_cycle: ""  # "Q1", "fiscal year end", etc.

  objections_anticipated:
    - objection: ""
      response_strategy: ""

  value_proposition_fit:
    - pain_point: ""
      our_solution: ""
      proof_point: ""
```

### Research Sources

```yaml
sources:
  - type: "website"
    url: ""
    date_accessed: ""
    key_findings: []

  - type: "linkedin"
    url: ""
    date_accessed: ""
    key_findings: []

  - type: "glassdoor"
    url: ""
    date_accessed: ""
    key_findings: []

  - type: "news"
    url: ""
    date_accessed: ""
    key_findings: []

research_gaps:
  - question: ""
    how_to_find: ""
```

---

## Tech Stack Discovery Guide

### Discovery Methods

#### 1. Job Postings (Best Signal)

**Where to look:**
- Indeed, LinkedIn Jobs, Glassdoor
- Company careers page

**What to search for:**
```
"[Company Name]" AND ("software" OR "systems" OR "ERP" OR "CRM")
```

**Gold mine phrases:**
- "Experience with [Software] required"
- "Familiarity with [Software] a plus"
- "Must know [Software]"
- "Will train on [Software]"

**Example findings:**
```
Job: Project Manager
Found: "Experience with Procore and Bluebeam required"
Insight: Using Procore for project management

Job: Service Dispatcher
Found: "Knowledge of ServiceTitan preferred"
Insight: Either using ServiceTitan or evaluating it
```

#### 2. Website Analysis

**Pages to check:**
- /about - May mention technology investments
- /careers - Job requirements reveal stack
- /integrations - If they're a vendor
- /case-studies - Often mention tools used
- /blog - Tech announcements

**Footer/badges to look for:**
- "Powered by [Platform]"
- Integration partner logos
- Certification badges

#### 3. LinkedIn Company Page

**Signals:**
- Technology section in company details
- Posts about software rollouts
- Employee profiles mentioning tools
- "We're excited to announce our partnership with..."

#### 4. Review Sites

**G2, Capterra, TrustRadius:**
- Search company name in reviews
- Check "Companies Like Us" sections
- Look at comparison pages

**Google Reviews:**
- Search: `"[company name]" "software" OR "system" OR "app"`

#### 5. Industry Forums & Reddit

**Search patterns:**
```
site:reddit.com "[company name]" software
site:electriciantalk.com "[company name]"
site:hvac-talk.com "[company name]"
```

---

### Software Categories to Identify

#### Tier 1: Core Operations (Must Find)

| Category | Common Options | Discovery Priority |
|----------|---------------|-------------------|
| CRM | Salesforce, HubSpot, Pipedrive, Spreadsheets | HIGH |
| Project Mgmt | Procore, Buildertrend, CoConstruct, Monday | HIGH |
| Accounting | QuickBooks, Sage, Viewpoint, FreshBooks | HIGH |
| Field Service | ServiceTitan, FieldEdge, Housecall Pro | HIGH |

#### Tier 2: Operations (Good to Find)

| Category | Common Options | Discovery Priority |
|----------|---------------|-------------------|
| Estimating | Accubid, ConEst, RS Means, spreadsheets | MEDIUM |
| Scheduling | Calendly, Dispatch, custom, paper | MEDIUM |
| Fleet/GPS | Verizon Connect, Samsara, GPS Trackit | MEDIUM |
| Time Tracking | TSheets, Clockify, paper timesheets | MEDIUM |

#### Tier 3: Specialized (Nice to Have)

| Category | Common Options | Discovery Priority |
|----------|---------------|-------------------|
| Design/CAD | AutoCAD, Revit, Bluebeam | LOW |
| Inventory | Fishbowl, inFlow, spreadsheets | LOW |
| Safety | SafetyCulture, iAuditor | LOW |
| Training | ProCore, Cornerstone | LOW |

---

### Stack Patterns by Company Size

#### Pattern A: Enterprise ($50M+)
```
CRM: Salesforce
Project: Procore or Viewpoint
Field Service: ServiceTitan or ServiceMax
Accounting: Sage 300 or Viewpoint Spectrum
Estimating: Accubid or ConEst
```

#### Pattern B: Mid-Market ($10-50M)
```
CRM: HubSpot or Salesforce Essentials
Project: Buildertrend or CoConstruct
Field Service: ServiceTitan or FieldEdge
Accounting: QuickBooks Enterprise
Estimating: ConEst or spreadsheets
```

#### Pattern C: SMB ($2-10M)
```
CRM: Spreadsheets or basic HubSpot
Project: Buildertrend or Jobber
Field Service: Housecall Pro or Jobber
Accounting: QuickBooks Online
Estimating: Spreadsheets
```

#### Pattern D: "The Gap" (Pain Point Target)
```
CRM: Spreadsheets + maybe HubSpot free
Project: One tool that doesn't fit
Field Service: Different tool or spreadsheets
Accounting: QuickBooks (only thing that works)
Estimating: Spreadsheets
Pain: "Nothing talks to each other"
```

---

### Stack Satisfaction Signals

**Happy with current stack:**
- Long tenure (5+ years)
- Posting jobs that require it
- Case studies featuring them
- Active in user community

**Frustrated with current stack:**
- Multiple systems for same function
- "Spreadsheets" mentioned anywhere
- Recent switch (< 2 years)
- Glassdoor mentions "outdated systems"
- Job posts mention "help us improve processes"

**Actively evaluating:**
- RFP mentions online
- Attending software demos (trade shows)
- LinkedIn activity on vendor pages
- "Looking for recommendations" posts

---

## ICP Scoring Framework

### The Sweet Spot

**Revenue:** $5M - $50M annually

**Why this range:**
- < $5M: Too small, Jobber/Housecall Pro works fine
- $5-50M: "No man's land" - too complex for SMB tools, too small for ServiceTitan
- > $50M: ServiceTitan, Procore ecosystem makes sense

**Trades:** Multi-trade operations (2+ of these)
- Electrical (commercial/residential)
- HVAC
- Plumbing
- Low voltage / Fire alarm
- Solar / Battery

**Why multi-trade matters:**
- Single-trade shops can use vertical-specific tools
- Multi-trade = integration nightmare = opportunity

---

### Scoring Criteria

#### Must-Haves (Disqualify if missing)

| Criteria | Requirement | Weight |
|----------|-------------|--------|
| Revenue | $5M - $50M | Gate |
| Trades | 2+ trades OR 50+ employees | Gate |
| Geography | US-based | Gate |
| Growth | Not declining | Gate |

#### Scoring Factors (0-100 total)

| Factor | Max Points | How to Score |
|--------|-----------|--------------|
| Multi-trade complexity | 25 | 2 trades=15, 3+=25 |
| Tech stack pain | 25 | Spreadsheets=25, Multiple systems=20, One bad system=15 |
| Growth signals | 20 | Hiring=10, New markets=10, Revenue growth=10 |
| Decision maker access | 15 | Owner=15, Ops Director=10, PM=5 |
| Timing signals | 15 | Active search=15, Mentioned pain=10, Nothing=0 |

#### Tier Assignment

| Score | Tier | Action |
|-------|------|--------|
| 70-100 | GOLD | Immediate outreach, personalized |
| 50-69 | SILVER | Week 1 sequence, semi-personalized |
| 30-49 | BRONZE | Nurture sequence, templated |
| 0-29 | DISQUALIFY | Don't pursue |

---

### Pain Points to Solve

**Pain Point 1: System Fragmentation**
- Signal: "We use [X] for projects and [Y] for service calls"
- Answer: Single platform for all work types

**Pain Point 2: Spreadsheet Hell**
- Signal: "Trucks/equipment/scheduling in spreadsheets"
- Answer: Built-in asset and resource management

**Pain Point 3: Outgrown Current Tools**
- Signal: "Jobber was great when we were smaller"
- Answer: Scales without enterprise complexity

**Pain Point 4: Failed Implementation**
- Signal: "We tried [ServiceTitan/Procore] and it didn't work"
- Answer: Right-sized for mid-market, not enterprise bloat

**Pain Point 5: No Single Source of Truth**
- Signal: "I don't know what's profitable"
- Answer: Job costing that actually works

---

### Disqualification Signals

**Hard No:**
- Single trade, single location, < $3M revenue
- Already happy with ServiceTitan (rare but exists)
- Government/public sector (procurement nightmare)
- Franchise operations (corporate decides)

**Soft No (Nurture):**
- Currently in contract (when does it end?)
- Just implemented something (give it 12 months)
- No decision maker access (find another way in)
- "We're fine" (need triggering event)

---

## Competitive Analysis Framework

### Research Process

#### Step 1: Identify Competitors (15 min)

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

#### Step 2: Gather Intelligence (30-60 min per competitor)

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

### Competitor Profile Template

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

### Analysis Frameworks

#### SWOT Analysis

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

#### Feature Comparison Matrix

| Feature | Us | Competitor A | Competitor B |
|---------|----|--------------| -------------|
| Feature 1 | [check] Full | [warn] Partial | [x] None |
| Feature 2 | [check] Full | [check] Full | [warn] Partial |
| Feature 3 | [warn] Partial | [check] Full | [check] Full |

#### Positioning Map

```
                    HIGH PRICE
                        |
                        |
         Enterprise ────┼──── Premium
                        |
    LOW ────────────────┼──────────────── HIGH
    COMPLEXITY          |            COMPLEXITY
                        |
         Budget ────────┼──── Mid-Market
                        |
                    LOW PRICE
```

---

### Battle Card Template

#### Competitor: [Name]

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

### Win/Loss Analysis

After every competitive deal, document:

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

### Competitive Response Playbook

#### When They Go Negative on Us

**Response framework:**
1. Acknowledge (don't dismiss)
2. Reframe the comparison
3. Redirect to our strength
4. Provide proof point

**Example:**
> Prospect: "[Competitor] says you can't handle enterprise scale."
> Response: "Fair concern. We're built for $5-50M companies specifically - that's our sweet spot. [Competitor] is designed for $100M+ enterprises, which means complexity you don't need. Here's a reference at your exact size..."

#### When They're Cheaper

**Never compete on price alone.**

1. Shift to total cost of ownership
2. Quantify implementation time/cost
3. Calculate productivity gains
4. Show hidden costs in their model

**Example:**
> "[Competitor] is $X cheaper per month, but their implementation takes 6 months vs our 6 weeks. What's 4 months of productivity worth to you?"

#### When They Have a Feature We Lack

1. Validate the need (don't dismiss)
2. Explain our approach
3. Show workaround if exists
4. Share roadmap if coming

**Example:**
> "You're right, we don't have [feature] today. Here's why: [reason]. Most customers solve this by [workaround]. It's on our roadmap for [timeframe] - want me to connect you with a customer who had the same concern?"
