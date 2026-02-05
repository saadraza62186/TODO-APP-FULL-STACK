# Feature: Task CRUD Operations

## User Stories

### Create Task
- **As a user**, I can create a new task with a title and optional description
- **As a user**, my task is automatically associated with my account
- **As a user**, I cannot create tasks for other users

### View Tasks
- **As a user**, I can view all my tasks in a list
- **As a user**, I can only see my own tasks, not other users' tasks
- **As a user**, I can see task details including title, description, status, and created date

### Update Task
- **As a user**, I can edit the title and description of my tasks
- **As a user**, I cannot edit other users' tasks
- **As a user**, the updated timestamp is automatically set

### Delete Task
- **As a user**, I can delete my tasks
- **As a user**, I cannot delete other users' tasks
- **As a user**, deleted tasks are permanently removed

### Toggle Completion
- **As a user**, I can mark a task as complete or incomplete
- **As a user**, completed tasks are visually distinguished from pending tasks

## Acceptance Criteria

### Create Task
- ✅ Title is required (1-200 characters)
- ✅ Description is optional (max 1000 characters)
- ✅ Task is associated with logged-in user's ID
- ✅ Created timestamp is automatically set
- ✅ Task defaults to incomplete status
- ✅ Returns 401 if user is not authenticated
- ✅ Returns created task with ID in response

### View Tasks
- ✅ Only show tasks for authenticated user
- ✅ Display title, description, status, created date
- ✅ Support filtering by status (all/pending/completed)
- ✅ Support sorting (by created date, title, due date)
- ✅ Returns empty array if user has no tasks
- ✅ Returns 401 if user is not authenticated

### Update Task
- ✅ Can update title and/or description
- ✅ Cannot change user_id (ownership)
- ✅ Updated timestamp automatically set
- ✅ Returns 404 if task doesn't exist
- ✅ Returns 403 if task belongs to different user
- ✅ Returns 401 if user is not authenticated

### Delete Task
- ✅ Permanently removes task from database
- ✅ Returns 404 if task doesn't exist
- ✅ Returns 403 if task belongs to different user
- ✅ Returns 401 if user is not authenticated
- ✅ Returns 204 on successful deletion

### Toggle Completion
- ✅ Toggles completed status (true ↔ false)
- ✅ Updated timestamp automatically set
- ✅ Returns updated task
- ✅ Returns 404 if task doesn't exist
- ✅ Returns 403 if task belongs to different user
- ✅ Returns 401 if user is not authenticated

## UI/UX Requirements

### Task List Page
- Display all tasks in a responsive grid or list
- Show task title prominently
- Show completion status with visual indicator (checkbox/badge)
- Show creation date in relative format ("2 days ago")
- Provide quick actions: complete, edit, delete
- Empty state message when no tasks exist
- Loading state while fetching tasks

### Create Task Form
- Simple form with title and description fields
- Title field is required with inline validation
- Description field is optional (textarea)
- Submit button disabled while saving
- Clear form after successful creation
- Show error message if creation fails

### Edit Task Dialog
- Modal or slide-over panel
- Pre-populate with current task data
- Same validation as create form
- Cancel and Save buttons
- Show loading state while saving

### Delete Confirmation
- Confirmation dialog before deletion
- "Are you sure?" message
- Cancel and Confirm buttons
- Show loading state while deleting

## Validation Rules

### Title
- **Required**: Cannot be empty
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Trim**: Leading/trailing whitespace removed

### Description
- **Optional**: Can be empty/null
- **Max Length**: 1000 characters
- **Trim**: Leading/trailing whitespace removed

## Error Handling

### Client-side Errors
- Show inline validation errors
- Display toast/alert for network errors
- Disable submit button during validation errors

### Server-side Errors
- 400: Show validation error message to user
- 401: Redirect to login page
- 403: Show "Permission denied" message
- 404: Show "Task not found" message
- 500: Show generic error message

## Performance Requirements
- Task list should load within 500ms
- Create/update/delete operations should complete within 1 second
- UI should remain responsive during operations (optimistic updates)

## Accessibility Requirements
- All interactive elements keyboard accessible
- Proper ARIA labels for screen readers
- Focus management in modals/dialogs
- Sufficient color contrast for status indicators
