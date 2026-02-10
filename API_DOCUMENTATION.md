# API Documentation: Todo Full-Stack Web Application

## Base URL
Production: `https://your-domain.com/api`
Development: `http://localhost:8000/api`

## Authentication
All endpoints except authentication endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "John Doe"
}
```

**Response (200):**
```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```

**Errors:**
- 400: Invalid request data
- 409: User already exists

#### POST /auth/login
Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200):**
```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "token_type": "bearer"
}
```

**Errors:**
- 400: Invalid login data
- 401: Invalid credentials

#### POST /auth/logout
Log out the current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

### Task Management

#### GET /tasks/
Retrieve all tasks for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Sample Task",
    "description": "Task description",
    "completed": false,
    "user_id": "user-uuid",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
  }
]
```

**Errors:**
- 401: Invalid or missing JWT token

#### POST /tasks/
Create a new task for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "completed": false
}
```

**Response (201):**
```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 400: Invalid request body
- 401: Invalid or missing JWT token

#### GET /tasks/{id}
Retrieve a specific task by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description",
  "completed": false,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

**Errors:**
- 401: Invalid or missing JWT token
- 404: Task does not exist

#### PUT /tasks/{id}
Update a specific task by ID.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-02T00:00:00"
}
```

**Errors:**
- 400: Invalid request body
- 401: Invalid or missing JWT token
- 404: Task does not exist

#### DELETE /tasks/{id}
Delete a specific task by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204):** No content

**Errors:**
- 401: Invalid or missing JWT token
- 404: Task does not exist

#### PATCH /tasks/{id}/complete
Toggle the completion status of a specific task.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "completed": true
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Sample Task",
  "description": "Task description",
  "completed": true,
  "user_id": "user-uuid",
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-02T00:00:00"
}
```

**Errors:**
- 400: Invalid request body
- 401: Invalid or missing JWT token
- 404: Task does not exist

## Error Responses

All error responses follow this format:

**Response (4XX/5XX):**
```json
{
  "detail": "Error message"
}
```

## Security

- All API requests (except authentication) require a valid JWT token
- Users can only access their own tasks
- Passwords are hashed using bcrypt
- Input is validated and sanitized to prevent injection attacks