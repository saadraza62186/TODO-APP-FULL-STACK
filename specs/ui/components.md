# UI Components Specification

## Design System

### Colors
- **Primary**: Blue (#3B82F6)
- **Success**: Green (#10B981)
- **Danger**: Red (#EF4444)
- **Gray Scale**: Tailwind gray palette
- **Background**: White / Gray-50
- **Text**: Gray-900 / Gray-600

### Typography
- **Font Family**: System font stack (Tailwind default)
- **Headings**: Font-bold, varying sizes
- **Body**: Font-normal, text-base
- **Labels**: Font-medium, text-sm

## Core Components

### TaskCard
Displays a single task in the list.

**Props:**
- `task`: Task object
- `onToggle`: Function to toggle completion
- `onEdit`: Function to edit task
- `onDelete`: Function to delete task

**Features:**
- Checkbox for completion status
- Strikethrough text for completed tasks
- Edit and delete buttons
- Hover state with actions
- Responsive layout

**Example:**
```tsx
<TaskCard
  task={task}
  onToggle={() => handleToggle(task.id)}
  onEdit={() => handleEdit(task.id)}
  onDelete={() => handleDelete(task.id)}
/>
```

---

### TaskList
Container for displaying multiple tasks.

**Props:**
- `tasks`: Array of Task objects
- `loading`: Boolean loading state
- `emptyMessage`: String to show when no tasks

**Features:**
- Grid or list layout (responsive)
- Loading skeleton
- Empty state with message
- Smooth animations

---

### TaskForm
Form for creating or editing tasks.

**Props:**
- `task`: Optional Task object (for editing)
- `onSubmit`: Function called with form data
- `onCancel`: Function to cancel form

**Features:**
- Title input (required)
- Description textarea (optional)
- Character count indicators
- Inline validation
- Submit and cancel buttons
- Loading state during submission

---

### Button
Reusable button component.

**Variants:**
- `primary`: Blue background
- `secondary`: Gray background
- `danger`: Red background
- `ghost`: Transparent with border

**Sizes:**
- `sm`: Small button
- `md`: Medium button (default)
- `lg`: Large button

**Props:**
- `variant`: Button style variant
- `size`: Button size
- `loading`: Show loading spinner
- `disabled`: Disable button
- `onClick`: Click handler
- `children`: Button content

---

### Modal
Reusable modal/dialog component.

**Props:**
- `isOpen`: Boolean to control visibility
- `onClose`: Function to close modal
- `title`: Modal title
- `children`: Modal content

**Features:**
- Backdrop overlay (dim background)
- Close on escape key
- Close on backdrop click
- Smooth open/close animation
- Focus trap (keyboard navigation)
- Scroll lock (body)

---

### Input
Form input component.

**Props:**
- `label`: Input label
- `type`: Input type (text, email, password)
- `value`: Current value
- `onChange`: Change handler
- `error`: Error message
- `placeholder`: Placeholder text
- `required`: Is required field
- `maxLength`: Maximum character length

**Features:**
- Label with required indicator
- Error message display
- Character counter (optional)
- Focus ring styling
- Disabled state

---

### Textarea
Multiline text input.

**Props:**
- Same as Input, plus:
- `rows`: Number of rows
- `resize`: Allow resize (boolean)

---

### Checkbox
Checkbox input with label.

**Props:**
- `checked`: Boolean checked state
- `onChange`: Change handler
- `label`: Checkbox label
- `disabled`: Disable checkbox

---

### Header
Application header/navbar.

**Features:**
- App logo/title
- User profile menu
- Sign out button
- Responsive (hamburger menu on mobile)

---

### AuthForm
Form for sign in and sign up.

**Props:**
- `mode`: "signin" | "signup"
- `onSubmit`: Submit handler
- `onModeChange`: Function to switch modes

**Features:**
- Email and password inputs
- Name input (signup only)
- Submit button
- Mode toggle link
- Error message display
- Loading state

## Layout Components

### Container
Max-width wrapper for content.

```tsx
<Container>
  {/* Content */}
</Container>
```

---

### PageHeader
Page title and actions.

**Props:**
- `title`: Page title
- `actions`: Optional action buttons

```tsx
<PageHeader 
  title="My Tasks" 
  actions={<Button>New Task</Button>}
/>
```

## State Components

### Loading
Loading spinner or skeleton.

**Variants:**
- `spinner`: Spinning loader
- `skeleton`: Content skeleton

---

### EmptyState
Empty state message with optional action.

**Props:**
- `message`: Message to display
- `action`: Optional action button

```tsx
<EmptyState
  message="No tasks yet"
  action={<Button>Create your first task</Button>}
/>
```

---

### ErrorMessage
Error message display.

**Props:**
- `message`: Error message
- `onRetry`: Optional retry handler

## Utility Components

### Toast
Notification toast.

**Types:**
- `success`: Green toast
- `error`: Red toast
- `info`: Blue toast

**Features:**
- Auto-dismiss after 3 seconds
- Manual dismiss button
- Stack multiple toasts
- Slide-in animation

---

### ConfirmDialog
Confirmation dialog for destructive actions.

**Props:**
- `isOpen`: Boolean visibility
- `title`: Dialog title
- `message`: Confirmation message
- `onConfirm`: Confirm handler
- `onCancel`: Cancel handler
- `confirmText`: Confirm button text (default: "Confirm")
- `cancelText`: Cancel button text (default: "Cancel")

## Responsive Behavior

### Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

### Mobile Adaptations
- Stack form inputs vertically
- Full-width buttons
- Simplified header with menu
- Single column task list

### Desktop Optimizations
- Multi-column task grid
- Inline form actions
- Hover states on interactive elements

## Accessibility

### Requirements
- All interactive elements keyboard accessible
- Proper ARIA labels and roles
- Focus visible (outline/ring)
- Screen reader text for icons
- Sufficient color contrast (WCAG AA)
- Error messages announced to screen readers

### Focus Management
- Modal: Focus first input on open
- Form: Focus first error on submit
- Delete: Focus next item after deletion

## Animation

### Transitions
- Duration: 150-300ms
- Easing: ease-in-out
- Properties: opacity, transform

### Examples
- Modal fade in/out
- Toast slide in
- Task card hover lift
- Button press scale

## Dark Mode (Optional)
If implementing dark mode:
- Use Tailwind's dark: variant
- Toggle in user preferences
- Persist choice in localStorage
