# Enterprise SaaS Dashboard Patterns

> Deep-dive reference for building production SaaS dashboards. Load when implementing
> dashboard layouts, KPI cards, charts, command palettes, notifications, RBAC UI,
> activity feeds, settings pages, or responsive collapse patterns.

---

## Table of Contents

1. [Dashboard Layout Architecture](#dashboard-layout-architecture)
2. [Sidebar Navigation](#sidebar-navigation)
3. [KPI Card Grid](#kpi-card-grid)
4. [Chart Integration (Recharts)](#chart-integration-recharts)
5. [Command Palette (cmdk)](#command-palette-cmdk)
6. [Notification System](#notification-system)
7. [RBAC UI Patterns](#rbac-ui-patterns)
8. [Activity Feed](#activity-feed)
9. [Settings Page](#settings-page)
10. [Responsive Collapse](#responsive-collapse)

---

## Dashboard Layout Architecture

The standard SaaS dashboard uses a three-zone layout: fixed sidebar, top header, and
scrollable main content area.

```tsx
// app/dashboard/layout.tsx
import { SidebarProvider } from "@/components/app/sidebar-context"
import { AppSidebar } from "@/components/app/app-sidebar"
import { DashboardHeader } from "@/components/app/dashboard-header"

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar — fixed width, full height */}
        <AppSidebar />

        {/* Main area — fills remaining space */}
        <div className="flex flex-1 flex-col overflow-hidden">
          <DashboardHeader />
          <main className="flex-1 overflow-y-auto p-6">
            {children}
          </main>
        </div>
      </div>
    </SidebarProvider>
  )
}
```

### CSS Considerations

```css
/* Ensure full viewport height, no scroll on outer container */
html, body { height: 100%; overflow: hidden; }

/* Main content scrolls independently */
main { scrollbar-gutter: stable; }
```

---

## Sidebar Navigation

### Collapsible Sidebar with Context

```tsx
// components/app/sidebar-context.tsx
"use client"

import { createContext, useContext, useState, useCallback } from "react"

type SidebarState = {
  collapsed: boolean
  toggle: () => void
  mobileOpen: boolean
  setMobileOpen: (open: boolean) => void
}

const SidebarContext = createContext<SidebarState | null>(null)

function SidebarProvider({ children }: { children: React.ReactNode }) {
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const toggle = useCallback(() => setCollapsed((c) => !c), [])

  return (
    <SidebarContext.Provider value={{ collapsed, toggle, mobileOpen, setMobileOpen }}>
      {children}
    </SidebarContext.Provider>
  )
}

function useSidebar() {
  const ctx = useContext(SidebarContext)
  if (!ctx) throw new Error("useSidebar must be used within SidebarProvider")
  return ctx
}

export { SidebarProvider, useSidebar }
```

### Sidebar Component

```tsx
"use client"

import { useSidebar } from "./sidebar-context"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard, Users, Settings, CreditCard, BarChart3,
  ChevronLeft, ChevronRight
} from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Sheet, SheetContent } from "@/components/ui/sheet"

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Analytics", href: "/dashboard/analytics", icon: BarChart3 },
  { label: "Customers", href: "/dashboard/customers", icon: Users },
  { label: "Billing", href: "/dashboard/billing", icon: CreditCard },
  { label: "Settings", href: "/dashboard/settings", icon: Settings },
]

function SidebarContent() {
  const { collapsed } = useSidebar()
  const pathname = usePathname()

  return (
    <div className="flex h-full flex-col">
      {/* Logo */}
      <div className="flex h-16 items-center border-b px-4">
        <span className={cn("font-bold text-lg transition-all", collapsed && "sr-only")}>
          Acme Inc
        </span>
      </div>

      {/* Nav items */}
      <nav className="flex-1 space-y-1 p-2" aria-label="Main navigation">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/")
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground/70",
                collapsed && "justify-center px-2"
              )}
              aria-current={isActive ? "page" : undefined}
            >
              <item.icon className="h-5 w-5 shrink-0" />
              <span className={cn("transition-all", collapsed && "sr-only")}>
                {item.label}
              </span>
            </Link>
          )
        })}
      </nav>

      {/* Collapse toggle */}
      <CollapseButton />
    </div>
  )
}

function CollapseButton() {
  const { collapsed, toggle } = useSidebar()
  return (
    <button
      onClick={toggle}
      className="flex items-center justify-center border-t p-3 text-sidebar-foreground/50 hover:text-sidebar-foreground"
      aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
    >
      {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
    </button>
  )
}

function AppSidebar() {
  const { collapsed, mobileOpen, setMobileOpen } = useSidebar()

  return (
    <>
      {/* Desktop sidebar */}
      <aside
        className={cn(
          "hidden lg:flex flex-col border-r bg-sidebar transition-all duration-200",
          collapsed ? "w-16" : "w-64"
        )}
      >
        <SidebarContent />
      </aside>

      {/* Mobile sidebar — Sheet overlay */}
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetContent side="left" className="w-64 p-0 bg-sidebar">
          <SidebarContent />
        </SheetContent>
      </Sheet>
    </>
  )
}

export { AppSidebar }
```

### Nested Route Groups

```tsx
const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  {
    label: "Analytics",
    icon: BarChart3,
    children: [
      { label: "Overview", href: "/dashboard/analytics" },
      { label: "Reports", href: "/dashboard/analytics/reports" },
      { label: "Funnels", href: "/dashboard/analytics/funnels" },
    ],
  },
]
```

Render nested items with an accordion/disclosure:

```tsx
{item.children ? (
  <Collapsible>
    <CollapsibleTrigger className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm">
      <item.icon className="h-5 w-5" />
      <span className="flex-1 text-left">{item.label}</span>
      <ChevronDown className="h-4 w-4 transition-transform [[data-state=open]>&]:rotate-180" />
    </CollapsibleTrigger>
    <CollapsibleContent className="ml-8 space-y-1">
      {item.children.map((child) => (
        <Link key={child.href} href={child.href} className="block rounded-md px-3 py-1.5 text-sm">
          {child.label}
        </Link>
      ))}
    </CollapsibleContent>
  </Collapsible>
) : (
  <Link href={item.href} className="...">...</Link>
)}
```

---

## KPI Card Grid

### Responsive Grid with Container Queries

```tsx
// components/app/dashboard/kpi-grid.tsx
import { KPICard } from "./kpi-card"

type Metric = {
  title: string
  value: string
  change: number
  changeLabel: string
  sparkline?: number[]
}

function KPIGrid({ metrics }: { metrics: Metric[] }) {
  return (
    <div className="@container">
      <div className="grid grid-cols-1 @sm:grid-cols-2 @xl:grid-cols-4 gap-4">
        {metrics.map((metric) => (
          <KPICard key={metric.title} {...metric} />
        ))}
      </div>
    </div>
  )
}

export { KPIGrid }
```

### KPI Card with Trend Indicator

```tsx
// components/app/dashboard/kpi-card.tsx
import { cn } from "@/lib/utils"
import { TrendingUp, TrendingDown, Minus } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

type KPICardProps = {
  title: string
  value: string
  change: number
  changeLabel: string
  sparkline?: number[]
}

function KPICard({ title, value, change, changeLabel, sparkline }: KPICardProps) {
  const trend = change > 0 ? "up" : change < 0 ? "down" : "flat"
  const TrendIcon = trend === "up" ? TrendingUp : trend === "down" ? TrendingDown : Minus

  return (
    <Card data-slot="kpi-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        <TrendIcon className={cn(
          "h-4 w-4",
          trend === "up" && "text-green-600",
          trend === "down" && "text-red-600",
          trend === "flat" && "text-muted-foreground",
        )} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className="flex items-center gap-2 mt-1">
          <span className={cn(
            "text-xs font-medium",
            trend === "up" && "text-green-600",
            trend === "down" && "text-red-600",
            trend === "flat" && "text-muted-foreground",
          )}>
            {change > 0 ? "+" : ""}{change}%
          </span>
          <span className="text-xs text-muted-foreground">{changeLabel}</span>
        </div>
        {sparkline && <Sparkline data={sparkline} className="mt-3 h-8" />}
      </CardContent>
    </Card>
  )
}

export { KPICard }
```

### Sparkline Component

```tsx
"use client"

function Sparkline({ data, className }: { data: number[]; className?: string }) {
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1
  const width = 100
  const height = 32

  const points = data
    .map((v, i) => {
      const x = (i / (data.length - 1)) * width
      const y = height - ((v - min) / range) * height
      return `${x},${y}`
    })
    .join(" ")

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className={cn("w-full", className)} preserveAspectRatio="none">
      <polyline fill="none" stroke="currentColor" strokeWidth="1.5" points={points} className="text-primary" />
    </svg>
  )
}

export { Sparkline }
```

---

## Chart Integration (Recharts)

### Setup

```bash
npm install recharts
```

Charts are always Client Components (they use DOM measurement and animation).

### Line Chart

```tsx
"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

type RevenuePoint = { month: string; revenue: number; target: number }

function RevenueChart({ data }: { data: RevenuePoint[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Revenue vs Target</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={data} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
            <XAxis dataKey="month" className="text-xs fill-muted-foreground" />
            <YAxis className="text-xs fill-muted-foreground" tickFormatter={(v) => `$${v / 1000}k`} />
            <Tooltip
              contentStyle={{
                backgroundColor: "var(--color-popover)",
                borderColor: "var(--color-border)",
                borderRadius: "var(--radius-md)",
                color: "var(--color-popover-foreground)",
              }}
            />
            <Legend />
            <Line type="monotone" dataKey="revenue" stroke="var(--color-chart-1)" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="target" stroke="var(--color-chart-2)" strokeWidth={2} strokeDasharray="5 5" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export { RevenueChart }
```

### Bar Chart

```tsx
"use client"

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

function UserGrowthChart({ data }: { data: { month: string; newUsers: number; churned: number }[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>User Growth</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
            <XAxis dataKey="month" className="text-xs fill-muted-foreground" />
            <YAxis className="text-xs fill-muted-foreground" />
            <Tooltip contentStyle={{ backgroundColor: "var(--color-popover)", borderColor: "var(--color-border)", borderRadius: "var(--radius-md)" }} />
            <Bar dataKey="newUsers" fill="var(--color-chart-1)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="churned" fill="var(--color-chart-5)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}

export { UserGrowthChart }
```

### Area Chart and Pie Chart

```tsx
"use client"

import { AreaChart, Area, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"

// Area chart — good for showing volume over time
function TrafficChart({ data }: { data: { date: string; visits: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data}>
        <XAxis dataKey="date" className="text-xs fill-muted-foreground" />
        <YAxis className="text-xs fill-muted-foreground" />
        <Tooltip contentStyle={{ backgroundColor: "var(--color-popover)", borderColor: "var(--color-border)", borderRadius: "var(--radius-md)" }} />
        <Area type="monotone" dataKey="visits" stroke="var(--color-chart-1)" fill="var(--color-chart-1)" fillOpacity={0.2} />
      </AreaChart>
    </ResponsiveContainer>
  )
}

// Pie chart — good for proportional breakdown
const COLORS = ["var(--color-chart-1)", "var(--color-chart-2)", "var(--color-chart-3)", "var(--color-chart-4)"]

function PlanDistribution({ data }: { data: { name: string; value: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={2} dataKey="value">
          {data.map((_, i) => (
            <Cell key={i} fill={COLORS[i % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip contentStyle={{ backgroundColor: "var(--color-popover)", borderColor: "var(--color-border)", borderRadius: "var(--radius-md)" }} />
      </PieChart>
    </ResponsiveContainer>
  )
}

export { TrafficChart, PlanDistribution }
```

---

## Command Palette (cmdk)

### Setup

```bash
npx shadcn@latest add command
# Installs cmdk under the hood
```

### Global Cmd+K Trigger

```tsx
"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import {
  CommandDialog, CommandInput, CommandList, CommandEmpty,
  CommandGroup, CommandItem, CommandSeparator, CommandShortcut
} from "@/components/ui/command"
import { LayoutDashboard, Users, Settings, CreditCard, Search, FileText } from "lucide-react"

const navCommands = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard, group: "Navigation" },
  { label: "Customers", href: "/dashboard/customers", icon: Users, group: "Navigation" },
  { label: "Billing", href: "/dashboard/billing", icon: CreditCard, group: "Navigation" },
  { label: "Settings", href: "/dashboard/settings", icon: Settings, group: "Navigation" },
]

function CommandPalette() {
  const [open, setOpen] = useState(false)
  const router = useRouter()

  // Global keyboard shortcut
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault()
        setOpen((o) => !o)
      }
    }
    document.addEventListener("keydown", onKeyDown)
    return () => document.removeEventListener("keydown", onKeyDown)
  }, [])

  function runCommand(command: () => void) {
    setOpen(false)
    command()
  }

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>

        <CommandGroup heading="Navigation">
          {navCommands.map((cmd) => (
            <CommandItem
              key={cmd.href}
              onSelect={() => runCommand(() => router.push(cmd.href))}
              className="flex items-center gap-2"
            >
              <cmd.icon className="h-4 w-4 text-muted-foreground" />
              <span>{cmd.label}</span>
            </CommandItem>
          ))}
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Actions">
          <CommandItem onSelect={() => runCommand(() => router.push("/dashboard/customers/new"))}>
            <Users className="mr-2 h-4 w-4" />
            <span>Create Customer</span>
            <CommandShortcut>Ctrl+N</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/dashboard/reports/new"))}>
            <FileText className="mr-2 h-4 w-4" />
            <span>Generate Report</span>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}

export { CommandPalette }
```

### Header Search Trigger

```tsx
function SearchButton() {
  return (
    <button
      onClick={() => document.dispatchEvent(new KeyboardEvent("keydown", { key: "k", metaKey: true }))}
      className="flex items-center gap-2 rounded-md border bg-background px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent"
    >
      <Search className="h-4 w-4" />
      <span className="hidden sm:inline">Search...</span>
      <kbd className="ml-auto hidden rounded bg-muted px-1.5 py-0.5 text-xs font-mono sm:inline">
        Cmd+K
      </kbd>
    </button>
  )
}
```

---

## Notification System

### Bell Icon with Dropdown

```tsx
"use client"

import { useState } from "react"
import { Bell, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"

type Notification = {
  id: string
  title: string
  body: string
  read: boolean
  createdAt: Date
}

function NotificationBell({ notifications }: { notifications: Notification[] }) {
  const [items, setItems] = useState(notifications)
  const unreadCount = items.filter((n) => !n.read).length

  function markRead(id: string) {
    setItems((prev) => prev.map((n) => (n.id === id ? { ...n, read: true } : n)))
  }

  function markAllRead() {
    setItems((prev) => prev.map((n) => ({ ...n, read: true })))
  }

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="ghost" size="icon" className="relative" aria-label={`Notifications (${unreadCount} unread)`}>
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-destructive text-xs text-destructive-foreground">
              {unreadCount > 9 ? "9+" : unreadCount}
            </span>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-80 p-0">
        <div className="flex items-center justify-between border-b px-4 py-3">
          <h3 className="text-sm font-semibold">Notifications</h3>
          {unreadCount > 0 && (
            <button onClick={markAllRead} className="text-xs text-primary hover:underline">
              Mark all read
            </button>
          )}
        </div>
        <ScrollArea className="h-80">
          {items.length === 0 ? (
            <p className="p-4 text-center text-sm text-muted-foreground">No notifications</p>
          ) : (
            items.map((n) => (
              <button
                key={n.id}
                onClick={() => markRead(n.id)}
                className={cn(
                  "flex w-full gap-3 border-b p-4 text-left text-sm transition-colors hover:bg-accent",
                  !n.read && "bg-primary/5"
                )}
              >
                <div className="flex-1">
                  <p className={cn("font-medium", !n.read && "text-foreground")}>{n.title}</p>
                  <p className="text-muted-foreground line-clamp-2">{n.body}</p>
                  <p className="mt-1 text-xs text-muted-foreground">
                    {formatRelativeDate(n.createdAt)}
                  </p>
                </div>
                {!n.read && <div className="mt-1 h-2 w-2 shrink-0 rounded-full bg-primary" />}
              </button>
            ))
          )}
        </ScrollArea>
      </PopoverContent>
    </Popover>
  )
}

function formatRelativeDate(date: Date): string {
  const now = new Date()
  const diffMs = now.getTime() - date.getTime()
  const diffMin = Math.floor(diffMs / 60_000)
  if (diffMin < 1) return "Just now"
  if (diffMin < 60) return `${diffMin}m ago`
  const diffHr = Math.floor(diffMin / 60)
  if (diffHr < 24) return `${diffHr}h ago`
  const diffDay = Math.floor(diffHr / 24)
  if (diffDay < 7) return `${diffDay}d ago`
  return date.toLocaleDateString()
}

export { NotificationBell }
```

### Real-Time Updates (SSE or WebSocket)

```tsx
"use client"

import { useEffect, useState } from "react"

function useNotifications(userId: string) {
  const [notifications, setNotifications] = useState<Notification[]>([])

  useEffect(() => {
    const eventSource = new EventSource(`/api/notifications/stream?userId=${userId}`)

    eventSource.onmessage = (event) => {
      const notification: Notification = JSON.parse(event.data)
      setNotifications((prev) => [notification, ...prev])
    }

    return () => eventSource.close()
  }, [userId])

  return notifications
}
```

---

## RBAC UI Patterns

### Permission-Based Navigation

```tsx
type NavItem = {
  label: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  requiredPermission?: string
}

const navItems: NavItem[] = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Customers", href: "/dashboard/customers", icon: Users, requiredPermission: "customers:read" },
  { label: "Billing", href: "/dashboard/billing", icon: CreditCard, requiredPermission: "billing:read" },
  { label: "Admin", href: "/dashboard/admin", icon: Settings, requiredPermission: "admin:access" },
]

function FilteredNav({ userPermissions }: { userPermissions: string[] }) {
  const visibleItems = navItems.filter(
    (item) => !item.requiredPermission || userPermissions.includes(item.requiredPermission)
  )

  return (
    <nav aria-label="Main navigation">
      {visibleItems.map((item) => (
        <Link key={item.href} href={item.href} className="flex items-center gap-2 px-3 py-2 rounded-md">
          <item.icon className="h-5 w-5" />
          {item.label}
        </Link>
      ))}
    </nav>
  )
}
```

### Permission Guard Component

```tsx
// lib/permissions.ts
type Permission = string
type Role = "admin" | "manager" | "member" | "viewer"

const rolePermissions: Record<Role, Permission[]> = {
  admin: ["*"],
  manager: ["customers:read", "customers:write", "billing:read", "reports:read", "reports:write"],
  member: ["customers:read", "reports:read"],
  viewer: ["reports:read"],
}

function hasPermission(userRole: Role, permission: Permission): boolean {
  const perms = rolePermissions[userRole]
  return perms.includes("*") || perms.includes(permission)
}

export { hasPermission, type Role, type Permission }
```

```tsx
// components/app/permission-gate.tsx
import { hasPermission, type Role, type Permission } from "@/lib/permissions"

function PermissionGate({
  role,
  permission,
  children,
  fallback = null,
}: {
  role: Role
  permission: Permission
  children: React.ReactNode
  fallback?: React.ReactNode
}) {
  if (!hasPermission(role, permission)) return <>{fallback}</>
  return <>{children}</>
}

// Usage
<PermissionGate role={user.role} permission="billing:write">
  <Button>Upgrade Plan</Button>
</PermissionGate>
```

### Admin Panel Section

```tsx
function AdminPanel({ role }: { role: Role }) {
  if (!hasPermission(role, "admin:access")) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Administration</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Team Members</p>
            <p className="text-sm text-muted-foreground">Manage roles and invitations</p>
          </div>
          <Button variant="outline" asChild>
            <Link href="/dashboard/admin/team">Manage</Link>
          </Button>
        </div>
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">API Keys</p>
            <p className="text-sm text-muted-foreground">Create and revoke API access</p>
          </div>
          <Button variant="outline" asChild>
            <Link href="/dashboard/admin/api-keys">Manage</Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
```

---

## Activity Feed

### Timeline Component

```tsx
import { cn } from "@/lib/utils"

type ActivityItem = {
  id: string
  user: { name: string; avatarUrl: string }
  action: string
  target: string
  createdAt: Date
}

function ActivityFeed({ items }: { items: ActivityItem[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-0">
          {items.map((item, index) => (
            <div key={item.id} className="flex gap-3 pb-6 last:pb-0">
              {/* Timeline line + avatar */}
              <div className="flex flex-col items-center">
                <img
                  src={item.user.avatarUrl}
                  alt={item.user.name}
                  className="h-8 w-8 rounded-full ring-2 ring-background"
                />
                {index < items.length - 1 && (
                  <div className="mt-2 w-px flex-1 bg-border" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 pt-0.5">
                <p className="text-sm">
                  <span className="font-medium">{item.user.name}</span>
                  {" "}{item.action}{" "}
                  <span className="font-medium">{item.target}</span>
                </p>
                <time className="text-xs text-muted-foreground" dateTime={item.createdAt.toISOString()}>
                  {formatRelativeDate(item.createdAt)}
                </time>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export { ActivityFeed }
```

---

## Settings Page

### Tabs Layout with Form Sections

```tsx
// app/dashboard/settings/page.tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ProfileForm } from "./profile-form"
import { TeamSettings } from "./team-settings"
import { BillingSettings } from "./billing-settings"
import { DangerZone } from "./danger-zone"

export default function SettingsPage() {
  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-muted-foreground">Manage your account and preferences.</p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="team">Team</TabsTrigger>
          <TabsTrigger value="billing">Billing</TabsTrigger>
          <TabsTrigger value="danger">Danger Zone</TabsTrigger>
        </TabsList>

        <TabsContent value="profile"><ProfileForm /></TabsContent>
        <TabsContent value="team"><TeamSettings /></TabsContent>
        <TabsContent value="billing"><BillingSettings /></TabsContent>
        <TabsContent value="danger"><DangerZone /></TabsContent>
      </Tabs>
    </div>
  )
}
```

### Danger Zone Section

```tsx
"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent,
  AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
  AlertDialogTrigger } from "@/components/ui/alert-dialog"
import { Input } from "@/components/ui/input"

function DangerZone() {
  const [confirmText, setConfirmText] = useState("")
  const canDelete = confirmText === "DELETE"

  return (
    <Card className="border-destructive/50">
      <CardHeader>
        <CardTitle className="text-destructive">Danger Zone</CardTitle>
        <CardDescription>Irreversible actions that affect your entire account.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Export data */}
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Export all data</p>
            <p className="text-sm text-muted-foreground">Download a complete archive of your data.</p>
          </div>
          <Button variant="outline">Export</Button>
        </div>

        {/* Delete account */}
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Delete account</p>
            <p className="text-sm text-muted-foreground">Permanently delete your account and all data.</p>
          </div>
          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="destructive">Delete Account</Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                <AlertDialogDescription>
                  This action cannot be undone. This will permanently delete your account
                  and remove all associated data from our servers.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <div className="space-y-2">
                <p className="text-sm font-medium">Type DELETE to confirm:</p>
                <Input
                  value={confirmText}
                  onChange={(e) => setConfirmText(e.target.value)}
                  placeholder="DELETE"
                />
              </div>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction disabled={!canDelete} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                  Delete Account
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </CardContent>
    </Card>
  )
}

export { DangerZone }
```

---

## Responsive Collapse

### Sidebar to Sheet on Mobile

The sidebar component above already implements this: `hidden lg:flex` for the desktop
sidebar, `Sheet` for mobile. The header triggers the mobile sheet.

```tsx
// components/app/dashboard-header.tsx
"use client"

import { Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useSidebar } from "./sidebar-context"
import { NotificationBell } from "./notification-bell"
import { SearchButton } from "./search-button"
import { UserNav } from "./user-nav"

function DashboardHeader() {
  const { setMobileOpen } = useSidebar()

  return (
    <header className="flex h-16 items-center gap-4 border-b bg-background px-4 lg:px-6">
      {/* Mobile menu trigger — hidden on desktop */}
      <Button variant="ghost" size="icon" className="lg:hidden" onClick={() => setMobileOpen(true)}
        aria-label="Open navigation menu">
        <Menu className="h-5 w-5" />
      </Button>

      {/* Search */}
      <div className="flex-1">
        <SearchButton />
      </div>

      {/* Right side actions */}
      <div className="flex items-center gap-2">
        <NotificationBell notifications={[]} />
        <UserNav />
      </div>
    </header>
  )
}

export { DashboardHeader }
```

### KPI Grid Stacking

```tsx
{/* 1 column on mobile, 2 on medium containers, 4 on large */}
<div className="@container">
  <div className="grid grid-cols-1 @sm:grid-cols-2 @xl:grid-cols-4 gap-4">
    <KPICard title="Revenue" value="$45,231" change={12.5} changeLabel="vs last month" />
    <KPICard title="Customers" value="2,350" change={3.2} changeLabel="vs last month" />
    <KPICard title="MRR" value="$12,450" change={-1.8} changeLabel="vs last month" />
    <KPICard title="Churn" value="2.4%" change={-0.5} changeLabel="vs last month" />
  </div>
</div>
```

### Charts: Side by Side to Stacked

```tsx
{/* 2 columns on large viewport, stacked on mobile */}
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
  <RevenueChart data={revenueData} />
  <UserGrowthChart data={growthData} />
</div>
```

### Complete Dashboard Page

```tsx
// app/dashboard/page.tsx
export default async function DashboardPage() {
  const [metrics, revenue, growth, activities] = await Promise.all([
    getMetrics(),
    getRevenueData(),
    getGrowthData(),
    getRecentActivities(),
  ])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Overview of your business metrics.</p>
      </div>

      {/* KPI cards — responsive grid */}
      <KPIGrid metrics={metrics} />

      {/* Charts row — 2-up on desktop, stacked on mobile */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RevenueChart data={revenue} />
        <UserGrowthChart data={growth} />
      </div>

      {/* Bottom row — table + activity feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RecentCustomersTable />
        </div>
        <ActivityFeed items={activities} />
      </div>
    </div>
  )
}
```
