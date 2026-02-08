'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: Array<{
    tool: string;
    arguments: Record<string, any>;
    result: any;
  }>;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    tool: string;
    arguments: Record<string, any>;
    result: any;
  }>;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check authentication and get user ID
  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    const uid = localStorage.getItem('user_id');

    if (!token || !uid) {
      router.push('/signin');
      return;
    }

    setUserId(uid);
  }, [router]);

  // Load initial greeting
  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: "Hello! I'm your task management assistant. I can help you add, view, complete, update, or delete tasks. What would you like to do?"
      }
    ]);
  }, []);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim() || isLoading || !userId) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
        },
        body: JSON.stringify({
          message: userMessage,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        if (response.status === 401) {
          router.push('/signin');
          return;
        }
        throw new Error('Failed to send message');
      }

      const data: ChatResponse = await response.json();
      
      // Update conversation ID if it's a new conversation
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant response to chat
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
          tool_calls: data.tool_calls
        }
      ]);

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "I'm sorry, I encountered an error processing your request. Please try again."
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const newChat = () => {
    setConversationId(null);
    setMessages([
      {
        role: 'assistant',
        content: "Hello! I'm your task management assistant. I can help you add, view, complete, update, or delete tasks. What would you like to do?"
      }
    ]);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">AI Task Assistant</h1>
          <p className="text-sm text-gray-500">Chat with AI to manage your tasks</p>
        </div>
        <button
          onClick={newChat}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition"
        >
          New Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4 bg-gray-50">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[70%] rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-900 shadow-sm border border-gray-200'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              
              {/* Show tool calls if present */}
              {message.tool_calls && message.tool_calls.length > 0 && (
                <div className="mt-2 pt-2 border-t border-gray-200 text-xs opacity-75">
                  <p className="font-semibold mb-1">Actions performed:</p>
                  <ul className="list-disc list-inside space-y-1">
                    {message.tool_calls.map((tc, idx) => (
                      <li key={idx}>
                        {tc.tool.replace('_', ' ')}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[70%] rounded-lg px-4 py-3 bg-white text-gray-900 shadow-sm border border-gray-200">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={sendMessage} className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex items-center space-x-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message... (e.g., 'Add a task to buy groceries')"
            disabled={isLoading}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim() || !userId}
            className="px-6 py-3 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
        
        {/* Example commands */}
        <div className="mt-4 flex flex-wrap gap-2">
          <span className="text-xs text-gray-500">Try:</span>
          {['Add task to buy groceries', 'Show all my tasks', 'What is pending?', 'Mark task 1 as complete'].map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => setInput(example)}
              disabled={isLoading}
              className="text-xs px-3 py-1 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {example}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
}
