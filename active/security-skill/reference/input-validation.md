# Input Validation

## Validation Principles

### Defense in Depth

```
┌────────────────────────────────────────────────────────────┐
│ Layer 1: Client-side validation (UX only, not security)    │
├────────────────────────────────────────────────────────────┤
│ Layer 2: API route validation (Zod schemas)                │
├────────────────────────────────────────────────────────────┤
│ Layer 3: Business logic validation (domain rules)          │
├────────────────────────────────────────────────────────────┤
│ Layer 4: Database constraints (unique, check, foreign key) │
└────────────────────────────────────────────────────────────┘
```

### What to Validate

| Input Type | Validations |
|------------|-------------|
| Strings | Length, format (regex), encoding, special chars |
| Numbers | Range, integer vs float, precision |
| Emails | Format, domain allowlist (optional) |
| URLs | Protocol (https), domain allowlist |
| Files | Size, type, extension, content inspection |
| Arrays | Length, element types, uniqueness |
| Objects | Required fields, extra fields, nested validation |

## Zod Patterns

### Basic Schemas

```typescript
import { z } from 'zod';

// Primitives
const stringSchema = z.string().min(1).max(255);
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const numberSchema = z.number().int().positive();
const booleanSchema = z.boolean();
const dateSchema = z.coerce.date(); // Coerces string to Date

// Enums
const statusSchema = z.enum(['pending', 'active', 'archived']);

// Optional with default
const limitSchema = z.number().int().min(1).max(100).default(20);
```

### Object Schemas

```typescript
// User creation
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string()
    .min(8)
    .max(128)
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[0-9]/, 'Must contain number'),
  name: z.string().min(1).max(100),
  role: z.enum(['user', 'admin']).default('user'),
});

// Update (all fields optional)
const updateUserSchema = createUserSchema.partial();

// Patch (specific fields)
const patchUserSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  avatar: z.string().url().optional(),
});
```

### Query Parameters

```typescript
const paginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc'),
  sortBy: z.string().optional(),
});

const filterSchema = z.object({
  search: z.string().max(100).optional(),
  status: z.enum(['all', 'active', 'archived']).default('all'),
  startDate: z.coerce.date().optional(),
  endDate: z.coerce.date().optional(),
});

// Combined
const listQuerySchema = paginationSchema.merge(filterSchema);
```

### Transformations

```typescript
// Trim and lowercase email
const emailSchema = z.string()
  .email()
  .transform(email => email.toLowerCase().trim());

// Parse JSON string
const jsonSchema = z.string().transform((str, ctx) => {
  try {
    return JSON.parse(str);
  } catch {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Invalid JSON',
    });
    return z.NEVER;
  }
});

// Sanitize HTML
import DOMPurify from 'dompurify';

const htmlSchema = z.string().transform(html =>
  DOMPurify.sanitize(html, { ALLOWED_TAGS: ['b', 'i', 'p', 'a'] })
);
```

### Custom Validators

```typescript
// Check for profanity
const noProfanity = z.string().refine(
  (val) => !containsProfanity(val),
  { message: 'Content contains inappropriate language' }
);

// Async validation (e.g., check uniqueness)
const uniqueEmail = z.string().email().refine(
  async (email) => {
    const exists = await db.user.findUnique({ where: { email } });
    return !exists;
  },
  { message: 'Email already registered' }
);

// Cross-field validation
const dateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).refine(
  (data) => data.endDate > data.startDate,
  { message: 'End date must be after start date', path: ['endDate'] }
);
```

## API Integration

### Next.js Route Handler

```typescript
// app/api/users/route.ts
import { z } from 'zod';

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export async function POST(req: Request) {
  // Parse body
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return Response.json(
      { error: 'Invalid JSON body' },
      { status: 400 }
    );
  }

  // Validate
  const result = createUserSchema.safeParse(body);

  if (!result.success) {
    return Response.json(
      {
        error: 'Validation failed',
        details: result.error.flatten(),
      },
      { status: 400 }
    );
  }

  // result.data is typed and validated
  const user = await createUser(result.data);

  return Response.json(user, { status: 201 });
}
```

### Reusable Validation Middleware

```typescript
// lib/validate.ts
import { z, ZodSchema } from 'zod';

type ValidationTarget = 'body' | 'query' | 'params';

export function validate<T extends ZodSchema>(
  schema: T,
  target: ValidationTarget = 'body'
) {
  return async (req: Request): Promise<z.infer<T>> => {
    let data: unknown;

    switch (target) {
      case 'body':
        data = await req.json();
        break;
      case 'query':
        data = Object.fromEntries(new URL(req.url).searchParams);
        break;
      case 'params':
        // Extract from route
        break;
    }

    return schema.parse(data);
  };
}

// Usage
const bodyValidator = validate(createUserSchema, 'body');
const queryValidator = validate(paginationSchema, 'query');

export async function POST(req: Request) {
  const body = await bodyValidator(req);
  // ...
}
```

## Sanitization

### String Sanitization

```typescript
// Remove potential XSS
function sanitizeString(input: string): string {
  return input
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
}

// Or use a library
import escape from 'lodash/escape';
const safe = escape(userInput);
```

### HTML Sanitization

```typescript
import DOMPurify from 'dompurify';

// Strict: text only
const textOnly = DOMPurify.sanitize(input, { ALLOWED_TAGS: [] });

// Basic formatting
const basic = DOMPurify.sanitize(input, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
});

// Rich text
const rich = DOMPurify.sanitize(input, {
  ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li', 'a', 'h1', 'h2', 'h3'],
  ALLOWED_ATTR: ['href', 'target'],
  ALLOW_DATA_ATTR: false,
});
```

### URL Validation

```typescript
const safeUrlSchema = z.string().url().refine(
  (url) => {
    const parsed = new URL(url);
    // Only allow https
    if (parsed.protocol !== 'https:') return false;
    // Block internal IPs
    const ip = parsed.hostname;
    if (isPrivateIP(ip)) return false;
    // Optional: allowlist domains
    const allowedDomains = ['example.com', 'api.example.com'];
    if (!allowedDomains.includes(parsed.hostname)) return false;
    return true;
  },
  { message: 'Invalid or disallowed URL' }
);
```

## File Upload Validation

### File Validation Schema

```typescript
const fileSchema = z.object({
  name: z.string().max(255),
  type: z.enum(['image/jpeg', 'image/png', 'image/webp', 'application/pdf']),
  size: z.number().max(10 * 1024 * 1024), // 10MB
});

// Validate file upload
async function validateFile(file: File) {
  // Basic validation
  const result = fileSchema.safeParse({
    name: file.name,
    type: file.type,
    size: file.size,
  });

  if (!result.success) {
    throw new Error('Invalid file');
  }

  // Content-based validation (magic bytes)
  const buffer = await file.arrayBuffer();
  const bytes = new Uint8Array(buffer);

  const magicBytes: Record<string, number[]> = {
    'image/jpeg': [0xFF, 0xD8, 0xFF],
    'image/png': [0x89, 0x50, 0x4E, 0x47],
    'application/pdf': [0x25, 0x50, 0x44, 0x46],
  };

  const expected = magicBytes[file.type];
  if (!expected) return false;

  for (let i = 0; i < expected.length; i++) {
    if (bytes[i] !== expected[i]) {
      throw new Error('File content does not match type');
    }
  }

  return true;
}
```

## Error Responses

### Consistent Error Format

```typescript
interface ValidationError {
  error: 'validation_error';
  message: string;
  details: {
    field: string;
    message: string;
    code: string;
  }[];
}

function formatZodError(error: z.ZodError): ValidationError {
  return {
    error: 'validation_error',
    message: 'Validation failed',
    details: error.errors.map((e) => ({
      field: e.path.join('.'),
      message: e.message,
      code: e.code,
    })),
  };
}
```
