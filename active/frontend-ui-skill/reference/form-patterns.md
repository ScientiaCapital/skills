# Advanced Form Patterns

React Hook Form + Zod + shadcn/ui Form + Server Actions.

---

## Basic Form

```tsx
// components/forms/contact-form.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { toast } from "sonner"
import { submitContact } from "@/app/actions/contact"

// Shared schema — same file used by server action
export const contactSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  message: z.string().min(10, "Message must be at least 10 characters").max(1000),
})

type ContactFormValues = z.infer<typeof contactSchema>

function ContactForm() {
  const form = useForm<ContactFormValues>({
    resolver: zodResolver(contactSchema),
    defaultValues: { name: "", email: "", message: "" },
    mode: "onBlur",
  })

  async function onSubmit(data: ContactFormValues) {
    const result = await submitContact(data)

    if (result.error) {
      toast.error(result.error)
      // Set server-side field errors
      if (result.fieldErrors) {
        for (const [field, message] of Object.entries(result.fieldErrors)) {
          form.setError(field as keyof ContactFormValues, { message })
        }
      }
      return
    }

    toast.success("Message sent!")
    form.reset()
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Jane Smith" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="jane@example.com" type="email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="message"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Message</FormLabel>
              <FormControl>
                <Textarea placeholder="How can we help?" rows={5} {...field} />
              </FormControl>
              <FormDescription>Max 1000 characters</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Sending..." : "Send message"}
        </Button>
      </form>
    </Form>
  )
}
```

---

## Multi-Step Wizard

```tsx
// components/forms/onboarding-wizard.tsx
"use client"

import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Progress } from "@/components/ui/progress"
import { toast } from "sonner"

// Per-step schemas
const step1Schema = z.object({
  companyName: z.string().min(2),
  industry: z.string().min(1, "Select an industry"),
})

const step2Schema = z.object({
  teamSize: z.string().min(1, "Select team size"),
  role: z.string().min(2),
})

const step3Schema = z.object({
  goal: z.string().min(10, "Tell us more about your goal"),
})

// Combined schema for final submission
const fullSchema = step1Schema.merge(step2Schema).merge(step3Schema)
type WizardValues = z.infer<typeof fullSchema>

const STEPS = [
  { schema: step1Schema, title: "Company Info" },
  { schema: step2Schema, title: "Your Team" },
  { schema: step3Schema, title: "Goals" },
] as const

function OnboardingWizard() {
  const [step, setStep] = useState(0)
  const currentStep = STEPS[step]
  const progress = ((step + 1) / STEPS.length) * 100

  const form = useForm<WizardValues>({
    resolver: zodResolver(currentStep.schema),
    defaultValues: {
      companyName: "", industry: "", teamSize: "", role: "", goal: "",
    },
    mode: "onBlur",
  })

  async function handleNext() {
    // Validate only current step's fields
    const fields = Object.keys(currentStep.schema.shape) as (keyof WizardValues)[]
    const valid = await form.trigger(fields)
    if (!valid) return

    if (step < STEPS.length - 1) {
      setStep(step + 1)
    } else {
      // Final submit
      const data = form.getValues()
      const parsed = fullSchema.safeParse(data)
      if (!parsed.success) {
        toast.error("Please fill in all fields correctly")
        return
      }
      toast.success("Onboarding complete!")
    }
  }

  function handleBack() {
    if (step > 0) setStep(step - 1)
  }

  return (
    <div className="mx-auto max-w-lg space-y-6">
      {/* Progress indicator */}
      <div>
        <div className="mb-2 flex justify-between text-sm">
          <span>Step {step + 1} of {STEPS.length}</span>
          <span>{currentStep.title}</span>
        </div>
        <Progress value={progress} aria-label={`Step ${step + 1} of ${STEPS.length}`} />
      </div>

      {/* Step indicators */}
      <nav aria-label="Wizard steps" className="flex justify-center gap-2">
        {STEPS.map((s, i) => (
          <div
            key={i}
            className={`size-3 rounded-full ${i <= step ? "bg-primary" : "bg-muted"}`}
            aria-current={i === step ? "step" : undefined}
            aria-label={`${s.title}${i < step ? " (completed)" : i === step ? " (current)" : ""}`}
          />
        ))}
      </nav>

      <Form {...form}>
        <form onSubmit={(e) => { e.preventDefault(); handleNext() }} className="space-y-4">
          {step === 0 && (
            <>
              <FormField control={form.control} name="companyName" render={({ field }) => (
                <FormItem>
                  <FormLabel>Company name</FormLabel>
                  <FormControl><Input {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
              <FormField control={form.control} name="industry" render={({ field }) => (
                <FormItem>
                  <FormLabel>Industry</FormLabel>
                  <Select onValueChange={field.onChange} value={field.value}>
                    <FormControl>
                      <SelectTrigger><SelectValue placeholder="Select industry" /></SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="saas">SaaS</SelectItem>
                      <SelectItem value="ecommerce">E-commerce</SelectItem>
                      <SelectItem value="fintech">Fintech</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )} />
            </>
          )}

          {step === 1 && (
            <>
              <FormField control={form.control} name="teamSize" render={({ field }) => (
                <FormItem>
                  <FormLabel>Team size</FormLabel>
                  <Select onValueChange={field.onChange} value={field.value}>
                    <FormControl>
                      <SelectTrigger><SelectValue placeholder="Select size" /></SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      <SelectItem value="1-5">1-5</SelectItem>
                      <SelectItem value="6-20">6-20</SelectItem>
                      <SelectItem value="21-100">21-100</SelectItem>
                      <SelectItem value="100+">100+</SelectItem>
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )} />
              <FormField control={form.control} name="role" render={({ field }) => (
                <FormItem>
                  <FormLabel>Your role</FormLabel>
                  <FormControl><Input placeholder="CTO, Engineer, etc." {...field} /></FormControl>
                  <FormMessage />
                </FormItem>
              )} />
            </>
          )}

          {step === 2 && (
            <FormField control={form.control} name="goal" render={({ field }) => (
              <FormItem>
                <FormLabel>What is your primary goal?</FormLabel>
                <FormControl><Input placeholder="Reduce churn by 20%..." {...field} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
          )}

          <div className="flex justify-between pt-4">
            <Button type="button" variant="outline" onClick={handleBack} disabled={step === 0}>
              Back
            </Button>
            <Button type="submit">
              {step === STEPS.length - 1 ? "Complete" : "Next"}
            </Button>
          </div>
        </form>
      </Form>
    </div>
  )
}
```

---

## File Upload with Drag-and-Drop

```tsx
// components/forms/file-upload.tsx
"use client"

import { useState, useCallback, type DragEvent } from "react"
import { UploadCloudIcon, XIcon, FileIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"

const MAX_SIZE = 10 * 1024 * 1024 // 10MB
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"]

function FileUpload({ onUpload }: { onUpload: (file: File) => Promise<void> }) {
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const [dragging, setDragging] = useState(false)

  function validate(f: File): string | null {
    if (!ALLOWED_TYPES.includes(f.type)) return "File type not allowed. Use JPEG, PNG, WebP, or PDF."
    if (f.size > MAX_SIZE) return "File too large. Maximum 10MB."
    return null
  }

  function handleFile(f: File) {
    const err = validate(f)
    if (err) { setError(err); return }

    setError(null)
    setFile(f)

    if (f.type.startsWith("image/")) {
      const reader = new FileReader()
      reader.onload = (e) => setPreview(e.target?.result as string)
      reader.readAsDataURL(f)
    }
  }

  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }, [])

  async function handleUpload() {
    if (!file) return
    setProgress(10)
    try {
      await onUpload(file)
      setProgress(100)
    } catch {
      setError("Upload failed. Please try again.")
      setProgress(0)
    }
  }

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={cn(
          "flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-8 transition-colors",
          dragging ? "border-primary bg-primary/5" : "border-muted-foreground/25",
          error && "border-destructive"
        )}
        role="button"
        tabIndex={0}
        aria-label="Upload file. Drag and drop or click to browse."
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault()
            document.getElementById("file-input")?.click()
          }
        }}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <UploadCloudIcon className="mb-2 size-10 text-muted-foreground" aria-hidden="true" />
        <p className="text-sm text-muted-foreground">
          Drag & drop or <span className="font-medium text-primary">browse</span>
        </p>
        <p className="mt-1 text-xs text-muted-foreground">JPEG, PNG, WebP, PDF up to 10MB</p>
        <input
          id="file-input"
          type="file"
          accept={ALLOWED_TYPES.join(",")}
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0]
            if (f) handleFile(f)
          }}
        />
      </div>

      {error && <p className="text-sm text-destructive" role="alert">{error}</p>}

      {file && (
        <div className="flex items-center gap-3 rounded-md border p-3">
          {preview ? (
            <img src={preview} alt="Upload preview" className="size-12 rounded object-cover" />
          ) : (
            <FileIcon className="size-12 text-muted-foreground" aria-hidden="true" />
          )}
          <div className="flex-1 min-w-0">
            <p className="truncate text-sm font-medium">{file.name}</p>
            <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(0)} KB</p>
            {progress > 0 && <Progress value={progress} className="mt-1 h-1" />}
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => { setFile(null); setPreview(null); setProgress(0) }}
            aria-label="Remove file"
          >
            <XIcon className="size-4" />
          </Button>
        </div>
      )}

      {file && progress === 0 && (
        <Button onClick={handleUpload} className="w-full">Upload</Button>
      )}
    </div>
  )
}
```

---

## Debounced Search with Async Validation

```tsx
// hooks/use-debounce.ts
import { useEffect, useState } from "react"

export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(timer)
  }, [value, delay])

  return debounced
}
```

```tsx
// components/forms/username-field.tsx
"use client"

import { useEffect, useState } from "react"
import { useFormContext } from "react-hook-form"
import { useDebounce } from "@/hooks/use-debounce"
import { Input } from "@/components/ui/input"
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { CheckCircleIcon, Loader2Icon, XCircleIcon } from "lucide-react"
import { checkUsernameAvailable } from "@/app/actions/users"

function UsernameField() {
  const form = useFormContext()
  const username = form.watch("username")
  const debouncedUsername = useDebounce(username, 500)
  const [checking, setChecking] = useState(false)
  const [available, setAvailable] = useState<boolean | null>(null)

  useEffect(() => {
    if (!debouncedUsername || debouncedUsername.length < 3) {
      setAvailable(null)
      return
    }

    async function check() {
      setChecking(true)
      const result = await checkUsernameAvailable(debouncedUsername)
      setAvailable(result.available)
      if (!result.available) {
        form.setError("username", { message: "Username already taken" })
      } else {
        form.clearErrors("username")
      }
      setChecking(false)
    }

    check()
  }, [debouncedUsername, form])

  return (
    <FormField control={form.control} name="username" render={({ field }) => (
      <FormItem>
        <FormLabel>Username</FormLabel>
        <div className="relative">
          <FormControl>
            <Input placeholder="johndoe" {...field} />
          </FormControl>
          <div className="absolute right-3 top-1/2 -translate-y-1/2">
            {checking && <Loader2Icon className="size-4 animate-spin text-muted-foreground" aria-label="Checking availability" />}
            {!checking && available === true && <CheckCircleIcon className="size-4 text-green-600" aria-label="Username available" />}
            {!checking && available === false && <XCircleIcon className="size-4 text-destructive" aria-label="Username taken" />}
          </div>
        </div>
        <FormMessage />
      </FormItem>
    )} />
  )
}
```

---

## Dynamic Field Arrays

```tsx
// components/forms/team-invite-form.tsx
"use client"

import { useForm, useFieldArray } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Form, FormControl, FormField, FormItem, FormMessage } from "@/components/ui/form"
import { PlusIcon, TrashIcon } from "lucide-react"

const inviteSchema = z.object({
  invites: z.array(z.object({
    email: z.string().email("Invalid email"),
    role: z.enum(["admin", "editor", "viewer"]),
  })).min(1, "Add at least one invite").max(10, "Maximum 10 invites at once"),
})

type InviteValues = z.infer<typeof inviteSchema>

function TeamInviteForm() {
  const form = useForm<InviteValues>({
    resolver: zodResolver(inviteSchema),
    defaultValues: {
      invites: [{ email: "", role: "viewer" }],
    },
  })

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "invites",
  })

  function onSubmit(data: InviteValues) {
    console.log("Inviting:", data.invites)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {fields.map((field, index) => (
          <div key={field.id} className="flex items-start gap-3">
            <FormField control={form.control} name={`invites.${index}.email`} render={({ field }) => (
              <FormItem className="flex-1">
                <FormControl>
                  <Input placeholder="teammate@company.com" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )} />

            <FormField control={form.control} name={`invites.${index}.role`} render={({ field }) => (
              <FormItem className="w-32">
                <Select onValueChange={field.onChange} value={field.value}>
                  <FormControl>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="editor">Editor</SelectItem>
                    <SelectItem value="viewer">Viewer</SelectItem>
                  </SelectContent>
                </Select>
              </FormItem>
            )} />

            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={() => remove(index)}
              disabled={fields.length === 1}
              aria-label={`Remove invite ${index + 1}`}
            >
              <TrashIcon className="size-4" />
            </Button>
          </div>
        ))}

        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => append({ email: "", role: "viewer" })}
          disabled={fields.length >= 10}
        >
          <PlusIcon className="mr-2 size-4" /> Add another
        </Button>

        <Button type="submit" className="w-full">
          Send {fields.length} invite{fields.length !== 1 && "s"}
        </Button>
      </form>
    </Form>
  )
}
```

---

## Dependent / Conditional Fields

```tsx
// watch() to show fields conditionally
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const addressSchema = z.object({
  country: z.string().min(1),
  state: z.string().optional(),
  postalCode: z.string().min(1),
}).refine(
  (data) => data.country !== "US" || (data.state && data.state.length >= 2),
  { message: "State is required for US addresses", path: ["state"] }
)

function AddressForm() {
  const form = useForm<z.infer<typeof addressSchema>>({
    resolver: zodResolver(addressSchema),
    defaultValues: { country: "", state: "", postalCode: "" },
  })

  const country = form.watch("country")

  return (
    <Form {...form}>
      <form className="space-y-4">
        <FormField control={form.control} name="country" render={({ field }) => (
          <FormItem>
            <FormLabel>Country</FormLabel>
            <Select onValueChange={(v) => { field.onChange(v); form.setValue("state", "") }} value={field.value}>
              <FormControl><SelectTrigger><SelectValue placeholder="Select" /></SelectTrigger></FormControl>
              <SelectContent>
                <SelectItem value="US">United States</SelectItem>
                <SelectItem value="CA">Canada</SelectItem>
                <SelectItem value="GB">United Kingdom</SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        )} />

        {/* Show state field only for US */}
        {country === "US" && (
          <FormField control={form.control} name="state" render={({ field }) => (
            <FormItem>
              <FormLabel>State</FormLabel>
              <Select onValueChange={field.onChange} value={field.value}>
                <FormControl><SelectTrigger><SelectValue placeholder="Select state" /></SelectTrigger></FormControl>
                <SelectContent>
                  <SelectItem value="CA">California</SelectItem>
                  <SelectItem value="NY">New York</SelectItem>
                  <SelectItem value="TX">Texas</SelectItem>
                  {/* ... more states */}
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )} />
        )}

        <FormField control={form.control} name="postalCode" render={({ field }) => (
          <FormItem>
            <FormLabel>{country === "GB" ? "Postcode" : "ZIP / Postal code"}</FormLabel>
            <FormControl><Input {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
      </form>
    </Form>
  )
}
```

---

## Server Action Integration

### Shared Zod Schema Pattern

```typescript
// lib/schemas/contact.ts — single source of truth
import { z } from "zod"

export const contactSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  message: z.string().min(10).max(1000),
})

export type ContactInput = z.infer<typeof contactSchema>
```

### Server Action with Error Return

```typescript
// app/actions/contact.ts
"use server"

import { contactSchema } from "@/lib/schemas/contact"
import { revalidatePath } from "next/cache"

type ActionResult = {
  success?: boolean
  error?: string
  fieldErrors?: Record<string, string>
}

export async function submitContact(data: unknown): Promise<ActionResult> {
  // Always validate on the server — client validation can be bypassed
  const parsed = contactSchema.safeParse(data)

  if (!parsed.success) {
    const fieldErrors: Record<string, string> = {}
    for (const issue of parsed.error.issues) {
      const field = issue.path[0]?.toString()
      if (field) fieldErrors[field] = issue.message
    }
    return { error: "Validation failed", fieldErrors }
  }

  try {
    // Database insert, email send, etc.
    await db.insert(contacts).values(parsed.data)
    revalidatePath("/contact")
    return { success: true }
  } catch {
    return { error: "Failed to submit. Please try again." }
  }
}
```

### Toast on Success/Error

```tsx
"use client"

import { toast } from "sonner"

async function onSubmit(data: ContactInput) {
  const result = await submitContact(data)

  if (result.error) {
    toast.error("Submission failed", {
      description: result.error,
      action: {
        label: "Retry",
        onClick: () => form.handleSubmit(onSubmit)(),
      },
    })

    // Map server field errors back to form
    if (result.fieldErrors) {
      for (const [field, message] of Object.entries(result.fieldErrors)) {
        form.setError(field as keyof ContactInput, { message })
      }
    }
    return
  }

  toast.success("Submitted!", {
    description: "We'll be in touch within 24 hours.",
  })
  form.reset()
}
```

---

## Optimistic Updates

```tsx
"use client"

import { useOptimistic, useTransition } from "react"
import { toggleFavorite } from "@/app/actions/favorites"
import { HeartIcon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

function FavoriteButton({ itemId, isFavorited }: { itemId: string; isFavorited: boolean }) {
  const [optimistic, setOptimistic] = useOptimistic(isFavorited)
  const [isPending, startTransition] = useTransition()

  function handleToggle() {
    startTransition(async () => {
      setOptimistic(!optimistic)
      try {
        await toggleFavorite(itemId)
      } catch {
        // React automatically reverts optimistic state on error
      }
    })
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={handleToggle}
      disabled={isPending}
      aria-label={optimistic ? "Remove from favorites" : "Add to favorites"}
      aria-pressed={optimistic}
    >
      <HeartIcon className={cn("size-5", optimistic && "fill-red-500 text-red-500")} />
    </Button>
  )
}
```

---

## Form Pattern Quick Reference

| Pattern | Key Imports | When |
|---------|------------|------|
| Basic form | `useForm`, `zodResolver`, `Form` | Simple create/edit forms |
| Multi-step | `useForm` + `useState` for step, per-step `trigger()` | Onboarding, checkout |
| File upload | `useState`, `DragEvent`, `FileReader` | Avatars, documents |
| Debounced search | `useDebounce`, `watch()` | Username check, search |
| Field arrays | `useFieldArray` | Repeatable rows (invites, line items) |
| Dependent fields | `watch()` | Country/state, conditional sections |
| Optimistic | `useOptimistic`, `useTransition` | Like/favorite, toggle |
| Server action | Shared Zod schema, `safeParse`, field error return | All mutations |
