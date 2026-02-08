# Phase III API Endpoints

## Chat Endpoint

### Send Message and Get AI Response

**Endpoint:** `POST /api/{user_id}/chat`

**Description:** Send a message to the AI chatbot and receive a response. The chatbot can manage tasks through natural language.

**Path Parameters:**
- `user_id` (string, required) - ID of the user sending the message

**Request Body:**
```json
{
  "conversation_id": 123,  // Optional - creates new if not provided
  "message": "Add a task to buy groceries"  // Required
}
```

**Request Schema:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| conversation_id | integer | No | Existing conversation ID (creates new if not provided) |
| message | string | Yes | User's natural language message |

**Response Body:**
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list (Task #5). Anything else?",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "user_id": "ziakhan",
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

**Response Schema:**
| Field | Type | Description |
|-------|------|-------------|
| conversation_id | integer | The conversation ID (existing or newly created) |
| response | string | AI assistant's response text |
| tool_calls | array | List of MCP tools invoked during this request |

**Status Codes:**
- `200 OK` - Successful response
- `400 Bad Request` - Invalid request body or missing required fields
- `401 Unauthorized` - Invalid or missing authentication token
- `500 Internal Server Error` - Server error

**Example Requests:**

#### 1. Start New Conversation
```bash
curl -X POST "http://localhost:8000/api/ziakhan/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
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
        "user_id": "ziakhan",
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

#### 2. Continue Existing Conversation
```bash
curl -X POST "http://localhost:8000/api/ziakhan/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "conversation_id": 1,
    "message": "Show me all my tasks"
  }'
```

**Response:**
```json
{
  "conversation_id": 1,
  "response": "Here are all your tasks:\n1. Buy groceries\n2. Call mom\n3. Finish report\n\nYou have 3 tasks total.",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "arguments": {
        "user_id": "ziakhan",
        "status": "all"
      },
      "result": [
        {
          "id": 5,
          "title": "Buy groceries",
          "completed": false
        },
        {
          "id": 6,
          "title": "Call mom",
          "completed": false
        },
        {
          "id": 7,
          "title": "Finish report",
          "completed": false
        }
      ]
    }
  ]
}
```

#### 3. Multiple Actions in One Request
```bash
curl -X POST "http://localhost:8000/api/ziakhan/chat" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "conversation_id": 1,
    "message": "Mark task 5 as complete and show me what is left"
  }'
```

**Response:**
```json
{
  "conversation_id": 1,
  "response": "Great! I've marked 'Buy groceries' as completed. 🎉\n\nHere's what's left:\n1. Call mom\n2. Finish report",
  "tool_calls": [
    {
      "tool": "complete_task",
      "arguments": {
        "user_id": "ziakhan",
        "task_id": 5
      },
      "result": {
        "task_id": 5,
        "status": "completed",
        "title": "Buy groceries"
      }
    },
    {
      "tool": "list_tasks",
      "arguments": {
        "user_id": "ziakhan",
        "status": "pending"
      },
      "result": [
        {
          "id": 6,
          "title": "Call mom",
          "completed": false
        },
        {
          "id": 7,
          "title": "Finish report",
          "completed": false
        }
      ]
    }
  ]
}
```

## Conversation Management Endpoints (Optional)

### List User Conversations

**Endpoint:** `GET /api/{user_id}/conversations`

**Description:** Get all conversations for a user

**Response:**
```json
{
  "conversations": [
    {
      "id": 1,
      "created_at": "2026-02-08T10:00:00Z",
      "updated_at": "2026-02-08T15:30:00Z",
      "message_count": 12
    }
  ]
}
```

### Get Conversation History

**Endpoint:** `GET /api/{user_id}/conversations/{conversation_id}`

**Description:** Get all messages in a conversation

**Response:**
```json
{
  "conversation_id": 1,
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "Add a task to buy groceries",
      "created_at": "2026-02-08T10:00:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "I've added 'Buy groceries' to your task list (Task #5).",
      "created_at": "2026-02-08T10:00:01Z"
    }
  ]
}
```

### Delete Conversation

**Endpoint:** `DELETE /api/{user_id}/conversations/{conversation_id}`

**Description:** Delete a conversation and all its messages

**Response:**
```json
{
  "status": "deleted",
  "conversation_id": 1
}
```

## Error Responses

**400 Bad Request:**
```json
{
  "detail": "Message is required"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Invalid or missing authentication token"
}
```

**404 Not Found:**
```json
{
  "detail": "Conversation not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "An error occurred while processing your request"
}
```
