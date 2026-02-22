// SPA App Layout Template — Vite + React Router v7
// Usage: Adapt this as your App.tsx root component
//
// Includes:
// - BrowserRouter setup with providers
// - Dashboard layout with sidebar (same pattern as Next.js template)
// - React.lazy() code splitting per route
// - Protected route wrapper
// - Error boundary

import { StrictMode, lazy, Suspense, Component, type ReactNode } from "react"
import { BrowserRouter, Routes, Route, Navigate, Outlet, NavLink, useLocation } from "react-router"
import { QueryClientProvider, QueryClient } from "@tanstack/react-query"
import { cn } from "@/lib/utils"
import { Toaster } from "@/components/ui/sonner"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import {
  LayoutDashboard, Settings, BarChart3, Users, AlertCircle,
} from "lucide-react"

// ---------------------------------------------------------------------------
// Lazy-loaded route components (each becomes a separate chunk)
// ---------------------------------------------------------------------------
const Dashboard = lazy(() => import("@/pages/Dashboard"))
const Analytics = lazy(() => import("@/pages/Analytics"))
const Team = lazy(() => import("@/pages/Team"))
const SettingsPage = lazy(() => import("@/pages/Settings"))
const Login = lazy(() => import("@/pages/auth/Login"))

// ---------------------------------------------------------------------------
// Query client
// ---------------------------------------------------------------------------
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 5 * 60_000, retry: 1, refetchOnWindowFocus: false },
  },
})

// ---------------------------------------------------------------------------
// Error Boundary
// ---------------------------------------------------------------------------
interface ErrorBoundaryState { hasError: boolean; error: Error | null }

class ErrorBoundary extends Component<{ children: ReactNode }, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  render() {
    if (!this.state.hasError) return this.props.children
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
        <AlertCircle className="h-12 w-12 text-destructive" />
        <h2 className="text-xl font-semibold">Something went wrong</h2>
        <p className="text-muted-foreground text-sm">{this.state.error?.message}</p>
        <Button variant="outline" onClick={() => window.location.reload()}>
          Reload page
        </Button>
      </div>
    )
  }
}

// ---------------------------------------------------------------------------
// Protected Route (replace useAuth with your auth hook)
// ---------------------------------------------------------------------------
function ProtectedRoute() {
  // TODO: Replace with your auth hook
  // const { user, isLoading } = useAuth()
  const user = true // placeholder
  const isLoading = false // placeholder
  const location = useLocation()

  if (isLoading) return <PageSkeleton />
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />
  return <Outlet />
}

// ---------------------------------------------------------------------------
// Page Skeleton (loading fallback)
// ---------------------------------------------------------------------------
function PageSkeleton() {
  return (
    <div className="p-6 space-y-4">
      <Skeleton className="h-8 w-48" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
      </div>
      <Skeleton className="h-64" />
    </div>
  )
}

// ---------------------------------------------------------------------------
// Sidebar
// ---------------------------------------------------------------------------
const navItems = [
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/dashboard/analytics", icon: BarChart3, label: "Analytics" },
  { to: "/dashboard/team", icon: Users, label: "Team" },
  { to: "/dashboard/settings", icon: Settings, label: "Settings" },
]

function Sidebar() {
  return (
    <aside className="w-64 hidden lg:flex border-r bg-card flex-col">
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
                  : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
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

// ---------------------------------------------------------------------------
// Dashboard Layout
// ---------------------------------------------------------------------------
function DashboardLayout() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-14 border-b flex items-center px-6 bg-card">
          <span className="text-sm font-medium">Header — search, user menu, notifications</span>
        </header>
        <main className="flex-1 overflow-auto p-6">
          <ErrorBoundary>
            <Suspense fallback={<PageSkeleton />}>
              <Outlet />
            </Suspense>
          </ErrorBoundary>
        </main>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// App (Root)
// ---------------------------------------------------------------------------
export default function App() {
  return (
    <StrictMode>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={
              <Suspense fallback={<PageSkeleton />}><Login /></Suspense>
            } />

            {/* Protected routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="dashboard" element={<DashboardLayout />}>
                <Route index element={<Dashboard />} />
                <Route path="analytics" element={<Analytics />} />
                <Route path="team" element={<Team />} />
                <Route path="settings" element={<SettingsPage />} />
              </Route>
            </Route>

            {/* Redirects */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
          <Toaster />
        </BrowserRouter>
      </QueryClientProvider>
    </StrictMode>
  )
}
