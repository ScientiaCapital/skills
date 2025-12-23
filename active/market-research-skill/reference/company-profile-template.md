# Company Profile Template

## Basic Information

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

## Operations Profile

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

## Technology Stack

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

## Pain Points & Signals

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

## Decision Makers

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

## Sales Intelligence

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

## Research Sources

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

## Example: Completed Profile

```yaml
company:
  name: "Valley Electric Services"
  website: "valleyelectric.com"
  linkedin: "linkedin.com/company/valley-electric-services"
  founded: "2008"
  headquarters: "Phoenix, AZ"
  
industry:
  primary: "Electrical Contractor"
  secondary: ["Low Voltage", "Solar"]
  
size:
  employees_total: 85
  employees_field: 65
  employees_office: 20
  trucks_vehicles: 40
  revenue_estimate: "$15-20M"
  growth_stage: "growth"
  
software:
  crm:
    name: "HubSpot"
    satisfaction: "neutral"
    years_using: 2
  project_management:
    name: "Buildertrend"
    satisfaction: "frustrated"
    years_using: 3
  accounting:
    name: "QuickBooks Enterprise"
    satisfaction: "happy"
    years_using: 8
  field_service:
    name: "None - using spreadsheets"
    satisfaction: "frustrated"
    
pain_points:
  operational:
    - description: "Dispatching 40 trucks with spreadsheets"
      severity: "high"
      evidence: "Glassdoor review mentioned 'chaos every morning'"
  technology:
    - description: "Buildertrend doesn't handle service calls"
      severity: "high"
      evidence: "Indeed posting mentions 'multiple systems'"
      
decision_makers:
  - name: "Mike Chen"
    title: "Operations Director"
    role_in_decision: "champion"
    notes: "Former ServiceTitan user, knows what good looks like"
    
sales_intel:
  icp_fit_score: 85
  tier: "GOLD"
  timing_signals:
    - signal: "Hiring dispatcher and 2 PMs"
      implication: "Scaling, need better systems"
```
