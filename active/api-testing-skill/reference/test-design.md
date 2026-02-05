# API Test Design

## Test Coverage Strategy

### Coverage Pyramid for APIs

```
          ┌─────────────────────┐
          │   E2E Workflows     │  ~10% - Full user journeys
          │   (Login → Action)  │
          ├─────────────────────┤
          │   Integration       │  ~30% - Multi-endpoint flows
          │   (Create → Get)    │
          ├─────────────────────┤
          │   Endpoint Tests    │  ~60% - Individual endpoints
          │   (CRUD per entity) │
          └─────────────────────┘
```

### Test Types

| Type | What It Tests | Example |
|------|---------------|---------|
| Smoke | API is alive | `GET /health` returns 200 |
| Functional | Correct behavior | `POST /users` creates user |
| Contract | Response structure | Response matches schema |
| Performance | Speed | Response < 500ms |
| Security | Auth/AuthZ | 401 without token |

---

## Test Case Design

### Happy Path Tests

For each endpoint, test the expected successful flow:

```javascript
// POST /api/users - Happy path
pm.test("Creates user with valid data", function () {
    pm.response.to.have.status(201);

    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json.email).to.equal(pm.environment.get("testEmail"));
    pm.expect(json.createdAt).to.exist;
});
```

### Error Path Tests

| Error Type | HTTP Status | Test Focus |
|------------|-------------|------------|
| Validation | 400 | Missing/invalid fields |
| Authentication | 401 | Missing/invalid token |
| Authorization | 403 | Wrong permissions |
| Not Found | 404 | Invalid resource ID |
| Conflict | 409 | Duplicate creation |
| Rate Limit | 429 | Too many requests |
| Server Error | 5xx | Graceful error handling |

### Boundary Tests

```javascript
// Test string length limits
pm.test("Name max length enforced", function () {
    // Request body has 256 char name (limit is 255)
    pm.response.to.have.status(400);
    pm.expect(pm.response.json().details[0].field).to.equal("name");
});

// Test numeric limits
pm.test("Quantity must be positive", function () {
    // Request body has quantity: 0
    pm.response.to.have.status(400);
});

// Test array limits
pm.test("Max 100 items per request", function () {
    // Request body has 101 items
    pm.response.to.have.status(400);
});
```

---

## CRUD Test Matrix

### Standard Tests per Endpoint

| Operation | Method | Tests |
|-----------|--------|-------|
| Create | POST | Valid data → 201, Invalid → 400, Duplicate → 409, Unauthorized → 401 |
| Read | GET | Exists → 200, Not found → 404, Unauthorized → 401 |
| Update | PUT/PATCH | Valid → 200, Invalid → 400, Not found → 404, Unauthorized → 401 |
| Delete | DELETE | Exists → 204, Not found → 404, Unauthorized → 401 |
| List | GET | Empty → 200 (empty array), With data → 200 (array), Pagination works |

### Example: User CRUD Tests

```
users/
├── create-user-happy.bru       # 201 with valid data
├── create-user-invalid.bru     # 400 missing email
├── create-user-duplicate.bru   # 409 email exists
├── get-user-happy.bru          # 200 existing user
├── get-user-not-found.bru      # 404 invalid ID
├── update-user-happy.bru       # 200 with valid changes
├── update-user-invalid.bru     # 400 invalid email format
├── delete-user-happy.bru       # 204 existing user
└── delete-user-not-found.bru   # 404 invalid ID
```

---

## Response Validation

### Status Code Assertions

```javascript
// Success codes
pm.response.to.have.status(200);  // OK
pm.response.to.have.status(201);  // Created
pm.response.to.have.status(204);  // No Content

// Client errors
pm.response.to.have.status(400);  // Bad Request
pm.response.to.have.status(401);  // Unauthorized
pm.response.to.have.status(403);  // Forbidden
pm.response.to.have.status(404);  // Not Found
pm.response.to.have.status(409);  // Conflict
pm.response.to.have.status(422);  // Unprocessable Entity
pm.response.to.have.status(429);  // Too Many Requests
```

### Body Structure Assertions

```javascript
// Object structure
pm.test("Response has expected structure", function () {
    const json = pm.response.json();

    // Required fields
    pm.expect(json).to.have.all.keys("id", "email", "name", "createdAt");

    // Field types
    pm.expect(json.id).to.be.a("string");
    pm.expect(json.email).to.be.a("string");
    pm.expect(json.metadata).to.be.an("object");

    // Field formats
    pm.expect(json.id).to.match(/^[a-f0-9-]{36}$/);  // UUID
    pm.expect(json.email).to.match(/^[\w-]+@[\w-]+\.\w+$/);
});

// Array structure
pm.test("List response structure", function () {
    const json = pm.response.json();

    pm.expect(json).to.have.property("data");
    pm.expect(json.data).to.be.an("array");
    pm.expect(json).to.have.property("meta");
    pm.expect(json.meta).to.have.property("total");
    pm.expect(json.meta).to.have.property("page");
});
```

### Error Response Validation

```javascript
pm.test("Error response format", function () {
    const json = pm.response.json();

    // Standard error structure
    pm.expect(json).to.have.property("error");
    pm.expect(json).to.have.property("message");
    pm.expect(json).to.have.property("requestId");

    // Validation error specifics
    if (pm.response.code === 400) {
        pm.expect(json).to.have.property("details");
        pm.expect(json.details).to.be.an("array");

        json.details.forEach(detail => {
            pm.expect(detail).to.have.property("field");
            pm.expect(detail).to.have.property("message");
        });
    }
});
```

---

## Edge Cases

### Empty/Null Values

```javascript
// Test empty string
{ "name": "" }  // Should fail validation

// Test null
{ "name": null }  // Should fail or be ignored

// Test whitespace only
{ "name": "   " }  // Should fail validation
```

### Special Characters

```javascript
// Test Unicode
{ "name": "用户名" }  // Chinese characters

// Test emoji
{ "name": "Test 🎉" }  // Emoji in string

// Test injection attempts
{ "name": "'; DROP TABLE users; --" }  // SQL injection
{ "name": "<script>alert(1)</script>" }  // XSS
```

### Large Payloads

```javascript
// Test large strings
{ "description": "x".repeat(100000) }  // 100KB string

// Test many array items
{ "tags": Array(1000).fill("tag") }  // 1000 items

// Test deeply nested objects
{ "data": { "level1": { "level2": { ... } } } }
```

---

## Security Testing

### Authentication Tests

```javascript
// No token
pm.test("401 without token", function () {
    // Remove Authorization header
    pm.response.to.have.status(401);
});

// Invalid token
pm.test("401 with invalid token", function () {
    // Authorization: Bearer invalid_token_xxx
    pm.response.to.have.status(401);
});

// Expired token
pm.test("401 with expired token", function () {
    // Use pre-expired token
    pm.response.to.have.status(401);
});
```

### Authorization Tests

```javascript
// Wrong user's resource
pm.test("403 accessing other user's data", function () {
    // User A trying to access User B's resource
    pm.response.to.have.status(403);
});

// Wrong role
pm.test("403 without admin role", function () {
    // Regular user accessing admin endpoint
    pm.response.to.have.status(403);
});
```

### Input Validation Security

```javascript
// SQL injection attempt
pm.test("SQL injection blocked", function () {
    // Body: { "search": "'; DROP TABLE users; --" }
    pm.response.to.not.have.status(500);
    // Should either 400 or process safely
});

// XSS attempt
pm.test("XSS sanitized", function () {
    // Body: { "name": "<script>alert(1)</script>" }
    const json = pm.response.json();
    pm.expect(json.name).to.not.include("<script>");
});
```

---

## Performance Testing

### Response Time Thresholds

```javascript
// Individual endpoint
pm.test("Response under 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Tiered thresholds
pm.test("Response time acceptable", function () {
    const endpoint = pm.request.url.path.join("/");
    const thresholds = {
        "/health": 100,
        "/api/users": 500,
        "/api/reports": 2000
    };

    const threshold = thresholds[endpoint] || 1000;
    pm.expect(pm.response.responseTime).to.be.below(threshold);
});
```

### Load Testing Patterns

```javascript
// Data file iteration for load testing
// Run with: newman run collection.json -d users.json -n 100

// users.json
[
    { "email": "user1@test.com" },
    { "email": "user2@test.com" },
    // ... 100 users
]
```

---

## Test Naming Conventions

### Good Test Names

```javascript
// Pattern: [method] [endpoint] - [scenario] → [expected result]

pm.test("POST /users - valid data → 201 with user object", ...);
pm.test("POST /users - missing email → 400 validation error", ...);
pm.test("GET /users/:id - valid ID → 200 with user data", ...);
pm.test("GET /users/:id - invalid ID → 404 not found", ...);
pm.test("DELETE /users/:id - no auth → 401 unauthorized", ...);
```

### Folder/File Naming

```
users/
├── post-create-user-success.bru
├── post-create-user-invalid-email.bru
├── post-create-user-duplicate.bru
├── get-user-success.bru
├── get-user-not-found.bru
└── delete-user-success.bru
```
