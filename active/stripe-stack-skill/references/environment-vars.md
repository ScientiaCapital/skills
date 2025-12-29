# Environment Variables Reference

## Standard Variables

### Required (All Projects)

```bash
# Server-side Stripe API key (NEVER expose to client)
STRIPE_SECRET_KEY=sk_test_51RsY6U...

# Webhook signing secret (from Stripe Dashboard)
STRIPE_WEBHOOK_SECRET=whsec_...

# Client-side publishable key (safe to expose)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51RsY6U...
```

### Optional (Price IDs)

```bash
# Use env vars for easy test→live switching
STRIPE_PRICE_STARTER_MONTHLY=price_1ABC...
STRIPE_PRICE_STARTER_ANNUAL=price_1DEF...
STRIPE_PRICE_PRO_MONTHLY=price_1GHI...
STRIPE_PRICE_PRO_ANNUAL=price_1JKL...
STRIPE_PRICE_BUSINESS_MONTHLY=price_1MNO...

# Credit packs
STRIPE_PRICE_CREDIT_100=price_1PQR...
STRIPE_PRICE_CREDIT_250=price_1STU...
```

---

## Test vs Live Keys

| Environment | Secret Key Prefix | Publishable Prefix | Webhook Prefix |
|-------------|-------------------|--------------------| ---------------|
| Test | `sk_test_` | `pk_test_` | `whsec_` (from test endpoint) |
| Live | `sk_live_` | `pk_live_` | `whsec_` (from live endpoint) |

**Note:** Webhook secrets don't have `test_` or `live_` prefixes - they're tied to the endpoint which is mode-specific.

---

## Getting Your Keys

### API Keys
1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Make sure correct mode is selected (Test/Live toggle)
3. Developers → API keys
4. Copy Secret key and Publishable key

### Webhook Secret
1. Developers → Webhooks
2. Click your endpoint (or create one)
3. Click "Reveal" under Signing secret
4. Copy the `whsec_...` value

---

## Local Development

### .env.local (Never commit!)
```bash
# .env.local
STRIPE_SECRET_KEY=sk_test_51RsY6UCI542nEcDo...
STRIPE_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51RsY6UCI542nEcDo...

# For local webhook testing with Stripe CLI
# Override with CLI-provided secret:
# STRIPE_WEBHOOK_SECRET=whsec_xxx (from `stripe listen`)
```

### .env.example (Commit this)
```bash
# .env.example
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here

# Optional price IDs
STRIPE_PRICE_STARTER_MONTHLY=
STRIPE_PRICE_PRO_MONTHLY=
```

---

## Vercel Configuration

### Via Dashboard
1. Project → Settings → Environment Variables
2. Add each variable
3. Select environments (Production, Preview, Development)

### Via CLI
```bash
# Add variable
echo "sk_live_..." | vercel env add STRIPE_SECRET_KEY production

# List variables
vercel env ls production

# Remove variable
vercel env rm STRIPE_SECRET_KEY production
```

---

## Code Patterns

### Accessing Keys
```typescript
// Server-side only
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-12-15.clover',
});

// Client-side (Next.js)
const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);
```

### Validation at Startup
```typescript
export function getStripe(): Stripe {
  const key = process.env.STRIPE_SECRET_KEY;

  if (!key) {
    throw new Error('STRIPE_SECRET_KEY is not configured');
  }

  if (!key.startsWith('sk_')) {
    throw new Error('Invalid STRIPE_SECRET_KEY format');
  }

  return new Stripe(key, { apiVersion: '2025-12-15.clover' });
}
```

### Price ID with Fallback
```typescript
const PLANS = {
  pro: {
    priceId: process.env.STRIPE_PRICE_PRO_MONTHLY || 'price_test_fallback',
  },
};

// Stricter: fail in production if not set
function getPriceId(key: string): string {
  const priceId = process.env[key];

  if (!priceId && process.env.NODE_ENV === 'production') {
    throw new Error(`Missing required env var: ${key}`);
  }

  return priceId || 'price_test_fallback';
}
```

---

## Shared Account Pattern

All NetZero Suite projects share ONE Stripe account:

```bash
# Same keys across all projects:
# - netzero-bot
# - solarappraisal-ai
# - fieldvault-ai
# - solarvoice-ai

STRIPE_SECRET_KEY=sk_test_51RsY6UCI542nEcDo...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51RsY6UCI542nEcDo...

# DIFFERENT webhook secrets per project (each has own endpoint)
# netzero-bot
STRIPE_WEBHOOK_SECRET=whsec_abc...

# solarappraisal-ai
STRIPE_WEBHOOK_SECRET=whsec_def...
```

---

## Security Checklist

- [ ] Never commit `.env.local` to git
- [ ] Add `.env.local` to `.gitignore`
- [ ] Use `NEXT_PUBLIC_` prefix ONLY for client-safe vars
- [ ] Verify webhook secret matches endpoint mode (test/live)
- [ ] Rotate keys if exposed
- [ ] Use different webhook secrets per project
