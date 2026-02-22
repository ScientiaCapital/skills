# SaaS Pricing & Checkout Patterns

## 3-Tier Pricing Layout

The proven conversion pattern: Starter (anchor) | **Professional (conversion target)** | Enterprise (custom).

### Pricing Data Structure

```typescript
// lib/pricing.ts
import { z } from "zod"

const planSchema = z.object({
  id: z.enum(["starter", "pro", "enterprise"]),
  name: z.string(),
  description: z.string(),
  monthlyPrice: z.number(),
  annualPrice: z.number(),
  stripePriceId: z.object({
    monthly: z.string(),
    annual: z.string(),
  }),
  features: z.array(z.object({
    name: z.string(),
    included: z.union([z.boolean(), z.literal("coming-soon")]),
    tooltip: z.string().optional(),
  })),
  highlight: z.boolean().default(false),
  cta: z.string(),
})

type Plan = z.infer<typeof planSchema>

export const PLANS: Plan[] = [
  {
    id: "starter",
    name: "Starter",
    description: "For individuals getting started",
    monthlyPrice: 19,
    annualPrice: 15,
    stripePriceId: {
      monthly: process.env.NEXT_PUBLIC_STRIPE_STARTER_MONTHLY!,
      annual: process.env.NEXT_PUBLIC_STRIPE_STARTER_ANNUAL!,
    },
    features: [
      { name: "5 projects", included: true },
      { name: "Basic analytics", included: true },
      { name: "Email support", included: true },
      { name: "API access", included: false },
      { name: "Custom branding", included: false },
      { name: "SSO", included: false },
    ],
    highlight: false,
    cta: "Start free trial",
  },
  {
    id: "pro",
    name: "Professional",
    description: "For growing teams",
    monthlyPrice: 49,
    annualPrice: 39,
    stripePriceId: {
      monthly: process.env.NEXT_PUBLIC_STRIPE_PRO_MONTHLY!,
      annual: process.env.NEXT_PUBLIC_STRIPE_PRO_ANNUAL!,
    },
    features: [
      { name: "Unlimited projects", included: true },
      { name: "Advanced analytics", included: true },
      { name: "Priority support", included: true },
      { name: "API access", included: true },
      { name: "Custom branding", included: "coming-soon", tooltip: "Available Q2 2026" },
      { name: "SSO", included: false },
    ],
    highlight: true,
    cta: "Start free trial",
  },
  {
    id: "enterprise",
    name: "Enterprise",
    description: "For large organizations",
    monthlyPrice: 0,
    annualPrice: 0,
    stripePriceId: { monthly: "", annual: "" },
    features: [
      { name: "Unlimited projects", included: true },
      { name: "Advanced analytics", included: true },
      { name: "Dedicated support", included: true },
      { name: "API access", included: true },
      { name: "Custom branding", included: true },
      { name: "SSO", included: true, tooltip: "SAML, OIDC, Google Workspace" },
    ],
    highlight: false,
    cta: "Contact sales",
  },
]
```

---

## Monthly/Annual Toggle

```tsx
// components/pricing/billing-toggle.tsx
"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"

type BillingInterval = "monthly" | "annual"

function BillingToggle({
  interval,
  onIntervalChange,
}: {
  interval: BillingInterval
  onIntervalChange: (interval: BillingInterval) => void
}) {
  return (
    <div className="flex items-center justify-center gap-3" role="radiogroup" aria-label="Billing interval">
      <button
        role="radio"
        aria-checked={interval === "monthly"}
        onClick={() => onIntervalChange("monthly")}
        className={cn(
          "rounded-full px-4 py-2 text-sm font-medium transition-colors",
          interval === "monthly"
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:text-foreground"
        )}
      >
        Monthly
      </button>
      <button
        role="radio"
        aria-checked={interval === "annual"}
        onClick={() => onIntervalChange("annual")}
        className={cn(
          "rounded-full px-4 py-2 text-sm font-medium transition-colors",
          interval === "annual"
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:text-foreground"
        )}
      >
        Annual
        <span className="ml-2 rounded-full bg-green-100 px-2 py-0.5 text-xs font-semibold text-green-700 dark:bg-green-900 dark:text-green-300">
          Save 20%
        </span>
      </button>
    </div>
  )
}
```

---

## Pricing Cards Grid

```tsx
// components/pricing/pricing-section.tsx
"use client"

import { useState } from "react"
import { PLANS } from "@/lib/pricing"
import { BillingToggle } from "./billing-toggle"
import { PricingCard } from "./pricing-card"

function PricingSection() {
  const [interval, setInterval] = useState<"monthly" | "annual">("annual")

  return (
    <section aria-labelledby="pricing-heading" className="py-24">
      <div className="mx-auto max-w-7xl px-6">
        <div className="text-center">
          <h2 id="pricing-heading" className="text-3xl font-bold tracking-tight sm:text-4xl">
            Simple, transparent pricing
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Start free. Upgrade when you need more.
          </p>
        </div>

        <div className="mt-8 flex justify-center">
          <BillingToggle interval={interval} onIntervalChange={setInterval} />
        </div>

        {/* Stacks vertically on mobile, 3-col on lg */}
        <div className="mt-12 grid grid-cols-1 gap-8 lg:grid-cols-3">
          {PLANS.map((plan) => (
            <PricingCard key={plan.id} plan={plan} interval={interval} />
          ))}
        </div>
      </div>
    </section>
  )
}
```

### Individual Pricing Card

```tsx
// components/pricing/pricing-card.tsx
"use client"

import { CheckIcon, XIcon, ClockIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"
import type { Plan } from "@/lib/pricing"

function PricingCard({
  plan,
  interval,
}: {
  plan: Plan
  interval: "monthly" | "annual"
}) {
  const price = interval === "monthly" ? plan.monthlyPrice : plan.annualPrice
  const isEnterprise = plan.id === "enterprise"

  return (
    <div
      data-slot="pricing-card"
      className={cn(
        "relative flex flex-col rounded-2xl border bg-card p-8",
        plan.highlight && "ring-2 ring-primary shadow-xl scale-105 z-10"
      )}
      aria-label={`${plan.name} plan`}
    >
      {plan.highlight && (
        <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground">
          Most Popular
        </Badge>
      )}

      <div className="mb-6">
        <h3 className="text-lg font-semibold">{plan.name}</h3>
        <p className="mt-1 text-sm text-muted-foreground">{plan.description}</p>
      </div>

      <div className="mb-6" aria-label={isEnterprise ? "Custom pricing" : `$${price} per month`}>
        {isEnterprise ? (
          <span className="text-4xl font-bold">Custom</span>
        ) : (
          <>
            <span className="text-4xl font-bold">${price}</span>
            <span className="text-muted-foreground">/mo</span>
          </>
        )}
      </div>

      <ul className="mb-8 flex-1 space-y-3" role="list" aria-label={`${plan.name} features`}>
        {plan.features.map((feature) => (
          <li key={feature.name} className="flex items-center gap-3 text-sm">
            {feature.included === true && (
              <CheckIcon className="size-4 shrink-0 text-green-600" aria-hidden="true" />
            )}
            {feature.included === false && (
              <XIcon className="size-4 shrink-0 text-muted-foreground/40" aria-hidden="true" />
            )}
            {feature.included === "coming-soon" && (
              <ClockIcon className="size-4 shrink-0 text-amber-500" aria-hidden="true" />
            )}

            <span className={cn(feature.included === false && "text-muted-foreground/60")}>
              {feature.name}
            </span>

            {feature.included === "coming-soon" && (
              <Badge variant="outline" className="text-xs">Coming soon</Badge>
            )}

            {feature.tooltip && (
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button className="text-muted-foreground" aria-label={`More info about ${feature.name}`}>
                      <span className="sr-only">Info</span>
                      <span aria-hidden="true">?</span>
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>{feature.tooltip}</TooltipContent>
                </Tooltip>
              </TooltipProvider>
            )}
          </li>
        ))}
      </ul>

      <Button
        variant={plan.highlight ? "default" : "outline"}
        size="lg"
        className="w-full"
      >
        {plan.cta}
      </Button>
    </div>
  )
}
```

---

## Feature Comparison Table

Horizontal scroll on mobile, full table on desktop.

```tsx
// components/pricing/feature-comparison.tsx
import { CheckIcon, XIcon, ClockIcon } from "lucide-react"
import { PLANS } from "@/lib/pricing"

const FEATURE_GROUPS = [
  {
    name: "Core",
    features: ["Projects", "Team members", "Storage"],
  },
  {
    name: "Analytics",
    features: ["Basic reports", "Custom dashboards", "Data export"],
  },
  {
    name: "Support",
    features: ["Email", "Priority", "Dedicated CSM"],
  },
]

function FeatureComparison() {
  return (
    <div className="overflow-x-auto" role="region" aria-label="Feature comparison" tabIndex={0}>
      <table className="w-full min-w-[640px] text-sm">
        <thead>
          <tr className="border-b">
            <th className="py-4 text-left font-medium text-muted-foreground" scope="col">
              Features
            </th>
            {PLANS.map((plan) => (
              <th key={plan.id} className="py-4 text-center font-semibold" scope="col">
                {plan.name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {FEATURE_GROUPS.map((group) => (
            <>
              <tr key={group.name}>
                <td colSpan={4} className="pt-6 pb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {group.name}
                </td>
              </tr>
              {group.features.map((feature) => (
                <tr key={feature} className="border-b">
                  <td className="py-3">{feature}</td>
                  {PLANS.map((plan) => {
                    const f = plan.features.find((pf) => pf.name === feature)
                    return (
                      <td key={plan.id} className="py-3 text-center">
                        <FeatureIcon included={f?.included ?? false} />
                      </td>
                    )
                  })}
                </tr>
              ))}
            </>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function FeatureIcon({ included }: { included: boolean | "coming-soon" }) {
  if (included === true) return <CheckIcon className="mx-auto size-5 text-green-600" aria-label="Included" />
  if (included === "coming-soon") return <ClockIcon className="mx-auto size-5 text-amber-500" aria-label="Coming soon" />
  return <XIcon className="mx-auto size-5 text-muted-foreground/30" aria-label="Not included" />
}
```

---

## Conversion Optimization

### Social Proof Bar

```tsx
function SocialProof() {
  return (
    <div className="flex flex-wrap items-center justify-center gap-6 py-8 text-sm text-muted-foreground">
      <div className="flex items-center gap-2">
        <div className="flex -space-x-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <img
              key={i}
              src={`/avatars/${i}.jpg`}
              alt=""
              className="size-8 rounded-full border-2 border-background"
            />
          ))}
        </div>
        <span>Trusted by <strong className="text-foreground">2,400+</strong> teams</span>
      </div>
      <div className="flex items-center gap-1">
        {Array.from({ length: 5 }).map((_, i) => (
          <span key={i} className="text-yellow-500" aria-hidden="true">&#9733;</span>
        ))}
        <span>4.9/5 on G2</span>
      </div>
    </div>
  )
}
```

### Trust Badges

```tsx
function TrustBadges() {
  return (
    <div className="flex flex-wrap items-center justify-center gap-8 py-6 opacity-60">
      <span className="text-sm font-medium">SOC 2 Type II</span>
      <span className="text-sm font-medium">GDPR Compliant</span>
      <span className="text-sm font-medium">99.9% Uptime SLA</span>
      <span className="text-sm font-medium">256-bit Encryption</span>
    </div>
  )
}
```

### FAQ Section

```tsx
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

const FAQ_ITEMS = [
  { q: "Can I switch plans?", a: "Yes. Upgrade anytime and we'll prorate. Downgrade takes effect next billing cycle." },
  { q: "Is there a free trial?", a: "Every paid plan includes a 14-day free trial. No credit card required." },
  { q: "What payment methods?", a: "Visa, Mastercard, Amex via Stripe. Annual plans also support wire transfer." },
  { q: "Can I cancel anytime?", a: "Yes, cancel anytime from your billing settings. No cancellation fees." },
]

function PricingFAQ() {
  return (
    <section aria-labelledby="faq-heading" className="mx-auto max-w-2xl py-16">
      <h2 id="faq-heading" className="mb-8 text-center text-2xl font-bold">
        Frequently asked questions
      </h2>
      <Accordion type="single" collapsible>
        {FAQ_ITEMS.map((item, i) => (
          <AccordionItem key={i} value={`faq-${i}`}>
            <AccordionTrigger>{item.q}</AccordionTrigger>
            <AccordionContent>{item.a}</AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </section>
  )
}
```

---

## Stripe Checkout Integration

### Checkout Button with Loading State

```tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"
import { createCheckoutSession } from "@/app/actions/stripe"

function CheckoutButton({
  priceId,
  planName,
}: {
  priceId: string
  planName: string
}) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleCheckout() {
    setLoading(true)
    setError(null)

    try {
      const { url } = await createCheckoutSession(priceId)
      if (url) window.location.href = url
    } catch (err) {
      setError("Something went wrong. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Button
        onClick={handleCheckout}
        disabled={loading}
        size="lg"
        className="w-full"
        aria-busy={loading}
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 size-4 animate-spin" aria-hidden="true" />
            Redirecting to checkout...
          </>
        ) : (
          `Get ${planName}`
        )}
      </Button>
      {error && (
        <p className="mt-2 text-sm text-destructive" role="alert">{error}</p>
      )}
    </div>
  )
}
```

### Server Action for Checkout

```typescript
// app/actions/stripe.ts
"use server"

import Stripe from "stripe"
import { auth } from "@/lib/auth"
import { redirect } from "next/navigation"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function createCheckoutSession(priceId: string) {
  const session = await auth()
  if (!session?.user) redirect("/login")

  const checkoutSession = await stripe.checkout.sessions.create({
    customer_email: session.user.email!,
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_URL}/billing?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing`,
    allow_promotion_codes: true,
    billing_address_collection: "auto",
    metadata: {
      userId: session.user.id,
    },
  })

  return { url: checkoutSession.url }
}
```

---

## Billing Management UI

### Current Plan Display

```tsx
// components/billing/current-plan.tsx
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { getUserSubscription } from "@/lib/billing"

async function CurrentPlanCard() {
  const sub = await getUserSubscription()

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Current Plan</CardTitle>
          <Badge variant={sub.status === "active" ? "default" : "destructive"}>
            {sub.status}
          </Badge>
        </div>
        <CardDescription>
          {sub.cancelAtPeriodEnd
            ? `Cancels on ${new Date(sub.currentPeriodEnd).toLocaleDateString()}`
            : `Renews on ${new Date(sub.currentPeriodEnd).toLocaleDateString()}`}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-baseline gap-1">
          <span className="text-3xl font-bold">${sub.plan.price / 100}</span>
          <span className="text-muted-foreground">/{sub.interval}</span>
        </div>
        <p className="mt-1 text-sm text-muted-foreground">{sub.plan.name} plan</p>

        <div className="mt-6 flex gap-3">
          <Button variant="outline" asChild>
            <a href="/pricing">Change plan</a>
          </Button>
          <Button variant="ghost" className="text-destructive">
            Cancel subscription
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
```

### Upgrade/Downgrade Flow

```typescript
// app/actions/billing.ts
"use server"

import Stripe from "stripe"
import { revalidatePath } from "next/cache"

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function changePlan(subscriptionId: string, newPriceId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId)

  await stripe.subscriptions.update(subscriptionId, {
    items: [
      {
        id: subscription.items.data[0].id,
        price: newPriceId,
      },
    ],
    proration_behavior: "create_prorations",
  })

  revalidatePath("/billing")
  return { success: true }
}

export async function cancelSubscription(subscriptionId: string) {
  await stripe.subscriptions.update(subscriptionId, {
    cancel_at_period_end: true,
  })

  revalidatePath("/billing")
  return { success: true }
}
```

### Invoice History

```tsx
// components/billing/invoice-history.tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { DownloadIcon } from "lucide-react"

async function InvoiceHistory({ customerId }: { customerId: string }) {
  const invoices = await getInvoices(customerId)

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Date</TableHead>
          <TableHead>Amount</TableHead>
          <TableHead>Status</TableHead>
          <TableHead className="text-right">Invoice</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {invoices.map((invoice) => (
          <TableRow key={invoice.id}>
            <TableCell>{new Date(invoice.created * 1000).toLocaleDateString()}</TableCell>
            <TableCell>${(invoice.amount_paid / 100).toFixed(2)}</TableCell>
            <TableCell>
              <Badge variant={invoice.status === "paid" ? "default" : "destructive"}>
                {invoice.status}
              </Badge>
            </TableCell>
            <TableCell className="text-right">
              {invoice.invoice_pdf && (
                <Button variant="ghost" size="sm" asChild>
                  <a href={invoice.invoice_pdf} target="_blank" rel="noopener noreferrer" aria-label={`Download invoice from ${new Date(invoice.created * 1000).toLocaleDateString()}`}>
                    <DownloadIcon className="size-4" />
                  </a>
                </Button>
              )}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

---

## Responsive Behavior

| Breakpoint | Layout |
|-----------|--------|
| < 640px (mobile) | Cards stacked vertically, highlighted card first (CSS `order`) |
| 640px - 1023px | 2-col grid, Enterprise spans full width below |
| >= 1024px | 3-col grid, center card elevated with `scale-105` |
| Feature table | Horizontal scroll on mobile, `overflow-x-auto` with `tabIndex={0}` |

```css
/* Mobile-first: reorder so highlighted plan shows first */
@media (max-width: 1023px) {
  [data-slot="pricing-card"][class*="ring-2"] {
    order: -1;
  }
}
```

---

## Accessibility Notes

- **Billing toggle:** Uses `role="radiogroup"` and `role="radio"` with `aria-checked`
- **Feature table:** Wrapped in `role="region"` with `aria-label` and `tabIndex={0}` for keyboard scroll
- **Checkout button:** `aria-busy={true}` during loading, error shown with `role="alert"`
- **Invoice links:** Descriptive `aria-label` on download buttons including the invoice date
- **Screen readers:** Plan details announced via semantic heading hierarchy and labeled lists
- **Keyboard:** All interactive elements reachable via Tab, toggle via Enter/Space
