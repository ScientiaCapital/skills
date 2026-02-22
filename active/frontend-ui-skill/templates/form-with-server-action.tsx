/**
 * Complete form with Zod + React Hook Form + shadcn Form + Server Action
 *
 * Features:
 * - Shared Zod schema (client validation + server re-validation)
 * - React Hook Form with zodResolver, mode: "onBlur"
 * - shadcn Form components for accessible field wiring
 * - Server Action stub with error handling
 * - Loading state on submit button
 * - Toast notification on success/error (sonner)
 *
 * Dependencies:
 *   npx shadcn@latest add form input select textarea button
 *   npm install sonner zod react-hook-form @hookform/resolvers
 *
 * File structure:
 *   lib/schemas/user.ts       — Zod schema (shared)
 *   app/actions/user.ts       — Server Action
 *   app/users/new/page.tsx    — This form component
 */

// ── Shared Zod Schema ─────────────────────────────── lib/schemas/user.ts

import { z } from "zod"

export const userFormSchema = z.object({
  name: z
    .string()
    .min(2, "Name must be at least 2 characters")
    .max(100, "Name must be under 100 characters"),
  email: z
    .string()
    .email("Please enter a valid email address"),
  role: z.enum(["admin", "editor", "viewer"], {
    required_error: "Please select a role",
  }),
  bio: z
    .string()
    .max(500, "Bio must be under 500 characters")
    .optional()
    .default(""),
})

export type UserFormValues = z.infer<typeof userFormSchema>

// ── Server Action ─────────────────────────────────── app/actions/user.ts

"use server"

import { revalidatePath } from "next/cache"

export type ActionResult = {
  success: boolean
  message: string
  errors?: Partial<Record<keyof UserFormValues, string[]>>
}

export async function createUser(
  values: UserFormValues
): Promise<ActionResult> {
  // Server-side re-validation — never trust the client
  const parsed = userFormSchema.safeParse(values)

  if (!parsed.success) {
    return {
      success: false,
      message: "Validation failed",
      errors: parsed.error.flatten().fieldErrors as ActionResult["errors"],
    }
  }

  try {
    // TODO: Replace with your database call
    // await db.user.create({ data: parsed.data })

    revalidatePath("/dashboard/users")

    return {
      success: true,
      message: "User created successfully",
    }
  } catch (error) {
    return {
      success: false,
      message:
        error instanceof Error ? error.message : "An unexpected error occurred",
    }
  }
}

// ── Form Component ────────────────────── app/users/new/user-form.tsx

"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Loader2 } from "lucide-react"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

export function UserForm() {
  const form = useForm<UserFormValues>({
    resolver: zodResolver(userFormSchema),
    mode: "onBlur",
    defaultValues: {
      name: "",
      email: "",
      role: undefined,
      bio: "",
    },
  })

  const { isSubmitting } = form.formState

  async function onSubmit(values: UserFormValues) {
    const result = await createUser(values)

    if (!result.success) {
      // Surface server-side field errors back to the form
      if (result.errors) {
        for (const [field, messages] of Object.entries(result.errors)) {
          if (messages?.[0]) {
            form.setError(field as keyof UserFormValues, {
              type: "server",
              message: messages[0],
            })
          }
        }
      }

      toast.error(result.message)
      return
    }

    toast.success(result.message)
    form.reset()
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-6"
        noValidate
      >
        {/* Name */}
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Jane Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Email */}
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="jane@acme.com"
                  autoComplete="email"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Role */}
        <FormField
          control={form.control}
          name="role"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Role</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a role" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="admin">Admin</SelectItem>
                  <SelectItem value="editor">Editor</SelectItem>
                  <SelectItem value="viewer">Viewer</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Bio */}
        <FormField
          control={form.control}
          name="bio"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Bio</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Tell us about yourself..."
                  rows={4}
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Submit */}
        <Button type="submit" disabled={isSubmitting} className="w-full">
          {isSubmitting && <Loader2 className="mr-2 size-4 animate-spin" />}
          {isSubmitting ? "Creating..." : "Create User"}
        </Button>
      </form>
    </Form>
  )
}
