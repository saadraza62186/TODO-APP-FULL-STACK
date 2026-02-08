# MCP Tools Specification

## Overview
This document specifies the MCP (Model Context Protocol) tools that enable AI agents to manage tasks through natural language interactions.

## Tool Definitions

### 1. add_task

**Purpose:** Create a new task

**Parameters:**
- `user_id` (string, required) - ID of the user creating the task
- `title` (string, required) - Task title
- `description` (string, optional) - Task description

**Returns:**
```json
{
  "task_id": integer,
  "status": "created",
  "title": string
}
```

**Example:**
```json
// Input
{
  "user_id": "ziakhan",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

// Output
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

### 2. list_tasks

**Purpose:** Retrieve tasks from the list

**Parameters:**
- `user_id` (string, required) - ID of the user
- `status` (string, optional) - Filter by status: "all", "pending", "completed" (default: "all")

**Returns:**
```json
[
  {
    "id": integer,
    "title": string,
    "description": string,
    "completed": boolean,
    "created_at": string,
    "updated_at": string
  }
]
```

**Example:**
```json
// Input
{
  "user_id": "ziakhan",
  "status": "pending"
}

// Output
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-08T10:00:00Z",
    "updated_at": "2026-02-08T10:00:00Z"
  }
]
```

### 3. complete_task

**Purpose:** Mark a task as complete

**Parameters:**
- `user_id` (string, required) - ID of the user
- `task_id` (integer, required) - ID of the task to complete

**Returns:**
```json
{
  "task_id": integer,
  "status": "completed",
  "title": string
}
```

**Example:**
```json
// Input
{
  "user_id": "ziakhan",
  "task_id": 3
}

// Output
{
  "task_id": 3,
  "status": "completed",
  "title": "Call mom"
}
```

### 4. delete_task

**Purpose:** Remove a task from the list

**Parameters:**
- `user_id` (string, required) - ID of the user
- `task_id` (integer, required) - ID of the task to delete

**Returns:**
```json
{
  "task_id": integer,
  "status": "deleted",
  "title": string
}
```

**Example:**
```json
// Input
{
  "user_id": "ziakhan",
  "task_id": 2
}

// Output
{
  "task_id": 2,
  "status": "deleted",
  "title": "Old task"
}
```

### 5. update_task

**Purpose:** Modify task title or description

**Parameters:**
- `user_id` (string, required) - ID of the user
- `task_id` (integer, required) - ID of the task to update
- `title` (string, optional) - New task title
- `description` (string, optional) - New task description

**Returns:**
```json
{
  "task_id": integer,
  "status": "updated",
  "title": string
}
```

**Example:**
```json
// Input
{
  "user_id": "ziakhan",
  "task_id": 1,
  "title": "Buy groceries and fruits"
}

// Output
{
  "task_id": 1,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

## Error Handling

All tools should return standardized error responses:

```json
{
  "error": true,
  "message": "Description of the error",
  "code": "ERROR_CODE"
}
```

### Common Error Codes:
- `TASK_NOT_FOUND` - Task ID doesn't exist
- `UNAUTHORIZED` - User doesn't have access to the task
- `INVALID_INPUT` - Required parameters missing or invalid
- `DATABASE_ERROR` - Database operation failed
