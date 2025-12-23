---
name: market-research-skill
description: |
  Company research, competitive analysis, and lead enrichment for B2B sales.
  Use when researching companies, building profiles, analyzing competitors, or
  preparing for sales calls. Triggers: "research this company", "analyze competitors",
  "find market opportunities", "assess market size", "build company profile",
  "what's their tech stack", "who are the decision makers", "ICP analysis".
---

# Market Research Skill

Company intelligence and competitive analysis for B2B GTM.

## Quick Reference

| Research Type | Output | When to Use |
|---------------|--------|-------------|
| Company Profile | Structured profile | Before outreach, call prep |
| Tech Stack Discovery | Software + integrations | Lead qualification |
| Competitive Intel | Market position, pricing | Deal strategy |
| Leadership Research | Key contacts, changes | Targeting, timing |
| Industry Analysis | Trends, challenges | ICP refinement |

## Company Profile Framework

```python
company_profile = {
    # Basics
    'name': str,
    'website': str,
    'industry': str,
    'employee_count': int,
    'revenue_estimate': str,  # "$5-10M", "$10-50M"
    
    # Operations
    'field_vs_office': {'field': int, 'office': int},
    'service_area': list[str],  # States/regions
    'trades': list[str],  # Electrical, HVAC, Plumbing
    
    # Technology
    'software_stack': {
        'crm': str,
        'project_mgmt': str,
        'accounting': str,
        'field_service': str,
        'other': list[str]
    },
    
    # Sales Intel
    'pain_signals': list[str],
    'growth_indicators': list[str],
    'failed_implementations': list[str],
    'decision_makers': list[dict]
}
```

## Tech Stack Discovery

**Common MEP+E Software:**

| Category | Enterprise | Mid-Market | SMB |
|----------|-----------|------------|-----|
| Project Mgmt | Procore, Autodesk | Buildertrend, CoConstruct | Jobber, Housecall |
| Field Service | ServiceTitan | ServiceMax, FieldEdge | Housecall Pro |
| Accounting | Sage, Viewpoint | QuickBooks Enterprise | QuickBooks Online |
| CRM | Salesforce | HubSpot | Spreadsheets |

**Discovery Questions:**
1. What shows on their job postings? (Indeed, LinkedIn)
2. What integrations do they advertise?
3. What's mentioned in reviews? (Glassdoor, Google)
4. What does their tech team use? (GitHub, StackShare)

## Pain Signal Detection

| Signal | Indicates | Priority |
|--------|-----------|----------|
| Multiple systems mentioned | Integration pain | HIGH |
| "Growing fast" in news | Scaling challenges | HIGH |
| Recent leadership change | Open to new vendors | MEDIUM |
| Hiring ops/admin roles | Process problems | MEDIUM |
| Bad software reviews | Ready to switch | HIGH |
| No online presence | Not tech-savvy | LOW |

## Competitive Positioning

When researching competitors for a prospect:

```
1. What are they using now?
2. How long have they used it?
3. What's broken? (Check reviews, Reddit, forums)
4. What would make them switch?
5. Who else are they evaluating?
```

## Research Workflow

```
Step 1: Basic Discovery
└── Website, LinkedIn, Google News, Glassdoor

Step 2: Tech Stack
└── Job postings, integrations page, case studies

Step 3: Pain Signals
└── Reviews, social mentions, forum posts

Step 4: Decision Makers
└── LinkedIn Sales Nav, company about page

Step 5: Synthesize
└── Generate company profile, score against ICP
```

## Integration Notes

- **Feeds into:** dealer-scraper (enrichment), sales-agent (qualification)
- **Data sources:** LinkedIn, Glassdoor, Indeed, G2, Capterra, Google
- **Pairs with:** sales-outreach-skill (messaging), opportunity-evaluator-skill (deals)

## Reference Files

- `reference/company-profile-template.md` - Full template with examples
- `reference/tech-stack-discovery.md` - Deep dive on software detection
- `reference/mep-contractor-icp.md` - Coperniq-specific ICP criteria
- `reference/competitive-analysis.md` - Competitor research framework
