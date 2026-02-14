# Authentication API Contracts

## Signin Endpoint
```
POST /api/auth/signin
```

### Request
```json
{
  "usernameOrEmail": "string",
  "password": "string"
}
```

### Response (Success)
```json
{
  "success": true,
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "firstName": "string",
    "lastName": "string"
  }
}
```

### Response (Error)
```json
{
  "success": false,
  "error": "string",
  "fieldErrors": {
    "usernameOrEmail": "string",
    "password": "string"
  }
}
```

## Signup Endpoint
```
POST /api/auth/signup
```

### Request
```json
{
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "password": "string",
  "confirmPassword": "string"
}
```

### Response (Success)
```json
{
  "success": true,
  "token": "string",
  "user": {
    "id": "string",
    "email": "string",
    "firstName": "string",
    "lastName": "string"
  }
}
```

### Response (Error)
```json
{
  "success": false,
  "error": "string",
  "fieldErrors": {
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "password": "string",
    "confirmPassword": "string"
  }
}
```

## Validation Rules

### Username or Email
- Required
- If email format: must be valid email
- If username format: 3-30 characters, alphanumeric and underscores only

### Password
- Required
- Minimum 8 characters
- Contains at least one uppercase letter
- Contains at least one lowercase letter
- Contains at least one number

### First Name
- Required for signup
- Maximum 50 characters
- Only letters, spaces, hyphens, and apostrophes

### Last Name
- Required for signup
- Maximum 50 characters
- Only letters, spaces, hyphens, and apostrophes