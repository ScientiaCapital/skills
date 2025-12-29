# Common Stripe Errors & Solutions

## Webhook Errors

### 400 "Invalid signature"

**Symptoms:**
- Webhook returns 400
- `Webhook signature verification failed` in logs

**Causes & Solutions:**

1. **Wrong webhook secret**
   ```bash
   # Check you're using the right secret for the endpoint
   # Test endpoint → test secret
   # Live endpoint → live secret
   ```

2. **Using request.json() instead of request.text()**
   ```typescript
   // Wrong
   const body = await request.json();

   // Correct
   const body = await request.text();
   ```

3. **Body modified before verification**
   ```typescript
   // Don't parse or modify body before constructEvent
   const body = await request.text();
   const event = stripe.webhooks.constructEvent(body, sig, secret);
   ```

4. **Stripe CLI secret mismatch**
   ```bash
   # When using `stripe listen`, use the CLI-provided secret
   stripe listen --forward-to localhost:3000/api/stripe/webhook
   # Copy the whsec_xxx from output, use in .env.local
   ```

---

### Duplicate Event Processing

**Symptoms:**
- Same action happens twice
- Subscription created multiple times
- Credits added twice

**Causes & Solutions:**

1. **Using in-memory idempotency**
   ```typescript
   // Wrong: Lost on serverless cold start
   const processed = new Set<string>();

   // Correct: Database-backed
   const { data } = await supabase
     .from('stripe_webhook_events')
     .select('id')
     .eq('id', event.id)
     .single();
   ```

2. **Inserting after processing**
   ```typescript
   // Wrong: If processing fails, event won't be recorded
   await processEvent(event);
   await logEvent(event);

   // Correct: Insert before processing
   await logEvent(event);
   await processEvent(event);
   ```

3. **Missing idempotency table**
   ```sql
   -- Create if missing
   CREATE TABLE stripe_webhook_events (
     id TEXT PRIMARY KEY,
     type TEXT NOT NULL,
     data JSONB NOT NULL,
     processed_at TIMESTAMPTZ DEFAULT NOW()
   );
   ```

---

### Webhook Not Firing

**Symptoms:**
- No webhook events in Stripe Dashboard
- Endpoint shows 0 attempts

**Causes & Solutions:**

1. **Endpoint registered in wrong mode**
   - Check: Test mode endpoint won't fire for live transactions
   - Solution: Register endpoint in correct mode

2. **Wrong events selected**
   - Check: Dashboard → Webhooks → Endpoint → Events
   - Verify all needed events are checked

3. **URL not reachable**
   - Check: Endpoint URL is publicly accessible
   - Verify: No auth middleware blocking the route

4. **HTTPS required**
   - Stripe requires HTTPS for production webhooks
   - Local dev: Use Stripe CLI or ngrok

---

## Checkout Errors

### "No such price"

**Symptoms:**
- Checkout fails with "No such price: price_xxx"

**Causes & Solutions:**

1. **Using test price ID with live key**
   ```typescript
   // Wrong: Hardcoded test price
   price: 'price_1ABCtest...'

   // Correct: Environment variable
   price: process.env.STRIPE_PRICE_PRO_MONTHLY
   ```

2. **Product not copied to live mode**
   - Dashboard: Products → [Product] → "Copy to live mode"

3. **Price ID typo**
   - Double-check the exact ID from Dashboard

---

### "Invalid API Key provided"

**Symptoms:**
- All Stripe calls fail with auth error

**Causes & Solutions:**

1. **Key format wrong**
   ```typescript
   // Check key starts with correct prefix
   if (!process.env.STRIPE_SECRET_KEY?.startsWith('sk_')) {
     throw new Error('Invalid key format');
   }
   ```

2. **Using publishable key server-side**
   ```typescript
   // Wrong: pk_ key on server
   new Stripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);

   // Correct: sk_ key on server
   new Stripe(process.env.STRIPE_SECRET_KEY);
   ```

3. **Key expired or revoked**
   - Generate new key in Dashboard → Developers → API keys

---

## Subscription Errors

### User Can't Access Features After Payment

**Symptoms:**
- Payment successful
- User still shows as free tier

**Causes & Solutions:**

1. **Webhook not processing**
   - Check: Stripe Dashboard → Webhooks → Recent events
   - Look for failed deliveries

2. **User ID not in metadata**
   ```typescript
   // Ensure user_id is passed in checkout
   const session = await stripe.checkout.sessions.create({
     metadata: { user_id: userId },
     subscription_data: {
       metadata: { user_id: userId },
     },
   });
   ```

3. **Database update failing silently**
   ```typescript
   const { error } = await supabase.from('subscriptions').upsert(...);
   if (error) console.error('DB update failed:', error);
   ```

---

### Subscription Shows Wrong Status

**Symptoms:**
- User cancelled but still shows active
- Status stuck in past_due

**Causes & Solutions:**

1. **Not handling subscription.updated event**
   ```typescript
   case 'customer.subscription.updated':
     await handleSubscriptionChange(event.data.object);
     break;
   ```

2. **Looking up by wrong ID**
   ```typescript
   // Correct: Use subscription ID, not customer ID
   .eq('stripe_subscription_id', subscription.id)
   ```

---

## Invoice Errors

### Usage Not Resetting Monthly

**Symptoms:**
- Usage counter doesn't reset after renewal

**Causes & Solutions:**

1. **Not handling invoice.paid event**
   ```typescript
   case 'invoice.paid':
     await handleInvoicePaid(event.data.object);
     break;
   ```

2. **Subscription ID extraction failing**
   ```typescript
   // Modern Stripe invoice structure
   const subscriptionId = getSubscriptionId(invoice);
   if (!subscriptionId) {
     console.log('Not a subscription invoice');
     return;
   }
   ```

---

## Type Errors

### "Property 'x' does not exist on type 'never'"

**Symptoms:**
- TypeScript errors on Supabase operations
- Properties showing as `never`

**Causes & Solutions:**

1. **Missing generated types**
   ```bash
   # Regenerate Supabase types
   npx supabase gen types typescript --local > src/types/supabase.ts
   ```

2. **Type assertion workaround**
   ```typescript
   // Temporary fix: Cast to any
   const { data } = await (supabase as any)
     .from('stripe_webhook_events')
     .select('id');
   ```

---

### "current_period_start doesn't exist on Subscription"

**Symptoms:**
- TypeScript error accessing subscription period

**Solution:**
```typescript
// Use type assertion
const subData = subscription as unknown as {
  current_period_start: number;
  current_period_end: number;
  status: string;
};

const periodStart = new Date(subData.current_period_start * 1000);
```

---

## Quick Debug Checklist

1. **Check Stripe Dashboard**
   - Webhooks → Recent events (any failures?)
   - Logs → Recent requests (any errors?)

2. **Check Vercel Logs**
   - Functions → View logs
   - Filter by `/api/stripe/webhook`

3. **Verify Environment**
   ```bash
   # Confirm keys are set
   vercel env ls production | grep STRIPE
   ```

4. **Test Locally**
   ```bash
   stripe listen --forward-to localhost:3000/api/stripe/webhook
   stripe trigger checkout.session.completed
   ```

5. **Check Database**
   ```sql
   SELECT * FROM stripe_webhook_events ORDER BY processed_at DESC LIMIT 10;
   ```
