# Database Schema

## Overview
PostgreSQL database with two main tables: `users` (managed by Better Auth) and `tasks`.

## Database Provider
**Neon Serverless PostgreSQL**
- Serverless, auto-scaling
- Branch-based development
- Generous free tier
- Connection URL format: `postgresql://user:password@host/database?sslmode=require`

## Tables

### users
Managed by Better Auth. Do not modify this table structure manually.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique user identifier (UUID) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(255) | | User's display name |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password (bcrypt) |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last updated time |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`

---

### tasks
User's todo tasks.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing task ID |
| user_id | VARCHAR(255) | FOREIGN KEY, NOT NULL | Owner's user ID |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | | Task description (optional) |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last updated time |

**Foreign Keys:**
- `user_id` REFERENCES `users(id)` ON DELETE CASCADE

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `user_id` (for filtering by user)
- INDEX on `completed` (for status filtering)
- INDEX on `created_at` (for sorting)

**Constraints:**
- `title` length: 1-200 characters
- `description` length: 0-1000 characters

---

## Relationships

```
users (1) ──── (many) tasks
  id    ────────────   user_id
```

One user can have many tasks. When a user is deleted, all their tasks are automatically deleted (CASCADE).

## SQLModel Models

### User Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Migration Strategy

### Initial Setup
1. Create Neon database
2. Copy connection string
3. Set `DATABASE_URL` environment variable
4. Run SQLModel table creation:
```python
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

### Schema Updates
For future schema changes:
- Use Alembic migrations (recommended)
- Or manually update models and recreate tables (dev only)

## Data Integrity

### Constraints
- **User Isolation**: All queries filtered by `user_id`
- **Referential Integrity**: Foreign key ensures tasks belong to valid users
- **Cascade Delete**: Deleting user removes all their tasks

### Validation
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- Email: Must be valid email format
- Password: Min 8 characters (enforced at application level)

## Indexes for Performance

### Optimized Queries
- `tasks.user_id`: Fast filtering by user
- `tasks.completed`: Fast status filtering
- `tasks.created_at`: Fast sorting by date
- `users.email`: Fast login lookups

### Query Examples
```sql
-- Get all tasks for a user (uses user_id index)
SELECT * FROM tasks WHERE user_id = '123' ORDER BY created_at DESC;

-- Get pending tasks (uses user_id + completed indexes)
SELECT * FROM tasks WHERE user_id = '123' AND completed = false;

-- Get user by email (uses email index)
SELECT * FROM users WHERE email = 'user@example.com';
```

## Connection Pooling

For production, configure connection pool:
```python
from sqlmodel import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Test connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

## Environment Variables

### Required
```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

### Optional
```
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_ECHO=false  # Set to true for SQL query logging
```

## Backup Strategy

### Neon Features
- Automatic daily backups
- Point-in-time recovery
- Branch-based development (create database branches)

### Manual Backup
```bash
pg_dump $DATABASE_URL > backup.sql
```

## Security Considerations

1. **Never expose DATABASE_URL** in client-side code
2. **Use SSL** for database connections (sslmode=require)
3. **Rotate passwords** periodically
4. **Limit permissions** - application user should not have DROP/ALTER privileges
5. **Encrypt sensitive data** if storing PII beyond email
