# API Error Handling

## Error Response Structure

### Standard Format

```typescript
interface ApiError {
  error: {
    code: string;           // Machine-readable, snake_case
    message: string;        // Human-readable description
    details?: ErrorDetail[];// Field-level errors (validation)
    requestId?: string;     // Correlation ID for debugging
    timestamp?: string;     // ISO 8601 timestamp
    path?: string;          // Request path
  };
}

interface ErrorDetail {
  field: string;            // Field path (e.g., "user.email")
  message: string;          // Human-readable error
  code: string;             // Machine-readable code
  value?: unknown;          // Optionally include the invalid value
}
```

### Error Codes

```typescript
// Authentication errors
'unauthorized'              // Missing or invalid token
'token_expired'             // Token has expired
'invalid_credentials'       // Wrong email/password

// Authorization errors
'forbidden'                 // Not allowed to access
'insufficient_permissions'  // Missing required permission

// Resource errors
'not_found'                 // Resource doesn't exist
'already_exists'            // Duplicate resource (409)
'conflict'                  // State conflict

// Validation errors
'validation_error'          // Input validation failed
'invalid_format'            // Wrong format (email, date)
'required_field'            // Missing required field
'invalid_value'             // Value out of range or invalid

// Rate limiting
'rate_limited'              // Too many requests

// Server errors
'internal_error'            // Unexpected server error
'service_unavailable'       // External service down
'timeout'                   // Request timed out
```

## HTTP Status Codes

### Client Errors (4xx)

```typescript
// 400 Bad Request - Malformed request
{
  "error": {
    "code": "bad_request",
    "message": "Request body must be valid JSON"
  }
}

// 401 Unauthorized - Missing/invalid auth
{
  "error": {
    "code": "unauthorized",
    "message": "Authentication required"
  }
}

// 403 Forbidden - Authenticated but not authorized
{
  "error": {
    "code": "forbidden",
    "message": "You don't have permission to delete this resource"
  }
}

// 404 Not Found - Resource doesn't exist
{
  "error": {
    "code": "not_found",
    "message": "User with ID 'usr_123' not found"
  }
}

// 409 Conflict - State conflict
{
  "error": {
    "code": "already_exists",
    "message": "A user with this email already exists"
  }
}

// 422 Unprocessable Entity - Validation failed
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "code": "invalid_format",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "code": "min_value",
        "message": "Must be at least 13"
      }
    ]
  }
}

// 429 Too Many Requests - Rate limited
{
  "error": {
    "code": "rate_limited",
    "message": "Too many requests. Please retry after 60 seconds"
  }
}
// Headers: Retry-After: 60
```

### Server Errors (5xx)

```typescript
// 500 Internal Server Error
{
  "error": {
    "code": "internal_error",
    "message": "An unexpected error occurred",
    "requestId": "req_abc123"
  }
}

// 502 Bad Gateway
{
  "error": {
    "code": "bad_gateway",
    "message": "Unable to reach upstream service"
  }
}

// 503 Service Unavailable
{
  "error": {
    "code": "service_unavailable",
    "message": "Service temporarily unavailable. Please try again later"
  }
}
// Headers: Retry-After: 300

// 504 Gateway Timeout
{
  "error": {
    "code": "timeout",
    "message": "Request timed out"
  }
}
```

## Implementation

### Error Classes

```typescript
// Base error class
class ApiError extends Error {
  constructor(
    public statusCode: number,
    public code: string,
    message: string,
    public details?: ErrorDetail[]
  ) {
    super(message);
    this.name = 'ApiError';
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        ...(this.details && { details: this.details }),
      },
    };
  }
}

// Specific error classes
class NotFoundError extends ApiError {
  constructor(resource: string, id: string) {
    super(404, 'not_found', `${resource} with ID '${id}' not found`);
  }
}

class ValidationError extends ApiError {
  constructor(details: ErrorDetail[]) {
    super(422, 'validation_error', 'Validation failed', details);
  }
}

class UnauthorizedError extends ApiError {
  constructor(message = 'Authentication required') {
    super(401, 'unauthorized', message);
  }
}

class ForbiddenError extends ApiError {
  constructor(message = 'Access denied') {
    super(403, 'forbidden', message);
  }
}

class ConflictError extends ApiError {
  constructor(message: string) {
    super(409, 'conflict', message);
  }
}

class RateLimitError extends ApiError {
  constructor(public retryAfter: number) {
    super(429, 'rate_limited', `Too many requests. Retry after ${retryAfter} seconds`);
  }
}
```

### Error Handler Middleware

```typescript
// Express-style middleware
function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  const requestId = req.headers['x-request-id'] as string || crypto.randomUUID();

  // Known API errors
  if (error instanceof ApiError) {
    const response = error.toJSON();
    response.error.requestId = requestId;

    // Add Retry-After for rate limits
    if (error instanceof RateLimitError) {
      res.setHeader('Retry-After', error.retryAfter.toString());
    }

    return res.status(error.statusCode).json(response);
  }

  // Zod validation errors
  if (error instanceof z.ZodError) {
    return res.status(422).json({
      error: {
        code: 'validation_error',
        message: 'Validation failed',
        details: error.errors.map(e => ({
          field: e.path.join('.'),
          code: e.code,
          message: e.message,
        })),
        requestId,
      },
    });
  }

  // Unexpected errors
  console.error('Unexpected error:', {
    error: error.message,
    stack: error.stack,
    requestId,
  });

  return res.status(500).json({
    error: {
      code: 'internal_error',
      message: 'An unexpected error occurred',
      requestId,
    },
  });
}
```

### Next.js App Router

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET(req: Request) {
  try {
    const users = await getUsers();
    return NextResponse.json(users);
  } catch (error) {
    return handleError(error);
  }
}

function handleError(error: unknown): NextResponse {
  const requestId = crypto.randomUUID();

  if (error instanceof ApiError) {
    return NextResponse.json(
      {
        error: {
          ...error.toJSON().error,
          requestId,
        },
      },
      { status: error.statusCode }
    );
  }

  console.error('Unexpected error:', error);

  return NextResponse.json(
    {
      error: {
        code: 'internal_error',
        message: 'An unexpected error occurred',
        requestId,
      },
    },
    { status: 500 }
  );
}
```

## Client-Side Handling

### TypeScript Client

```typescript
interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Array<{
      field: string;
      message: string;
      code: string;
    }>;
    requestId?: string;
  };
}

class ApiClient {
  async request<T>(url: string, options?: RequestInit): Promise<T> {
    const response = await fetch(url, options);

    if (!response.ok) {
      const errorData: ApiErrorResponse = await response.json();
      throw new ApiClientError(
        response.status,
        errorData.error.code,
        errorData.error.message,
        errorData.error.details,
        errorData.error.requestId
      );
    }

    return response.json();
  }
}

// Usage
try {
  const user = await api.request<User>('/api/users/123');
} catch (error) {
  if (error instanceof ApiClientError) {
    if (error.code === 'not_found') {
      // Handle not found
    } else if (error.code === 'validation_error') {
      // Show field errors
      error.details?.forEach(d => {
        form.setError(d.field, d.message);
      });
    }
  }
}
```

## Best Practices

### Do's
- Include request ID in all error responses
- Log errors with context (requestId, userId, path)
- Use consistent error format across all endpoints
- Return appropriate HTTP status codes
- Provide actionable error messages

### Don'ts
- Don't expose stack traces in production
- Don't reveal internal implementation details
- Don't use generic "Error" messages
- Don't return 200 OK for errors
- Don't include sensitive data in error messages
