# Phase III Database Schema

## New Tables

### Conversation Table

**Table Name:** `conversations`

**Description:** Stores chat sessions between users and the AI assistant

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique conversation identifier |
| user_id | VARCHAR | NOT NULL, FOREIGN KEY → users(id) | User who owns this conversation |
| created_at | TIMESTAMP | NOT NULL, DEFAULT current_timestamp | When conversation was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT current_timestamp | Last message timestamp |

**Indexes:**
- `idx_conversations_user_id` on `user_id` - Fast lookup of user's conversations
- `idx_conversations_updated_at` on `updated_at` - Sort conversations by recent activity

**SQL Schema:**
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at DESC);
```

---

### Message Table

**Table Name:** `messages`

**Description:** Stores individual messages within conversations

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique message identifier |
| conversation_id | INTEGER | NOT NULL, FOREIGN KEY → conversations(id) | Conversation this message belongs to |
| user_id | VARCHAR | NOT NULL, FOREIGN KEY → users(id) | User who sent/received this message |
| role | VARCHAR(20) | NOT NULL, CHECK IN ('user', 'assistant') | Message sender: user or assistant |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT current_timestamp | When message was created |

**Indexes:**
- `idx_messages_conversation_id` on `conversation_id` - Fast lookup of conversation messages
- `idx_messages_created_at` on `created_at` - Order messages chronologically

**SQL Schema:**
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

---

## Updated Existing Tables

### Task Table (No Changes Required)

The existing `tasks` table already has all required fields for Phase III:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

---

## Relationships

```
users (1) ←→ (many) conversations
users (1) ←→ (many) messages
users (1) ←→ (many) tasks

conversations (1) ←→ (many) messages
```

**Diagram:**
```
┌─────────────┐
│   users     │
│  id (PK)    │
│  email      │
│  name       │
│  ...        │
└──────┬──────┘
       │
       ├─────────────────┬─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│conversations │  │   messages   │  │    tasks     │
│  id (PK)     │  │  id (PK)     │  │  id (PK)     │
│  user_id (FK)│  │  conv_id (FK)│  │  user_id (FK)│
│  created_at  │  │  user_id (FK)│  │  title       │
│  updated_at  │  │  role        │  │  completed   │
└──────┬───────┘  │  content     │  │  ...         │
       │          │  created_at  │  └──────────────┘
       │          └──────────────┘
       │                 ▲
       └─────────────────┘
```

---

## Migration Script

**File:** `backend/migrations/add_chat_tables.sql`

```sql
-- Migration: Add Chat Tables for Phase III
-- Date: 2026-02-08
-- Description: Add conversations and messages tables for AI chatbot functionality

BEGIN;

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for conversations
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at DESC);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for messages
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- Add a trigger to update conversations.updated_at when a message is added
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_conversation_timestamp
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION update_conversation_timestamp();

COMMIT;
```

---

## Sample Data

```sql
-- Sample conversation
INSERT INTO conversations (user_id, created_at, updated_at)
VALUES ('ziakhan', '2026-02-08 10:00:00', '2026-02-08 10:05:00');

-- Sample messages
INSERT INTO messages (conversation_id, user_id, role, content, created_at)
VALUES
(1, 'ziakhan', 'user', 'Add a task to buy groceries', '2026-02-08 10:00:00'),
(1, 'ziakhan', 'assistant', 'I''ve added ''Buy groceries'' to your task list (Task #5).', '2026-02-08 10:00:01'),
(1, 'ziakhan', 'user', 'Show me all my tasks', '2026-02-08 10:05:00'),
(1, 'ziakhan', 'assistant', 'Here are all your tasks: 1. Buy groceries', '2026-02-08 10:05:01');
```

---

## Query Examples

### Get conversation history
```sql
SELECT m.role, m.content, m.created_at
FROM messages m
WHERE m.conversation_id = 1
ORDER BY m.created_at ASC;
```

### Get user's conversations ordered by most recent
```sql
SELECT c.id, c.created_at, c.updated_at, COUNT(m.id) as message_count
FROM conversations c
LEFT JOIN messages m ON c.id = m.conversation_id
WHERE c.user_id = 'ziakhan'
GROUP BY c.id
ORDER BY c.updated_at DESC;
```

### Get all messages with task operations
```sql
SELECT m.content, m.role, m.created_at
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE c.user_id = 'ziakhan'
  AND m.content LIKE '%task%'
ORDER BY m.created_at DESC
LIMIT 10;
```
