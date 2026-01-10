# API Documentation

## OpenAPI Specification

### Basic Structure

```yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: API for managing users and posts

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      # ...
    post:
      summary: Create user
      # ...

components:
  schemas:
    User:
      type: object
      # ...
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
```

### Endpoint Documentation

```yaml
paths:
  /users:
    get:
      summary: List all users
      description: |
        Returns a paginated list of users. Results can be filtered
        by status and searched by name or email.
      operationId: listUsers
      tags:
        - Users
      security:
        - bearerAuth: []
      parameters:
        - name: status
          in: query
          description: Filter by user status
          schema:
            type: string
            enum: [active, inactive, all]
            default: all
        - name: search
          in: query
          description: Search by name or email
          schema:
            type: string
            maxLength: 100
        - name: limit
          in: query
          description: Number of results per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          description: Pagination cursor
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
              example:
                data:
                  - id: usr_123
                    name: John Doe
                    email: john@example.com
                pagination:
                  hasMore: true
                  nextCursor: eyJpZCI6MTIzfQ
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'
```

### Schema Definitions

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: string
          description: Unique user identifier
          example: usr_123
        name:
          type: string
          description: User's full name
          minLength: 1
          maxLength: 100
          example: John Doe
        email:
          type: string
          format: email
          description: User's email address
          example: john@example.com
        status:
          type: string
          enum: [active, inactive, pending]
          default: pending
        createdAt:
          type: string
          format: date-time
          description: When the user was created
          example: '2024-01-15T10:00:00Z'

    CreateUserRequest:
      type: object
      required:
        - name
        - email
        - password
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8
          maxLength: 128
          format: password

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        hasMore:
          type: boolean
        nextCursor:
          type: string
          nullable: true

    Error:
      type: object
      required:
        - error
      properties:
        error:
          type: object
          required:
            - code
            - message
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
                  code:
                    type: string
            requestId:
              type: string
```

### Reusable Components

```yaml
components:
  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: unauthorized
              message: Authentication required

    Forbidden:
      description: Access denied
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: forbidden
              message: You don't have permission to access this resource

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: not_found
              message: Resource not found

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: validation_error
              message: Validation failed
              details:
                - field: email
                  code: invalid_format
                  message: Invalid email format

    RateLimited:
      description: Too many requests
      headers:
        Retry-After:
          schema:
            type: integer
          description: Seconds to wait before retrying
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: rate_limited
              message: Too many requests

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT authentication token.
        Get a token from POST /auth/login.

  parameters:
    limitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    cursorParam:
      name: cursor
      in: query
      schema:
        type: string
```

## Documentation Tools

### Generating from OpenAPI

```bash
# Swagger UI
npx swagger-ui-express

# Redoc
npx @redocly/cli build-docs openapi.yaml --output docs/index.html

# Scalar
npx @scalar/cli serve openapi.yaml
```

### TypeScript Types from OpenAPI

```bash
# Generate types
npx openapi-typescript openapi.yaml -o src/api/types.ts

# Usage
import type { paths, components } from './api/types';

type User = components['schemas']['User'];
type CreateUserRequest = components['schemas']['CreateUserRequest'];
```

### Generating OpenAPI from Code

```typescript
// Using Zod to OpenAPI
import { z } from 'zod';
import { extendZodWithOpenApi } from '@anatine/zod-openapi';

extendZodWithOpenApi(z);

const UserSchema = z.object({
  id: z.string().openapi({ example: 'usr_123' }),
  name: z.string().min(1).max(100),
  email: z.string().email(),
}).openapi('User');
```

## README Documentation

### API Quick Start

```markdown
# My API

## Authentication

All requests require a Bearer token:

\`\`\`bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/v1/users
\`\`\`

Get a token:

\`\`\`bash
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "your-password"}'
\`\`\`

## Common Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | List users |
| POST | /users | Create user |
| GET | /users/:id | Get user |
| PATCH | /users/:id | Update user |
| DELETE | /users/:id | Delete user |

## Error Handling

All errors follow this format:

\`\`\`json
{
  "error": {
    "code": "error_code",
    "message": "Human readable message",
    "requestId": "req_abc123"
  }
}
\`\`\`

## Rate Limits

| Tier | Limit |
|------|-------|
| Free | 100 req/min |
| Pro | 1000 req/min |

Rate limit headers are included in every response.
```

## Best Practices

### Do's
- Include examples for every endpoint
- Document error codes and their meanings
- Show authentication flow
- Include rate limit information
- Keep docs in sync with code
- Provide SDKs or code examples

### Don'ts
- Don't leave examples blank
- Don't document removed features
- Don't use placeholder values
- Don't skip error documentation
- Don't forget authentication details
