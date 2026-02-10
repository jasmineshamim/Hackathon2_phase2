# Todo App

A secure, full-stack todo application with authentication and task management capabilities.

## Features

- User registration and authentication
- Secure JWT-based authentication
- Task management (create, read, update, delete)
- Task completion toggling
- Responsive UI that works on mobile and desktop
- User isolation (users can only access their own tasks)

## Tech Stack

- **Frontend**: Next.js 14+ with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT tokens with refresh mechanism
- **Deployment**: Frontend on Vercel, Backend on Railway/Render

## Setup Instructions

### Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL client tools (for Neon connection)

### Environment Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Install Backend Dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install Frontend Dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL="postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"
BETTER_AUTH_URL="http://localhost:3000"
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_BASE_URL="http://localhost:8000/api"
```

### Running the Application

#### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### Frontend (Next.js)
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Task Management (JWT Required)
- `GET /api/tasks/` - List all user tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle completion status

## Development Workflow

1. Start backend server on port 8000
2. Start frontend server on port 3000
3. Access the application at http://localhost:3000
4. Register/login to create tasks
5. All API calls will automatically include JWT tokens

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Security Features

- JWT-based authentication with refresh tokens
- User data isolation (users can only access their own tasks)
- Password hashing with bcrypt
- Input sanitization to prevent XSS
- Rate limiting for login attempts
- HTTPS enforcement in production

## Deployment

### Frontend
Deploy to Vercel or similar platform:
```bash
npm run build
```

### Backend
Deploy to Railway, Render, or similar platform with Python support.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.