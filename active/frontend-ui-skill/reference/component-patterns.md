# React Component Patterns

> Deep-dive reference for production React component patterns with Tailwind v4 and
> shadcn/ui. Load when building custom components, designing composition APIs, or
> making Server/Client Component decisions.

---

## Table of Contents

1. [Compound Components](#compound-components)
2. [cva Deep Dive](#cva-deep-dive)
3. [Polymorphic Components (asChild/Slot)](#polymorphic-components)
4. [data-slot Styling Hook Pattern](#data-slot-styling-hook-pattern)
5. [React.ComponentProps Usage](#reactcomponentprops-usage)
6. [Server vs Client Component Boundaries](#server-vs-client-component-boundaries)
7. [Context Providers at Boundaries](#context-providers-at-boundaries)
8. [Render Props and Composition](#render-props-and-composition)
9. [Component File Organization](#component-file-organization)

---

## Compound Components

Group related components under a namespace. Each sub-component handles one concern.
The parent manages shared state via context.

### Table Pattern

```tsx
// components/ui/table.tsx
import { cn } from "@/lib/utils"

function Table({ className, ref, ...props }: React.ComponentProps<"table">) {
  return (
    <div className="relative w-full overflow-auto">
      <table ref={ref} data-slot="table"
        className={cn("w-full caption-bottom text-sm", className)} {...props} />
    </div>
  )
}

function TableHeader({ className, ref, ...props }: React.ComponentProps<"thead">) {
  return <thead ref={ref} data-slot="table-header"
    className={cn("[&_tr]:border-b", className)} {...props} />
}

function TableBody({ className, ref, ...props }: React.ComponentProps<"tbody">) {
  return <tbody ref={ref} data-slot="table-body"
    className={cn("[&_tr:last-child]:border-0", className)} {...props} />
}

function TableRow({ className, ref, ...props }: React.ComponentProps<"tr">) {
  return <tr ref={ref} data-slot="table-row"
    className={cn("border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted", className)} {...props} />
}

function TableHead({ className, ref, ...props }: React.ComponentProps<"th">) {
  return <th ref={ref} data-slot="table-head"
    className={cn("h-12 px-4 text-left align-middle font-medium text-muted-foreground", className)} {...props} />
}

function TableCell({ className, ref, ...props }: React.ComponentProps<"td">) {
  return <td ref={ref} data-slot="table-cell"
    className={cn("p-4 align-middle", className)} {...props} />
}

export { Table, TableHeader, TableBody, TableRow, TableHead, TableCell }
```

**Usage:**

```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Name</TableHead>
      <TableHead>Status</TableHead>
      <TableHead className="text-right">Amount</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {invoices.map((inv) => (
      <TableRow key={inv.id}>
        <TableCell className="font-medium">{inv.name}</TableCell>
        <TableCell>{inv.status}</TableCell>
        <TableCell className="text-right">{inv.amount}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Dialog Pattern (with Context)

```tsx
"use client"

import { createContext, useContext, useState } from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

function Dialog({ children, ...props }: DialogPrimitive.DialogProps) {
  return <DialogPrimitive.Root {...props}>{children}</DialogPrimitive.Root>
}

function DialogTrigger({ className, ref, ...props }: React.ComponentProps<typeof DialogPrimitive.Trigger>) {
  return <DialogPrimitive.Trigger ref={ref} data-slot="dialog-trigger" className={className} {...props} />
}

function DialogContent({ className, children, ref, ...props }: React.ComponentProps<typeof DialogPrimitive.Content>) {
  return (
    <DialogPrimitive.Portal>
      <DialogPrimitive.Overlay data-slot="dialog-overlay"
        className="fixed inset-0 z-50 bg-black/80 animate-in fade-in-0" />
      <DialogPrimitive.Content ref={ref} data-slot="dialog-content"
        className={cn(
          "fixed left-1/2 top-1/2 z-50 w-full max-w-lg -translate-x-1/2 -translate-y-1/2",
          "rounded-lg border bg-background p-6 shadow-lg",
          "animate-in fade-in-0 zoom-in-95 slide-in-from-left-1/2 slide-in-from-top-[48%]",
          className
        )}
        {...props}
      >
        {children}
        <DialogPrimitive.Close
          className="absolute right-4 top-4 rounded-xs opacity-70 hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </DialogPrimitive.Close>
      </DialogPrimitive.Content>
    </DialogPrimitive.Portal>
  )
}

function DialogHeader({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="dialog-header" className={cn("flex flex-col gap-2 text-center sm:text-left", className)} {...props} />
}

function DialogTitle({ className, ref, ...props }: React.ComponentProps<typeof DialogPrimitive.Title>) {
  return <DialogPrimitive.Title ref={ref} data-slot="dialog-title"
    className={cn("text-lg font-semibold leading-none tracking-tight", className)} {...props} />
}

function DialogDescription({ className, ref, ...props }: React.ComponentProps<typeof DialogPrimitive.Description>) {
  return <DialogPrimitive.Description ref={ref} data-slot="dialog-description"
    className={cn("text-sm text-muted-foreground", className)} {...props} />
}

export { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription }
```

### Form Pattern (Compound + Context)

```tsx
"use client"

import { createContext, useContext } from "react"
import { useFormContext, Controller, type ControllerProps, type FieldPath, type FieldValues } from "react-hook-form"
import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"

// Context carries field metadata to child components
type FormFieldContextValue = { name: string }
const FormFieldContext = createContext<FormFieldContextValue>({ name: "" })

function FormField<T extends FieldValues, N extends FieldPath<T>>(props: ControllerProps<T, N>) {
  return (
    <FormFieldContext.Provider value={{ name: props.name }}>
      <Controller {...props} />
    </FormFieldContext.Provider>
  )
}

function useFormField() {
  const { name } = useContext(FormFieldContext)
  const { getFieldState, formState } = useFormContext()
  const fieldState = getFieldState(name, formState)
  return { name, ...fieldState }
}

function FormItem({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="form-item" className={cn("space-y-2", className)} {...props} />
}

function FormLabel({ className, ...props }: React.ComponentProps<typeof Label>) {
  const { error } = useFormField()
  return <Label data-slot="form-label" className={cn(error && "text-destructive", className)} {...props} />
}

function FormMessage({ className, ...props }: React.ComponentProps<"p">) {
  const { error } = useFormField()
  if (!error?.message) return null
  return (
    <p data-slot="form-message" role="alert"
      className={cn("text-sm font-medium text-destructive", className)} {...props}>
      {error.message}
    </p>
  )
}

export { FormField, FormItem, FormLabel, FormMessage, useFormField }
```

---

## cva Deep Dive

`class-variance-authority` creates type-safe variant APIs for components.

### Basic Usage

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const alertVariants = cva(
  // Base classes — always applied
  "relative w-full rounded-lg border p-4 text-sm [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg+div]:translate-y-[-3px] pl-11",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive: "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
        success: "border-green-500/50 text-green-700 bg-green-50 dark:bg-green-950 dark:text-green-300 [&>svg]:text-green-600",
        warning: "border-yellow-500/50 text-yellow-700 bg-yellow-50 dark:bg-yellow-950 dark:text-yellow-300 [&>svg]:text-yellow-600",
      },
    },
    defaultVariants: { variant: "default" },
  }
)

type AlertProps = React.ComponentProps<"div"> & VariantProps<typeof alertVariants>

function Alert({ className, variant, ref, ...props }: AlertProps) {
  return <div ref={ref} role="alert" data-slot="alert"
    className={cn(alertVariants({ variant, className }))} {...props} />
}
```

### Compound Variants

Apply classes only when multiple variant values match simultaneously.

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
      intent: {
        neutral: "",
        danger: "",
      },
    },
    compoundVariants: [
      // Danger + default = red background
      { variant: "default", intent: "danger", className: "bg-destructive text-destructive-foreground hover:bg-destructive/90" },
      // Danger + outline = red border
      { variant: "outline", intent: "danger", className: "border-destructive text-destructive hover:bg-destructive/10" },
      // Danger + ghost = red text
      { variant: "ghost", intent: "danger", className: "text-destructive hover:bg-destructive/10 hover:text-destructive" },
    ],
    defaultVariants: { variant: "default", size: "default", intent: "neutral" },
  }
)
```

### Boolean Variants

```tsx
const inputVariants = cva(
  "flex h-10 w-full rounded-md border px-3 py-2 text-sm transition-colors",
  {
    variants: {
      hasError: {
        true: "border-destructive focus-visible:ring-destructive",
        false: "border-input focus-visible:ring-ring",
      },
      fullWidth: {
        true: "w-full",
        false: "w-auto",
      },
    },
    defaultVariants: { hasError: false, fullWidth: true },
  }
)
```

---

## Polymorphic Components

The `asChild` pattern lets a component render as a different element, merging props
and behavior onto the child.

### Slot from Radix

```tsx
import { Slot } from "@radix-ui/react-slot"

type ButtonProps = React.ComponentProps<"button"> & {
  asChild?: boolean
}

function Button({ asChild = false, className, ref, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button"
  return <Comp ref={ref} data-slot="button" className={cn("...", className)} {...props} />
}

// Render as <button>
<Button>Click me</Button>

// Render as <a> — Button styles on a link
<Button asChild>
  <a href="/dashboard">Go to dashboard</a>
</Button>

// Render as Next.js Link
<Button asChild>
  <Link href="/dashboard">Go to dashboard</Link>
</Button>
```

### How Slot Works

`Slot` merges its props onto its single child element:
- `className` is merged (not replaced)
- `ref` is forwarded
- Event handlers are composed (both fire)
- Other props from Slot are spread onto the child

---

## data-slot Styling Hook Pattern

`data-slot` provides stable, semantic CSS hooks for parent-child styling without
coupling to implementation details.

### Defining Slots

```tsx
function Card({ className, ref, ...props }: React.ComponentProps<"div">) {
  return <div ref={ref} data-slot="card" className={cn("rounded-xl border bg-card", className)} {...props} />
}

function CardTitle({ className, ref, ...props }: React.ComponentProps<"h3">) {
  return <h3 ref={ref} data-slot="card-title" className={cn("text-lg font-semibold", className)} {...props} />
}

function CardDescription({ className, ref, ...props }: React.ComponentProps<"p">) {
  return <p ref={ref} data-slot="card-description" className={cn("text-sm text-muted-foreground", className)} {...props} />
}
```

### Targeting Slots from Parents

```tsx
{/* Compact card variant — tighten spacing on all sub-slots */}
<div className="[&_[data-slot=card]]:p-3 [&_[data-slot=card-title]]:text-sm [&_[data-slot=card-description]]:text-xs">
  <Card>
    <CardTitle>Compact Title</CardTitle>
    <CardDescription>Tight spacing</CardDescription>
  </Card>
</div>
```

### Nested Slot Targeting

```tsx
{/* Only style cards inside the dashboard grid */}
<section data-slot="dashboard-grid"
  className="grid grid-cols-3 gap-4 [&_[data-slot=card]]:shadow-sm [&_[data-slot=card]]:hover:shadow-md">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</section>
```

### When to Use data-slot vs className Prop

| Approach | When |
|----------|------|
| `className` prop | One-off style override on a single instance |
| `data-slot` targeting | Systematic styling of many instances from a shared parent |
| cva variant | Predefined, type-safe style variations |

---

## React.ComponentProps Usage

React 19 removes the need for `forwardRef`. Use `React.ComponentProps<>` to get the
full prop type including `ref`.

### Native Element Props

```tsx
// Gets all <button> props including ref, onClick, disabled, aria-*, etc.
function Button({ className, ref, ...props }: React.ComponentProps<"button">) {
  return <button ref={ref} className={cn("...", className)} {...props} />
}

// Gets all <input> props
function Input({ className, type, ref, ...props }: React.ComponentProps<"input">) {
  return <input ref={ref} type={type} className={cn("...", className)} {...props} />
}

// Gets all <a> props
function NavLink({ className, ref, ...props }: React.ComponentProps<"a">) {
  return <a ref={ref} className={cn("...", className)} {...props} />
}
```

### Radix Primitive Props

```tsx
import * as DialogPrimitive from "@radix-ui/react-dialog"

function DialogContent({ className, ref, ...props }: React.ComponentProps<typeof DialogPrimitive.Content>) {
  return <DialogPrimitive.Content ref={ref} className={cn("...", className)} {...props} />
}
```

### Extending with Custom Props

```tsx
type MetricCardProps = React.ComponentProps<"div"> & {
  title: string
  value: string | number
  trend?: { direction: "up" | "down" | "flat"; percentage: number }
}

function MetricCard({ title, value, trend, className, ref, ...props }: MetricCardProps) {
  return (
    <div ref={ref} data-slot="metric-card" className={cn("rounded-lg border p-4", className)} {...props}>
      <p className="text-sm text-muted-foreground">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
      {trend && <TrendIndicator {...trend} />}
    </div>
  )
}
```

---

## Server vs Client Component Boundaries

### Decision Framework

| Question | Server Component | Client Component |
|----------|-----------------|------------------|
| Needs useState/useEffect? | | Yes |
| Needs event handlers (onClick, onChange)? | | Yes |
| Needs browser APIs (window, localStorage)? | | Yes |
| Fetches data from DB/API? | Yes | |
| Uses secrets/env vars? | Yes | |
| Is purely presentational? | Yes | |
| Third-party client library (chart, editor)? | | Yes |

### The Leaf Rule

Push `"use client"` to the smallest possible component. Keep parent layouts as Server
Components.

```tsx
// app/dashboard/page.tsx — Server Component (default)
export default async function DashboardPage() {
  const metrics = await getMetrics()
  const activities = await getActivities()

  return (
    <main className="p-6 space-y-6">
      {/* Server-rendered — zero JS */}
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <KPIGrid metrics={metrics} />

      {/* Client islands — only these ship JS */}
      <RevenueChart data={metrics.revenue} />
      <ActivityFeed initialItems={activities} />
    </main>
  )
}
```

```tsx
// components/app/revenue-chart.tsx — Client Component (leaf)
"use client"

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

function RevenueChart({ data }: { data: RevenuePoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="revenue" stroke="var(--color-primary)" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  )
}

export { RevenueChart }
```

### Composition Pattern — Server Wrapper, Client Child

```tsx
// Server Component fetches data
async function UserSection() {
  const user = await getUser()
  return <UserMenu user={user} /> // passes serializable data to client
}

// Client Component handles interactivity
"use client"
function UserMenu({ user }: { user: User }) {
  const [open, setOpen] = useState(false)
  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger>{user.name}</DropdownMenuTrigger>
      <DropdownMenuContent>...</DropdownMenuContent>
    </DropdownMenu>
  )
}
```

---

## Context Providers at Boundaries

Place Context providers at the client boundary, not at the root (to avoid making the
entire tree client-rendered).

### Pattern: Provider Wrapper Component

```tsx
// providers/theme-provider.tsx
"use client"

import { ThemeProvider as NextThemesProvider } from "next-themes"

function ThemeProvider({ children, ...props }: React.ComponentProps<typeof NextThemesProvider>) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}

export { ThemeProvider }
```

```tsx
// app/layout.tsx — remains a Server Component
import { ThemeProvider } from "@/providers/theme-provider"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children} {/* children can still be Server Components */}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

### Multiple Providers — Compose with a Single Wrapper

```tsx
// providers/index.tsx
"use client"

import { ThemeProvider } from "next-themes"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Toaster } from "@/components/ui/sonner"

const queryClient = new QueryClient()

function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        {children}
        <Toaster />
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export { Providers }
```

---

## Render Props and Composition

### Headless Component with Render Prop

```tsx
"use client"

import { useState, useCallback } from "react"

type PaginationState = { page: number; pageSize: number; totalPages: number }

type PaginationRenderProps = PaginationState & {
  next: () => void
  prev: () => void
  goTo: (page: number) => void
}

function Pagination({
  totalItems,
  pageSize = 10,
  children,
}: {
  totalItems: number
  pageSize?: number
  children: (props: PaginationRenderProps) => React.ReactNode
}) {
  const [page, setPage] = useState(1)
  const totalPages = Math.ceil(totalItems / pageSize)

  const next = useCallback(() => setPage((p) => Math.min(p + 1, totalPages)), [totalPages])
  const prev = useCallback(() => setPage((p) => Math.max(p - 1, 1)), [])
  const goTo = useCallback((p: number) => setPage(Math.min(Math.max(p, 1), totalPages)), [totalPages])

  return <>{children({ page, pageSize, totalPages, next, prev, goTo })}</>
}

// Usage
<Pagination totalItems={users.length} pageSize={10}>
  {({ page, totalPages, next, prev }) => (
    <div className="flex items-center gap-2">
      <Button variant="outline" size="sm" onClick={prev} disabled={page === 1}>Previous</Button>
      <span className="text-sm text-muted-foreground">Page {page} of {totalPages}</span>
      <Button variant="outline" size="sm" onClick={next} disabled={page === totalPages}>Next</Button>
    </div>
  )}
</Pagination>
```

### Children as Composition

Prefer children composition over render props when you do not need to pass state up.

```tsx
// Good — composition via children
<Card>
  <CardHeader>
    <CardTitle>Revenue</CardTitle>
  </CardHeader>
  <CardContent>
    <RevenueChart data={data} />
  </CardContent>
</Card>

// Avoid — unnecessary render prop
<Card renderHeader={() => <h2>Revenue</h2>} renderContent={() => <RevenueChart />} />
```

---

## Component File Organization

### Directory Structure

```
src/
  components/
    ui/                   # shadcn/ui primitives
      button.tsx
      card.tsx
      dialog.tsx
      input.tsx
      table.tsx
      ...
    app/                  # Application-specific components
      dashboard/
        kpi-card.tsx
        revenue-chart.tsx
        activity-feed.tsx
      settings/
        profile-form.tsx
        team-settings.tsx
      shared/
        user-nav.tsx
        search-command.tsx
        data-table.tsx
  lib/
    utils.ts              # cn() and shared utilities
    validations.ts        # Shared Zod schemas
  hooks/
    use-debounce.ts
    use-media-query.ts
  providers/
    theme-provider.tsx
    query-provider.tsx
```

### Naming Conventions

| Pattern | Example |
|---------|---------|
| Component file | `kpi-card.tsx` (kebab-case) |
| Component name | `KPICard` (PascalCase) |
| Variant file | `button.tsx` exports `buttonVariants` + `Button` |
| Hook file | `use-debounce.ts` |
| Utility file | `utils.ts` |
| Type-only file | `types.ts` |

### Export Pattern

```tsx
// components/ui/button.tsx
function Button({ ... }: ...) { ... }
export { Button, buttonVariants }

// components/app/dashboard/kpi-card.tsx
function KPICard({ ... }: ...) { ... }
export { KPICard }
```

Use named exports exclusively. Default exports are only for page components
(`page.tsx`, `layout.tsx`) as required by Next.js.
