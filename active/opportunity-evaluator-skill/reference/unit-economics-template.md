# Unit Economics Template

## Quick Viability Check

Before deep analysis, answer:

```markdown
## 5-Minute Viability Test

1. How much will one customer pay? $____/month
2. How many customers can I realistically get in 6 months? ____
3. What does it cost to serve one customer? $____/month
4. How many hours/week will this take me? ____

Quick math:
- Monthly revenue (6 months): #2 × #1 = $____
- Monthly costs: #2 × #3 = $____
- Monthly margin: Revenue - Costs = $____
- Hourly rate equivalent: Margin ÷ (hours × 4) = $____/hr

Is hourly rate > $100? 
[ ] Yes → Continue analysis
[ ] No → Needs rethink
```

---

## Revenue Model Analysis

### Model 1: Subscription (SaaS/MRR)

```yaml
subscription_economics:
  pricing:
    tier_1:
      name: "Starter"
      price_monthly: 0
      price_annual: 0
      features: []
      target: ""
      
    tier_2:
      name: "Pro"
      price_monthly: 0
      price_annual: 0
      features: []
      target: ""
      
    tier_3:
      name: "Enterprise"
      price_monthly: 0
      price_annual: 0
      features: []
      target: ""
      
  metrics:
    arpu: 0  # Average Revenue Per User
    conversion_free_to_paid: 0.0  # %
    monthly_churn: 0.0  # %
    expansion_rate: 0.0  # % revenue expansion from existing
    
  projections:
    month_1:
      users: 0
      paying: 0
      mrr: 0
    month_6:
      users: 0
      paying: 0
      mrr: 0
    month_12:
      users: 0
      paying: 0
      mrr: 0
```

**Key formulas:**
```python
# Customer Lifetime Value
LTV = ARPU / monthly_churn

# Months to recover CAC
payback_months = CAC / ARPU

# Net Revenue Retention
NRR = (starting_mrr + expansion - contraction - churn) / starting_mrr
```

### Model 2: Consulting / Services

```yaml
consulting_economics:
  rates:
    hourly: 0
    daily: 0
    project_minimum: 0
    retainer_monthly: 0
    
  utilization:
    billable_hours_per_week: 0  # realistic
    weeks_per_year: 48  # accounting for time off
    
  capacity:
    max_active_clients: 0
    hours_per_client_monthly: 0
    
  revenue_potential:
    monthly: 0  # hours × rate
    annual: 0
    
  costs:
    tools_monthly: 0
    insurance: 0
    admin_time_value: 0  # non-billable hours
```

**Key formulas:**
```python
# Effective hourly rate
effective_rate = total_revenue / total_hours_worked  # includes non-billable

# Monthly capacity
monthly_capacity = billable_hours_per_week * 4.33

# Break-even clients
break_even_clients = fixed_costs / (avg_client_revenue - variable_cost_per_client)
```

### Model 3: Marketplace / Transaction Fee

```yaml
marketplace_economics:
  transaction_model:
    take_rate: 0.0  # % of GMV
    minimum_fee: 0
    
  volume_projections:
    transactions_month_1: 0
    avg_transaction_value: 0
    gmv_month_1: 0
    revenue_month_1: 0  # GMV × take_rate
    
  growth:
    monthly_transaction_growth: 0.0  # %
    
  costs:
    payment_processing: 0.029  # typical 2.9%
    hosting_per_transaction: 0
    support_per_transaction: 0
```

### Model 4: Productized Service

```yaml
productized_service:
  offering:
    name: ""
    description: ""
    price: 0
    delivery_time: ""
    
  capacity:
    max_per_month: 0
    hours_per_delivery: 0
    
  economics:
    monthly_revenue_max: 0  # max × price
    monthly_hours_max: 0  # max × hours
    effective_hourly: 0  # revenue / hours
    
  scaling:
    can_delegate: bool
    delegation_cost: 0
    margin_after_delegation: 0
```

---

## Cost Structure Analysis

### Fixed Costs

```yaml
fixed_costs_monthly:
  infrastructure:
    hosting: 0  # Vercel, RunPod, etc.
    database: 0  # Supabase
    domains: 0
    
  tools:
    development: 0  # Cursor, GitHub, etc.
    marketing: 0
    operations: 0
    
  services:
    accounting: 0
    legal: 0
    insurance: 0
    
  total_fixed: 0
```

### Variable Costs

```yaml
variable_costs_per_unit:
  api_costs:
    llm_per_request: 0  # Average LLM cost
    other_apis: 0
    
  payment_processing: 0.029  # 2.9% + $0.30 typical
  
  support:
    time_per_customer_monthly: 0  # hours
    cost_per_hour: 0
    
  infrastructure_scaling:
    cost_per_1000_users: 0
    
  total_variable_per_unit: 0
```

### Time Investment (Opportunity Cost)

```yaml
time_investment:
  development:
    initial_build_hours: 0
    ongoing_maintenance_hours_monthly: 0
    
  sales_marketing:
    hours_per_customer_acquisition: 0
    ongoing_marketing_hours_monthly: 0
    
  support:
    hours_per_customer_monthly: 0
    
  operations:
    admin_hours_monthly: 0
    
  total_monthly_hours: 0
  
  # Opportunity cost calculation
  alternative_hourly_rate: 150  # What else could I earn?
  monthly_opportunity_cost: 0  # hours × rate
```

---

## Scenario Analysis

### Conservative Case

```yaml
conservative:
  assumptions:
    customer_acquisition: "50% of plan"
    churn: "2x expected"
    price: "starting tier only"
    
  month_6:
    customers: 0
    mrr: 0
    costs: 0
    net: 0
    
  month_12:
    customers: 0
    mrr: 0
    costs: 0
    net: 0
    
  viable: bool
```

### Base Case

```yaml
base:
  assumptions:
    customer_acquisition: "as planned"
    churn: "as expected"
    price: "tier mix as expected"
    
  month_6:
    customers: 0
    mrr: 0
    costs: 0
    net: 0
    
  month_12:
    customers: 0
    mrr: 0
    costs: 0
    net: 0
    
  viable: bool
```

### Optimistic Case

```yaml
optimistic:
  assumptions:
    customer_acquisition: "150% of plan"
    churn: "50% of expected"
    price: "upgrades above plan"
    
  month_6:
    customers: 0
    mrr: 0
    costs: 0
    net: 0
    
  month_12:
    customers: 0
    mrr: 0
    costs: 0
    net: 0
    
  viable: bool
```

---

## Key Metrics Dashboard

### SaaS Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| MRR | | | |
| MRR Growth | >10%/mo | | |
| Churn Rate | <5%/mo | | |
| LTV | >3x CAC | | |
| CAC Payback | <12 mo | | |
| NRR | >100% | | |

### Services Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Monthly Revenue | | | |
| Utilization | >70% | | |
| Effective Rate | >$100/hr | | |
| Client Retention | >80% | | |
| Profit Margin | >40% | | |

### Marketplace Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| GMV | | | |
| Take Rate | | | |
| Net Revenue | | | |
| Transaction Volume | | | |
| Repeat Rate | | | |

---

## Break-Even Analysis

```python
def calculate_break_even(
    fixed_costs: float,
    price_per_unit: float,
    variable_cost_per_unit: float
) -> dict:
    """
    Calculate break-even point
    """
    contribution_margin = price_per_unit - variable_cost_per_unit
    break_even_units = fixed_costs / contribution_margin
    
    return {
        'contribution_margin': contribution_margin,
        'break_even_units': break_even_units,
        'break_even_revenue': break_even_units * price_per_unit
    }

# Example
result = calculate_break_even(
    fixed_costs=500,      # monthly
    price_per_unit=50,    # per customer
    variable_cost_per_unit=5  # API costs, etc.
)
# break_even_units = 500 / (50-5) = 11.1 customers
```

---

## Decision Summary Template

```yaml
unit_economics_summary:
  opportunity: ""
  date: ""
  
  revenue_model: ""
  monthly_revenue_potential: 0
  monthly_costs: 0
  monthly_profit_potential: 0
  
  time_investment: 0  # hours/month
  effective_hourly_rate: 0
  
  break_even:
    units: 0
    months: 0
    
  viability_assessment:
    conservative: ""  # viable, marginal, not viable
    base: ""
    optimistic: ""
    
  key_assumptions:
    - ""
    - ""
    
  biggest_risks:
    - ""
    - ""
    
  recommendation: ""  # proceed, iterate, pass
  
  next_validation_steps:
    - ""
```
