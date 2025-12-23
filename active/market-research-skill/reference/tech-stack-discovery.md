# Tech Stack Discovery Guide

## Discovery Methods

### 1. Job Postings (Best Signal)

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

### 2. Website Analysis

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

### 3. LinkedIn Company Page

**Signals:**
- Technology section in company details
- Posts about software rollouts
- Employee profiles mentioning tools
- "We're excited to announce our partnership with..."

### 4. Review Sites

**G2, Capterra, TrustRadius:**
- Search company name in reviews
- Check "Companies Like Us" sections
- Look at comparison pages

**Google Reviews:**
- Search: `"[company name]" "software" OR "system" OR "app"`

### 5. Industry Forums & Reddit

**Search patterns:**
```
site:reddit.com "[company name]" software
site:electriciantalk.com "[company name]"
site:hvac-talk.com "[company name]" 
```

---

## Software Categories to Identify

### Tier 1: Core Operations (Must Find)

| Category | Common Options | Discovery Priority |
|----------|---------------|-------------------|
| CRM | Salesforce, HubSpot, Pipedrive, Spreadsheets | HIGH |
| Project Mgmt | Procore, Buildertrend, CoConstruct, Monday | HIGH |
| Accounting | QuickBooks, Sage, Viewpoint, FreshBooks | HIGH |
| Field Service | ServiceTitan, FieldEdge, Housecall Pro | HIGH |

### Tier 2: Operations (Good to Find)

| Category | Common Options | Discovery Priority |
|----------|---------------|-------------------|
| Estimating | Accubid, ConEst, RS Means, spreadsheets | MEDIUM |
| Scheduling | Calendly, Dispatch, custom, paper | MEDIUM |
| Fleet/GPS | Verizon Connect, Samsara, GPS Trackit | MEDIUM |
| Time Tracking | TSheets, Clockify, paper timesheets | MEDIUM |

### Tier 3: Specialized (Nice to Have)

| Category | Common Options | Discovery Priority |
|----------|---------------|-------------------|
| Design/CAD | AutoCAD, Revit, Bluebeam | LOW |
| Inventory | Fishbowl, inFlow, spreadsheets | LOW |
| Safety | SafetyCulture, iAuditor | LOW |
| Training | ProCore, Cornerstone | LOW |

---

## MEP+E Specific Stack Patterns

### Pattern A: Enterprise ($50M+)
```
CRM: Salesforce
Project: Procore or Viewpoint
Field Service: ServiceTitan or ServiceMax
Accounting: Sage 300 or Viewpoint Spectrum
Estimating: Accubid or ConEst
```

### Pattern B: Mid-Market ($10-50M)
```
CRM: HubSpot or Salesforce Essentials
Project: Buildertrend or CoConstruct
Field Service: ServiceTitan or FieldEdge
Accounting: QuickBooks Enterprise
Estimating: ConEst or spreadsheets
```

### Pattern C: SMB ($2-10M)
```
CRM: Spreadsheets or basic HubSpot
Project: Buildertrend or Jobber
Field Service: Housecall Pro or Jobber
Accounting: QuickBooks Online
Estimating: Spreadsheets
```

### Pattern D: "The Gap" (Coperniq Target)
```
CRM: Spreadsheets + maybe HubSpot free
Project: One tool that doesn't fit
Field Service: Different tool or spreadsheets
Accounting: QuickBooks (only thing that works)
Estimating: Spreadsheets
Pain: "Nothing talks to each other"
```

---

## Stack Satisfaction Signals

### Happy with current stack:
- Long tenure (5+ years)
- Posting jobs that require it
- Case studies featuring them
- Active in user community

### Frustrated with current stack:
- Multiple systems for same function
- "Spreadsheets" mentioned anywhere
- Recent switch (< 2 years)
- Glassdoor mentions "outdated systems"
- Job posts mention "help us improve processes"

### Actively evaluating:
- RFP mentions online
- Attending software demos (trade shows)
- LinkedIn activity on vendor pages
- "Looking for recommendations" posts

---

## Quick Research Script

```python
def research_tech_stack(company_name: str) -> dict:
    """
    30-minute tech stack research workflow
    """
    stack = {
        'confirmed': [],      # Direct evidence
        'likely': [],         # Strong signals
        'possible': [],       # Weak signals
        'gaps': [],           # Using spreadsheets/paper
        'sources': []
    }
    
    # Step 1: Job postings (10 min)
    # Search Indeed, LinkedIn for company + software terms
    
    # Step 2: Website scan (5 min)
    # Check careers, about, integrations pages
    
    # Step 3: LinkedIn (5 min)
    # Company page, recent posts, employee profiles
    
    # Step 4: Review sites (5 min)
    # G2, Capterra for company mentions
    
    # Step 5: Google search (5 min)
    # "[company] software" "[company] CRM" etc.
    
    return stack
```

---

## Output Format

After research, document findings:

```yaml
tech_stack_research:
  company: "ABC Electric"
  researched_date: "2025-01-15"
  confidence: "high"  # high/medium/low
  
  confirmed:
    - software: "QuickBooks Enterprise"
      evidence: "Job posting requires QB experience"
      source_url: ""
      
  likely:
    - software: "Buildertrend"
      evidence: "Logo on their website partners page"
      source_url: ""
      
  gaps_identified:
    - area: "Field service dispatch"
      current_solution: "Spreadsheets"
      evidence: "Glassdoor review: 'dispatch is chaos'"
      
  pain_indicators:
    - "Multiple systems mentioned in ops manager posting"
    - "Hiring 'systems administrator' - scaling pains"
```
