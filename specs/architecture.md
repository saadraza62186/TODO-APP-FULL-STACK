# System Architecture

## Overview
This is a full-stack web application with clear separation between frontend and backend services.

## Component Architecture

```
┌─────────────────────────────────────────────┐
│           Browser (Client)                  │
│  ┌───────────────────────────────────────┐  │
│  │     Next.js Frontend (Port 3000)      │  │
│  │  - Server Components                  │  │
│  │  - Client Components                  │  │
│  │  - Better Auth Integration            │  │
│  └───────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │ HTTP + JWT
                  │
┌─────────────────▼───────────────────────────┐
│     FastAPI Backend (Port 8000)             │
│  ┌───────────────────────────────────────┐  │
│  │  JWT Verification Middleware          │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  REST API Routes                      │  │
│  │  - /api/{user_id}/tasks               │  │
│  └───────────────────────────────────────┘  │
│  ┌───────────────────────────────────────┐  │
│  │  SQLModel ORM                         │  │
│  └───────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │ SQL
                  │
┌─────────────────▼───────────────────────────┐
│   Neon Serverless PostgreSQL                │
│  - users table (Better Auth)                │
│  - tasks table                              │
└─────────────────────────────────────────────┘
```

## Authentication Flow

1. **User Registration/Login**
   - User submits credentials to Better Auth
   - Better Auth creates session and issues JWT token
   - Token stored in browser (httpOnly cookie or localStorage)

2. **API Request**
   - Frontend includes JWT in Authorization header
   - Backend middleware verifies JWT signature
   - Backend extracts user_id from token
   - Backend validates user_id matches URL parameter

3. **Data Access**
   - All database queries filtered by authenticated user_id
   - Ensures complete data isolation between users

## Technology Choices

### Frontend: Next.js 16+ (App Router)
- **Why**: Server components for better performance, modern React patterns
- **Benefits**: SEO-friendly, fast page loads, automatic code splitting

### Backend: FastAPI
- **Why**: Fast, modern Python framework with automatic API documentation
- **Benefits**: Type hints, async support, OpenAPI integration

### ORM: SQLModel
- **Why**: Combines Pydantic and SQLAlchemy, works perfectly with FastAPI
- **Benefits**: Type safety, easy validation, great developer experience

### Database: Neon Serverless PostgreSQL
- **Why**: Serverless, auto-scaling, generous free tier
- **Benefits**: No infrastructure management, branch-based workflows

### Auth: Better Auth
- **Why**: Modern, TypeScript-first auth library for Next.js
- **Benefits**: JWT support, easy integration, flexible configuration

## API Security

### JWT Token Structure
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Security Measures
1. **Token Verification**: Backend verifies JWT signature on every request
2. **User Isolation**: All queries filtered by authenticated user_id
3. **Token Expiry**: JWTs expire after configured time (e.g., 7 days)
4. **HTTPS Only**: Production requires HTTPS for token transmission
5. **Shared Secret**: Same secret key used for signing and verification

## Data Flow

### Creating a Task
1. User fills task form in Next.js frontend
2. Frontend calls API client with task data
3. API client attaches JWT token to request
4. Backend verifies JWT and extracts user_id
5. Backend creates task with authenticated user_id
6. Response sent back to frontend
7. Frontend updates UI with new task

### Listing Tasks
1. User navigates to tasks page
2. Frontend calls GET /api/{user_id}/tasks
3. JWT token included in Authorization header
4. Backend verifies token and extracts user_id
5. Backend queries tasks WHERE user_id = authenticated_user_id
6. Only user's tasks returned, never other users' data
7. Frontend renders task list

## Environment Configuration

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

## Deployment Architecture

### Development
- Frontend: `npm run dev` (localhost:3000)
- Backend: `uvicorn main:app --reload` (localhost:8000)
- Database: Neon free tier

### Production
- Frontend: Vercel or similar Next.js hosting
- Backend: Railway, Render, or similar Python hosting
- Database: Neon serverless (same connection string)
