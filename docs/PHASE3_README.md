# Phase III: AI-Powered Todo Chatbot

## Overview

Phase III adds an AI-powered chatbot interface that allows users to manage their todos through natural language conversations. The implementation uses:

- **Frontend**: Custom React-based chat interface
- **Backend**: FastAPI with OpenAI GPT-4 integration
- **AI Framework**: OpenAI Chat Completions API with function calling
- **MCP Server**: Custom implementation using official MCP SDK
- **Database**: Neon PostgreSQL (conversations and messages tables)

## Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │           FastAPI Server                     │     │                 │
│   Chat UI       │────▶│  ┌────────────────────────────────────────┐  │     │   Neon DB       │
│  (Frontend)     │     │  │  POST /api/{user_id}/chat              │  │     │  (PostgreSQL)   │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │  - tasks        │
│                 │     │                  ▼                           │     │  - conversations│
│                 │◀────│  ┌────────────────────────────────────────┐  │     │  - messages     │
│                 │     │  │     AI Service (OpenAI GPT-4)          │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │  MCP Server (Task Operation Tools)     │  │     │                 │
│                 │     │  │  - add_task                            │  │◀────│                 │
│                 │     │  │  - list_tasks                          │  │     │                 │
│                 │     │  │  - complete_task                       │  │     │                 │
│                 │     │  │  - delete_task                         │  │     │                 │
│                 │     │  │  - update_task                         │  │     │                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## Features

### 1. Natural Language Task Management

Users can interact with the chatbot using natural language to:

- **Add tasks**: "Add a task to buy groceries"
- **List tasks**: "Show me all my tasks" or "What's pending?"
- **Complete tasks**: "Mark task 3 as complete"
- **Delete tasks**: "Delete the meeting task"
- **Update tasks**: "Change task 1 to 'Call mom tonight'"

### 2. Stateless Architecture

- Server maintains no state between requests
- All conversation history stored in database
- Each request is independent and reproducible
- Horizontally scalable design

### 3. Context-Aware Conversations

- Maintains conversation history across sessions
- Can reference previous messages
- Remembers task IDs from earlier in conversation
- Server restarts don't lose context

### 4. Multi-Tool Execution

- AI can chain multiple tool calls in one response
- Example: "Complete task 1 and show me what's left"
- Executes operations in logical order

## Database Schema

### New Tables

#### conversations
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### messages
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id),
    user_id VARCHAR NOT NULL REFERENCES users(id),
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Chat Endpoint

**POST** `/api/{user_id}/chat`

Send a message to the AI chatbot and receive a response.

**Request:**
```json
{
  "conversation_id": 1,  // Optional - creates new if not provided
  "message": "Add a task to buy groceries"
}
```

**Response:**
```json
{
  "conversation_id": 1,
  "response": "I've added 'Buy groceries' to your task list (Task #5). What else can I help you with?",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "Buy groceries"
      },
      "result": {
        "task_id": 5,
        "status": "created",
        "title": "Buy groceries"
      }
    }
  ]
}
```

### Additional Endpoints

- **GET** `/api/{user_id}/conversations` - List all conversations
- **GET** `/api/{user_id}/conversations/{conversation_id}` - Get conversation history
- **DELETE** `/api/{user_id}/conversations/{conversation_id}` - Delete conversation

## MCP Tools

The following tools are exposed to the AI agent:

### 1. add_task
Create a new task for the user.

**Parameters:**
- `user_id` (string, required)
- `title` (string, required)
- `description` (string, optional)

### 2. list_tasks
Retrieve the user's tasks.

**Parameters:**
- `user_id` (string, required)
- `status` (string, optional): "all", "pending", or "completed"

### 3. complete_task
Mark a task as complete.

**Parameters:**
- `user_id` (string, required)
- `task_id` (integer, required)

### 4. delete_task
Remove a task from the list.

**Parameters:**
- `user_id` (string, required)
- `task_id` (integer, required)

### 5. update_task
Modify a task's title or description.

**Parameters:**
- `user_id` (string, required)
- `task_id` (integer, required)
- `title` (string, optional)
- `description` (string, optional)

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install openai==1.54.0 mcp==1.1.2
```

### 2. Configure Environment

Add to `backend/.env`:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Run Database Migration

The tables will be created automatically when you start the server, or run manually:

```bash
cd backend/migrations
python run_migration.py
```

### 4. Start Backend Server

```bash
cd backend
python main.py
```

Server runs on http://localhost:8000

### 5. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on http://localhost:3000

### 6. Access Chat Interface

Navigate to http://localhost:3000/chat

## Usage Examples

### Adding Tasks

**User**: "Add a task to buy groceries"

**Assistant**: "I've added 'Buy groceries' to your task list (Task #5). What else can I help you with?"

---

**User**: "I need to remember to call mom and pay bills"

**Assistant**: "I've added two new tasks:
- Task #6: Call mom
- Task #7: Pay bills

Anything else?"

### Listing Tasks

**User**: "Show me all my tasks"

**Assistant**: "Here are all your tasks:
1. Buy groceries
2. Call mom
3. Pay bills

You have 3 tasks total."

---

**User**: "What's pending?"

**Assistant**: "You have 3 pending tasks:
1. Buy groceries
2. Call mom
3. Pay bills"

### Completing Tasks

**User**: "Mark task 5 as complete"

**Assistant**: "Great! I've marked 'Buy groceries' as completed. Well done! 🎉"

---

**User**: "I finished buying groceries"

**Assistant**: "Excellent! I've marked 'Buy groceries' as completed. 🎉"

### Updating Tasks

**User**: "Change task 6 to 'Call mom tonight'"

**Assistant**: "I've updated task #6 to 'Call mom tonight'."

### Deleting Tasks

**User**: "Delete task 7"

**Assistant**: "I've deleted 'Pay bills' from your list."

### Complex Commands

**User**: "Complete task 5 and show me what's left"

**Assistant**: "Great! I've marked 'Buy groceries' as completed. 🎉

Here's what's left:
1. Call mom tonight
2. Finish report"

## Technical Implementation

### AI Service (`backend/services/ai_service.py`)

Handles OpenAI API integration:
- Manages conversation history
- Formats messages for OpenAI
- Executes function calls (MCP tools)
- Saves messages to database
- Provides stateless chat interface

### MCP Server (`backend/mcp/server.py`)

Implements MCP protocol:
- Defines 5 task operation tools
- Provides tool descriptions for AI
- Executes database operations
- Returns standardized responses

### Chat Route (`backend/routes/chat.py`)

FastAPI endpoints:
- POST `/api/{user_id}/chat` - Main chat interface
- GET `/api/{user_id}/conversations` - List conversations
- GET `/api/{user_id}/conversations/{id}` - Get history
- DELETE `/api/{user_id}/conversations/{id}` - Delete conversation

### Frontend Chat Page (`frontend/app/chat/page.tsx`)

React component with:
- Real-time chat interface
- Message history display
- Loading states
- Error handling
- Example commands
- New conversation button

## Key Benefits

### 1. Stateless Server
- Any server instance can handle any request
- Easy horizontal scaling
- No memory leaks from stored state
- Server restarts don't lose data

### 2. Persistent History
- All conversations stored in database
- Can resume conversations anytime
- Full audit trail of interactions
- Data survives server restarts

### 3. Natural Language Interface
- Intuitive user experience
- No need to learn commands
- Flexible input handling
- Context-aware responses

### 4. Tool Composition
- AI can chain multiple operations
- Intelligent task management
- Reduces user effort
- More efficient workflows

## Security Considerations

1. **Authentication**: All endpoints require valid JWT token
2. **Authorization**: Users can only access their own data
3. **Input Validation**: All inputs validated before processing
4. **Rate Limiting**: Consider adding rate limits for API calls
5. **API Key Security**: OpenAI key stored in environment variables

## Performance Optimization

1. **Database Indexes**: Optimized for conversation and message queries
2. **Conversation History Limit**: Default 10 messages for context
3. **Connection Pooling**: Database pool configured for concurrent requests
4. **Async Execution**: MCP tools use async operations

## Future Enhancements

- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Task scheduling and reminders
- [ ] Rich media in tasks (images, files)
- [ ] Task priorities and categories
- [ ] Shared tasks and collaboration
- [ ] Analytics and insights
- [ ] Custom AI personalities

## Troubleshooting

### Issue: "No module named 'openai'"
**Solution**: Install OpenAI package: `pip install openai==1.54.0`

### Issue: "OPENAI_API_KEY not found"
**Solution**: Add API key to `backend/.env` file

### Issue: Tables don't exist
**Solution**: Run migration script or restart server to auto-create tables

### Issue: Chat doesn't respond
**Solution**: Check OpenAI API key is valid and has credits

### Issue: 401 Unauthorized
**Solution**: Ensure you're logged in and auth token is valid

## Contributing

When adding new MCP tools:

1. Define tool in `backend/mcp/server.py`
2. Add to OpenAI tools list in `backend/services/ai_service.py`
3. Update tool map in `execute_mcp_tool()`
4. Document in `specs/phase3/mcp-tools.md`
5. Add usage examples to this README

## Credits

- **OpenAI**: GPT-4 language model
- **FastAPI**: Backend framework
- **Next.js**: Frontend framework
- **Neon**: PostgreSQL database
- **MCP SDK**: Model Context Protocol implementation

---

**Phase III implemented**: February 8, 2026
**Status**: ✅ Complete and operational
