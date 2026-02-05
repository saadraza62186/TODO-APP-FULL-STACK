# Todo App - Hackathon II

## Project Overview
This is a monorepo using GitHub Spec-Kit for spec-driven development.

## Spec-Kit Structure
Specifications are organized in `/specs`:
- `/specs/overview.md` - Project overview
- `/specs/architecture.md` - System architecture
- `/specs/features/` - Feature specs (what to build)
- `/specs/api/` - API endpoint specifications
- `/specs/database/` - Schema and model specs
- `/specs/ui/` - Component and page specs

## How to Use Specs
1. Always read relevant spec before implementing
2. Reference specs with: `@specs/features/task-crud.md`
3. Update specs if requirements change

## Project Structure
```
hackathon-todo/
├── .spec-kit/           # Spec-Kit configuration
├── specs/               # All specifications
├── frontend/            # Next.js 16 app
├── backend/             # Python FastAPI server
├── docker-compose.yml   # Docker orchestration
└── README.md            # Setup instructions
```

## Technology Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth**: Better Auth with JWT

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL

## Development Workflow
1. **Read spec**: `@specs/features/[feature].md`
2. **Implement backend**: `@backend/CLAUDE.md`
3. **Implement frontend**: `@frontend/CLAUDE.md`
4. **Test and iterate**

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL (or Neon account)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Create `.env` files in both frontend and backend directories. See `.env.example` in each directory for required variables.

## Commands

### Development
- **Frontend**: `cd frontend && npm run dev` (port 3000)
- **Backend**: `cd backend && uvicorn main:app --reload` (port 8000)
- **Both**: `docker-compose up` (if using Docker)

### Testing
- **Frontend**: `cd frontend && npm test`
- **Backend**: `cd backend && pytest`

### Database
- **Create tables**: Handled automatically by SQLModel on first run
- **Migrations**: Use Alembic (see backend/README.md)

## API Documentation
When backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Phase II Features
- ✅ User authentication (Better Auth + JWT)
- ✅ Task CRUD operations
- ✅ Multi-user support with data isolation
- ✅ RESTful API with JWT security
- ✅ Responsive frontend interface
- ✅ PostgreSQL persistent storage

## Architecture Overview

### Authentication Flow
1. User signs up/in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend includes token in all API requests
4. Backend verifies token and extracts user_id
5. All data queries filtered by user_id

### API Endpoints
```
GET    /api/{user_id}/tasks           - List all tasks
POST   /api/{user_id}/tasks           - Create task
GET    /api/{user_id}/tasks/{id}      - Get task details
PUT    /api/{user_id}/tasks/{id}      - Update task
DELETE /api/{user_id}/tasks/{id}      - Delete task
PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion
```

## Project Guidelines

### Code Style
- **Frontend**: TypeScript with strict mode, Prettier formatting
- **Backend**: PEP 8 style, Black formatting
- **Commits**: Conventional commits (feat:, fix:, docs:, etc.)

### Security
- All API endpoints require valid JWT token
- User data completely isolated (can only access own tasks)
- Passwords hashed with bcrypt
- HTTPS required in production
- Environment secrets never committed to git

### Testing
- Write tests for all API endpoints
- Test authentication and authorization
- Test user data isolation
- Frontend component tests

## Troubleshooting

### Common Issues
1. **CORS errors**: Check CORS_ORIGINS in backend .env
2. **Auth errors**: Ensure BETTER_AUTH_SECRET matches in both services
3. **Database errors**: Verify DATABASE_URL is correct
4. **Port conflicts**: Check ports 3000 and 8000 are available

### Debug Mode
- **Backend**: Set `DEBUG=true` in .env for detailed logs
- **Frontend**: Check browser console for errors

## Resources
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Better Auth Documentation](https://better-auth.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon Documentation](https://neon.tech/docs)

## Contributing
This is a hackathon project. Follow spec-driven development approach:
1. Update/create spec in `/specs`
2. Reference spec when implementing
3. Test implementation against spec requirements

## License
MIT License - Hackathon II Project
