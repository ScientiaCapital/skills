/**
 * Enterprise SaaS dashboard layout — Sidebar + Header + Main
 *
 * Features:
 * - Collapsible sidebar on desktop, Sheet overlay on mobile
 * - Header with hamburger (mobile), breadcrumbs, Cmd+K search trigger, user menu
 * - Responsive: sidebar hidden below lg breakpoint
 * - Semantic HTML, skip link, keyboard accessible
 *
 * Dependencies:
 *   npx shadcn@latest add button sheet avatar dropdown-menu
 *   npm install lucide-react
 *
 * File structure suggestion:
 *   app/(dashboard)/layout.tsx  — use <DashboardLayout>
 *   app/(dashboard)/page.tsx    — main dashboard content
 */

// ── Types ────────────────────────────────────────────────────

import type { ReactNode } from "react"

interface NavItem {
  label: string
  href: string
  icon: React.ComponentType<{ className?: string }>
  badge?: string
}

interface DashboardLayoutProps {
  children: ReactNode
}

// ── Layout (Server Component) ────────────────────────────────

import {
  LayoutDashboard,
  Users,
  ShoppingCart,
  Package,
  Settings,
} from "lucide-react"

const navItems: NavItem[] = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Customers", href: "/dashboard/customers", icon: Users, badge: "12" },
  { label: "Orders", href: "/dashboard/orders", icon: ShoppingCart },
  { label: "Products", href: "/dashboard/products", icon: Package },
  { label: "Settings", href: "/dashboard/settings", icon: Settings },
]

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Skip link */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
      >
        Skip to main content
      </a>

      {/* Desktop sidebar — hidden on mobile */}
      <aside className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:bg-sidebar">
        <DesktopSidebar items={navItems} />
      </aside>

      {/* Main column */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <DashboardHeader items={navItems} />
        <main
          id="main-content"
          className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8"
        >
          {children}
        </main>
      </div>
    </div>
  )
}

// ── Desktop Sidebar (Server Component) ───────────────────────

function DesktopSidebar({ items }: { items: NavItem[] }) {
  return (
    <nav className="flex flex-1 flex-col" aria-label="Main navigation">
      {/* Logo */}
      <div className="flex h-16 items-center gap-2 border-b px-6">
        <div className="size-8 rounded-lg bg-primary" />
        <span className="text-lg font-semibold text-sidebar-foreground">
          Acme Inc
        </span>
      </div>

      {/* Nav items */}
      <div className="flex-1 space-y-1 px-3 py-4">
        <SidebarNavItems items={items} />
      </div>

      {/* Footer */}
      <div className="border-t px-3 py-4">
        <p className="px-3 text-xs text-muted-foreground">v1.0.0</p>
      </div>
    </nav>
  )
}

function SidebarNavItems({ items }: { items: NavItem[] }) {
  return (
    <ul className="space-y-1" role="list">
      {items.map((item) => (
        <li key={item.href}>
          <SidebarNavLink item={item} />
        </li>
      ))}
    </ul>
  )
}

function SidebarNavLink({ item }: { item: NavItem }) {
  // In production, replace with usePathname() check or a server-side prop
  const isActive = false

  return (
    <a
      href={item.href}
      className={`flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
        isActive
          ? "bg-sidebar-accent text-sidebar-accent-foreground"
          : "text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
      }`}
      aria-current={isActive ? "page" : undefined}
    >
      <item.icon className="size-5 shrink-0" />
      <span className="flex-1">{item.label}</span>
      {item.badge && (
        <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
          {item.badge}
        </span>
      )}
    </a>
  )
}

// ── Header (Client Component) ────────────────────────────────
// "use client" boundary is here — only the header needs interactivity

"use client"

import { useState } from "react"
import { Menu, Search, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

function DashboardHeader({ items }: { items: NavItem[] }) {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6">
      {/* Mobile hamburger */}
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetTrigger asChild>
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            aria-label="Open navigation menu"
          >
            <Menu className="size-5" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-72 p-0">
          <SheetHeader className="border-b px-6 py-4">
            <SheetTitle className="flex items-center gap-2">
              <div className="size-8 rounded-lg bg-primary" />
              Acme Inc
            </SheetTitle>
          </SheetHeader>
          <nav className="px-3 py-4" aria-label="Mobile navigation">
            <ul className="space-y-1" role="list">
              {items.map((item) => (
                <li key={item.href}>
                  <a
                    href={item.href}
                    onClick={() => setMobileOpen(false)}
                    className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-foreground/70 hover:bg-accent hover:text-accent-foreground"
                  >
                    <item.icon className="size-5 shrink-0" />
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </SheetContent>
      </Sheet>

      {/* Breadcrumbs */}
      <nav aria-label="Breadcrumb" className="hidden md:flex md:items-center md:gap-1.5 md:text-sm">
        <a
          href="/dashboard"
          className="text-muted-foreground hover:text-foreground"
        >
          Dashboard
        </a>
        <ChevronRight className="size-3.5 text-muted-foreground" />
        <span className="font-medium text-foreground">Overview</span>
      </nav>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Search trigger */}
      <Button
        variant="outline"
        className="hidden gap-2 text-muted-foreground md:flex"
        aria-label="Open search"
      >
        <Search className="size-4" />
        <span className="text-sm">Search...</span>
        <kbd className="pointer-events-none rounded border bg-muted px-1.5 py-0.5 text-[10px] font-medium text-muted-foreground">
          &#8984;K
        </kbd>
      </Button>

      {/* Mobile search (icon only) */}
      <Button
        variant="ghost"
        size="icon"
        className="md:hidden"
        aria-label="Open search"
      >
        <Search className="size-5" />
      </Button>

      {/* User menu */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            className="relative size-9 rounded-full"
            aria-label="User menu"
          >
            <Avatar className="size-9">
              <AvatarImage src="/avatars/user.png" alt="" />
              <AvatarFallback>TK</AvatarFallback>
            </Avatar>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-56">
          <DropdownMenuLabel>
            <p className="text-sm font-medium">Tim K</p>
            <p className="text-xs text-muted-foreground">tim@acme.com</p>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem asChild>
            <a href="/dashboard/settings">Settings</a>
          </DropdownMenuItem>
          <DropdownMenuItem asChild>
            <a href="/dashboard/billing">Billing</a>
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem className="text-destructive focus:text-destructive">
            Sign out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </header>
  )
}
