---
name: auth-skills
description: Build secure authentication systems including signup, signin, password hashing, JWT tokens, and Better Auth integration. Use for implementing and validating authentication flows.
---

# Authentication Skills

## Instructions

1. **Signup Flow**
   - Validate email format and password strength
   - Prevent duplicate user registration
   - Hash passwords securely before storing
   - Never store plain-text passwords
   - Return safe user responses without sensitive data

2. **Signin Flow**
   - Verify user credentials securely
   - Compare hashed passwords correctly
   - Handle invalid login attempts safely
   - Generate JWT token on successful login
   - Standardize error responses

3. **Password Hashing**
   - Use secure hashing algorithms (bcrypt or argon2)
   - Automatically apply salt
   - Never expose hash values in logs or APIs
   - Rehash passwords when security standards evolve

4. **JWT Token Handling**
   - Generate signed JWT tokens securely
   - Include user ID and expiration in payload
   - Validate token signature on every request
   - Reject expired or malformed tokens
   - Extract authenticated user safely

5. **Better Auth Integration**
   - Configure Better Auth correctly in frontend
   - Enable JWT plugin for token issuance
   - Attach JWT token to every API request header
   - Share secret key between frontend and backend
   - Handle session expiration safely

6. **Validation Rules**
   - Validate all inputs strictly
   - Sanitize user-provided data
   - Enforce required fields
   - Prevent malformed requests
   - Return meaningful validation errors

## Best Practices
- Never log sensitive credentials
- Store secrets in environment variables
- Follow least privilege principle
- Fail securely by default
- Keep authentication logic centralized
- Enforce HTTPS in production
- Validate before processing

## Example Structure
```text
User Signup → Validate Input → Hash Password → Store User → Return Success  
User Signin → Verify Credentials → Generate JWT → Return Token  
API Request → Verify JWT → Extract User → Authorize Access
