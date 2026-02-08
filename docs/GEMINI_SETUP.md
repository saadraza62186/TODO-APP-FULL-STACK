# Google Gemini Setup Guide

## ✨ Your app is now configured to use Google Gemini instead of OpenAI!

## Get Your Gemini API Key

1. **Visit Google AI Studio**:
   - Go to https://aistudio.google.com/app/apikey
   
2. **Sign in** with your Google account

3. **Create API Key**:
   - Click "Create API Key"
   - Select a Google Cloud project (or create a new one)
   - Copy the API key

## Add API Key to Your Project

Edit `backend/.env` and add your API key:

```env
GOOGLE_API_KEY=your-api-key-here
```

## Restart Backend

```bash
cd backend
python main.py
```

## Features Using Gemini

- **Model**: Gemini 1.5 Flash (fast and efficient)
- **Function Calling**: Full support for MCP tools
- **Free Tier**: 15 requests per minute (generous for development)
- **Cost**: Much cheaper than OpenAI for production

## Test the Chatbot

1. Open http://localhost:3000/chat
2. Try these commands:
   - "Add a task to buy groceries"
   - "Show me all my tasks"
   - "Mark task 1 as complete"
   - "What's pending?"

## Gemini vs OpenAI

| Feature | Gemini 1.5 Flash | GPT-4 |
|---------|-----------------|-------|
| **Speed** | Very Fast ⚡ | Fast |
| **Cost** | $0.10/1M tokens | $10/1M tokens |
| **Free Tier** | 15 RPM free | $5 credit only |
| **Function Calling** | ✅ Yes | ✅ Yes |
| **Context Window** | 1M tokens | 128K tokens |
| **Best For** | High-volume, cost-effective | Complex reasoning |

## Rate Limits (Free Tier)

- **Requests per minute**: 15
- **Requests per day**: 1,500
- **Tokens per minute**: 1 million

Perfect for development and small-scale production!

## Upgrade to Paid (Optional)

For production with higher limits:
- Go to https://console.cloud.google.com/
- Enable billing on your project
- Get 60 requests per minute

## Troubleshooting

### "GOOGLE_API_KEY not found"
- Make sure you added it to `backend/.env`
- Restart the backend server

### "API key not valid"
- Check the key is copied correctly
- Make sure there are no extra spaces
- Key should start with "AI"

### "Resource exhausted" error
- You've hit the free tier rate limit
- Wait a minute before trying again
- Or enable billing for higher limits

### Import errors
```bash
pip install google-generativeai==0.3.2
```

## Changes Made

✅ Replaced OpenAI with Google Generative AI package
✅ Updated `ai_service.py` to use Gemini API
✅ Modified function calling to Gemini format
✅ Updated requirements.txt
✅ Updated environment variables

## Links

- **AI Studio**: https://aistudio.google.com/
- **Documentation**: https://ai.google.dev/docs
- **Pricing**: https://ai.google.dev/pricing
- **API Reference**: https://ai.google.dev/api/python

---

**Your chatbot is ready with Google Gemini!** 🚀
Just add your API key and start chatting!
