# Webhook Patterns Reference

## Core Principle: Idempotency

Stripe may send the same event multiple times due to:
- Network issues
- Retry logic
- Dashboard "resend" feature

**NEVER** process the same event twice.

### Database Idempotency (Required)

```typescript
// Check BEFORE processing
const { data: existing } = await supabase
  .from('stripe_webhook_events')
  .select('id')
  .eq('id', event.id)
  .single();

if (existing) {
  return NextResponse.json({ duplicate: true });
}

// Insert BEFORE processing (not after)
await supabase.from('stripe_webhook_events').insert({
  id: event.id,
  type: event.type,
  data: event,
});

// Now process...
```

### Why Insert Before Processing?

If processing fails and you insert after:
1. Event processes partially
2. Crash before insert
3. Stripe retries
4. Event processes again → **duplicate action**

If you insert before:
1. Event logged
2. Processing starts
3. Crash mid-process
4. Stripe retries
5. Duplicate detected → **safe skip**
6. Manual investigation via stored payload

---

## Event Handler Structure

```typescript
export async function POST(request: NextRequest) {
  // 1. Get raw body (required for signature)
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  // 2. Verify signature
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, signature!, webhookSecret);
  } catch (err) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  // 3. Idempotency check (see above)

  // 4. Route to handler
  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckout(event.data.object);
        break;
      // ... more handlers
    }
    return NextResponse.json({ received: true });
  } catch (error) {
    // 5. Log but still return 200 to prevent infinite retries
    console.error('Handler error:', error);
    return NextResponse.json({ error: 'Handler failed' }, { status: 500 });
  }
}
```

---

## Common Events and Actions

| Event | When | Action |
|-------|------|--------|
| `checkout.session.completed` | Customer completes payment | Create subscription/credit record |
| `customer.subscription.created` | New subscription | Initialize user limits |
| `customer.subscription.updated` | Plan change, status change | Sync plan and limits |
| `customer.subscription.deleted` | Cancellation | Downgrade to free |
| `invoice.paid` | Monthly renewal | Reset usage counters |
| `invoice.payment_failed` | Card declined | Mark past_due, notify user |

---

## Extracting Subscription ID from Invoice

Invoice structure changed in recent Stripe versions:

```typescript
// Modern approach (handles both old and new structure)
function getSubscriptionId(invoice: Stripe.Invoice): string | undefined {
  // Try new structure first
  const invoiceAny = invoice as Record<string, any>;
  const parent = invoiceAny.parent;
  const subDetails = parent?.subscription_details;

  if (subDetails?.subscription) {
    const sub = subDetails.subscription;
    return typeof sub === 'string' ? sub : sub?.id;
  }

  // Fallback to line items
  const lineSub = invoice.lines?.data?.[0]?.subscription;
  return typeof lineSub === 'string' ? lineSub : undefined;
}
```

---

## Getting Subscription Period Dates

Stripe SDK types don't always include period fields:

```typescript
// Type assertion for period access
const subscription = await stripe.subscriptions.retrieve(subscriptionId);
const subData = subscription as unknown as {
  current_period_start: number;
  current_period_end: number;
  status: string;
};

const periodStart = new Date(subData.current_period_start * 1000);
const periodEnd = new Date(subData.current_period_end * 1000);
```

---

## Error Handling Best Practices

### Return 200 Even on Errors

```typescript
} catch (error) {
  console.error('Handler error:', error);
  // Return 500 to indicate failure, but Stripe will retry
  // Consider: return 200 to prevent retries if you've logged the event
  return NextResponse.json({ error: 'Failed' }, { status: 500 });
}
```

### Log Event ID for Debugging

```typescript
console.log(`[Stripe] Processing ${event.type} (${event.id})`);
```

### Store Error in Database

```typescript
await supabase
  .from('stripe_webhook_events')
  .update({ error: String(error), processed_at: null })
  .eq('id', event.id);
```

---

## Testing Webhooks Locally

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward to local server
stripe listen --forward-to localhost:3000/api/stripe/webhook

# Trigger specific events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.paid
```

---

## Webhook Endpoint Configuration

### Vercel Route Config

```typescript
// At top of route.ts
export const runtime = 'nodejs';
export const maxDuration = 30; // seconds
export const dynamic = 'force-dynamic';
```

### Events to Subscribe

Minimum set for subscriptions:
- `checkout.session.completed`
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.paid`
- `invoice.payment_failed`

Optional:
- `customer.created` (for early customer tracking)
- `payment_intent.succeeded` (for one-time payments)
- `charge.refunded` (for refund handling)
