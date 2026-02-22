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

| Assertion Type | What to Check | Example |
|---------------|---------------|---------|
| Status codes | 200, 201, 400, 401, 404 | `pm.response.to.have.status(200)` |
| Response body | Required fields, types, patterns | `pm.expect(json).to.have.property("id")` |
| Response time | Under threshold | `pm.expect(pm.response.responseTime).to.be.below(500)` |
| Headers | Content-Type, X-Request-Id | `pm.response.to.have.header("Content-Type")` |
| JSON schema | Full schema validation | `pm.response.to.have.jsonSchema(schema)` |

See `reference/test-design.md` for full assertion patterns with Postman and Bruno examples.
</test_patterns>

<environment_management>
## Environment Management

**Variable scope (Postman):** Global → Collection → Environment → Data → Local (highest priority).

Use environment files for `baseUrl`, `apiKey` per env (local/staging/production). Chain requests by saving response values (`pm.environment.set("authToken", json.accessToken)`) for use in subsequent requests.

See `reference/data-management.md` for environment file formats, dynamic variables, and request chaining patterns.
</environment_management>

<authentication_testing>
## Authentication Testing

| Auth Type | Method | Key Pattern |
|-----------|--------|-------------|
| Bearer token | Save from login response, use in `Authorization` header | `pm.environment.set("accessToken", json.accessToken)` |
| API key | Header (`X-API-Key`) or query param | `{{apiKey}}` variable |
| OAuth 2.0 | Pre-request script checks expiry, refreshes automatically | `pm.sendRequest()` for token refresh |

Always test: 401 without token, 403 with wrong role.

See `reference/postman-patterns.md` for OAuth 2.0 refresh flow and auth failure test patterns.
</authentication_testing>

<error_testing>
## Error Response Testing

Test each error class: 400 (validation errors with `details` array), 404 (not found), 429 (rate limit headers present), 5xx (has `requestId`).

See `reference/test-design.md` for error response assertion patterns.
</error_testing>

<ci_integration>
## CI/CD Integration

| Tool | CLI | Run Command |
|------|-----|-------------|
| Postman | Newman | `newman run collection.json -e staging.json` |
| Bruno | Bruno CLI | `bru run --env staging` |

Integrate via GitHub Actions: install CLI, run collection, upload HTML report as artifact. Use `${{ secrets.* }}` for sensitive env vars.

See `reference/ci-integration.md` for GitHub Actions workflow, reporters, and secrets handling.
</ci_integration>

<data_management>
## Test Data Management

Use data files (`newman run -d test-data.json`) for iteration-based testing. Postman has built-in dynamic variables (`{{$guid}}`, `{{$randomEmail}}`, `{{$timestamp}}`). Add cleanup scripts in post-request to delete created resources.

See `reference/data-management.md` for data file formats, dynamic generation, and cleanup patterns.
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
