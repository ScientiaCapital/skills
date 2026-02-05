---
name: "api-testing"
description: "Tool-based API testing with Postman and Bruno - collections, environments, test assertions, CI integration. Use when: postman, bruno, API testing, test API endpoint, API collection, HTTP request testing, endpoint validation."
---

<objective>
Expert-level skill for tool-based API testing using Postman and Bruno. Covers collection organization, environment management, test scripting, response validation, and CI/CD integration.

This skill complements testing-skill (code-based tests) and api-design-skill (API structure). Use this when you need to test existing APIs with dedicated tools rather than writing programmatic tests.

Key distinction:
- testing-skill: Code-based tests (supertest, MSW, pytest requests)
- api-testing-skill: Tool-based tests (Postman, Bruno collections)
- api-design-skill: How to design APIs (structure, conventions)
</objective>

<quick_start>
**Postman Quick Test:**

```javascript
// Tests tab in Postman
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has user data", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json).to.have.property("email");
});
```

**Bruno Quick Test:**

```javascript
// tests/get-user.bru
meta {
  name: Get User
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/api/users/{{userId}}
}

tests {
  test("should return 200", function() {
    expect(res.status).to.equal(200);
  });
}
```

**Environment Setup:**
```json
{
  "baseUrl": "https://api.example.com",
  "apiKey": "test_key_xxx"
}
```
</quick_start>

<success_criteria>
API testing is successful when:
- All endpoints have at least one happy path test
- Error cases tested (4xx, 5xx responses)
- Response schema validated (not just status codes)
- Environment variables used for all configurable values
- Collections organized by resource/domain
- Authentication flows tested end-to-end
- CI pipeline runs collections on every PR
- Test data is reproducible (fixtures or dynamic generation)
</success_criteria>

<tool_comparison>
## Postman vs Bruno

| Feature | Postman | Bruno |
|---------|---------|-------|
| Storage | Cloud/Local | Git-native (.bru files) |
| Collaboration | Team sync | Git branches |
| Pricing | Free tier + paid | Free and open source |
| Offline | Desktop app | Full offline |
| Scripting | JavaScript | JavaScript |
| CI/CD | Newman CLI | Bruno CLI |
| Schema | JSON | Plain text .bru |
| Best For | Teams, API documentation | Git workflows, privacy |

### When to Use Each

**Choose Postman when:**
- Team needs real-time collaboration
- API documentation is primary output
- Mock servers needed for frontend dev
- Complex OAuth flows with token refresh

**Choose Bruno when:**
- Git-native workflow preferred
- Privacy/self-hosting required
- Simpler test scenarios
- Developers prefer code-like syntax
</tool_comparison>

<collection_organization>
## Collection Structure

### Folder Hierarchy

```
my-api-tests/
├── auth/
│   ├── login.bru
│   ├── refresh-token.bru
│   └── logout.bru
├── users/
│   ├── create-user.bru
│   ├── get-user.bru
│   ├── update-user.bru
│   └── delete-user.bru
├── orders/
│   ├── create-order.bru
│   ├── get-orders.bru
│   └── cancel-order.bru
├── environments/
│   ├── local.bru
│   ├── staging.bru
│   └── production.bru
└── collection.bru
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Folders | kebab-case, plural | `users`, `auth-flows` |
| Requests | verb-noun | `create-user`, `get-orders` |
| Variables | camelCase | `{{baseUrl}}`, `{{authToken}}` |
| Environments | lowercase | `local`, `staging`, `production` |

### Request Ordering

Use sequence numbers for dependent requests:

```
1. auth/login.bru          (seq: 1)
2. users/create-user.bru   (seq: 2) - needs auth token
3. users/get-user.bru      (seq: 3) - uses created user ID
```
</collection_organization>

<test_patterns>
## Test Assertion Patterns

### Status Code Validation

```javascript
// Postman
pm.test("Success response", () => pm.response.to.have.status(200));
pm.test("Created response", () => pm.response.to.have.status(201));
pm.test("Not found", () => pm.response.to.have.status(404));

// Bruno
test("Success response", () => expect(res.status).to.equal(200));
```

### Response Body Validation

```javascript
// Postman
pm.test("Has required fields", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json.id).to.be.a("string");
    pm.expect(json.email).to.match(/^[\w-]+@[\w-]+\.\w+$/);
});

// Array validation
pm.test("Returns array of users", function () {
    const json = pm.response.json();
    pm.expect(json.users).to.be.an("array");
    pm.expect(json.users.length).to.be.greaterThan(0);
});
```

### Response Time Validation

```javascript
pm.test("Response time < 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### Header Validation

```javascript
pm.test("Content-Type is JSON", function () {
    pm.response.to.have.header("Content-Type", /application\/json/);
});

pm.test("Has request ID", function () {
    pm.response.to.have.header("X-Request-Id");
});
```

### JSON Schema Validation (Postman)

```javascript
const schema = {
    type: "object",
    required: ["id", "name", "email"],
    properties: {
        id: { type: "string", format: "uuid" },
        name: { type: "string", minLength: 1 },
        email: { type: "string", format: "email" }
    }
};

pm.test("Schema is valid", function () {
    pm.response.to.have.jsonSchema(schema);
});
```
</test_patterns>

<environment_management>
## Environment Management

### Variable Scopes (Postman)

```
Global → Collection → Environment → Data → Local
(lowest priority)         (highest priority)
```

### Environment Files

**Postman environment.json:**
```json
{
    "id": "env-uuid",
    "name": "staging",
    "values": [
        { "key": "baseUrl", "value": "https://staging.api.com", "enabled": true },
        { "key": "apiKey", "value": "stg_key_xxx", "enabled": true, "type": "secret" }
    ]
}
```

**Bruno environment:**
```javascript
// environments/staging.bru
vars {
  baseUrl: https://staging.api.com
  apiKey: stg_key_xxx
}
```

### Dynamic Variables

```javascript
// Pre-request script - set dynamic values
const timestamp = Date.now();
const uniqueEmail = `test_${timestamp}@example.com`;

// Postman
pm.environment.set("uniqueEmail", uniqueEmail);
pm.environment.set("timestamp", timestamp);

// Bruno (in pre-request)
bru.setVar("uniqueEmail", uniqueEmail);
```

### Chaining Requests

```javascript
// Request 1: Login - save token
pm.test("Save auth token", function () {
    const json = pm.response.json();
    pm.environment.set("authToken", json.accessToken);
    pm.environment.set("userId", json.user.id);
});

// Request 2: Use saved token
// Headers: Authorization: Bearer {{authToken}}
// URL: {{baseUrl}}/users/{{userId}}
```
</environment_management>

<authentication_testing>
## Authentication Testing

### Bearer Token Flow

```javascript
// 1. Login request - Pre-request or separate request
// 2. Save token to environment
pm.environment.set("accessToken", pm.response.json().accessToken);

// 3. Use in subsequent requests
// Header: Authorization: Bearer {{accessToken}}
```

### API Key Authentication

```javascript
// Header-based
// X-API-Key: {{apiKey}}

// Query param
// GET {{baseUrl}}/endpoint?api_key={{apiKey}}
```

### OAuth 2.0 with Refresh

```javascript
// Pre-request script for token refresh
const tokenExpiry = pm.environment.get("tokenExpiry");
const now = Date.now();

if (!tokenExpiry || now > tokenExpiry) {
    pm.sendRequest({
        url: pm.environment.get("authUrl") + "/token",
        method: "POST",
        header: { "Content-Type": "application/x-www-form-urlencoded" },
        body: {
            mode: "urlencoded",
            urlencoded: [
                { key: "grant_type", value: "refresh_token" },
                { key: "refresh_token", value: pm.environment.get("refreshToken") },
                { key: "client_id", value: pm.environment.get("clientId") }
            ]
        }
    }, (err, res) => {
        if (!err) {
            const json = res.json();
            pm.environment.set("accessToken", json.access_token);
            pm.environment.set("tokenExpiry", now + (json.expires_in * 1000));
        }
    });
}
```

### Testing Auth Failures

```javascript
// Test unauthorized access
pm.test("Returns 401 without token", function () {
    pm.response.to.have.status(401);
});

// Test forbidden access
pm.test("Returns 403 for wrong role", function () {
    pm.response.to.have.status(403);
    pm.expect(pm.response.json().error).to.include("permission");
});
```
</authentication_testing>

<error_testing>
## Error Response Testing

### Validation Errors (400)

```javascript
pm.test("Returns validation error", function () {
    pm.response.to.have.status(400);

    const json = pm.response.json();
    pm.expect(json.error).to.equal("VALIDATION_ERROR");
    pm.expect(json.details).to.be.an("array");
    pm.expect(json.details[0]).to.have.property("field");
    pm.expect(json.details[0]).to.have.property("message");
});
```

### Not Found (404)

```javascript
pm.test("Returns 404 for missing resource", function () {
    pm.response.to.have.status(404);
    pm.expect(pm.response.json().error).to.equal("NOT_FOUND");
});
```

### Rate Limiting (429)

```javascript
pm.test("Rate limit headers present", function () {
    pm.response.to.have.header("X-RateLimit-Limit");
    pm.response.to.have.header("X-RateLimit-Remaining");
    pm.response.to.have.header("X-RateLimit-Reset");
});
```

### Server Errors (5xx)

```javascript
// Test graceful error handling
pm.test("Error response has request ID", function () {
    pm.expect(pm.response.json()).to.have.property("requestId");
});
```
</error_testing>

<ci_integration>
## CI/CD Integration

### Newman (Postman CLI)

```bash
# Install
npm install -g newman

# Run collection
newman run collection.json -e environment.json

# With reporters
newman run collection.json \
  -e staging.json \
  --reporters cli,junit \
  --reporter-junit-export results.xml

# Specific folder
newman run collection.json --folder "users"
```

### Bruno CLI

```bash
# Install
npm install -g @usebruno/cli

# Run collection
bru run --env staging

# Specific file
bru run users/create-user.bru --env local
```

### GitHub Actions Example

```yaml
name: API Tests

on:
  pull_request:
    branches: [main]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install Newman
        run: npm install -g newman newman-reporter-htmlextra

      - name: Run API Tests
        run: |
          newman run tests/api/collection.json \
            -e tests/api/ci.json \
            --reporters cli,htmlextra \
            --reporter-htmlextra-export report.html

      - name: Upload Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: api-test-report
          path: report.html
```

### Environment Secrets in CI

```yaml
# Use GitHub Secrets for sensitive values
- name: Run API Tests
  env:
    API_KEY: ${{ secrets.STAGING_API_KEY }}
  run: |
    newman run collection.json \
      --env-var "apiKey=$API_KEY" \
      -e staging.json
```
</ci_integration>

<data_management>
## Test Data Management

### Data Files (Newman)

```json
// test-data.json
[
    { "email": "user1@test.com", "name": "User One" },
    { "email": "user2@test.com", "name": "User Two" },
    { "email": "user3@test.com", "name": "User Three" }
]
```

```bash
# Run with data iterations
newman run collection.json -d test-data.json -n 3
```

### Dynamic Data Generation

```javascript
// Pre-request script
const faker = require("faker"); // Postman has built-in faker

pm.environment.set("randomEmail", pm.variables.replaceIn("{{$randomEmail}}"));
pm.environment.set("randomName", pm.variables.replaceIn("{{$randomFullName}}"));
pm.environment.set("randomUUID", pm.variables.replaceIn("{{$guid}}"));
```

### Built-in Dynamic Variables (Postman)

| Variable | Example Output |
|----------|----------------|
| `{{$guid}}` | `a8b2c3d4-e5f6-7890-abcd-ef1234567890` |
| `{{$timestamp}}` | `1612345678` |
| `{{$randomEmail}}` | `test.user@example.com` |
| `{{$randomInt}}` | `42` |
| `{{$randomFullName}}` | `John Smith` |

### Cleanup Scripts

```javascript
// Post-request script - cleanup created resources
if (pm.response.code === 201) {
    const createdId = pm.response.json().id;

    pm.sendRequest({
        url: pm.environment.get("baseUrl") + "/users/" + createdId,
        method: "DELETE",
        header: { "Authorization": "Bearer " + pm.environment.get("authToken") }
    }, (err, res) => {
        console.log("Cleanup: deleted user " + createdId);
    });
}
```
</data_management>

<checklist>
## API Testing Checklist

Before creating collection:
- [ ] API documentation reviewed
- [ ] Authentication method identified
- [ ] Base URLs for all environments defined
- [ ] Test data strategy determined

For each endpoint:
- [ ] Happy path test (expected input, expected output)
- [ ] Required field validation (400 errors)
- [ ] Authentication test (401 without token)
- [ ] Authorization test (403 wrong permissions)
- [ ] Not found test (404 invalid ID)
- [ ] Response schema validated
- [ ] Response time asserted

Collection organization:
- [ ] Requests grouped by resource
- [ ] Sequence numbers for dependent requests
- [ ] Environments for local/staging/production
- [ ] Sensitive values marked as secrets

CI integration:
- [ ] Newman/Bruno CLI configured
- [ ] GitHub Actions workflow created
- [ ] Test reports uploaded as artifacts
- [ ] Secrets stored in CI environment
</checklist>

<references>
For detailed patterns, load the appropriate reference:

| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| Postman advanced patterns | `reference/postman-patterns.md` | Collections, scripting, monitors |
| Bruno workflow | `reference/bruno-patterns.md` | .bru files, git integration |
| Test case design | `reference/test-design.md` | Coverage strategies, edge cases |
| Test data strategies | `reference/data-management.md` | Fixtures, dynamic data, cleanup |
| CI/CD pipelines | `reference/ci-integration.md` | Newman, GitHub Actions, reporting |

**To load:** Ask for the specific topic or check if context suggests it.
</references>
