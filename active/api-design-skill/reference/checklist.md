# API Design Checklist

Use this checklist to validate your API design before implementation.

## Endpoints
- [ ] Resource names are plural nouns
- [ ] Consistent naming convention (kebab-case)
- [ ] Appropriate HTTP methods
- [ ] Correct status codes

## Responses
- [ ] Consistent response format
- [ ] Consistent error format
- [ ] Includes request ID for debugging

## Pagination
- [ ] List endpoints are paginated
- [ ] Cursor-based for real-time data
- [ ] Includes hasMore/total indicators

## Security
- [ ] Authentication required where needed
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] CORS configured correctly

## Documentation
- [ ] OpenAPI spec exists
- [ ] Examples for all endpoints
- [ ] Error codes documented
