# Bruno Patterns

Bruno is a Git-native API client. All requests are stored as `.bru` files that can be version controlled.

## File Structure

### Basic .bru File

```javascript
meta {
  name: Get User
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/api/users/{{userId}}
  body: none
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}

headers {
  Accept: application/json
  X-Request-Id: {{$guid}}
}

tests {
  test("Status is 200", function() {
    expect(res.status).to.equal(200);
  });

  test("Has user data", function() {
    expect(res.body).to.have.property('id');
    expect(res.body).to.have.property('email');
  });
}
```

### POST Request with Body

```javascript
meta {
  name: Create User
  type: http
  seq: 2
}

post {
  url: {{baseUrl}}/api/users
  body: json
  auth: bearer
}

auth:bearer {
  token: {{accessToken}}
}

headers {
  Content-Type: application/json
}

body:json {
  {
    "email": "{{testEmail}}",
    "name": "Test User",
    "role": "member"
  }
}

script:pre-request {
  const timestamp = Date.now();
  bru.setVar("testEmail", `test_${timestamp}@example.com`);
}

tests {
  test("User created", function() {
    expect(res.status).to.equal(201);
  });

  test("Save user ID", function() {
    bru.setVar("createdUserId", res.body.id);
  });
}
```

---

## Project Structure

### Recommended Layout

```
my-api/
├── bruno.json           # Collection config
├── environments/
│   ├── local.bru
│   ├── staging.bru
│   └── production.bru
├── auth/
│   ├── login.bru
│   ├── refresh-token.bru
│   └── logout.bru
├── users/
│   ├── create-user.bru
│   ├── get-user.bru
│   ├── update-user.bru
│   ├── delete-user.bru
│   └── search-users.bru
├── orders/
│   ├── create-order.bru
│   ├── get-orders.bru
│   └── cancel-order.bru
└── _data/
    └── test-users.json
```

### bruno.json Configuration

```json
{
  "version": "1",
  "name": "My API Tests",
  "type": "collection",
  "ignore": [
    "node_modules",
    ".git"
  ]
}
```

---

## Environments

### Environment File (.bru)

```javascript
// environments/staging.bru
vars {
  baseUrl: https://staging.api.example.com
  apiVersion: v1
}

vars:secret [
  accessToken,
  apiKey
]
```

### Multiple Environments

```javascript
// environments/local.bru
vars {
  baseUrl: http://localhost:3000
  apiVersion: v1
  debug: true
}

// environments/production.bru
vars {
  baseUrl: https://api.example.com
  apiVersion: v1
  debug: false
}
```

### Using Environment Variables

```bash
# CLI with environment
bru run --env staging

# Override variables
bru run --env staging --env-var "baseUrl=https://custom.api.com"
```

---

## Scripting

### Pre-request Scripts

```javascript
script:pre-request {
  // Generate unique test data
  const uuid = require('uuid');
  bru.setVar("testId", uuid.v4());

  // Set timestamp
  bru.setVar("timestamp", Date.now());

  // Conditional logic
  if (!bru.getVar("accessToken")) {
    console.log("Warning: No access token set");
  }
}
```

### Post-response Scripts

```javascript
script:post-response {
  // Save response data
  if (res.status === 200) {
    bru.setVar("lastResponseId", res.body.id);
  }

  // Log for debugging
  console.log(`Response time: ${res.responseTime}ms`);
}
```

### Test Scripts

```javascript
tests {
  test("Status code is 200", function() {
    expect(res.status).to.equal(200);
  });

  test("Response has required fields", function() {
    expect(res.body).to.have.property('id');
    expect(res.body).to.have.property('email');
    expect(res.body.email).to.be.a('string');
  });

  test("Array response", function() {
    expect(res.body.users).to.be.an('array');
    expect(res.body.users.length).to.be.greaterThan(0);
  });

  test("Response time acceptable", function() {
    expect(res.responseTime).to.be.below(1000);
  });
}
```

---

## Authentication

### Bearer Token

```javascript
auth:bearer {
  token: {{accessToken}}
}
```

### API Key (Header)

```javascript
headers {
  X-API-Key: {{apiKey}}
}
```

### API Key (Query Param)

```javascript
get {
  url: {{baseUrl}}/api/data?api_key={{apiKey}}
}
```

### Basic Auth

```javascript
auth:basic {
  username: {{username}}
  password: {{password}}
}
```

### OAuth 2.0 Flow

```javascript
// auth/get-token.bru
meta {
  name: Get OAuth Token
  type: http
  seq: 1
}

post {
  url: {{authUrl}}/oauth/token
  body: formUrlEncoded
}

body:form-urlencoded {
  grant_type: client_credentials
  client_id: {{clientId}}
  client_secret: {{clientSecret}}
  scope: read write
}

tests {
  test("Save access token", function() {
    expect(res.status).to.equal(200);
    bru.setVar("accessToken", res.body.access_token);
    bru.setVar("tokenExpiry", Date.now() + (res.body.expires_in * 1000));
  });
}
```

---

## Request Chaining

### Sequential Execution

```javascript
// 1-login.bru (seq: 1)
meta {
  name: Login
  seq: 1
}

// Saves accessToken

// 2-create-user.bru (seq: 2)
meta {
  name: Create User
  seq: 2
}

// Uses {{accessToken}}, saves {{createdUserId}}

// 3-get-user.bru (seq: 3)
meta {
  name: Get User
  seq: 3
}

// Uses {{createdUserId}}
```

### Variable Passing

```javascript
// First request - tests section
tests {
  test("Save for next request", function() {
    bru.setVar("orderId", res.body.id);
    bru.setVar("orderTotal", res.body.total);
  });
}

// Second request - URL
get {
  url: {{baseUrl}}/api/orders/{{orderId}}/details
}
```

---

## CLI Usage

### Basic Commands

```bash
# Run all requests in collection
bru run

# Run with specific environment
bru run --env staging

# Run specific file
bru run users/create-user.bru

# Run specific folder
bru run users/

# Run with environment variable override
bru run --env staging --env-var "baseUrl=http://localhost:3000"
```

### CI/CD Integration

```bash
# Run and output results
bru run --env ci --output results.json

# Fail on first error
bru run --env ci --bail

# Run with timeout
bru run --env ci --timeout 30000
```

### Example GitHub Action

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Bruno CLI
        run: npm install -g @usebruno/cli

      - name: Run API Tests
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          bru run --env ci \
            --env-var "apiKey=$API_KEY"
```

---

## Best Practices

### File Naming

```
# Good
create-user.bru
get-user-by-id.bru
search-users.bru
delete-user.bru

# Avoid
user1.bru
test.bru
new.bru
```

### Sequence Numbers

```javascript
// Use seq for dependent requests
meta { seq: 1 }  // Setup/auth
meta { seq: 2 }  // Create resources
meta { seq: 3 }  // Read/verify
meta { seq: 10 } // Cleanup (high number = runs last)
```

### Git Workflow

```bash
# .gitignore for Bruno
environments/local.bru    # Local overrides
*.local.bru               # Local files
.bruno/                   # Cache directory
```

### Secret Management

```javascript
// environments/staging.bru

// Public variables
vars {
  baseUrl: https://staging.api.com
  apiVersion: v1
}

// Secret variables (not committed to git)
vars:secret [
  accessToken,
  apiKey,
  clientSecret
]
```

### Documentation in Files

```javascript
meta {
  name: Create Order
  type: http
  seq: 3
}

docs {
  Creates a new order for the authenticated user.

  Prerequisites:
  - Valid access token (run login.bru first)
  - User must have "create_order" permission

  Expected response: 201 Created with order object
}

post {
  url: {{baseUrl}}/api/orders
  body: json
}
```
