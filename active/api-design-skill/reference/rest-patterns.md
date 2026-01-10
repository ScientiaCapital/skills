# REST Patterns

## Resource Design

### Flat vs Nested Resources

```
# Flat (preferred for independent resources)
GET /posts
GET /posts/{postId}
GET /comments
GET /comments/{commentId}

# Nested (for dependent resources)
GET /posts/{postId}/comments
GET /users/{userId}/settings

# Mixed (both work)
GET /posts/{postId}/comments        # Comments for a post
GET /comments?post_id={postId}      # Same, different style
```

### When to Nest

**Nest when:**
- Child cannot exist without parent (comments → post)
- Child is tightly coupled (user → settings)
- URL makes semantic sense

**Don't nest when:**
- Resource has independent identity
- Resource belongs to multiple parents
- Nesting would be > 2 levels deep

```
# TOO DEEP - avoid this
GET /companies/{id}/departments/{id}/employees/{id}/tasks

# BETTER - flatten with filters
GET /tasks?employee_id={id}
GET /employees/{id}/tasks
```

## Request Patterns

### Create (POST)

```typescript
// Request
POST /users
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe"
}

// Response - 201 Created
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:00:00Z"
}

// Headers
Location: /users/usr_123
```

### Read (GET)

```typescript
// Single resource
GET /users/usr_123

// Response - 200 OK
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:00:00Z"
}

// Collection
GET /users?status=active&limit=20

// Response - 200 OK
{
  "data": [
    { "id": "usr_123", "email": "...", "name": "..." },
    { "id": "usr_124", "email": "...", "name": "..." }
  ],
  "pagination": {
    "hasMore": true,
    "nextCursor": "eyJpZCI6InVzcl8xMjQifQ"
  }
}
```

### Update (PUT vs PATCH)

```typescript
// PUT - Replace entire resource
PUT /users/usr_123
{
  "email": "new@example.com",
  "name": "Jane Doe",
  "role": "admin"
}

// Response - 200 OK (entire resource)
{
  "id": "usr_123",
  "email": "new@example.com",
  "name": "Jane Doe",
  "role": "admin",
  "updatedAt": "2024-01-15T11:00:00Z"
}

// PATCH - Partial update
PATCH /users/usr_123
{
  "name": "Jane Doe"
}

// Response - 200 OK (entire resource)
{
  "id": "usr_123",
  "email": "user@example.com",  // unchanged
  "name": "Jane Doe",           // updated
  "role": "user",               // unchanged
  "updatedAt": "2024-01-15T11:00:00Z"
}
```

### Delete (DELETE)

```typescript
// Request
DELETE /users/usr_123

// Response - 204 No Content
// (empty body)

// Or 200 OK with confirmation
{
  "deleted": true,
  "id": "usr_123"
}
```

## Response Patterns

### Envelope vs Direct

```typescript
// Envelope (wraps data)
{
  "data": { "id": "usr_123", "name": "John" },
  "meta": { "timestamp": "2024-01-15T10:00:00Z" }
}

// Direct (no wrapper)
{
  "id": "usr_123",
  "name": "John"
}

// Recommendation: Use envelope for collections, direct for single resources
// Collections
{
  "data": [...],
  "pagination": {...}
}

// Single resource
{
  "id": "usr_123",
  "name": "John"
}
```

### Including Related Resources

```typescript
// Request with include
GET /posts/123?include=author,comments

// Response
{
  "id": "123",
  "title": "My Post",
  "authorId": "usr_456",
  "author": {
    "id": "usr_456",
    "name": "John Doe"
  },
  "comments": [
    { "id": "cmt_1", "text": "Great post!" }
  ]
}

// Or with _embedded (HAL style)
{
  "id": "123",
  "title": "My Post",
  "_embedded": {
    "author": { "id": "usr_456", "name": "John" },
    "comments": [...]
  }
}
```

### Sparse Fieldsets

```typescript
// Request specific fields only
GET /users?fields=id,name,email

// Response
{
  "data": [
    { "id": "usr_123", "name": "John", "email": "john@example.com" },
    { "id": "usr_124", "name": "Jane", "email": "jane@example.com" }
  ]
}

// Implementation
const allowedFields = ['id', 'name', 'email', 'role', 'createdAt'];
const requestedFields = req.query.fields?.split(',') || allowedFields;
const fields = requestedFields.filter(f => allowedFields.includes(f));

const users = await db.user.findMany({
  select: Object.fromEntries(fields.map(f => [f, true]))
});
```

## Action Endpoints

### Non-CRUD Operations

```typescript
// Resource state changes
POST /orders/{id}/cancel
POST /orders/{id}/ship
POST /users/{id}/suspend
POST /users/{id}/activate

// Controller-style actions
POST /auth/login
POST /auth/logout
POST /auth/refresh
POST /auth/forgot-password
POST /auth/reset-password

// Batch operations
POST /emails/send-batch
{
  "recipients": ["a@example.com", "b@example.com"],
  "template": "welcome"
}

// Long-running operations
POST /reports/generate
// Returns 202 Accepted
{
  "jobId": "job_123",
  "status": "pending",
  "statusUrl": "/jobs/job_123"
}

GET /jobs/job_123
{
  "id": "job_123",
  "status": "completed",
  "resultUrl": "/reports/report_456"
}
```

## Idempotency

### Idempotency Keys

```typescript
// Client sends idempotency key
POST /payments
Idempotency-Key: key_abc123
{
  "amount": 1000,
  "currency": "usd"
}

// Server implementation
async function createPayment(req: Request) {
  const idempotencyKey = req.headers['idempotency-key'];

  if (idempotencyKey) {
    // Check if we've seen this key before
    const existing = await redis.get(`idempotency:${idempotencyKey}`);
    if (existing) {
      return JSON.parse(existing); // Return cached response
    }
  }

  // Process payment
  const payment = await stripe.charges.create({...});

  // Cache response
  if (idempotencyKey) {
    await redis.set(
      `idempotency:${idempotencyKey}`,
      JSON.stringify(payment),
      'EX', 24 * 60 * 60 // 24 hours
    );
  }

  return payment;
}
```

## Content Negotiation

### Request Headers

```
Accept: application/json          # Preferred response format
Content-Type: application/json    # Request body format
Accept-Language: en-US            # Preferred language
Accept-Encoding: gzip, deflate    # Compression
```

### Response Headers

```
Content-Type: application/json; charset=utf-8
Content-Language: en-US
Content-Encoding: gzip
Cache-Control: max-age=3600
ETag: "abc123"
Last-Modified: Sat, 15 Jan 2024 10:00:00 GMT
```

## Caching

### Cache Headers

```typescript
// Cacheable response
res.setHeader('Cache-Control', 'public, max-age=3600');
res.setHeader('ETag', `"${hash(data)}"`);

// Non-cacheable (user-specific data)
res.setHeader('Cache-Control', 'private, no-cache');

// Conditional GET
const etag = req.headers['if-none-match'];
if (etag === currentEtag) {
  return res.status(304).end(); // Not Modified
}
```

### Cache Strategies

| Resource Type | Strategy |
|--------------|----------|
| Static assets | `public, max-age=31536000` (1 year) |
| Public data | `public, max-age=3600, stale-while-revalidate=60` |
| User data | `private, no-cache` |
| Real-time | `no-store` |
