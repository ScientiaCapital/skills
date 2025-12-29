# Go Live Checklist: Test → Production

## Pre-Flight Checks

### Stripe Account Activation
- [ ] Business verification complete
- [ ] Bank account linked for payouts
- [ ] Identity verification approved
- [ ] Live mode API keys available

### Code Readiness
- [ ] All webhook handlers use database idempotency (NOT in-memory)
- [ ] Price IDs use environment variables (not hardcoded)
- [ ] Error handling returns 200 to prevent Stripe retries
- [ ] Logging captures event IDs for debugging

---

## Step 1: Copy Products to Live Mode

### Option A: Stripe Dashboard (Recommended)
1. Go to Products in TEST mode
2. Click each product
3. Click "Copy to live mode"
4. Repeat for all products

### Option B: Python Script
```python
import stripe

TEST_KEY = "sk_test_..."
LIVE_KEY = "sk_live_..."

def copy_products():
    stripe.api_key = TEST_KEY
    products = stripe.Product.list(limit=100)

    for product in products.auto_paging_iter():
        stripe.api_key = LIVE_KEY
        live_product = stripe.Product.create(
            name=product.name,
            description=product.description,
            metadata=product.metadata,
        )

        stripe.api_key = TEST_KEY
        prices = stripe.Price.list(product=product.id)

        for price in prices.auto_paging_iter():
            stripe.api_key = LIVE_KEY
            stripe.Price.create(
                product=live_product.id,
                unit_amount=price.unit_amount,
                currency=price.currency,
                recurring=price.recurring,
                metadata=price.metadata,
            )
            print(f"Created price for {product.name}")

copy_products()
```

---

## Step 2: Register Live Webhook Endpoints

1. Go to Stripe Dashboard → Developers → Webhooks
2. Click "Add endpoint"
3. Select **Live mode** (important!)
4. Enter production URL:
   ```
   https://your-app.vercel.app/api/stripe/webhook
   ```
5. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
6. Copy the **live** signing secret

---

## Step 3: Update Environment Variables

### Vercel Dashboard
1. Go to Project → Settings → Environment Variables
2. Update for **Production** environment:

| Variable | Test Value | Live Value |
|----------|------------|------------|
| `STRIPE_SECRET_KEY` | `sk_test_...` | `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_test_...` | `whsec_live_...` |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_test_...` | `pk_live_...` |

3. If using price ID env vars, update those too:
   - `STRIPE_PRICE_STARTER_MONTHLY`
   - `STRIPE_PRICE_PRO_MONTHLY`
   - etc.

### CLI Alternative
```bash
vercel env rm STRIPE_SECRET_KEY production
echo "sk_live_..." | vercel env add STRIPE_SECRET_KEY production
```

---

## Step 4: Deploy

```bash
vercel --prod
```

Or push to main branch if auto-deploy is configured.

---

## Step 5: Verify Live Integration

### Test Real Payment
1. Go to your live pricing page
2. Select cheapest plan
3. Use a **real** credit card (yours)
4. Complete checkout
5. Verify:
   - [ ] Webhook received in Stripe Dashboard → Webhooks → Recent events
   - [ ] User record created in database
   - [ ] Subscription active

### Refund Test Charge
1. Go to Stripe Dashboard → Payments
2. Find your test payment
3. Click "Refund"
4. Full refund

---

## Post-Launch Monitoring

### First 24 Hours
- [ ] Monitor Stripe Dashboard → Webhooks for failures
- [ ] Check Vercel logs for webhook handler errors
- [ ] Verify new signups create proper records

### First Week
- [ ] Review failed webhook attempts
- [ ] Check for duplicate event handling
- [ ] Verify invoice.paid resets usage counters

### Ongoing
- [ ] Set up Stripe email notifications for failed payments
- [ ] Configure retry policy for failed webhooks
- [ ] Monitor for unusual patterns (potential fraud)

---

## Rollback Plan

If issues arise:

1. **Quick fix**: Switch back to test keys in Vercel
2. **Pause signups**: Temporarily disable checkout button
3. **Debug**: Check Stripe Dashboard webhooks + Vercel logs

---

## Common Go-Live Issues

### "No such price" Error
- Forgot to copy products to live mode
- Using test price IDs with live keys

### Webhooks Not Firing
- Registered for test mode instead of live
- Wrong webhook URL

### 400 Signature Errors
- Using test webhook secret with live endpoint
- Cached old secret in Vercel

### Duplicate Events
- In-memory idempotency reset on cold start
- Database table not created in production

---

## Security Checklist

- [ ] No test card numbers in codebase
- [ ] No hardcoded API keys
- [ ] Webhook secret not logged
- [ ] HTTPS only for webhook endpoints
- [ ] RLS enabled on subscription tables
