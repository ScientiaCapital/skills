# WCAG 2.1 AA Accessibility Checklist

## Per-Component ARIA Patterns

### Dialog / Modal

```tsx
"use client"

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

function ConfirmDeleteDialog({ onConfirm }: { onConfirm: () => void }) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete project</Button>
      </DialogTrigger>
      {/* Focus trapped automatically by Radix. Escape closes. Focus restored on close. */}
      <DialogContent aria-describedby="delete-desc">
        <DialogHeader>
          <DialogTitle>Delete this project?</DialogTitle>
          <DialogDescription id="delete-desc">
            This action cannot be undone. All data will be permanently removed.
          </DialogDescription>
        </DialogHeader>
        <div className="flex justify-end gap-3 pt-4">
          <DialogTrigger asChild>
            <Button variant="outline">Cancel</Button>
          </DialogTrigger>
          <Button variant="destructive" onClick={onConfirm}>
            Yes, delete
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

**Rules:**
- `aria-labelledby` points to the title (Radix does this automatically)
- `aria-describedby` points to the description
- Focus moves into modal on open, returns to trigger on close
- Escape closes the dialog
- Click outside closes (configurable via `onInteractOutside`)

### Combobox / Autocomplete

```tsx
"use client"

import { useState } from "react"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { CheckIcon, ChevronsUpDownIcon } from "lucide-react"
import { cn } from "@/lib/utils"

const FRAMEWORKS = [
  { value: "next", label: "Next.js" },
  { value: "remix", label: "Remix" },
  { value: "astro", label: "Astro" },
]

function ComboboxDemo() {
  const [open, setOpen] = useState(false)
  const [value, setValue] = useState("")

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          aria-label="Select framework"
          className="w-[200px] justify-between"
        >
          {value ? FRAMEWORKS.find((f) => f.value === value)?.label : "Select framework..."}
          <ChevronsUpDownIcon className="ml-2 size-4 opacity-50" aria-hidden="true" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search framework..." />
          <CommandList>
            <CommandEmpty>No framework found.</CommandEmpty>
            <CommandGroup>
              {FRAMEWORKS.map((fw) => (
                <CommandItem
                  key={fw.value}
                  value={fw.value}
                  onSelect={(v) => { setValue(v); setOpen(false) }}
                >
                  <CheckIcon className={cn("mr-2 size-4", value === fw.value ? "opacity-100" : "opacity-0")} />
                  {fw.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
```

**Rules:**
- `role="combobox"` on the trigger with `aria-expanded`
- Arrow keys navigate options, Enter selects, Escape closes
- Type-ahead filters the list
- Selected item announced with checkmark visual + screen reader text

### Tabs

```tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

function SettingsTabs() {
  return (
    <Tabs defaultValue="general">
      {/* role="tablist" applied automatically */}
      <TabsList aria-label="Settings sections">
        {/* role="tab" + aria-selected applied automatically */}
        <TabsTrigger value="general">General</TabsTrigger>
        <TabsTrigger value="security">Security</TabsTrigger>
        <TabsTrigger value="billing">Billing</TabsTrigger>
      </TabsList>
      {/* role="tabpanel" applied automatically */}
      <TabsContent value="general">General settings...</TabsContent>
      <TabsContent value="security">Security settings...</TabsContent>
      <TabsContent value="billing">Billing settings...</TabsContent>
    </Tabs>
  )
}
```

**Rules:**
- Left/Right arrow keys move between tabs (Radix handles this)
- Home/End move to first/last tab
- Tab key moves focus into the active panel (not between tabs)
- `aria-label` on TabsList provides context

### Menu / Dropdown

```tsx
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { MoreHorizontalIcon } from "lucide-react"

function RowActions({ itemName }: { itemName: string }) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" aria-label={`Actions for ${itemName}`}>
          <MoreHorizontalIcon className="size-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>Actions</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem>Edit</DropdownMenuItem>
        <DropdownMenuItem>Duplicate</DropdownMenuItem>
        <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

**Rules:**
- Arrow keys navigate items, Enter activates, Escape closes
- Trigger has descriptive `aria-label` (not just an icon)
- Destructive items visually distinct (color) and ideally confirm before acting

### Toast / Notification

```tsx
// Sonner integration — accessible by default
import { toast } from "sonner"

// Success
toast.success("Project saved successfully")

// Error with action
toast.error("Failed to save", {
  description: "Check your connection and try again.",
  action: {
    label: "Retry",
    onClick: () => handleRetry(),
  },
})
```

**Rules:**
- Sonner uses `role="status"` and `aria-live="polite"` automatically
- Errors should include recovery action when possible
- Do not rely on toast alone for critical errors (show inline too)
- Auto-dismiss: 4-5s for info, longer or manual dismiss for errors

### Tooltip

```tsx
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

function InfoTooltip({ label, content }: { label: string; content: string }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          {/* Must be a focusable element */}
          <button aria-label={label} className="text-muted-foreground">
            <span aria-hidden="true">?</span>
          </button>
        </TooltipTrigger>
        <TooltipContent>
          <p>{content}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
```

**Rules:**
- Trigger must be focusable (button, link, input)
- Shows on hover AND focus
- `role="tooltip"` applied automatically by Radix
- Escape dismisses without closing parent
- Do not put interactive content inside tooltips (use Popover instead)

### Data Table

```tsx
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

function UsersTable({ users }: { users: User[] }) {
  return (
    <div role="region" aria-label="Users table" tabIndex={0} className="overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead scope="col">Name</TableHead>
            <TableHead scope="col">Email</TableHead>
            <TableHead scope="col">Role</TableHead>
            <TableHead scope="col">
              <span className="sr-only">Actions</span>
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center text-muted-foreground">
                No users found.
              </TableCell>
            </TableRow>
          ) : (
            users.map((user) => (
              <TableRow key={user.id}>
                <TableCell className="font-medium">{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.role}</TableCell>
                <TableCell>
                  <RowActions itemName={user.name} />
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}
```

**Rules:**
- `scope="col"` on header cells
- Scrollable containers get `role="region"`, `aria-label`, and `tabIndex={0}`
- Actions column has `sr-only` heading
- Empty state announced in table body
- Sortable columns: `aria-sort="ascending|descending|none"` on `<th>`

---

## Keyboard Navigation Patterns

| Pattern | Keys | Behavior |
|---------|------|----------|
| Tab order | `Tab` / `Shift+Tab` | Moves between focusable elements in DOM order |
| Arrow navigation | `ArrowUp/Down/Left/Right` | Moves within composite widgets (tabs, menus, listbox) |
| Activate | `Enter` or `Space` | Clicks buttons/links, selects options |
| Close/dismiss | `Escape` | Closes modals, menus, popovers, tooltips |
| First/last | `Home` / `End` | Moves to first/last item in list/tab group |
| Skip link | `Tab` (first element) | Jumps past navigation to main content |

### Skip Link

```tsx
// app/layout.tsx — first child inside <body>
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-background focus:px-4 focus:py-2 focus:shadow-lg"
>
  Skip to main content
</a>
{/* ... nav, header ... */}
<main id="main-content" tabIndex={-1}>
  {children}
</main>
```

---

## Focus Management

### Focus Trap in Modals

Radix Dialog handles this automatically. For custom modals:

```tsx
"use client"

import { useEffect, useRef } from "react"

function useFocusTrap(isOpen: boolean) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isOpen || !containerRef.current) return

    const focusableSelector = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    const focusable = containerRef.current.querySelectorAll<HTMLElement>(focusableSelector)
    const first = focusable[0]
    const last = focusable[focusable.length - 1]

    // Store previously focused element
    const previouslyFocused = document.activeElement as HTMLElement
    first?.focus()

    function handleKeyDown(e: KeyboardEvent) {
      if (e.key !== "Tab") return

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault()
        last?.focus()
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault()
        first?.focus()
      }
    }

    document.addEventListener("keydown", handleKeyDown)
    return () => {
      document.removeEventListener("keydown", handleKeyDown)
      previouslyFocused?.focus() // Restore focus on close
    }
  }, [isOpen])

  return containerRef
}
```

### Roving Tabindex

For toolbar, tab list, or radio group where arrow keys navigate:

```tsx
"use client"

import { useState, type KeyboardEvent } from "react"

function Toolbar({ items }: { items: { id: string; label: string }[] }) {
  const [activeIndex, setActiveIndex] = useState(0)

  function handleKeyDown(e: KeyboardEvent) {
    let next = activeIndex
    if (e.key === "ArrowRight") next = (activeIndex + 1) % items.length
    if (e.key === "ArrowLeft") next = (activeIndex - 1 + items.length) % items.length
    if (e.key === "Home") next = 0
    if (e.key === "End") next = items.length - 1

    if (next !== activeIndex) {
      e.preventDefault()
      setActiveIndex(next)
      document.getElementById(`toolbar-${items[next].id}`)?.focus()
    }
  }

  return (
    <div role="toolbar" aria-label="Formatting" onKeyDown={handleKeyDown}>
      {items.map((item, i) => (
        <button
          key={item.id}
          id={`toolbar-${item.id}`}
          tabIndex={i === activeIndex ? 0 : -1}
          aria-pressed={false}
        >
          {item.label}
        </button>
      ))}
    </div>
  )
}
```

---

## Screen Reader Testing

### VoiceOver (macOS)

| Command | Action |
|---------|--------|
| `Cmd + F5` | Toggle VoiceOver on/off |
| `VO + Right` (`Ctrl+Option+Right`) | Next element |
| `VO + Space` | Activate element |
| `VO + U` | Open rotor (headings, links, landmarks) |
| `VO + Shift + Down` | Enter group/table |

### Testing Checklist

1. **Navigate headings** (rotor): Logical hierarchy? Missing levels?
2. **Navigate landmarks** (rotor): `<header>`, `<nav>`, `<main>`, `<footer>` all present?
3. **Read through page**: All content announced? Decorative images skipped?
4. **Interact with forms**: Labels read? Errors announced? Required fields indicated?
5. **Test dynamic content**: Toasts announced? Loading states communicated?

### Live Region Patterns

```tsx
// Polite: announce when idle (status updates, toasts)
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Assertive: interrupt immediately (errors only)
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>

// Loading announcement
<div aria-live="polite">
  {isLoading ? "Loading results..." : `${count} results found`}
</div>
```

---

## Color and Contrast

### OKLCH-Based Contrast Checking

Tailwind v4 uses OKLCH. The lightness channel (L) determines contrast:

| Requirement | Ratio | OKLCH Guidance |
|-------------|-------|----------------|
| Body text | >= 4.5:1 | L difference >= 0.40 from background |
| Large text (18px+ bold, 24px+) | >= 3:1 | L difference >= 0.30 |
| UI components (borders, icons) | >= 3:1 | L difference >= 0.30 |
| Focus indicators | >= 3:1 | Use distinct color, not just lightness |

```css
@theme inline {
  /* Light mode: L=1.0 background, L<=0.40 for text */
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);        /* Ratio ~15:1 */
  --color-muted-foreground: oklch(0.40 0 0);   /* Ratio ~4.6:1 — barely passing */

  /* Dark mode: L=0.10 background, L>=0.65 for text */
  --color-background: oklch(0.10 0 0);
  --color-foreground: oklch(0.95 0 0);
  --color-muted-foreground: oklch(0.65 0 0);
}
```

### Do Not Rely on Color Alone

```tsx
// Bad: color is the only indicator
<span className={error ? "text-red-500" : "text-green-500"}>
  {status}
</span>

// Good: color + icon + text
<span className={cn("flex items-center gap-1", error ? "text-destructive" : "text-green-600")}>
  {error ? <XCircleIcon className="size-4" /> : <CheckCircleIcon className="size-4" />}
  {error ? "Failed" : "Success"}
</span>
```

---

## Motion and Animation

### Respect Reduced Motion

```css
/* globals.css — global safety net */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

```tsx
// Component-level check
"use client"

import { useEffect, useState } from "react"

function usePrefersReducedMotion() {
  const [prefers, setPrefers] = useState(false)

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)")
    setPrefers(mq.matches)
    const handler = (e: MediaQueryListEvent) => setPrefers(e.matches)
    mq.addEventListener("change", handler)
    return () => mq.removeEventListener("change", handler)
  }, [])

  return prefers
}

// Usage: skip animation if user prefers reduced motion
function AnimatedCounter({ value }: { value: number }) {
  const reducedMotion = usePrefersReducedMotion()
  // If reduced motion: show value immediately, no counting animation
  if (reducedMotion) return <span>{value}</span>
  return <CountUpAnimation target={value} />
}
```

---

## Forms Accessibility

```tsx
// Accessible form with shadcn Form
<FormField
  control={form.control}
  name="email"
  render={({ field }) => (
    <FormItem>
      {/* <label> with htmlFor handled automatically */}
      <FormLabel>Email address</FormLabel>
      <FormControl>
        {/* aria-invalid, aria-describedby auto-wired by shadcn Form */}
        <Input placeholder="you@example.com" type="email" {...field} />
      </FormControl>
      <FormDescription>We will never share your email.</FormDescription>
      {/* role="alert" on error message */}
      <FormMessage />
    </FormItem>
  )}
/>
```

### Required Fields

```tsx
<FormLabel>
  Email <span aria-hidden="true" className="text-destructive">*</span>
  <span className="sr-only">(required)</span>
</FormLabel>
<Input required aria-required="true" {...field} />
```

### Error Summary

```tsx
function ErrorSummary({ errors }: { errors: Record<string, { message: string }> }) {
  const errorList = Object.entries(errors)
  if (errorList.length === 0) return null

  return (
    <div role="alert" className="rounded-md border border-destructive bg-destructive/10 p-4">
      <p className="font-medium text-destructive">
        Please fix {errorList.length} error{errorList.length > 1 ? "s" : ""}:
      </p>
      <ul className="mt-2 list-disc pl-5 text-sm text-destructive">
        {errorList.map(([field, error]) => (
          <li key={field}>
            <a href={`#${field}`} className="underline">{error.message}</a>
          </li>
        ))}
      </ul>
    </div>
  )
}
```

---

## Images and Media

### Alt Text Rules

| Image Type | Alt Text |
|-----------|----------|
| Informative | Describe the content: `alt="Revenue chart showing 40% growth"` |
| Decorative | Empty alt: `alt=""` (screen reader skips it) |
| Functional (link/button) | Describe the action: `alt="Download PDF report"` |
| Complex (chart/graph) | Short alt + longer `aria-describedby` or adjacent text |
| User avatar | `alt="Profile photo of {name}"` or `alt=""` if name shown nearby |

```tsx
import Image from "next/image"

// Informative
<Image src="/hero.jpg" alt="Team collaborating in an office" width={800} height={400} />

// Decorative
<Image src="/pattern.svg" alt="" width={200} height={200} aria-hidden="true" />

// Chart with description
<figure>
  <Image src="/revenue.png" alt="Revenue chart" width={600} height={300} aria-describedby="chart-desc" />
  <figcaption id="chart-desc">
    Revenue grew 40% year-over-year, from $1.2M in 2024 to $1.68M in 2025.
  </figcaption>
</figure>
```

---

## Testing Tools

### axe-core with Vitest

```typescript
// __tests__/accessibility.test.tsx
import { render } from "@testing-library/react"
import { axe, toHaveNoViolations } from "jest-axe"
import { PricingSection } from "@/components/pricing/pricing-section"

expect.extend(toHaveNoViolations)

test("PricingSection has no a11y violations", async () => {
  const { container } = render(<PricingSection />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### axe-core with Playwright

```typescript
// e2e/accessibility.spec.ts
import { test, expect } from "@playwright/test"
import AxeBuilder from "@axe-core/playwright"

test("pricing page is accessible", async ({ page }) => {
  await page.goto("/pricing")
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa"])
    .analyze()
  expect(results.violations).toEqual([])
})

test("keyboard navigation works on pricing toggle", async ({ page }) => {
  await page.goto("/pricing")
  await page.keyboard.press("Tab") // Skip link
  await page.keyboard.press("Tab") // First nav item
  // Continue to pricing toggle
  await page.keyboard.press("Enter")
  await expect(page.getByRole("radio", { name: /annual/i })).toBeFocused()
})
```

### Lighthouse CI

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
        "categories:accessibility": ["error", { "minScore": 0.95 }],
        "categories:best-practices": ["warn", { "minScore": 0.9 }]
      }
    }
  }
}
```

### Manual Keyboard Test Script

1. Press `Tab` from top of page. Does skip link appear?
2. Activate skip link. Does focus move to `<main>`?
3. Tab through all interactive elements. Is focus visible on each?
4. Open a modal. Is focus trapped? Does Escape close and restore focus?
5. Navigate tabs with arrow keys. Does content update?
6. Use a dropdown menu. Do arrow keys move selection?
7. Submit a form with errors. Are errors announced?
8. Tab to every image. Are decorative images skipped?
