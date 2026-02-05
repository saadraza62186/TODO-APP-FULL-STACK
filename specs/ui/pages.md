# UI Pages Specification

## Page Structure
All pages follow consistent layout:
- Header with navigation
- Main content area
- Responsive design

## Pages Overview

1. **Sign In Page** - `/signin`
2. **Sign Up Page** - `/signup`
3. **Tasks Page** - `/tasks` (default/home)
4. **Not Found Page** - `/404`

---

## 1. Sign In Page

### Route
`/signin`

### Purpose
Allow existing users to log into their account.

### Layout
```
┌─────────────────────────────────┐
│                                 │
│          [App Logo]             │
│                                 │
│      Sign In to Your Account    │
│                                 │
│   ┌─────────────────────────┐   │
│   │ Email                   │   │
│   │ [email input]           │   │
│   │                         │   │
│   │ Password                │   │
│   │ [password input]        │   │
│   │                         │   │
│   │ [Sign In Button]        │   │
│   │                         │   │
│   │ Don't have an account?  │   │
│   │ [Sign Up]               │   │
│   └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

### Components
- `AuthForm` with mode="signin"
- Email input
- Password input (with show/hide toggle)
- Submit button
- Link to sign up page

### Behavior
- Form validation before submit
- Show loading state during authentication
- Display error message on failure
- Redirect to `/tasks` on success
- If already logged in, redirect to `/tasks`

### Validation
- Email: Required, valid format
- Password: Required

---

## 2. Sign Up Page

### Route
`/signup`

### Purpose
Allow new users to create an account.

### Layout
```
┌─────────────────────────────────┐
│                                 │
│          [App Logo]             │
│                                 │
│      Create Your Account        │
│                                 │
│   ┌─────────────────────────┐   │
│   │ Name (optional)         │   │
│   │ [text input]            │   │
│   │                         │   │
│   │ Email                   │   │
│   │ [email input]           │   │
│   │                         │   │
│   │ Password                │   │
│   │ [password input]        │   │
│   │ (min 8 characters)      │   │
│   │                         │   │
│   │ [Sign Up Button]        │   │
│   │                         │   │
│   │ Already have account?   │   │
│   │ [Sign In]               │   │
│   └─────────────────────────┘   │
│                                 │
└─────────────────────────────────┘
```

### Components
- `AuthForm` with mode="signup"
- Name input (optional)
- Email input
- Password input (with strength indicator)
- Submit button
- Link to sign in page

### Behavior
- Form validation before submit
- Show password strength indicator
- Show loading state during registration
- Display error message on failure (e.g., email exists)
- Automatically sign in and redirect to `/tasks` on success
- If already logged in, redirect to `/tasks`

### Validation
- Name: Optional, max 100 characters
- Email: Required, valid format, unique
- Password: Required, min 8 characters

---

## 3. Tasks Page (Home)

### Route
`/tasks` (default route after login)

### Purpose
Display, create, edit, and manage user's tasks.

### Layout
```
┌─────────────────────────────────────────────┐
│  [Logo] My Tasks        [User] [Sign Out]   │
├─────────────────────────────────────────────┤
│                                             │
│  My Tasks                    [+ New Task]   │
│                                             │
│  [All] [Pending] [Completed]                │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ ☐ Buy groceries            [···]      │  │
│  │   Milk, eggs, bread                   │  │
│  │   Created 2 days ago                  │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ ☑ Finish hackathon         [···]      │  │
│  │   Complete Phase II                   │  │
│  │   Created 5 days ago                  │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │ ☐ Review code              [···]      │  │
│  │                                       │  │
│  │   Created 1 hour ago                  │  │
│  └───────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

### Components
- `Header` with user info and sign out
- `PageHeader` with title and "New Task" button
- Filter tabs (All, Pending, Completed)
- `TaskList` with tasks
- `TaskCard` for each task
- `Modal` for create/edit task
- `ConfirmDialog` for delete confirmation
- Empty state when no tasks

### Behavior

#### Initial Load
- Fetch all tasks for authenticated user
- Show loading skeleton while fetching
- Display tasks in list/grid

#### Creating Task
1. Click "New Task" button
2. Open modal with empty form
3. Fill title (required) and description (optional)
4. Click "Create" button
5. Show loading state
6. On success: Close modal, add task to list, show success toast
7. On error: Show error message in modal

#### Editing Task
1. Click edit button (···) on task card
2. Open modal with pre-filled form
3. Modify title/description
4. Click "Save" button
5. Show loading state
6. On success: Close modal, update task in list, show success toast
7. On error: Show error message in modal

#### Toggling Completion
1. Click checkbox on task card
2. Send PATCH request
3. Show loading state (disable checkbox)
4. On success: Update UI with new status
5. On error: Revert checkbox, show error toast

#### Deleting Task
1. Click delete button on task card
2. Show confirmation dialog
3. Click "Confirm"
4. Show loading state
5. On success: Remove task from list, show success toast
6. On error: Show error toast

#### Filtering Tasks
1. Click filter tab (All, Pending, Completed)
2. Update URL query parameter
3. Fetch filtered tasks
4. Update task list

### States

#### Loading State
- Show skeleton cards while fetching

#### Empty State
- All: "No tasks yet. Create your first task!"
- Pending: "No pending tasks. Great job!"
- Completed: "No completed tasks yet."

#### Error State
- Failed to load: "Failed to load tasks. [Retry]"
- Failed to create: "Failed to create task. Please try again."
- Failed to update: "Failed to update task. Please try again."
- Failed to delete: "Failed to delete task. Please try again."

### Authentication
- Protected route (require authentication)
- Redirect to `/signin` if not logged in
- Verify token on page load

---

## 4. Not Found Page

### Route
`/404` (any unmatched route)

### Purpose
Show friendly message for invalid routes.

### Layout
```
┌─────────────────────────────────┐
│                                 │
│            404                  │
│       Page Not Found            │
│                                 │
│  The page you're looking for    │
│  doesn't exist.                 │
│                                 │
│      [Go to Tasks]              │
│                                 │
└─────────────────────────────────┘
```

### Components
- Heading: "404"
- Message: "Page Not Found"
- Button: Link to `/tasks`

---

## Navigation Flow

```
             ┌─────────────┐
             │  Landing    │
             │   (/)       │
             └──────┬──────┘
                    │
        ┌───────────┴───────────┐
        │                       │
   Not Logged In          Logged In
        │                       │
        v                       v
  ┌──────────┐           ┌──────────┐
  │  Sign In │◄─────────►│  Tasks   │
  │ (/signin)│           │ (/tasks) │
  └────┬─────┘           └──────────┘
       │
       │ Switch mode
       │
       v
  ┌──────────┐
  │  Sign Up │
  │ (/signup)│
  └──────────┘
```

### Route Protection

**Public Routes** (no auth required):
- `/signin`
- `/signup`
- `/404`

**Protected Routes** (auth required):
- `/tasks`
- `/` (redirects to `/tasks` if logged in, `/signin` if not)

### Redirects
- Logged in user visits `/signin` or `/signup` → redirect to `/tasks`
- Non-logged in user visits `/tasks` → redirect to `/signin`
- Non-logged in user visits `/` → redirect to `/signin`
- Logged in user visits `/` → redirect to `/tasks`

---

## Responsive Design

### Mobile (<768px)
- Single column layout
- Full-width task cards
- Stacked form inputs
- Hamburger menu for header
- Bottom-aligned buttons

### Tablet (768px-1024px)
- Two-column task grid
- Modal takes 80% width
- Side-by-side form layout

### Desktop (>1024px)
- Three-column task grid
- Modal max-width 600px
- Optimized spacing
- Hover effects enabled

---

## Performance Optimization

### Techniques
- Server components for initial render (Next.js)
- Client components only for interactivity
- Lazy load modals
- Debounce search/filter
- Optimistic UI updates
- Skeleton loading states

### Data Fetching
- Fetch tasks on page load
- Cache tasks in state
- Refetch after mutations
- Show stale data while revalidating

---

## SEO & Meta Tags

### Sign In Page
```html
<title>Sign In - Todo App</title>
<meta name="description" content="Sign in to your todo app account" />
```

### Sign Up Page
```html
<title>Sign Up - Todo App</title>
<meta name="description" content="Create a new todo app account" />
```

### Tasks Page
```html
<title>My Tasks - Todo App</title>
<meta name="description" content="Manage your tasks" />
```
