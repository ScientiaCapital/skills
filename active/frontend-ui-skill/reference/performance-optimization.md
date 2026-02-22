# Performance Optimization — Core Web Vitals

## LCP (Largest Contentful Paint) < 2.5s

The largest visible element (hero image, heading, video poster) must render fast.

### next/image with Priority

```tsx
import Image from "next/image"

// Above-the-fold hero: priority triggers preload
<Image
  src="/hero.webp"
  alt="Product dashboard screenshot"
  width={1200}
  height={630}
  priority
  className="rounded-xl"
/>

// Below-the-fold: lazy load (default behavior)
<Image src="/feature.webp" alt="Feature preview" width={600} height={400} />
```

### Font Optimization

```tsx
// app/layout.tsx — next/font eliminates layout shift from font loading
import { Inter } from "next/font/google"

const inter = Inter({
  subsets: ["latin"],
  display: "swap",       // Show fallback immediately
  variable: "--font-sans",
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
```

```css
/* app/globals.css — reference the CSS variable */
@theme inline {
  --font-sans: var(--font-sans, "Inter", system-ui, sans-serif);
}
```

### Server Rendering for Fast First Paint

```tsx
// Server Component — zero JS shipped, HTML streams immediately
export default async function PricingPage() {
  const plans = await getPlans() // Runs on server
  return (
    <main>
      <h1 className="text-4xl font-bold">Pricing</h1>
      <PricingGrid plans={plans} />
    </main>
  )
}
```

---

## INP (Interaction to Next Paint) < 200ms

Every tap, click, or keypress must produce visible feedback within 200ms.

### Code Splitting with dynamic()

```tsx
import dynamic from "next/dynamic"

// Heavy chart library — only loaded when needed
const RevenueChart = dynamic(() => import("@/components/charts/revenue-chart"), {
  loading: () => <div className="h-[400px] animate-pulse rounded-xl bg-muted" />,
  ssr: false, // Client-only (uses canvas/WebGL)
})

// Modals — loaded on interaction
const SettingsDialog = dynamic(() => import("@/components/settings-dialog"))
```

### Debounced Event Handlers

```tsx
"use client"

import { useCallback, useRef } from "react"

function useDebounceCallback<T extends (...args: unknown[]) => void>(fn: T, delay: number) {
  const timer = useRef<ReturnType<typeof setTimeout>>(null)

  return useCallback((...args: Parameters<T>) => {
    if (timer.current) clearTimeout(timer.current)
    timer.current = setTimeout(() => fn(...args), delay)
  }, [fn, delay]) as T
}

// Usage: search input that fires API call
function SearchInput() {
  const handleSearch = useDebounceCallback((query: string) => {
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
  }, 300)

  return <input onChange={(e) => handleSearch(e.target.value)} placeholder="Search..." />
}
```

### React.memo — Use Judiciously

```tsx
import { memo } from "react"

// Only memoize when:
// 1. Component re-renders often with same props
// 2. Rendering is expensive (large lists, complex calculations)
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>{/* expensive rendering */}</li>
      ))}
    </ul>
  )
})

// Do NOT memoize:
// - Components that always receive new props
// - Small/cheap components
// - Components that rarely re-render
```

---

## CLS (Cumulative Layout Shift) < 0.1

No unexpected movement of page content.

### Reserve Space for Images

```tsx
// next/image handles this automatically with width/height
<Image src="/photo.jpg" alt="" width={800} height={600} />

// For dynamic aspect ratios, use aspect-ratio
<div className="aspect-video relative">
  <Image src={url} alt="" fill className="object-cover" />
</div>
```

### Skeleton Loaders

```tsx
import { Skeleton } from "@/components/ui/skeleton"

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      {/* KPI cards — match exact layout dimensions */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-[120px] rounded-xl" />
        ))}
      </div>
      {/* Chart area */}
      <Skeleton className="h-[400px] rounded-xl" />
      {/* Table rows */}
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-12 rounded-md" />
        ))}
      </div>
    </div>
  )
}

// Use with Suspense
<Suspense fallback={<DashboardSkeleton />}>
  <Dashboard />
</Suspense>
```

### Font Display Swap

Handled by `next/font` with `display: "swap"` (shown in LCP section). The fallback system font shows immediately, then swaps to the custom font without layout shift because `next/font` adjusts font metrics.

---

## Bundle Analysis

### @next/bundle-analyzer

```bash
npm install @next/bundle-analyzer
```

```typescript
// next.config.ts
import withBundleAnalyzer from "@next/bundle-analyzer"

const config = withBundleAnalyzer({
  enabled: process.env.ANALYZE === "true",
})({
  // ... your Next.js config
})

export default config
```

```bash
ANALYZE=true npm run build
# Opens interactive treemap in browser
```

### Tree Shaking — Barrel File Dangers

```tsx
// BAD: barrel import pulls in every component
import { Button } from "@/components/ui"

// GOOD: direct import — tree shaking works correctly
import { Button } from "@/components/ui/button"
```

shadcn/ui uses direct file imports by default. Never create barrel files (`index.ts`) that re-export everything from a UI directory.

---

## Dynamic Imports

### Route-Based Splitting (Automatic)

Next.js App Router automatically code-splits per route. Each `page.tsx` is a separate bundle. No configuration needed.

### Component-Level Splitting

```tsx
import dynamic from "next/dynamic"

// Heavy library (chart, editor, map)
const MarkdownEditor = dynamic(() => import("@/components/markdown-editor"), {
  loading: () => <Skeleton className="h-[300px]" />,
})

// Conditional rendering — only load when needed
const AdminPanel = dynamic(() => import("@/components/admin-panel"))

export default function Page({ isAdmin }: { isAdmin: boolean }) {
  return (
    <main>
      <Content />
      {isAdmin && <AdminPanel />}
    </main>
  )
}
```

---

## Image Optimization

### next/image Formats and Responsive

```tsx
import Image from "next/image"

// Automatic WebP/AVIF conversion (Next.js image optimizer)
<Image
  src="/product.jpg"
  alt="Product screenshot"
  width={1200}
  height={800}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="rounded-xl"
/>

// Blur placeholder for perceived performance
import heroImage from "@/public/hero.jpg" // static import enables blur

<Image
  src={heroImage}
  alt="Hero"
  placeholder="blur"
  priority
/>

// Remote images — configure domains in next.config.ts
// next.config.ts:
// images: { remotePatterns: [{ hostname: "cdn.example.com" }] }
```

### Image Sizing Rules

| Context | Approach |
|---------|----------|
| Known dimensions | `width` + `height` props |
| Fill container | `fill` prop + parent `relative` + `object-cover` |
| Responsive | `sizes` prop matching your CSS breakpoints |
| Static import | Automatic dimensions from file metadata |

---

## Caching Strategies

### Next.js Fetch Cache

```tsx
// Cached indefinitely (default in Server Components)
const data = await fetch("https://api.example.com/data")

// Revalidate every 60 seconds (ISR)
const data = await fetch("https://api.example.com/data", {
  next: { revalidate: 60 },
})

// Never cache (always fresh)
const data = await fetch("https://api.example.com/data", {
  cache: "no-store",
})
```

### Static Generation vs ISR vs Dynamic

| Strategy | When | Config |
|----------|------|--------|
| Static (build-time) | Marketing pages, docs | Default behavior |
| ISR (timed revalidation) | Pricing, blog | `revalidate: 60` on fetch or page |
| Dynamic (per-request) | User dashboard, auth | `cache: "no-store"` or `cookies()`/`headers()` |

```tsx
// Force dynamic for pages using auth
import { cookies } from "next/headers"

export default async function DashboardPage() {
  const cookieStore = await cookies() // Makes page dynamic
  // ...
}
```

---

## Lighthouse CI

### Budget Configuration

```json
// budget.json
[
  {
    "path": "/*",
    "timings": [
      { "metric": "largest-contentful-paint", "budget": 2500 },
      { "metric": "interactive", "budget": 3500 },
      { "metric": "cumulative-layout-shift", "budget": 0.1 }
    ],
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "total", "budget": 800 }
    ]
  }
]
```

### CI Integration (GitHub Actions)

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci && npm run build
      - run: npm start &
      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: ./lighthouserc.json
          uploadArtifacts: true
```

```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/", "http://localhost:3000/pricing"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.95 }]
      }
    }
  }
}
```

---

## Tailwind v4 Performance Benefits

| Improvement | Details |
|-------------|---------|
| **70% smaller CSS** | Automatic unused style elimination; no purge config needed |
| **No build step** | Lightning CSS replaces PostCSS for faster builds |
| **Automatic content detection** | `@source` directive replaces manual `content` array |
| **Smaller runtime** | No JIT engine shipped to client |

The move from Tailwind v3 to v4 is a free performance win with zero code changes after migration via `npx @tailwindcss/upgrade`.

---

## Quick Checklist

- [ ] Hero image uses `next/image` with `priority`
- [ ] Fonts loaded via `next/font` with `display: "swap"`
- [ ] Heavy components lazy-loaded with `dynamic()`
- [ ] All images have explicit dimensions or `fill` + `aspect-ratio`
- [ ] Skeleton loaders match actual content layout dimensions
- [ ] No barrel file imports for UI components
- [ ] `sizes` prop on responsive images matches CSS breakpoints
- [ ] Fetch calls use appropriate caching (`revalidate` or `no-store`)
- [ ] Lighthouse CI runs on every PR with performance budgets
- [ ] Bundle analyzer checked for unexpected large dependencies
