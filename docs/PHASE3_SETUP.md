# Phase III Quick Setup Guide

## Prerequisites

1. ✅ Backend running on http://localhost:8000
2. ✅ Frontend running on http://localhost:3000
3. ✅ Neon database connected
4. ⭐ OpenAI API key (new requirement)

## Step-by-Step Setup

### 1. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Save it securely - you won't see it again!

### 2. Update Backend Environment

Edit `backend/.env` and add:

```env
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Stop Current Backend

If backend is running, stop it (Ctrl+C in terminal)

### 4. Tables Will Auto-Create

When you restart the backend, the new tables (`conversations` and `messages`) will be created automatically by SQLModel.

**Or run migration manually:**
```bash
cd backend/migrations
python run_migration.py
```

### 5. Restart Backend

```bash
cd backend
python main.py
```

You should see logs indicating:
- Database engine created successfully
- Database tables created successfully (including conversations and messages)
- Server running on http://0.0.0.0:8000

### 6. Verify New Endpoints

Open http://localhost:8000/docs

You should see new endpoints:
- POST `/api/{user_id}/chat`
- GET `/api/{user_id}/conversations`
- GET `/api/{user_id}/conversations/{conversation_id}`
- DELETE `/api/{user_id}/conversations/{conversation_id}`

### 7. Access Chat Interface

1. Open http://localhost:3000
2. Sign in to your account
3. Click "💬 AI Chat" in the header
4. Start chatting!

## Testing the Chatbot

### Example Commands to Try:

1. **Add a task:**
   - "Add a task to buy groceries"
   - "I need to remember to call mom"

2. **List tasks:**
   - "Show me all my tasks"
   - "What's pending?"
   - "What have I completed?"

3. **Complete a task:**
   - "Mark task 1 as complete"
   - "I finished buying groceries"

4. **Update a task:**
   - "Change task 1 to 'Buy groceries and fruits'"
   - "Update the title of task 2"

5. **Delete a task:**
   - "Delete task 3"
   - "Remove the meeting task"

6. **Complex commands:**
   - "Add two tasks: buy milk and call John"
   - "Complete task 1 and show me what's left"

## Troubleshooting

### Issue: "No module named 'openai'"
```bash
cd backend
pip install openai==1.54.0 mcp==1.1.2
```

### Issue: "OPENAI_API_KEY not found"
- Make sure you added it to `backend/.env`
- Restart the backend server

### Issue: Tables don't exist
```bash
cd backend/migrations
python run_migration.py
```

### Issue: Chat doesn't respond
- Check OpenAI API key is valid
- Check you have API credits: https://platform.openai.com/usage
- Check backend logs for errors

### Issue: 401 Unauthorized in chat
- Make sure you're logged in
- Check localStorage has auth_token
- Try logging out and back in

## Architecture Overview

```
User Message
    ↓
Frontend (Chat UI)
    ↓
POST /api/{user_id}/chat
    ↓
AI Service (backend/services/ai_service.py)
    ├─ Load conversation history from DB
    ├─ Format messages for OpenAI
    ├─ Call OpenAI API with function calls
    ├─ Execute MCP tools (backend/mcp/server.py)
    │   ├─ add_task
    │   ├─ list_tasks
    │   ├─ complete_task
    │   ├─ delete_task
    │   └─ update_task
    ├─ Get final response from OpenAI
    └─ Save messages to DB
    ↓
Response to Frontend
```

## Database Changes

Two new tables added:

**conversations**
- id (primary key)
- user_id (foreign key to users)
- created_at
- updated_at

**messages**
- id (primary key)
- conversation_id (foreign key to conversations)
- user_id (foreign key to users)
- role ('user' or 'assistant')
- content (TEXT)
- created_at

## Cost Considerations

**OpenAI API Usage:**
- GPT-4: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- Average chat message: ~500 tokens
- Estimated cost per message: ~$0.03-$0.05

**Tips to reduce costs:**
1. Use GPT-3.5-turbo instead of GPT-4 (change in `ai_service.py`)
2. Limit conversation history (currently 10 messages)
3. Monitor usage at https://platform.openai.com/usage

## Next Steps

1. ✅ Test all chat commands
2. ✅ Verify tasks are created/updated correctly
3. ✅ Check conversation history is saved
4. 🚀 Deploy to production (Vercel + Neon)

## Support

For issues or questions:
- Check logs in backend terminal
- Review [Phase III Documentation](../docs/PHASE3_README.md)
- Check [MCP Tools Spec](../specs/phase3/mcp-tools.md)
- Review [Agent Behavior Spec](../specs/phase3/agent-behavior.md)

---

**Phase III implemented**: February 8, 2026
**Status**: ✅ Complete and ready to use!
