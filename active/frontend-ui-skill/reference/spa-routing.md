# SPA Routing Patterns

Client-side routing for Vite + React SPAs. Covers React Router v7 (library mode) and TanStack Router.

> **Key insight:** In Next.js, the file system IS the router. In SPAs, you define routes explicitly.
> Everything else — Tailwind, shadcn/ui, components, accessibility, forms — works identically.

---

## React Router v7 (Library Mode)

React Router v7 has two modes:
- **Framework mode** — File-based routing with SSR (like Remix)
- **Library mode** — Manual route config, client-only (what we use for Vite SPAs)

### Installation

```bash
npm install react-router
```

### Basic Setup

```tsx
// src/main.tsx
import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router"
import App from "./App"
import "./index.css"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
)
```

```tsx
// src/App.tsx
import { Routes, Route } from "react-router"
import { RootLayout } from "@/components/layout/RootLayout"
import { DashboardLayout } from "@/components/layout/DashboardLayout"
import HomePage from "@/pages/Home"
import DashboardPage from "@/pages/Dashboard"
import SettingsPage from "@/pages/Settings"
import NotFoundPage from "@/pages/NotFound"

export default function App() {
  return (
    <Routes>
      <Route element={<RootLayout />}>
        <Route index element={<HomePage />} />

        {/* Nested dashboard routes share a layout */}
        <Route path="dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="team" element={<TeamPage />} />
        </Route>

        {/* Catch-all */}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}
```

---

## Nested Layouts with `<Outlet />`

The `<Outlet />` component renders child routes — equivalent to `{children}` in Next.js layouts.

### Root Layout

```tsx
// src/components/layout/RootLayout.tsx
import { Outlet } from "react-router"
import { Toaster } from "@/components/ui/sonner"

export function RootLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Outlet />
      <Toaster />
    </div>
  )
}
```

### Dashboard Layout (Sidebar + Header + Content)

```tsx
// src/components/layout/DashboardLayout.tsx
import { Outlet } from "react-router"
import { Sidebar } from "@/components/layout/Sidebar"
import { Header } from "@/components/layout/Header"

export function DashboardLayout() {
  return (
    <div className="flex h-screen">
      <Sidebar className="w-64 hidden lg:flex" />
      <div className="flex-1 flex flex-col min-w-0">
        <Header />
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

### Sidebar Navigation

```tsx
// src/components/layout/Sidebar.tsx
import { NavLink } from "react-router"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard, Settings, BarChart3, Users
} from "lucide-react"

const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/dashboard/analytics", icon: BarChart3, label: "Analytics" },
  { to: "/dashboard/team", icon: Users, label: "Team" },
  { to: "/dashboard/settings", icon: Settings, label: "Settings" },
]

export function Sidebar({ className }: { className?: string }) {
  return (
    <aside className={cn("border-r bg-card flex flex-col", className)}>
      <div className="p-6 font-semibold text-lg">My SaaS</div>
      <nav className="flex-1 px-3 space-y-1" aria-label="Main navigation">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/dashboard"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
              )
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
```

**`NavLink` vs `Link`:**
- `NavLink` provides `isActive` and `isPending` states for styling
- `Link` is simpler when you don't need active state indication
- Both use `to` prop (not `href` like Next.js `<Link>`)

---

## Code Splitting with React.lazy()

### Route-Level Splitting

```tsx
// src/App.tsx
import { lazy, Suspense } from "react"
import { Routes, Route } from "react-router"
import { PageSkeleton } from "@/components/shared/PageSkeleton"

// Each lazy() creates a separate JS chunk
const Dashboard = lazy(() => import("@/pages/Dashboard"))
const Settings = lazy(() => import("@/pages/Settings"))
const Analytics = lazy(() => import("@/pages/Analytics"))
const Team = lazy(() => import("@/pages/Team"))

export default function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route element={<RootLayout />}>
          <Route path="dashboard" element={<DashboardLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="settings" element={<Settings />} />
            <Route path="analytics" element={<Analytics />} />
            <Route path="team" element={<Team />} />
          </Route>
        </Route>
      </Routes>
    </Suspense>
  )
}
```

### Named Exports with React.lazy()

```tsx
// React.lazy() requires default exports. For named exports:
const Settings = lazy(() =>
  import("@/pages/Settings").then((mod) => ({ default: mod.SettingsPage }))
)
```

### Preload on Interaction

```tsx
// Preload route chunk on hover for instant navigation
const dashboardImport = () => import("@/pages/Dashboard")
const Dashboard = lazy(dashboardImport)

<NavLink
  to="/dashboard"
  onMouseEnter={() => dashboardImport()}
  onFocus={() => dashboardImport()}
>
  Dashboard
</NavLink>
```

---

## Data Loading Patterns

In Next.js, Server Components fetch data on the server. In SPAs, all data fetching is client-side.

### React Query for Data Fetching

```tsx
// src/lib/query-client.ts
import { QueryClient } from "@tanstack/react-query"

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,     // 5 minutes
      gcTime: 10 * 60 * 1000,        // 10 minutes (was cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})
```

```tsx
// src/providers/QueryProvider.tsx
import { QueryClientProvider } from "@tanstack/react-query"
import { queryClient } from "@/lib/query-client"

export function QueryProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

### Query Hooks per Feature

```tsx
// src/hooks/use-metrics.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "@/lib/api"

// Fetch
export function useMetrics() {
  return useQuery({
    queryKey: ["metrics"],
    queryFn: () => api.get<Metrics>("/api/metrics"),
  })
}

// Mutation with cache invalidation (replaces Server Actions + revalidatePath)
export function useUpdateMetric() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: UpdateMetricInput) => api.patch("/api/metrics", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["metrics"] })
    },
  })
}
```

### Using in Components

```tsx
// src/pages/Dashboard.tsx
import { useMetrics } from "@/hooks/use-metrics"
import { KPIGrid } from "@/components/dashboard/KPIGrid"
import { Skeleton } from "@/components/ui/skeleton"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { AlertCircle } from "lucide-react"

export default function Dashboard() {
  const { data: metrics, isLoading, error } = useMetrics()

  // State trio: Loading | Error | Empty
  if (isLoading) return <DashboardSkeleton />
  if (error) return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertDescription>Failed to load metrics. Please try again.</AlertDescription>
    </Alert>
  )
  if (!metrics?.length) return <EmptyState message="No metrics yet" />

  return <KPIGrid metrics={metrics} />
}
```

### API Client

```tsx
// src/lib/api.ts
import { env } from "@/lib/env"

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async get<T>(path: string): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      headers: this.headers(),
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  }

  async post<T>(path: string, body: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  }

  async patch<T>(path: string, body: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "PATCH",
      headers: this.headers(),
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
    return res.json()
  }

  async delete(path: string): Promise<void> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "DELETE",
      headers: this.headers(),
    })
    if (!res.ok) throw new ApiError(res.status, await res.text())
  }

  private headers(): HeadersInit {
    const token = localStorage.getItem("auth_token")
    return {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    }
  }
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = "ApiError"
  }
}

// In dev, proxy handles /api → backend. In prod, use VITE_API_URL.
export const api = new ApiClient(
  import.meta.env.DEV ? "" : env.VITE_API_URL
)
```

---

## Protected Routes

### Auth Guard Component

```tsx
// src/components/auth/ProtectedRoute.tsx
import { Navigate, Outlet, useLocation } from "react-router"
import { useAuth } from "@/hooks/use-auth"
import { PageSkeleton } from "@/components/shared/PageSkeleton"

interface ProtectedRouteProps {
  requiredRole?: string
}

export function ProtectedRoute({ requiredRole }: ProtectedRouteProps) {
  const { user, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) return <PageSkeleton />

  if (!user) {
    // Redirect to login, preserving intended destination
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (requiredRole && !user.roles.includes(requiredRole)) {
    return <Navigate to="/unauthorized" replace />
  }

  return <Outlet />
}
```

### Using in Routes

```tsx
<Routes>
  {/* Public routes */}
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />

  {/* Protected routes — requires authentication */}
  <Route element={<ProtectedRoute />}>
    <Route path="dashboard" element={<DashboardLayout />}>
      <Route index element={<Dashboard />} />
      <Route path="settings" element={<Settings />} />

      {/* Role-restricted route */}
      <Route element={<ProtectedRoute requiredRole="admin" />}>
        <Route path="admin" element={<AdminPanel />} />
      </Route>
    </Route>
  </Route>

  <Route path="/unauthorized" element={<Unauthorized />} />
  <Route path="*" element={<NotFound />} />
</Routes>
```

### Auth Hook with React Query

```tsx
// src/hooks/use-auth.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router"
import { api } from "@/lib/api"

interface User {
  id: string
  email: string
  name: string
  roles: string[]
}

export function useAuth() {
  const query = useQuery({
    queryKey: ["auth", "me"],
    queryFn: () => api.get<User>("/api/auth/me"),
    retry: false,
    staleTime: 10 * 60 * 1000,
  })

  return {
    user: query.data ?? null,
    isLoading: query.isLoading,
    isAuthenticated: !!query.data,
  }
}

export function useLogin() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (credentials: { email: string; password: string }) =>
      api.post<{ token: string }>("/api/auth/login", credentials),
    onSuccess: (data) => {
      localStorage.setItem("auth_token", data.token)
      queryClient.invalidateQueries({ queryKey: ["auth"] })
      navigate("/dashboard")
    },
  })
}

export function useLogout() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: () => api.post("/api/auth/logout", {}),
    onSettled: () => {
      localStorage.removeItem("auth_token")
      queryClient.clear()
      navigate("/login")
    },
  })
}
```

---

## Error Boundaries

```tsx
// src/components/shared/ErrorBoundary.tsx
import { Component, type ReactNode } from "react"
import { Button } from "@/components/ui/button"
import { AlertCircle } from "lucide-react"

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
          <AlertCircle className="h-12 w-12 text-destructive" />
          <h2 className="text-xl font-semibold">Something went wrong</h2>
          <p className="text-muted-foreground text-sm max-w-md text-center">
            {this.state.error?.message ?? "An unexpected error occurred."}
          </p>
          <Button
            variant="outline"
            onClick={() => {
              this.setState({ hasError: false, error: null })
              window.location.reload()
            }}
          >
            Try again
          </Button>
        </div>
      )
    }
    return this.props.children
  }
}
```

---

## TanStack Router (Alternative)

Type-safe routing with automatic route type inference.

### Installation

```bash
npm install @tanstack/react-router
npm install -D @tanstack/router-plugin  # Vite plugin for auto route generation
```

### Vite Plugin Config

```ts
// vite.config.ts
import { TanStackRouterVite } from "@tanstack/router-plugin/vite"

export default defineConfig({
  plugins: [
    TanStackRouterVite(),   // Must be before react()
    react(),
    tailwindcss(),
  ],
})
```

### File-Based Routes

```
src/routes/
├── __root.tsx          # Root layout
├── index.tsx           # / route
├── dashboard/
│   ├── route.tsx       # /dashboard layout
│   ├── index.tsx       # /dashboard
│   └── settings.tsx    # /dashboard/settings
├── login.tsx           # /login
└── _auth/              # Route group (no URL segment)
    └── profile.tsx     # Requires auth
```

### Type-Safe Links and Search Params

```tsx
// TanStack Router gives you type errors for invalid routes
<Link to="/dashboard/settings" />  // Type-checked route
<Link to="/invalid-route" />       // TypeScript error

// Type-safe search params
const Route = createFileRoute("/products")({
  validateSearch: z.object({
    page: z.number().default(1),
    sort: z.enum(["name", "price"]).default("name"),
  }),
})

// In component — fully typed
const { page, sort } = Route.useSearch()
```

### When to Choose TanStack Router

| Feature | React Router v7 | TanStack Router |
|---------|-----------------|-----------------|
| Type safety | Runtime only | Full compile-time |
| Search params | Manual parsing | Zod-validated, typed |
| Learning curve | Familiar, lower | Steeper, more concepts |
| Ecosystem | Massive | Growing fast |
| File-based routes | Framework mode only | Via Vite plugin |
| Bundle size | ~15KB | ~20KB |
| SSR support | Yes (framework mode) | Yes (TanStack Start) |

**Recommendation:** Use React Router v7 for most SPAs. Use TanStack Router when type-safe search params and validated loaders are critical (complex filtering UIs, data-heavy apps).

---

## Migration Table: Next.js to SPA

| Next.js Pattern | SPA Equivalent | Notes |
|----------------|----------------|-------|
| `app/page.tsx` | Route component | Explicitly defined in route config |
| `layout.tsx` | Layout with `<Outlet />` | Wraps child routes |
| `loading.tsx` | `<Suspense fallback={}>` | Wrap lazy components |
| `error.tsx` | `<ErrorBoundary>` | Class component or react-error-boundary |
| `not-found.tsx` | `<Route path="*">` | Catch-all route |
| Server Components | Client components + React Query | All rendering is client-side |
| `"use server"` actions | API calls + `useMutation` | Backend is a separate service |
| `revalidatePath()` | `queryClient.invalidateQueries()` | Cache invalidation |
| `next/link` (`<Link href>`) | `<Link to>` from react-router | `to` prop, not `href` |
| `next/image` | `<img>` with lazy loading | Or use `unpic-img` for optimization |
| `dynamic()` | `React.lazy()` + `<Suspense>` | Route-level code splitting |
| `useRouter().push()` | `useNavigate()` | Programmatic navigation |
| `usePathname()` | `useLocation().pathname` | Current URL path |
| `useSearchParams()` | `useSearchParams()` | Same name, different import |
| `redirect()` | `<Navigate to="" replace />` | In components |
| `middleware.ts` | Auth guard components | Route-level protection |
| `next/font` | `@font-face` in CSS | Or fontsource packages |
| `NEXT_PUBLIC_` env | `VITE_` env | `import.meta.env.VITE_*` |
| `getStaticParams` | N/A | SPAs don't pre-render |
| `generateMetadata` | `react-helmet-async` | Dynamic `<head>` management |
| `route.ts` API routes | Separate backend service | Express, Fastify, Hono, etc. |

---

## URL State Management

### Using `nuqs` (Works with Both Next.js and SPAs)

```bash
npm install nuqs
```

```tsx
import { useQueryState, parseAsInteger } from "nuqs"

function ProductList() {
  const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1))
  const [sort, setSort] = useQueryState("sort", { defaultValue: "name" })
  const [search, setSearch] = useQueryState("q", { defaultValue: "" })

  // URL: /products?page=2&sort=price&q=widget
  // All state is in the URL — shareable, bookmarkable, survives refresh
}
```

### Using React Router's useSearchParams

```tsx
import { useSearchParams } from "react-router"

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams()
  const page = Number(searchParams.get("page")) || 1
  const sort = searchParams.get("sort") || "name"

  const handlePageChange = (newPage: number) => {
    setSearchParams((prev) => {
      prev.set("page", String(newPage))
      return prev
    })
  }
}
```

**Prefer `nuqs`** — it handles parsing, defaults, and serialization with less boilerplate. Works in both Next.js and SPA contexts, making migration easier.

---

## Quick Reference

### Routing Checklist

- [ ] `BrowserRouter` wrapping the app in `main.tsx`
- [ ] Layouts use `<Outlet />` for child routes
- [ ] Route components lazy-loaded with `React.lazy()`
- [ ] `<Suspense>` wrapping lazy routes with skeleton fallback
- [ ] `<ErrorBoundary>` at layout level
- [ ] Protected routes with auth guard
- [ ] Catch-all `path="*"` for 404
- [ ] `NavLink` for navigation with active states
- [ ] SPA catch-all redirect configured on hosting platform

### Data Fetching Checklist

- [ ] React Query `QueryClientProvider` in app root
- [ ] Custom hooks per feature (`useMetrics`, `useUsers`, etc.)
- [ ] State trio (loading/error/empty) in every data component
- [ ] `useMutation` + `invalidateQueries` for writes
- [ ] API client with auth headers and error handling
- [ ] Optimistic updates for responsive mutations
