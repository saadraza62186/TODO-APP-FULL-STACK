# Backend - Todo API

## Overview
FastAPI backend for Todo application with JWT authentication and PostgreSQL database.

## Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification (Better Auth tokens)
- **Validation**: Pydantic

## Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL (or Neon account)
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env with your actual values
```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database connection (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require

# Authentication secret (MUST match frontend)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000

# Debug mode
DEBUG=false
```

**Important**: `BETTER_AUTH_SECRET` must be the same in both frontend and backend!

## Running the Application

### Development Mode
```bash
uvicorn main:app --reload --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Debug Logging
```bash
# Set DEBUG=true in .env, then:
uvicorn main:app --reload --log-level debug
```

## API Documentation

Once the server is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /health
```

### Task Endpoints (All require JWT authentication)

```
GET    /api/{user_id}/tasks              - List all tasks
POST   /api/{user_id}/tasks              - Create new task
GET    /api/{user_id}/tasks/{id}         - Get task details
PUT    /api/{user_id}/tasks/{id}         - Update task
DELETE /api/{user_id}/tasks/{id}         - Delete task
PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion
```

### Query Parameters

**GET /api/{user_id}/tasks**
- `status`: Filter by status (`all`, `pending`, `completed`)
- `sort`: Sort order (`created`, `title`, `updated`)

## Authentication

All task endpoints require JWT token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

The backend:
1. Verifies JWT signature using `BETTER_AUTH_SECRET`
2. Extracts `user_id` from token
3. Validates token `user_id` matches URL `user_id`
4. Filters all queries by authenticated user's ID

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration and settings
├── models.py            # SQLModel database models
├── schemas.py           # Pydantic request/response schemas
├── db.py                # Database connection and session
├── middleware/          # Custom middleware
│   ├── __init__.py
│   └── auth.py          # JWT verification
├── routes/              # API route handlers
│   ├── __init__.py
│   ├── health.py        # Health check endpoint
│   └── tasks.py         # Task CRUD endpoints
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (not in git)
```

## Database

### Schema

**users** (managed by Better Auth)
- id (string, PK)
- email (string, unique)
- name (string, nullable)
- password_hash (string)
- created_at (timestamp)
- updated_at (timestamp)

**tasks**
- id (serial, PK)
- user_id (string, FK)
- title (string, max 200)
- description (text, nullable)
- completed (boolean, default false)
- created_at (timestamp)
- updated_at (timestamp)

### Migrations

Tables are automatically created on first startup using SQLModel.

For production, consider using Alembic for database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Generate migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Testing

### Run Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Test Files
```
tests/
├── __init__.py
├── test_health.py
├── test_tasks.py
└── test_auth.py
```

## Code Quality

### Format Code
```bash
black .
```

### Lint Code
```bash
flake8 .
```

### Type Checking
```bash
mypy .
```

## Security

### Best Practices
- ✅ All endpoints require valid JWT token
- ✅ User data completely isolated (queries filtered by user_id)
- ✅ SQL injection prevention (SQLModel parameterized queries)
- ✅ Password hashing (handled by Better Auth)
- ✅ HTTPS in production (configure reverse proxy)
- ✅ Environment secrets never committed to git

### JWT Verification
- Token signature verified using shared secret
- Token expiration checked
- User ID extracted and validated
- URL user_id must match token user_id

## Deployment

### Prerequisites
- Set all environment variables
- Use production database (Neon PostgreSQL)
- Enable HTTPS (use reverse proxy like Nginx)
- Set `DEBUG=false`

### Platforms
- **Railway**: Automatic deployment from Git
- **Render**: Web service with auto-deploy
- **Heroku**: Using buildpack
- **AWS/GCP/Azure**: Container deployment

### Example: Railway
1. Push code to GitHub
2. Create new Railway project
3. Add PostgreSQL database (or use Neon)
4. Set environment variables
5. Deploy from GitHub repo

## Troubleshooting

### Common Issues

**1. Database connection error**
- Verify `DATABASE_URL` is correct
- Check database is running
- Ensure SSL mode is set correctly

**2. JWT authentication fails**
- Verify `BETTER_AUTH_SECRET` matches frontend
- Check token is included in Authorization header
- Ensure token hasn't expired

**3. CORS errors**
- Check `CORS_ORIGINS` includes frontend URL
- Verify credentials are allowed
- Check preflight requests succeed

**4. Import errors**
- Activate virtual environment
- Install all requirements: `pip install -r requirements.txt`

### Debug Mode
Enable detailed logging by setting `DEBUG=true` in `.env`

## Dependencies

Main dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlmodel` - ORM (combines SQLAlchemy + Pydantic)
- `pydantic-settings` - Settings management
- `pyjwt` - JWT token verification
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable loading

Development dependencies:
- `pytest` - Testing framework
- `pytest-cov` - Test coverage
- `httpx` - HTTP client for testing

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Neon Documentation](https://neon.tech/docs)

## License
MIT License - Hackathon II Project
