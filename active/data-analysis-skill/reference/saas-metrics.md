# SaaS Metrics Reference

Complete definitions and calculations for investor reporting.

## Revenue Metrics

### MRR (Monthly Recurring Revenue)

```python
def calculate_mrr(df: pd.DataFrame) -> float:
    """
    MRR = Sum of all active subscription values for the month.

    Best practice: Calculate as of month-end snapshot.
    """
    active = df[df['status'] == 'active']
    return active['monthly_value'].sum()
```

**MRR Components:**
- **New MRR**: Revenue from new customers
- **Expansion MRR**: Upsells and cross-sells
- **Contraction MRR**: Downgrades
- **Churn MRR**: Lost revenue from cancellations

```python
def mrr_waterfall(df: pd.DataFrame, prior_period: str, current_period: str) -> dict:
    """Calculate MRR movement components."""
    prior = df[df['period'] == prior_period]
    current = df[df['period'] == current_period]

    prior_customers = set(prior['customer_id'])
    current_customers = set(current['customer_id'])

    new_customers = current_customers - prior_customers
    churned_customers = prior_customers - current_customers
    continuing = prior_customers & current_customers

    return {
        'starting_mrr': prior['mrr'].sum(),
        'new_mrr': current[current['customer_id'].isin(new_customers)]['mrr'].sum(),
        'expansion_mrr': sum(
            max(0, current[current['customer_id'] == c]['mrr'].sum() -
                prior[prior['customer_id'] == c]['mrr'].sum())
            for c in continuing
        ),
        'contraction_mrr': sum(
            min(0, current[current['customer_id'] == c]['mrr'].sum() -
                prior[prior['customer_id'] == c]['mrr'].sum())
            for c in continuing
        ),
        'churn_mrr': -prior[prior['customer_id'].isin(churned_customers)]['mrr'].sum(),
        'ending_mrr': current['mrr'].sum(),
    }
```

### ARR (Annual Recurring Revenue)

```python
def calculate_arr(mrr: float) -> float:
    """ARR = MRR × 12"""
    return mrr * 12
```

**ARR Growth Rate:**
```python
def arr_growth_rate(current_arr: float, prior_arr: float) -> float:
    """YoY ARR growth."""
    return (current_arr - prior_arr) / prior_arr if prior_arr > 0 else 0
```

**Benchmarks (Series A):**
- $1.5M-$3M ARR baseline
- 100%+ YoY growth
- Path to $10M ARR in 18-24 months

## Unit Economics

### CAC (Customer Acquisition Cost)

```python
def calculate_cac(
    sales_cost: float,
    marketing_cost: float,
    new_customers: int,
    period: str = 'quarter'
) -> float:
    """
    CAC = (Sales + Marketing Cost) / New Customers Acquired

    Include:
    - Sales team salaries + commissions
    - Marketing spend (ads, content, events)
    - SDR/BDR costs
    - Sales tools and software

    Exclude:
    - Customer success (goes into LTV)
    - Product costs
    - G&A
    """
    total_cost = sales_cost + marketing_cost
    return total_cost / new_customers if new_customers > 0 else 0
```

**CAC by Channel:**
```python
def cac_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate CAC for each acquisition channel."""
    return df.groupby('channel').apply(
        lambda x: x['spend'].sum() / x['new_customers'].sum()
    ).reset_index(name='cac')
```

### LTV (Customer Lifetime Value)

```python
def calculate_ltv(
    arpu: float,
    gross_margin: float,
    churn_rate: float
) -> float:
    """
    LTV = (ARPU × Gross Margin) / Churn Rate

    Or simplified:
    LTV = ARPU × Average Customer Lifespan
    """
    if churn_rate <= 0:
        churn_rate = 0.01  # Cap at 100 months
    return (arpu * gross_margin) / churn_rate
```

**LTV Components:**
```python
def ltv_components(df: pd.DataFrame) -> dict:
    """Break down LTV calculation."""
    # Average Revenue Per User (monthly)
    arpu = df.groupby('customer_id')['mrr'].mean().mean()

    # Gross Margin (revenue - COGS)
    gross_margin = (df['revenue'].sum() - df['cogs'].sum()) / df['revenue'].sum()

    # Monthly churn rate
    churn_rate = df[df['churned']]['customer_id'].nunique() / df['customer_id'].nunique()

    # Average lifespan (months)
    avg_lifespan = 1 / churn_rate if churn_rate > 0 else 36

    ltv = arpu * gross_margin * avg_lifespan

    return {
        'arpu': arpu,
        'gross_margin': gross_margin,
        'churn_rate': churn_rate,
        'avg_lifespan_months': avg_lifespan,
        'ltv': ltv,
    }
```

### LTV:CAC Ratio

```python
def ltv_cac_ratio(ltv: float, cac: float) -> float:
    """
    LTV:CAC Ratio

    Benchmarks:
    - < 1:1 = Losing money on every customer
    - 1-3:1 = Inefficient growth
    - 3:1 = Healthy (industry standard)
    - 4:1+ = Best-in-class
    - > 5:1 = May be under-investing in growth
    """
    return ltv / cac if cac > 0 else 0
```

### CAC Payback Period

```python
def cac_payback_months(cac: float, arpu: float, gross_margin: float) -> float:
    """
    CAC Payback = CAC / (ARPU × Gross Margin)

    Benchmarks:
    - < 12 months = Best-in-class
    - 12-18 months = Healthy
    - 18-24 months = Acceptable for enterprise
    - > 24 months = Concerning
    """
    monthly_contribution = arpu * gross_margin
    return cac / monthly_contribution if monthly_contribution > 0 else float('inf')
```

## Retention Metrics

### Logo Churn (Customer Churn)

```python
def logo_churn_rate(
    churned_customers: int,
    starting_customers: int,
    period: str = 'month'
) -> float:
    """
    Logo Churn = Customers Lost / Starting Customers

    Benchmarks (monthly):
    - < 2% = Excellent
    - 2-5% = Good
    - 5-7% = Needs attention
    - > 7% = Critical issue
    """
    return churned_customers / starting_customers if starting_customers > 0 else 0
```

### Revenue Churn (Gross)

```python
def gross_revenue_churn(
    churned_mrr: float,
    contraction_mrr: float,
    starting_mrr: float
) -> float:
    """
    Gross Revenue Churn = (Churn + Contraction) / Starting MRR

    Only counts lost revenue, not expansion.
    """
    lost = churned_mrr + abs(contraction_mrr)
    return lost / starting_mrr if starting_mrr > 0 else 0
```

### Net Revenue Retention (NRR)

```python
def net_revenue_retention(
    starting_mrr: float,
    expansion_mrr: float,
    contraction_mrr: float,
    churn_mrr: float
) -> float:
    """
    NRR = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR

    Measures revenue from existing customers only.

    Benchmarks:
    - < 100% = Net churn (shrinking cohorts)
    - 100-110% = Good
    - 110-130% = Excellent
    - > 130% = Best-in-class (Snowflake territory)
    """
    ending = starting_mrr + expansion_mrr - abs(contraction_mrr) - abs(churn_mrr)
    return ending / starting_mrr if starting_mrr > 0 else 0
```

## Growth Efficiency

### Magic Number

```python
def magic_number(
    current_quarter_arr: float,
    prior_quarter_arr: float,
    prior_quarter_sales_marketing: float
) -> float:
    """
    Magic Number = Net New ARR / Prior Quarter S&M Spend

    Measures sales efficiency.

    Benchmarks:
    - < 0.5 = Inefficient
    - 0.5-0.75 = Okay
    - 0.75-1.0 = Good
    - > 1.0 = Excellent
    """
    net_new_arr = current_quarter_arr - prior_quarter_arr
    return net_new_arr / prior_quarter_sales_marketing if prior_quarter_sales_marketing > 0 else 0
```

### Burn Multiple

```python
def burn_multiple(
    net_burn: float,
    net_new_arr: float
) -> float:
    """
    Burn Multiple = Net Burn / Net New ARR

    How much cash burned for each dollar of ARR added.

    Benchmarks:
    - < 1x = Amazing (profitable growth)
    - 1-1.5x = Great
    - 1.5-2x = Good
    - 2-3x = Concerning
    - > 3x = Inefficient
    """
    return abs(net_burn) / net_new_arr if net_new_arr > 0 else float('inf')
```

### Rule of 40

```python
def rule_of_40(revenue_growth_rate: float, profit_margin: float) -> float:
    """
    Rule of 40 = Revenue Growth % + Profit Margin %

    Balances growth and profitability.

    Benchmarks:
    - < 20% = Needs improvement
    - 20-40% = Acceptable
    - 40%+ = Healthy
    - 60%+ = Elite
    """
    return (revenue_growth_rate * 100) + (profit_margin * 100)
```

## Cohort Analysis

### Retention Matrix

```python
def build_cohort_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build customer retention cohort matrix.

    df columns: customer_id, signup_date, activity_date, revenue
    """
    # Assign cohort month
    df['cohort'] = df.groupby('customer_id')['signup_date'].transform('min').dt.to_period('M')

    # Calculate cohort age
    df['activity_month'] = df['activity_date'].dt.to_period('M')
    df['cohort_age'] = (df['activity_month'] - df['cohort']).apply(lambda x: x.n)

    # Aggregate
    cohort_data = df.groupby(['cohort', 'cohort_age']).agg({
        'customer_id': 'nunique',
        'revenue': 'sum'
    }).reset_index()

    # Pivot to matrix
    retention_matrix = cohort_data.pivot(
        index='cohort',
        columns='cohort_age',
        values='customer_id'
    )

    # Convert to percentage
    cohort_sizes = retention_matrix.iloc[:, 0]
    retention_pct = retention_matrix.divide(cohort_sizes, axis=0) * 100

    return retention_pct
```

### Revenue Cohort

```python
def build_revenue_cohort(df: pd.DataFrame) -> pd.DataFrame:
    """Build revenue retention by cohort (for NRR analysis)."""
    df['cohort'] = df.groupby('customer_id')['signup_date'].transform('min').dt.to_period('M')
    df['activity_month'] = df['activity_date'].dt.to_period('M')
    df['cohort_age'] = (df['activity_month'] - df['cohort']).apply(lambda x: x.n)

    # Sum revenue by cohort and age
    revenue_matrix = df.pivot_table(
        index='cohort',
        columns='cohort_age',
        values='revenue',
        aggfunc='sum'
    )

    # Normalize to month 0
    month_0_revenue = revenue_matrix.iloc[:, 0]
    revenue_pct = revenue_matrix.divide(month_0_revenue, axis=0) * 100

    return revenue_pct
```

## Quick Reference Table

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| MRR | Sum of active subscriptions | - |
| ARR | MRR × 12 | $1.5-3M for Series A |
| CAC | (Sales + Marketing) / New Customers | Varies by ACV |
| LTV | (ARPU × Margin) / Churn | - |
| LTV:CAC | LTV / CAC | ≥ 3:1 |
| CAC Payback | CAC / (ARPU × Margin) | < 12 months |
| Logo Churn | Churned / Starting | < 5% monthly |
| NRR | (Start + Exp - Cont - Churn) / Start | > 100% |
| Magic Number | Net New ARR / Prior S&M | > 0.75 |
| Burn Multiple | Net Burn / Net New ARR | < 2x |
| Rule of 40 | Growth % + Margin % | ≥ 40% |
