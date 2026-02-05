# Backend Guidelines

## Stack
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Auth**: JWT verification (Better Auth tokens)
- **Validation**: Pydantic (built into FastAPI)

## Project Structure
```
backend/
├── main.py              # FastAPI app entry point
├── models.py            # SQLModel database models
├── schemas.py           # Pydantic request/response models
├── routes/              # API route handlers
│   ├── __init__.py
│   ├── tasks.py         # Task endpoints
│   └── health.py        # Health check
├── middleware/          # Custom middleware
│   ├── __init__.py
│   └── auth.py          # JWT verification
├── db.py                # Database connection and session
├── config.py            # Configuration and environment variables
├── requirements.txt     # Python dependencies
└── tests/               # Test files
```

## Development Patterns

### Application Setup
```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import tasks, health
from db import create_db_and_tables

app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(tasks.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

### Database Models
```python
# models.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Pydantic Schemas
```python
# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

### API Routes
```python
# routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from db import get_session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from middleware.auth import get_current_user

router = APIRouter(prefix="/{user_id}/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskResponse])
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Query tasks
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    
    # Create task
    task = Task(user_id=user_id, **task_data.dict())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### JWT Authentication Middleware
```python
# middleware/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from config import settings

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verify JWT token and extract user_id.
    Returns user_id if token is valid, raises HTTPException otherwise.
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

### Database Session
```python
# db.py
from sqlmodel import create_engine, SQLModel, Session
from config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Test connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for database session."""
    with Session(engine) as session:
        yield session
```

### Configuration
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    CORS_ORIGINS: str = "http://localhost:3000"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## API Conventions

### Naming
- **Endpoints**: Lowercase with hyphens (`/api/{user_id}/tasks`)
- **Functions**: Snake_case (`get_tasks`, `create_task`)
- **Classes**: PascalCase (`TaskCreate`, `TaskResponse`)
- **Variables**: Snake_case (`user_id`, `task_data`)

### Response Codes
- `200 OK`: Successful GET/PUT/PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing/invalid token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server error

### Error Handling
```python
from fastapi import HTTPException, status

# Not found
raise HTTPException(status_code=404, detail="Task not found")

# Forbidden
raise HTTPException(status_code=403, detail="Forbidden")

# Validation error (automatic via Pydantic)
# FastAPI handles this automatically
```

### Validation
Use Pydantic Field validators:
```python
from pydantic import BaseModel, Field, validator

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
```

## Database Operations

### Query Patterns
```python
from sqlmodel import select

# Get all tasks for user
statement = select(Task).where(Task.user_id == user_id)
tasks = session.exec(statement).all()

# Get single task
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id
)
task = session.exec(statement).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")

# Filter by status
statement = select(Task).where(
    Task.user_id == user_id,
    Task.completed == True
)
completed_tasks = session.exec(statement).all()

# Update task
task.title = new_title
task.updated_at = datetime.utcnow()
session.add(task)
session.commit()
session.refresh(task)

# Delete task
session.delete(task)
session.commit()
```

### Transactions
```python
from sqlmodel import Session

def create_multiple_tasks(user_id: str, tasks_data: List[TaskCreate]):
    with Session(engine) as session:
        try:
            for task_data in tasks_data:
                task = Task(user_id=user_id, **task_data.dict())
                session.add(task)
            session.commit()
        except Exception:
            session.rollback()
            raise
```

## Security Best Practices

### JWT Verification
- Always verify token signature
- Check token expiration
- Extract and validate user_id
- Compare with URL parameter

### User Data Isolation
- **Always filter by user_id** in database queries
- Never trust URL parameters alone
- Verify authenticated user matches requested resource owner

### Environment Secrets
```python
# Good - use environment variables
secret = os.getenv("BETTER_AUTH_SECRET")

# Bad - hardcoded secrets
secret = "my-secret-key-123"  # DON'T DO THIS
```

### SQL Injection Prevention
- SQLModel/SQLAlchemy handles this automatically
- Never use string concatenation for queries
- Use parameterized queries

## Testing

### Test Structure
```python
# tests/test_tasks.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_task():
    response = client.post(
        "/api/user123/tasks",
        json={"title": "Test Task"},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

def test_unauthorized():
    response = client.get("/api/user123/tasks")
    assert response.status_code == 401
```

## Environment Variables

### Required Variables
```env
# .env
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
DEBUG=false
```

### Loading Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

## Performance Optimization

### Database Connection Pooling
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Number of connections to maintain
    max_overflow=10,       # Max additional connections
    pool_pre_ping=True,    # Test connection before using
    pool_recycle=3600,     # Recycle after 1 hour
)
```

### Query Optimization
- Use indexes on frequently queried columns
- Avoid N+1 queries
- Use select() for filtering at database level
- Limit result sets when appropriate

## Development Commands

```bash
# Run development server
uvicorn main:app --reload --port 8000

# Run with debug mode
uvicorn main:app --reload --log-level debug

# Run tests
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html

# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## API Documentation
FastAPI automatically generates interactive docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Logging

### Setup Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/tasks")
def get_tasks():
    logger.info(f"Fetching tasks for user {user_id}")
    # ...
```

## Common Patterns

### Dependency Injection
```python
from fastapi import Depends

# Database session
def get_tasks(session: Session = Depends(get_session)):
    # Use session

# Current user
def get_tasks(current_user: str = Depends(get_current_user)):
    # Use current_user

# Multiple dependencies
def get_tasks(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    # Use both
```

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python JWT](https://pyjwt.readthedocs.io/)
