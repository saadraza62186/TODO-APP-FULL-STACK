# REST API Endpoints

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://api.yourdomain.com`

## Authentication
All endpoints require JWT token in header:
```
Authorization: Bearer <jwt_token>
```

Missing or invalid token returns `401 Unauthorized`.

## Common Response Codes
- `200 OK`: Successful GET request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Validation error
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server error

## Endpoints

### GET /api/{user_id}/tasks
List all tasks for authenticated user.

**Path Parameters:**
- `user_id` (string): User's ID (must match authenticated user)

**Query Parameters:**
- `status` (optional): Filter by status
  - Values: `all` | `pending` | `completed`
  - Default: `all`
- `sort` (optional): Sort order
  - Values: `created` | `title` | `updated`
  - Default: `created`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-01T10:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z"
  }
]
```

**Error Responses:**
- `401`: Token missing or invalid
- `403`: user_id doesn't match authenticated user

---

### POST /api/{user_id}/tasks
Create a new task.

**Path Parameters:**
- `user_id` (string): User's ID (must match authenticated user)

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation:**
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

**Error Responses:**
- `400`: Validation error (title missing or too long)
- `401`: Token missing or invalid
- `403`: user_id doesn't match authenticated user

---

### GET /api/{user_id}/tasks/{id}
Get details of a specific task.

**Path Parameters:**
- `user_id` (string): User's ID (must match authenticated user)
- `id` (integer): Task ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-01T10:00:00Z"
}
```

**Error Responses:**
- `401`: Token missing or invalid
- `403`: Task belongs to different user
- `404`: Task not found

---

### PUT /api/{user_id}/tasks/{id}
Update a task (full update).

**Path Parameters:**
- `user_id` (string): User's ID (must match authenticated user)
- `id` (integer): Task ID

**Request Body:**
```json
{
  "title": "Buy groceries and cook dinner",
  "description": "Updated description"
}
```

**Validation:**
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries and cook dinner",
  "description": "Updated description",
  "completed": false,
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-05T14:30:00Z"
}
```

**Error Responses:**
- `400`: Validation error
- `401`: Token missing or invalid
- `403`: Task belongs to different user
- `404`: Task not found

---

### DELETE /api/{user_id}/tasks/{id}
Delete a task.

**Path Parameters:**
- `user_id` (string): User's ID (must match authenticated user)
- `id` (integer): Task ID

**Response:** `204 No Content`
(Empty response body)

**Error Responses:**
- `401`: Token missing or invalid
- `403`: Task belongs to different user
- `404`: Task not found

---

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status.

**Path Parameters:**
- `user_id` (string): User's ID (must match authenticated user)
- `id` (integer): Task ID

**Request Body:**
```json
{
  "completed": true
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-02-01T10:00:00Z",
  "updated_at": "2026-02-05T15:00:00Z"
}
```

**Error Responses:**
- `401`: Token missing or invalid
- `403`: Task belongs to different user
- `404`: Task not found

---

## Security Implementation

### JWT Verification Flow
1. Extract token from `Authorization: Bearer <token>` header
2. Verify token signature using `BETTER_AUTH_SECRET`
3. Decode token to extract `user_id`
4. Compare token `user_id` with URL path `user_id`
5. If mismatch, return `403 Forbidden`
6. If match, proceed with request

### Data Isolation
All database queries MUST include:
```sql
WHERE user_id = <authenticated_user_id>
```

This ensures users can only access their own data.

## CORS Configuration
Backend must allow requests from frontend origin:
```python
# FastAPI CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Rate Limiting (Optional)
Consider implementing rate limiting for production:
- 100 requests per minute per user
- 429 status code when limit exceeded

## API Documentation
FastAPI automatically generates interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
