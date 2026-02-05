# Feature: User Authentication

## Overview
Implement secure user authentication using Better Auth with JWT tokens for API authorization.

## User Stories

### Sign Up
- **As a new user**, I can create an account with email and password
- **As a new user**, I receive immediate access after successful registration
- **As a new user**, I see validation errors if registration fails

### Sign In
- **As a returning user**, I can log in with my email and password
- **As a returning user**, I remain logged in across browser sessions
- **As a returning user**, I see an error message if credentials are invalid

### Sign Out
- **As a logged-in user**, I can sign out to end my session
- **As a logged-in user**, I'm redirected to login page after signing out

### Session Management
- **As a logged-in user**, my session persists across page refreshes
- **As a logged-in user**, I'm automatically logged out when my token expires
- **As a logged-in user**, I don't need to log in again for 7 days (token lifetime)

## Acceptance Criteria

### Sign Up
- ✅ Email is required and must be valid format
- ✅ Password is required (min 8 characters)
- ✅ Email must be unique (no duplicate accounts)
- ✅ User is automatically logged in after successful registration
- ✅ JWT token is issued and stored
- ✅ User is redirected to tasks page after registration
- ✅ Error messages shown for validation failures

### Sign In
- ✅ Email and password are required
- ✅ Credentials are verified against database
- ✅ JWT token is issued on successful login
- ✅ Token includes user_id and email
- ✅ User is redirected to tasks page after login
- ✅ Error message shown for invalid credentials

### Sign Out
- ✅ Session is terminated
- ✅ JWT token is removed from storage
- ✅ User is redirected to login page
- ✅ Subsequent API requests fail with 401

### Protected Routes
- ✅ Unauthenticated users redirected to login page
- ✅ Authenticated users can access task pages
- ✅ Token is automatically attached to all API requests
- ✅ Expired tokens trigger automatic logout

## Better Auth Configuration

### JWT Plugin Setup
```typescript
// Better Auth must be configured to issue JWT tokens
{
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET,
      expiresIn: '7d', // Token lifetime
      algorithm: 'HS256'
    })
  ]
}
```

### Token Storage
- Store JWT token in httpOnly cookie (preferred) or localStorage
- Token automatically included in API requests via Authorization header

## Frontend Integration

### API Client Configuration
```typescript
// All API requests must include JWT token
headers: {
  'Authorization': `Bearer ${token}`
}
```

### Protected Pages
- Wrap task pages with authentication check
- Redirect to login if no valid token
- Show loading state while checking auth

## Backend Integration

### JWT Verification Middleware
- Extract token from Authorization header
- Verify token signature using shared secret
- Decode token to get user_id
- Attach user_id to request context
- Return 401 if token is invalid or missing

### User ID Validation
- Compare token user_id with URL parameter user_id
- Return 403 if they don't match
- Ensures users can only access their own data

## Security Requirements

### Password Security
- Minimum 8 characters
- Better Auth handles hashing (bcrypt/argon2)
- Never store plain text passwords
- Never return passwords in API responses

### Token Security
- Use strong secret key (min 32 characters)
- Same secret on frontend and backend
- Tokens expire after 7 days
- HTTPS required in production
- httpOnly cookies prevent XSS attacks

### CORS Configuration
- Backend must allow frontend origin
- Credentials must be included in requests
- Preflight requests properly handled

## UI/UX Requirements

### Sign Up Page
- Email input field (type="email")
- Password input field (type="password" with show/hide toggle)
- Name input field (optional)
- Submit button
- Link to sign in page
- Display validation errors inline
- Loading state during registration

### Sign In Page
- Email input field
- Password input field with show/hide toggle
- Submit button
- Link to sign up page
- "Remember me" option (optional)
- Display error message for invalid credentials
- Loading state during login

### Navigation
- Show user's name/email in header when logged in
- Sign out button in header
- Hide auth-required navigation items when logged out

## Error Handling

### Client-side Errors
- Invalid email format
- Password too short
- Empty required fields
- Network errors

### Server-side Errors
- 400: Validation error (show specific message)
- 401: Authentication failed (show "Invalid credentials")
- 409: Email already exists (show "Account already exists")
- 500: Server error (show generic message)

## Environment Variables

### Frontend (.env.local)
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
```

⚠️ **Critical**: Both frontend and backend must use the SAME secret key!

## Testing Checklist

- [ ] Can create new account
- [ ] Cannot create duplicate account (same email)
- [ ] Can log in with valid credentials
- [ ] Cannot log in with invalid credentials
- [ ] Token is included in API requests
- [ ] Can access tasks after login
- [ ] Cannot access tasks when logged out
- [ ] Can log out successfully
- [ ] Token expires after configured time
- [ ] Session persists across page refreshes
