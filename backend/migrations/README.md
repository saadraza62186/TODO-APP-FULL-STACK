# Migrations

This directory contains database migration scripts for the Todo App.

## Running Migrations

### Method 1: Using SQLModel (Automatic)

The easiest way is to let SQLModel automatically create the tables when the application starts:

```bash
cd backend
python main.py
```

SQLModel will automatically create the `conversations` and `messages` tables based on the models defined in `models.py`.

### Method 2: Using SQL Migration Script

If you prefer to run the migration manually:

```bash
cd backend/migrations
python run_migration.py
```

This will execute the SQL script `001_add_chat_tables.sql` which creates:
- `conversations` table
- `messages` table  
- Indexes for performance
- Trigger to auto-update conversation timestamps

## Migration Files

- `001_add_chat_tables.sql` - SQL script for Phase III chat functionality
- `run_migration.py` - Python script to execute SQL migrations

## Verify Migration

After running the migration, verify the tables exist:

```bash
# Using psql
psql $DATABASE_URL -c "\dt"

# Should show:
# - users
# - tasks
# - conversations (new)
# - messages (new)
```

## Rollback

To rollback the Phase III tables:

```sql
DROP TRIGGER IF EXISTS trigger_update_conversation_timestamp ON messages;
DROP FUNCTION IF EXISTS update_conversation_timestamp();
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
```
