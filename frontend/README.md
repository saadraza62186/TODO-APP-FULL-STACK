# Frontend - Todo App

## Overview
Next.js 16 frontend for Todo application with Better Auth integration and Tailwind CSS.

## Tech Stack
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth**: Better Auth (JWT tokens)
- **State**: React hooks

## Setup

### Prerequisites
- Node.js 18 or higher
- npm or yarn

### Installation

1. **Install dependencies:**
```bash
npm install
# or
yarn install
```

2. **Configure environment variables:**
```bash
# Copy example env file
copy .env.example .env.local  # Windows
cp .env.example .env.local    # macOS/Linux

# Edit .env.local with your actual values
```

### Environment Variables

Create a `.env.local` file:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth configuration
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long
BETTER_AUTH_URL=http://localhost:3000

# Database (if Better Auth needs direct DB access)
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
```

**Important**: `BETTER_AUTH_SECRET` must match the backend!

## Running the Application

### Development Mode
```bash
npm run dev
```

Visit http://localhost:3000

### Production Build
```bash
npm run build
npm run start
```

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   ├── globals.css         # Global styles
│   ├── signin/             # Sign in page
│   ├── signup/             # Sign up page
│   └── tasks/              # Tasks page
├── components/             # React components
│   ├── layout/             # Layout components
│   │   └── header.tsx
│   ├── tasks/              # Task components
│   │   ├── task-list.tsx
│   │   ├── task-card.tsx
│   │   └── task-form.tsx
│   └── ui/                 # Reusable UI components
│       └── modal.tsx
├── lib/                    # Utilities
│   ├── api.ts              # API client
│   └── utils.ts            # Helper functions
├── types/                  # TypeScript types
│   └── index.ts
├── public/                 # Static assets
├── tailwind.config.js      # Tailwind configuration
├── tsconfig.json           # TypeScript configuration
└── package.json            # Dependencies
```

## Features

### Authentication
- Sign up with email and password
- Sign in with existing account
- JWT token-based authentication
- Automatic redirect to signin for unauthenticated users

### Task Management
- Create new tasks
- View all tasks
- Update tasks
- Delete tasks
- Toggle task completion
- Filter by status (all, pending, completed)

### UI/UX
- Responsive design (mobile, tablet, desktop)
- Loading states
- Empty states
- Error handling
- Modal dialogs
- Toast notifications (can be added)

## Pages

### `/` - Home
Redirects to `/tasks`

### `/signin` - Sign In
Login page for existing users

### `/signup` - Sign Up
Registration page for new users

### `/tasks` - Tasks (Protected)
Main application page with task management

## Components

### Layout Components
- `Header`: App header with user info and sign out

### Task Components
- `TaskList`: Grid of task cards with loading and empty states
- `TaskCard`: Individual task display with actions
- `TaskForm`: Create/edit task form

### UI Components
- `Modal`: Reusable modal dialog

## API Integration

The app communicates with the FastAPI backend via REST API:

```typescript
import { api } from '@/lib/api'

// Set JWT token
api.setToken(token)

// Fetch tasks
const tasks = await api.getTasks(userId)

// Create task
const task = await api.createTask(userId, { title, description })

// Update task
const updated = await api.updateTask(userId, taskId, { title })

// Delete task
await api.deleteTask(userId, taskId)

// Toggle completion
const toggled = await api.toggleTaskCompletion(userId, taskId, true)
```

## Styling

### Tailwind CSS
All styling uses Tailwind utility classes. Custom theme configured in [tailwind.config.js](tailwind.config.js).

### Color Palette
- **Primary**: Blue (#3B82F6 and shades)
- **Gray**: Tailwind gray palette
- **Success**: Green
- **Error**: Red

### Responsive Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

## Authentication (Better Auth)

**Note**: This implementation uses localStorage for demo purposes. In production, integrate Better Auth properly:

1. Install Better Auth:
```bash
npm install better-auth
```

2. Configure Better Auth with JWT plugin
3. Replace localStorage with Better Auth hooks
4. Set up authentication routes

### Better Auth Setup (TODO)
```typescript
// lib/auth.ts
import { BetterAuth } from 'better-auth'

export const auth = new BetterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  database: process.env.DATABASE_URL,
  plugins: [
    jwt({
      expiresIn: '7d'
    })
  ]
})
```

## TypeScript

### Type Definitions
All types defined in `types/index.ts`:
- `Task`: Task model
- `CreateTaskInput`: Create task payload
- `UpdateTaskInput`: Update task payload
- `User`: User model
- `AuthSession`: Authentication session

### Type Safety
- All components use TypeScript
- Strict mode enabled
- No `any` types (except error handling)

## Error Handling

### API Errors
```typescript
try {
  await api.createTask(userId, data)
} catch (error: any) {
  if (error.status === 401) {
    // Unauthorized - redirect to signin
  } else if (error.status === 403) {
    // Forbidden
  } else {
    // Generic error
  }
}
```

### Form Validation
- Client-side validation before API calls
- Inline error messages
- Character count indicators

## Performance

### Optimization Techniques
- Server Components for static content
- Client Components only when needed
- Lazy loading of modals
- Optimistic UI updates (can be added)

### Code Splitting
Next.js automatically splits code by route

## Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Other Platforms
- Netlify
- AWS Amplify
- Railway
- Render

### Environment Variables
Make sure to set all environment variables in your deployment platform.

## Troubleshooting

### Common Issues

**1. API connection error**
- Check `NEXT_PUBLIC_API_URL` is correct
- Ensure backend is running
- Check CORS configuration on backend

**2. Authentication issues**
- Verify `BETTER_AUTH_SECRET` matches backend
- Check JWT token is stored correctly
- Ensure token hasn't expired

**3. Build errors**
- Run `npm run type-check` to find TypeScript errors
- Clear `.next` folder: `rm -rf .next`
- Delete `node_modules` and reinstall

**4. Styling not working**
- Check Tailwind is configured correctly
- Ensure `globals.css` is imported in layout
- Clear browser cache

## Development Tips

### Hot Reload
Next.js automatically reloads on file changes in development mode.

### DevTools
- React DevTools for component inspection
- Network tab for API debugging
- Console for error messages

### Code Quality
- Use ESLint for code quality
- Use Prettier for formatting (optional)
- Run type checks before committing

## Testing (TODO)

### Unit Tests
```bash
npm test
```

### Integration Tests
Use `@testing-library/react` for component testing

### E2E Tests
Consider using Playwright or Cypress

## Resources
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Better Auth Documentation](https://better-auth.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## License
MIT License - Hackathon II Project
