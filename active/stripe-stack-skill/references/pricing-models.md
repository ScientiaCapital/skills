# Pricing Models Reference

## Three Models

| Model | Best For | Example |
|-------|----------|---------|
| **Subscription Plans** | Predictable usage, feature tiers | SaaS platforms |
| **Credit System** | Variable/expensive operations | AI analysis, reports |
| **Usage-Based** | Metered consumption | API calls, voice minutes |

---

## 1. Subscription Plans

### Structure
```typescript
const PLANS = {
  free: { price: 0, limits: { requests: 3 } },
  starter: { price: 2900, limits: { requests: 50 } },
  pro: { price: 7900, limits: { requests: 500 } },
  business: { price: 19900, limits: { requests: -1 } }, // unlimited
};
```

### Pros
- Predictable revenue
- Simple user experience
- Easy to understand

### Cons
- Users may under/over-utilize
- Hard to price fairly
- Feature gating complexity

### Database Schema
```sql
CREATE TABLE user_subscriptions (
  user_id UUID PRIMARY KEY,
  plan_id TEXT NOT NULL DEFAULT 'free',
  requests_monthly INTEGER DEFAULT 3,
  requests_used INTEGER DEFAULT 0,
  stripe_subscription_id TEXT
);
```

### Reset on Renewal
```typescript
async function handleInvoicePaid(invoice) {
  await supabase
    .from('user_subscriptions')
    .update({ requests_used: 0 })
    .eq('stripe_subscription_id', subscriptionId);
}
```

---

## 2. Credit System (Pay-As-You-Go)

### Structure
```typescript
const CREDIT_PACKS = {
  small: { amount: 2500, credits: 100 },   // $25 = 100 credits
  medium: { amount: 10000, credits: 400 }, // $100 = 400 credits
  large: { amount: 25000, credits: 1000 }, // $250 = 1000 credits
};

const OPERATION_COSTS = {
  basic_analysis: 1,    // $0.25
  detailed_report: 10,  // $2.50
  premium_feature: 50,  // $12.50
};
```

### Pros
- Fair pricing per usage
- No monthly commitment
- Easy to add new features with costs

### Cons
- Unpredictable revenue
- Users may hesitate to use
- Requires balance management

### Database Schema
```sql
CREATE TABLE user_credits (
  user_id UUID PRIMARY KEY,
  balance INTEGER DEFAULT 0,
  stripe_customer_id TEXT
);

CREATE TABLE credit_transactions (
  id UUID PRIMARY KEY,
  user_id UUID,
  amount INTEGER, -- positive = add, negative = deduct
  type TEXT,      -- 'purchase', 'usage', 'refund'
  description TEXT,
  created_at TIMESTAMPTZ
);
```

### Deduction Pattern
```typescript
async function deductCredits(userId, amount, description) {
  const { data } = await supabase
    .from('user_credits')
    .select('balance')
    .eq('user_id', userId)
    .single();

  if (data.balance < amount) {
    throw new Error('Insufficient credits');
  }

  await supabase.rpc('add_credits', {
    p_user_id: userId,
    p_amount: -amount,
    p_type: 'usage',
    p_description: description,
  });
}
```

---

## 3. Usage-Based (Metered Billing)

### Structure
Uses Stripe Billing Meter Events API:

```typescript
// Report usage to Stripe
await stripe.billing.meterEvents.create({
  event_name: 'voice_minutes',
  payload: {
    stripe_customer_id: customerId,
    value: minutesUsed.toString(),
  },
});
```

### Pros
- True pay-per-use
- Scales automatically
- Stripe handles billing

### Cons
- Complex setup
- Harder to predict costs
- Requires usage tracking

### Stripe Setup
1. Create a Billing Meter in Dashboard
2. Create a Price linked to the meter
3. Report usage events via API

---

## Hybrid Model: Subscription + Credits

Combine monthly base with overages:

```typescript
const HYBRID_PLANS = {
  starter: {
    price: 4900, // $49/month base
    includedCredits: 200,
    overageRate: 25, // cents per credit
  },
  pro: {
    price: 14900, // $149/month base
    includedCredits: 750,
    overageRate: 20, // discount for higher tier
  },
};
```

### Monthly Credit Grant
```typescript
async function handleInvoicePaid(invoice) {
  const plan = getPlan(subscriptionPlanId);

  await supabase.rpc('add_credits', {
    p_user_id: userId,
    p_amount: plan.includedCredits,
    p_type: 'subscription_grant',
    p_description: `Monthly ${plan.name} credits`,
  });
}
```

---

## Decision Matrix

| Factor | Plans | Credits | Usage-Based |
|--------|-------|---------|-------------|
| Revenue predictability | High | Low | Medium |
| User cost clarity | High | Medium | Low |
| Setup complexity | Low | Medium | High |
| Fairness | Medium | High | High |
| Best for | Feature tiers | Expensive ops | API/metered |

---

## NetZero Suite Examples

| Project | Model | Reason |
|---------|-------|--------|
| **netzero-bot** | Plans | Feature tiers (quotes/month) |
| **solarappraisal-ai** | Plans | Monthly appraisal limits |
| **fieldvault-ai** | Credits | Expensive VLM operations |
| **solarvoice-ai** | Usage-Based | Voice minutes metered |

---

## Price ID Management

### Use Environment Variables
```typescript
// Good: Env vars for test→live switching
const PLANS = {
  pro: {
    priceId: process.env.STRIPE_PRICE_PRO || 'price_fallback',
  },
};

// Bad: Hardcoded
const PLANS = {
  pro: {
    priceId: 'price_1ABC123',  // Won't work in live mode!
  },
};
```

### Fallback Pattern
```typescript
const priceId = process.env.STRIPE_PRICE_PRO_MONTHLY
  || (process.env.NODE_ENV === 'production'
    ? null  // Fail explicitly in production
    : 'price_test_fallback');
```
