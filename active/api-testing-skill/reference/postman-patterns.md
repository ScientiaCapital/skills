# Postman Advanced Patterns

## Collection Structure

### Folder Organization

```
My API Collection/
├── Setup/
│   ├── Health Check
│   └── Get Auth Token
├── Users/
│   ├── CRUD/
│   │   ├── Create User
│   │   ├── Get User
│   │   ├── Update User
│   │   └── Delete User
│   └── Search/
│       └── Search Users
├── Orders/
│   ├── Create Order
│   ├── Get Order
│   └── Cancel Order
└── Cleanup/
    └── Delete Test Data
```

### Collection Variables

```javascript
// Set at collection level
pm.collectionVariables.set("collectionId", "abc123");

// Access
const id = pm.collectionVariables.get("collectionId");
```

---

## Pre-request Scripts

### Token Refresh Pattern

```javascript
const tokenUrl = pm.environment.get("tokenUrl");
const refreshToken = pm.environment.get("refreshToken");
const tokenExpiry = pm.environment.get("tokenExpiry");

// Check if token needs refresh (1 minute buffer)
if (!tokenExpiry || Date.now() > (tokenExpiry - 60000)) {
    pm.sendRequest({
        url: tokenUrl,
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                grant_type: 'refresh_token',
                refresh_token: refreshToken
            })
        }
    }, (err, response) => {
        if (err) {
            console.error('Token refresh failed:', err);
            return;
        }

        const json = response.json();
        pm.environment.set("accessToken", json.access_token);
        pm.environment.set("tokenExpiry", Date.now() + (json.expires_in * 1000));

        if (json.refresh_token) {
            pm.environment.set("refreshToken", json.refresh_token);
        }
    });
}
```

### Generate Unique Test Data

```javascript
// Using built-in dynamic variables
const uniqueId = pm.variables.replaceIn('{{$guid}}');
const timestamp = pm.variables.replaceIn('{{$timestamp}}');
const randomEmail = pm.variables.replaceIn('{{$randomEmail}}');

pm.environment.set("testUserId", uniqueId);
pm.environment.set("testEmail", `test_${timestamp}@example.com`);

// Using JavaScript
const randomString = Math.random().toString(36).substring(7);
pm.environment.set("testSlug", `test-${randomString}`);
```

### Conditional Execution

```javascript
// Skip request based on condition
const shouldSkip = pm.environment.get("skipAuthTests") === "true";

if (shouldSkip) {
    pm.execution.skipRequest();
}
```

---

## Test Patterns

### Comprehensive Response Validation

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Response has correct content type", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});

pm.test("Response body structure is valid", function () {
    const json = pm.response.json();

    pm.expect(json).to.be.an("object");
    pm.expect(json).to.have.property("data");
    pm.expect(json).to.have.property("meta");
});

pm.test("Data array is not empty", function () {
    const json = pm.response.json();
    pm.expect(json.data).to.be.an("array").that.is.not.empty;
});
```

### JSON Schema Validation

```javascript
const userSchema = {
    type: "object",
    required: ["id", "email", "name", "createdAt"],
    properties: {
        id: {
            type: "string",
            pattern: "^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$"
        },
        email: {
            type: "string",
            format: "email"
        },
        name: {
            type: "string",
            minLength: 1,
            maxLength: 255
        },
        createdAt: {
            type: "string",
            format: "date-time"
        },
        metadata: {
            type: "object",
            additionalProperties: true
        }
    },
    additionalProperties: false
};

pm.test("Response matches user schema", function () {
    const json = pm.response.json();
    pm.expect(tv4.validate(json, userSchema)).to.be.true;
});
```

### Chained Request Validation

```javascript
// In Create User request tests
pm.test("Save created user ID", function () {
    const json = pm.response.json();
    pm.expect(json).to.have.property("id");

    // Save for next request
    pm.environment.set("createdUserId", json.id);
    pm.environment.set("createdUserEmail", json.email);
});

// In Get User request tests
pm.test("Retrieved user matches created user", function () {
    const json = pm.response.json();
    const expectedEmail = pm.environment.get("createdUserEmail");

    pm.expect(json.email).to.equal(expectedEmail);
});
```

---

## Workflows

### Collection Runner Setup

```javascript
// Run specific folders in order
// 1. Setup (auth)
// 2. Create resources
// 3. Test CRUD operations
// 4. Cleanup

// In Setup/Get Auth Token - tests:
pm.test("Auth token saved", function () {
    const json = pm.response.json();
    pm.environment.set("authToken", json.token);
});

// In Cleanup request - tests:
pm.test("Cleanup successful", function () {
    pm.environment.unset("createdUserId");
    pm.environment.unset("testEmail");
});
```

### Error Recovery

```javascript
// Handle failed prerequisite
pm.test("Handle missing auth token", function () {
    if (!pm.environment.get("authToken")) {
        pm.execution.setNextRequest("Get Auth Token");
        return;
    }
    // Continue with normal tests
});
```

---

## Monitors

### Health Check Monitor

```javascript
// Scheduled to run every 5 minutes
pm.test("API is healthy", function () {
    pm.response.to.have.status(200);

    const json = pm.response.json();
    pm.expect(json.status).to.equal("healthy");
});

pm.test("Response time SLA", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});

// Alert on failure (configure in Postman UI)
```

### Performance Baseline

```javascript
pm.test("Establish performance baseline", function () {
    const responseTime = pm.response.responseTime;

    // Log for trend analysis
    console.log(`Response time: ${responseTime}ms`);

    // Alert if degradation
    const baseline = 200; // ms
    const threshold = 1.5; // 50% degradation

    pm.expect(responseTime).to.be.below(baseline * threshold);
});
```

---

## Mock Servers

### Creating Mocks

1. Create collection with example responses
2. Enable mock server in Postman
3. Use mock URL for frontend development

### Example Response Setup

```javascript
// Save as example response for mock
{
    "id": "mock-user-123",
    "email": "mock@example.com",
    "name": "Mock User",
    "createdAt": "2024-01-01T00:00:00Z"
}
```

### Dynamic Mock Responses

```javascript
// In mock server's example, use variables
{
    "id": "{{$guid}}",
    "email": "{{$randomEmail}}",
    "createdAt": "{{$isoTimestamp}}"
}
```

---

## Best Practices

### Variables Naming

```
// Environment-specific
baseUrl, apiKey, authToken

// Test data
testUserId, testEmail, createdResourceId

// Configuration
timeout, retryCount, skipCleanup
```

### Secret Management

```json
// Mark sensitive variables
{
    "key": "apiKey",
    "value": "secret_xxx",
    "type": "secret",  // Masks in UI
    "enabled": true
}
```

### Documentation in Tests

```javascript
pm.test("User creation returns 201 with user object", function () {
    // Verify:
    // 1. Status code indicates resource created
    // 2. Response includes auto-generated ID
    // 3. Email matches input (case-insensitive)
    // 4. Timestamps are set

    pm.response.to.have.status(201);

    const json = pm.response.json();
    pm.expect(json).to.have.property("id");
    pm.expect(json.email.toLowerCase())
        .to.equal(pm.environment.get("testEmail").toLowerCase());
    pm.expect(json).to.have.property("createdAt");
});
```
