---
name: backend-skills
description: Build backend services by generating API routes, handling requests and responses, and connecting to databases. Use for creating scalable and maintainable server-side applications.
---

# Backend Development Skills

## Instructions

1. **Route Generation**
   - Define RESTful endpoints clearly
   - Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
   - Follow consistent URL naming conventions
   - Group routes by feature or resource
   - Version APIs when needed

2. **Request Handling**
   - Validate request body, params, and headers
   - Parse input data safely
   - Handle missing or invalid inputs gracefully
   - Enforce authentication and authorization where required
   - Log important request events safely

3. **Response Handling**
   - Return structured JSON responses
   - Use correct HTTP status codes
   - Provide meaningful success and error messages
   - Avoid exposing sensitive data
   - Maintain consistent response format

4. **Database Connection**
   - Establish secure database connections
   - Use ORM models for data access
   - Handle connection pooling properly
   - Close sessions safely
   - Prevent SQL injection and unsafe queries

5. **CRUD Operations**
   - Implement Create, Read, Update, Delete operations
   - Validate data before persistence
   - Handle missing records safely
   - Enforce ownership and access rules
   - Support filtering and pagination if needed

6. **Error Handling**
   - Catch and handle exceptions centrally
   - Return user-friendly error responses
   - Log errors for debugging
   - Prevent application crashes
   - Fail securely

## Best Practices
- Keep business logic separate from routing
- Follow clean architecture principles
- Use environment variables for secrets
- Write reusable services and utilities
- Maintain consistent folder structure
- Optimize database queries
- Write readable and maintainable code

## Example Usage
```text
Use backend-skills when implementing:
- API endpoints
- Database integration
- CRUD services
- Request validation
- Error handling middleware
- Backend architecture setup
