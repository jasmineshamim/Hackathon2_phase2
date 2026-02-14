# Todo App - Demo Instructions and Usage Guide

## Overview

This demo showcases a full-stack todo application with authentication, task management, and responsive UI built with Next.js, FastAPI, and Neon Serverless PostgreSQL.

## Features Demonstrated

1. **User Authentication** - Secure registration and login with JWT tokens
2. **Task Management** - Complete CRUD operations for tasks
3. **Data Isolation** - Users can only access their own tasks
4. **Responsive UI** - Works on mobile and desktop devices
5. **Security Features** - Input validation, sanitization, and proper error handling

## Setup Instructions

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.9 or higher)
- pip (Python package manager)

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   NEON_API_KEY=your_neon_api_key
   BETTER_AUTH_SECRET=your_auth_secret
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env.local` file with your configuration:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
   ```

4. Start the frontend:
   ```bash
   npm run dev
   ```

## Demo Flow

### 1. User Registration
- Navigate to `http://localhost:3000/auth/signup`
- Fill in registration details (email, password, name)
- Click "Sign up" to create an account
- Verify account is created successfully

### 2. User Login
- Navigate to `http://localhost:3000/auth/signin`
- Enter registered email and password
- Click "Sign in" to authenticate
- Verify JWT token is stored and user is redirected to dashboard

### 3. Task Management
- On the dashboard, click "Add Task" to create a new task
- Fill in task details (title and description)
- Click "Add Task" to save the task
- Verify the task appears in the task list
- Test editing, marking as complete/incomplete, and deleting tasks

### 4. Multi-User Isolation
- Register a second user account
- Create tasks for the second user
- Verify that each user can only see their own tasks
- Try accessing another user's tasks (should result in 403 Forbidden)

### 5. Responsive UI
- Test the application on different screen sizes
- Verify mobile navigation works properly
- Check that task cards and forms are responsive

### 6. Error Handling
- Try logging in with invalid credentials
- Verify appropriate error messages are displayed
- Test form validation with invalid inputs
- Check that unauthorized access attempts are handled properly

## Security Features

### Authentication
- JWT tokens are issued upon successful login
- Tokens are validated for all protected endpoints
- Session management handles token expiration

### Authorization
- Middleware validates that users can only access their own tasks
- Database queries are filtered by user_id
- API endpoints check user permissions

### Input Validation
- All user inputs are validated on both frontend and backend
- Maximum length restrictions prevent abuse
- Special characters are properly escaped

### Data Sanitization
- HTML escaping prevents XSS attacks
- SQL injection is prevented by using parameterized queries
- User inputs are sanitized before storage

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Task Management
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Troubleshooting

### Common Issues
1. **Backend not starting**: Verify Python and dependencies are installed
2. **Frontend not connecting to backend**: Check that both servers are running and URLs match
3. **Database connection errors**: Verify database URL and credentials in .env file
4. **Authentication not working**: Ensure BETTER_AUTH_SECRET is set correctly

### Debugging
- Check browser console for frontend errors
- Check terminal output for backend errors
- Verify all environment variables are set correctly
- Ensure the database is accessible and running

## Performance Tips

- The application uses efficient database queries with proper indexing
- API calls are optimized with appropriate caching headers
- Frontend implements loading states for better UX
- Database connection pooling is configured for performance

## Security Best Practices Demonstrated

1. **JWT Authentication**: Secure token-based authentication
2. **Input Validation**: Comprehensive validation on both frontend and backend
3. **Data Sanitization**: Prevention of XSS and injection attacks
4. **User Isolation**: Proper authorization to prevent data leakage
5. **Error Handling**: Appropriate error messages without sensitive information
6. **Secure Password Storage**: Passwords are hashed using bcrypt

## Conclusion

This demo showcases a production-ready todo application with proper security, performance, and user experience considerations. The implementation follows modern best practices for full-stack development with authentication, authorization, and responsive design.