# Todo Full-Stack Web Application with AI Chatbot

## 🎯 Project Overview

This is a complete full-stack todo application built using **spec-driven development** with Claude Code and Spec-Kit Plus. The application includes:

- **Phase I**: Console-based todo application
- **Phase II**: Multi-user web application with persistent storage
- **Phase III**: AI-powered chatbot for natural language task management ✨ NEW!

## 📋 Features Implemented

### Phase II Features

✅ **User Authentication** (Better Auth with JWT)
- User signup and signin
- JWT token-based authentication
- Secure session management
- User data isolation

✅ **Task CRUD Operations**
- Create new tasks
- View all tasks
- Update tasks
- Delete tasks
- Toggle task completion
- Filter by status (all, pending, completed)

✅ **RESTful API**
- All 6 required endpoints
- JWT authentication on all routes
- User data isolation
- Comprehensive error handling

✅ **Responsive Frontend**
- Modern, clean UI with Tailwind CSS
- Mobile-first responsive design
- Loading and empty states
- Smooth user experience

✅ **Persistent Storage**
- Neon Serverless PostgreSQL
- SQLModel ORM
- Automatic schema creation
- Connection pooling

### Phase III Features ✨ NEW!

✅ **AI-Powered Chatbot**
- Natural language task management
- Conversational interface
- Context-aware responses
- Multi-tool execution

✅ **MCP Server Architecture**
- 5 task operation tools (add, list, complete, delete, update)
- Stateless server design
- Standardized tool interface
- OpenAI function calling integration

✅ **Persistent Conversations**
- Conversation history stored in database
- Resume conversations anytime
- Full audit trail
- Stateless request cycle

✅ **Advanced AI Capabilities**
- GPT-4 language model
- Tool chaining and composition
- Intent recognition
- Error handling and recovery

**Example Commands:**
- "Add a task to buy groceries"
- "Show me all my pending tasks"
- "Mark task 3 as complete"
- "Delete the meeting task"
- "Change task 1 to 'Call mom tonight'"

[📖 Read full Phase III documentation](./docs/PHASE3_README.md)

## 🛠 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| **Backend** | Python FastAPI |
| **ORM** | SQLModel |
| **Database** | Neon Serverless PostgreSQL |
| **Authentication** | Better Auth with JWT |
| **AI** | OpenAI GPT-4 (Phase III) ✨ |
| **MCP** | Official MCP SDK (Phase III) ✨ |
| **Spec-Driven** | Claude Code + Spec-Kit Plus |

## 📁 Project Structure
TODO-APP-FULL-STACK/
├── specs/                  # Comprehensive specifications
│   ├── overview.md
│   ├── architecture.md
│   ├── features/           # Feature specs
│   ├── api/                # API specs
│   ├── database/           # Database schema
│   ├── ui/                 # UI specs
│   └── phase3/             # Phase III specs ✨
│       ├── mcp-tools.md
│       ├── agent-behavior.md
│       ├── api-endpoints.md
│       └── database-schema.md
├── backend/                # FastAPI backend
│   ├── main.py
│   ├── models.py           # Updated with Conversation & Message
│   ├── schemas.py          # Updated with chat schemas
│   ├── routes/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   └── chat.py         # Phase III chat routes ✨
│   ├── mcp/                # MCP server ✨
│   │   ├── server.py
│   │   └── __init__.py
│   ├── services/           # AI service ✨
│   │   ├── ai_service.py
│   │   └── __init__.py
│   ├── migrations/         # Database migrations ✨
│   │   ├── 001_add_chat_tables.sql
│   │   ├── run_migration.py
│   │   └── README.md
│   ├── middleware/
│   └── requirements.txt    # Updated with OpenAI & MCP
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── tasks/
│   │   ├── chat/           # AI chat page ✨
│   │   │   └── page.tsx
│   │   ├── signin/
│   │   └── signup/
│   ├── components/
│   │   ├── layout/
│   │   │   └── header.tsx  # Updated with chat link
│   │   └── tasks/
│   ├── lib/
│   ├── types/
│   └── package.json
├── docs/
│   └── PHASE3_README.md    # Phase III documentation ✨
├── docker-compose.yml      # Docker orchestration
├── docker-compose.yml      # Docker orchestration
├── CLAUDE.md               # Root instructions
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ 
- **Python** 3.11+
- **PostgreSQL** (or Neon account)
- **Git**

### Option 1: Docker (Recommended)

1. **Clone and navigate to project:**
```bash
cd "c:\Hackathon 2\Phase 2"
```

2. **Set up environment variables:**
```bash
# Copy example env file
copy .env.example .env

# Edit .env and set BETTER_AUTH_SECRET (min 32 characters)
```

3. **Start all services:**
```bash
docker-compose up
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env with your values

# Run server
uvicorn main:app --reload
```

Backend runs on http://localhost:8000

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
copy .env.example .env.local
# Edit .env.local with your values

# Run development server
npm run dev
```

Frontend runs on http://localhost:3000

## 🔐 Environment Variables

### Critical: BETTER_AUTH_SECRET

⚠️ **The `BETTER_AUTH_SECRET` MUST be the same in both frontend and backend!**

Generate a secure secret (min 32 characters):
```bash
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long
CORS_ORIGINS=http://localhost:3000
DEBUG=false

# Phase III: OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here
```

**Get OpenAI API Key:** https://platform.openai.com/api-keys

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long
BETTER_AUTH_URL=http://localhost:3000
```

## 📡 API Endpoints

All endpoints require JWT token in `Authorization: Bearer <token>` header.

### Task Endpoints (Phase II)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

**Query Parameters for GET /tasks:**
- `status`: Filter by status (all, pending, completed)
- `sort`: Sort order (created, title, updated)

### Chat Endpoints (Phase III) ✨

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send message to AI chatbot |
| GET | `/api/{user_id}/conversations` | List all conversations |
| GET | `/api/{user_id}/conversations/{id}` | Get conversation history |
| DELETE | `/api/{user_id}/conversations/{id}` | Delete conversation |

**Example Chat Request:**
```json
{
  "conversation_id": 1,  // Optional
  "message": "Add a task to buy groceries"
}
```

**Example Chat Response:**
```json
{
  "conversation_id": 1,
  "response": "I've added 'Buy groceries' to your task list (Task #5).",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {"user_id": "user123", "title": "Buy groceries"},
      "result": {"task_id": 5, "status": "created", "title": "Buy groceries"}
    }
  ]
}
```

## 🗄 Database Schema

### users (managed by Better Auth)
- id (string, PK)
- email (string, unique)
- name (string, nullable)
- password_hash (string)
- created_at, updated_at (timestamps)

### tasks
- id (serial, PK)
- user_id (string, FK → users.id)
- title (string, max 200)
- description (text, nullable, max 1000)
- completed (boolean, default false)
- created_at, updated_at (timestamps)

## 🔒 Security Features

✅ **JWT Authentication**
- All API endpoints protected
- Token signature verification
- User ID validation

✅ **User Data Isolation**
- Queries filtered by authenticated user
- Cannot access other users' data
- Enforced at API level

✅ **Password Security**
- Bcrypt hashing (Better Auth)
- Never stored in plain text
- Never returned in responses

✅ **SQL Injection Prevention**
- Parameterized queries (SQLModel)
- No string concatenation

✅ **CORS Configuration**
- Restricted origins
- Credentials allowed
- Proper preflight handling

## 📚 Specification Files

The project uses **Spec-Kit Plus** for organized specifications:

- **`specs/overview.md`** - Project overview and goals
- **`specs/architecture.md`** - System architecture and data flow
- **`specs/features/task-crud.md`** - Task management feature spec
- **`specs/features/authentication.md`** - Authentication feature spec
- **`specs/api/rest-endpoints.md`** - Complete API documentation
- **`specs/database/schema.md`** - Database schema and models
- **`specs/ui/components.md`** - UI component specifications
- **`specs/ui/pages.md`** - Page layout and behavior specs

## 🎨 UI/UX Features

- **Responsive Design** - Mobile, tablet, desktop optimized
- **Loading States** - Skeleton screens while fetching
- **Empty States** - Helpful messages when no data
- **Error Handling** - User-friendly error messages
- **Modal Dialogs** - Create and edit tasks
- **Keyboard Navigation** - Full keyboard accessibility
- **Visual Feedback** - Hover states, transitions

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment

**Recommended Platforms:**
- Railway
- Render
- Heroku
- AWS/GCP/Azure

**Requirements:**
- Set environment variables
- Use production database (Neon)
- Enable HTTPS
- Set `DEBUG=false`

### Frontend Deployment

**Recommended: Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

**Other Options:**
- Netlify
- AWS Amplify
- Railway

## 🐛 Troubleshooting

### Backend Issues

**Database connection error:**
- Verify `DATABASE_URL` format
- Check database is accessible
- Ensure SSL mode is correct

**JWT authentication fails:**
- Verify `BETTER_AUTH_SECRET` matches frontend
- Check token is in Authorization header
- Ensure token hasn't expired

### Frontend Issues

**API connection error:**
- Check `NEXT_PUBLIC_API_URL` is correct
- Ensure backend is running
- Verify CORS is configured

**Build errors:**
- Run `npm run type-check`
- Delete `.next` folder and rebuild
- Clear node_modules and reinstall

### Docker Issues

**Containers won't start:**
- Check port conflicts (3000, 8000, 5432)
- Verify .env file exists
- Check Docker daemon is running

**Database connection refused:**
- Wait for postgres health check to pass
- Check `depends_on` in docker-compose.yml

## 📖 Development Workflow

This project follows **spec-driven development**:

1. **Write Specification** → Create/update files in `/specs`
2. **Reference Specification** → Use `@specs/path/to/file.md`
3. **Implement Feature** → Claude Code implements based on spec
4. **Test Implementation** → Verify against spec requirements
5. **Iterate** → Update spec and code as needed

### Using CLAUDE.md Files

- **Root CLAUDE.md** - Project overview and navigation
- **frontend/CLAUDE.md** - Frontend patterns and guidelines
- **backend/CLAUDE.md** - Backend patterns and conventions

## 🤝 Contributing

This is a hackathon project using spec-driven development:

1. Update relevant specification in `/specs`
2. Reference spec when making changes
3. Ensure implementation matches spec
4. Update docs if needed

## 📝 Development Notes

### Better Auth Integration Status

⚠️ **Current Status**: Mock authentication using localStorage

**To Implement Full Better Auth:**
1. Install Better Auth: `npm install better-auth`
2. Configure with JWT plugin
3. Replace localStorage with Better Auth hooks
4. Update API client to use Better Auth tokens

### Future Enhancements (Phase III)

- AI Chatbot interface for task management
- Natural language task creation
- Task suggestions and prioritization
- Voice input support

## 📄 License

MIT License - Hackathon II Project

## 🙏 Acknowledgments

- **Claude Code** - AI-powered development assistant
- **Spec-Kit Plus** - Specification management tool
- **FastAPI** - Modern Python web framework
- **Next.js** - React framework for production
- **Neon** - Serverless PostgreSQL

## 📞 Support

For issues or questions:
1. Check specification files in `/specs`
2. Review CLAUDE.md files for guidelines
3. Check backend/frontend README files
4. Review API documentation at `/docs`

## ✅ Hackathon Requirements Checklist

- ✅ All 5 Basic Level features implemented as web application
- ✅ RESTful API with all 6 required endpoints
- ✅ Responsive frontend interface with Tailwind CSS
- ✅ Data stored in Neon Serverless PostgreSQL
- ✅ User authentication with Better Auth (JWT)
- ✅ Multi-user support with data isolation
- ✅ Spec-driven development with Spec-Kit Plus
- ✅ Monorepo organization
- ✅ Docker configuration
- ✅ Comprehensive documentation

---

**Built with ❤️ using Spec-Driven Development**

**Hackathon II - Phase 2**  
**Date**: February 2026  
**Approach**: No manual coding - fully AI-driven with Claude Code
