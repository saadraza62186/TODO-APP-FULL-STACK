# Frontend Guidelines

## Stack
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth**: Better Auth with JWT tokens
- **State Management**: React Context / Server State
- **HTTP Client**: Fetch API with custom wrapper

## Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page (redirects)
│   ├── signin/             # Sign in page
│   ├── signup/             # Sign up page
│   └── tasks/              # Tasks page (protected)
├── components/             # React components
│   ├── ui/                 # Reusable UI components
│   ├── auth/               # Auth-related components
│   └── tasks/              # Task-related components
├── lib/                    # Utilities and configs
│   ├── api.ts              # API client
│   ├── auth.ts             # Better Auth config
│   └── utils.ts            # Helper functions
├── types/                  # TypeScript type definitions
├── public/                 # Static assets
└── styles/                 # Global styles
```

## Development Patterns

### Server vs Client Components
- **Use Server Components by default** (better performance, SEO)
- **Use Client Components** only when needed:
  - User interactions (onClick, onChange)
  - React hooks (useState, useEffect)
  - Browser APIs
  - Better Auth session hooks

**Example:**
```tsx
// Server Component (default)
export default async function TasksPage() {
  const tasks = await getTasks() // Fetch on server
  return <TaskList tasks={tasks} />
}

// Client Component (add 'use client')
'use client'
export function TaskList({ tasks }) {
  const [filter, setFilter] = useState('all')
  // Interactive UI
}
```

### API Integration
All backend calls should use the API client:

```typescript
// lib/api.ts
import { api } from '@/lib/api'

// Usage
const tasks = await api.getTasks(userId)
const task = await api.createTask(userId, { title, description })
await api.deleteTask(userId, taskId)
```

**API client automatically:**
- Adds JWT token to requests
- Handles errors
- Parses JSON responses

### Authentication
Use Better Auth hooks and utilities:

```typescript
'use client'
import { useSession, signIn, signOut } from '@/lib/auth'

export function Header() {
  const { session, loading } = useSession()
  
  if (loading) return <Spinner />
  
  return (
    <header>
      {session ? (
        <>
          <span>{session.user.email}</span>
          <button onClick={() => signOut()}>Sign Out</button>
        </>
      ) : (
        <button onClick={() => signIn()}>Sign In</button>
      )}
    </header>
  )
}
```

### Protected Routes
Use middleware or layout to protect routes:

```typescript
// app/tasks/layout.tsx
import { redirect } from 'next/navigation'
import { getSession } from '@/lib/auth'

export default async function TasksLayout({ children }) {
  const session = await getSession()
  
  if (!session) {
    redirect('/signin')
  }
  
  return <>{children}</>
}
```

## Component Guidelines

### Component Structure
```tsx
'use client' // Only if needed

import { useState } from 'react'
import { Button } from '@/components/ui/button'

interface TaskCardProps {
  task: Task
  onToggle: (id: number) => void
  onEdit: (id: number) => void
  onDelete: (id: number) => void
}

export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  const [loading, setLoading] = useState(false)
  
  return (
    <div className="border rounded-lg p-4">
      {/* Component JSX */}
    </div>
  )
}
```

### Naming Conventions
- **Components**: PascalCase (`TaskCard`, `TaskList`)
- **Files**: kebab-case (`task-card.tsx`, `task-list.tsx`)
- **Utilities**: camelCase (`formatDate`, `validateEmail`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`)

## Styling with Tailwind CSS

### Approach
- **Use Tailwind utility classes** for styling
- **No inline styles** (except for dynamic values)
- **Follow existing patterns** for consistency

### Example
```tsx
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
  <h3 className="text-lg font-semibold text-gray-900">{task.title}</h3>
  <Button variant="ghost" size="sm">Edit</Button>
</div>
```

### Responsive Design
Use Tailwind breakpoints:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid: 1 col mobile, 2 tablet, 3 desktop */}
</div>
```

## Type Safety

### Define Types
```typescript
// types/task.ts
export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface CreateTaskInput {
  title: string
  description?: string
}
```

### Use Types Everywhere
```typescript
// Good
function createTask(data: CreateTaskInput): Promise<Task> {
  return api.post('/tasks', data)
}

// Bad - avoid 'any'
function createTask(data: any): Promise<any> {
  return api.post('/tasks', data)
}
```

## Error Handling

### User-Friendly Messages
```typescript
try {
  await api.deleteTask(userId, taskId)
  toast.success('Task deleted successfully')
} catch (error) {
  if (error.status === 404) {
    toast.error('Task not found')
  } else if (error.status === 403) {
    toast.error('You do not have permission to delete this task')
  } else {
    toast.error('Failed to delete task. Please try again.')
  }
}
```

### Loading States
Always show loading states for async operations:
```tsx
const [loading, setLoading] = useState(false)

async function handleSubmit() {
  setLoading(true)
  try {
    await api.createTask(userId, data)
  } finally {
    setLoading(false)
  }
}
```

## Performance Optimization

### Techniques
1. **Server Components**: Fetch data on server when possible
2. **Code Splitting**: Lazy load components with `dynamic()`
3. **Optimistic Updates**: Update UI before API response
4. **Debouncing**: For search/filter inputs
5. **Memoization**: Use `useMemo` and `useCallback` wisely

### Example: Optimistic Update
```typescript
function toggleTask(id: number) {
  // Update UI immediately
  setTasks(tasks.map(t => 
    t.id === id ? { ...t, completed: !t.completed } : t
  ))
  
  // Then update server
  api.toggleTask(userId, id).catch(() => {
    // Revert on error
    setTasks(prevTasks)
    toast.error('Failed to update task')
  })
}
```

## Environment Variables

### Required Variables
```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
```

### Usage
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL
```

**Note**: `NEXT_PUBLIC_` prefix makes variable available to browser.

## Testing

### Component Tests
```typescript
import { render, screen } from '@testing-library/react'
import { TaskCard } from './task-card'

describe('TaskCard', () => {
  it('renders task title', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText('Buy groceries')).toBeInTheDocument()
  })
})
```

## Accessibility

### Requirements
- All buttons and links keyboard accessible
- Proper semantic HTML (`<button>`, `<form>`, etc.)
- ARIA labels for icons and actions
- Focus management in modals
- Color contrast meets WCAG AA

### Example
```tsx
<button
  onClick={onDelete}
  aria-label="Delete task"
  className="..."
>
  <TrashIcon />
</button>
```

## Common Patterns

### Form Handling
```typescript
'use client'
import { useState } from 'react'

export function TaskForm({ onSubmit }) {
  const [title, setTitle] = useState('')
  const [error, setError] = useState('')
  
  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim()) {
      setError('Title is required')
      return
    }
    onSubmit({ title })
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="..."
      />
      {error && <span className="text-red-500">{error}</span>}
      <button type="submit">Create</button>
    </form>
  )
}
```

## Development Commands
```bash
npm run dev          # Start development server (port 3000)
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler
npm test             # Run tests
```

## Code Quality
- Enable TypeScript strict mode
- Use ESLint and Prettier
- No console.logs in production code
- Handle all error cases
- Write meaningful commit messages

## Resources
- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Better Auth Docs](https://better-auth.com/docs)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
