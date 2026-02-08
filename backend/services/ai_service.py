"""
AI Service for Chat Functionality (Using Google Gemini)
Handles interactions with Google Gemini API and MCP tools.
"""
import google.generativeai as genai
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from sqlmodel import Session, select
from datetime import datetime

from models import Conversation, Message
from db import engine
from config import settings
from mcp_tools.task_operations import (
    add_task, list_tasks, complete_task, delete_task, update_task, get_tool_definitions
)

logger = logging.getLogger(__name__)

# Initialize Gemini
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
else:
    logger.warning("GOOGLE_API_KEY not set - AI chat functionality will not work")


class AIService:
    """Service for handling AI chat interactions with MCP tools using Google Gemini."""
    
    def __init__(self):
        self.system_instruction = """You are a friendly and helpful AI task management assistant.
You can help users manage their tasks through natural language commands.

Your capabilities:
- Add new tasks
- List tasks (all, pending, or completed)
- Mark tasks as complete
- Delete tasks
- Update task titles or descriptions

Always:
- Be friendly and conversational
- Confirm actions clearly
- Handle errors gracefully
- Provide helpful suggestions
- Use emojis appropriately (✓, 🎉, 📝, ❌)

When listing tasks, format them as a numbered list for easy reading.
When completing actions, confirm what was done.
"""
        # Get tool definitions and initialize model with tools
        tools = self.get_gemini_tools()
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=self.system_instruction,
            tools=tools
        )
    
    def get_gemini_tools(self) -> List[Dict[str, Any]]:
        """
        Get MCP tools formatted for Gemini function calling.
        
        Returns:
            List of tool definitions in Gemini format
        """
        return get_tool_definitions()
    
    async def execute_mcp_tool(self, tool_name: str, arguments: Dict[str, Any], user_id: str) -> Any:
        """
        Execute an MCP tool by name.
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments to pass to the tool
            user_id: User ID to inject into tool arguments
            
        Returns:
            Tool execution result
        """
        tool_map = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task
        }
        
        tool = tool_map.get(tool_name)
        if not tool:
            return {"error": True, "message": f"Unknown tool: {tool_name}"}
        
        try:
            # Automatically inject user_id into arguments
            arguments["user_id"] = user_id
            result = await tool(**arguments)
            logger.info(f"Executed {tool_name} with args {arguments}: {result}")
            return result
        except Exception as e:
            logger.error(f"Error executing {tool_name}: {e}")
            return {"error": True, "message": str(e)}
    
    async def get_or_create_conversation(
        self, 
        user_id: str, 
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Get existing conversation or create new one.
        
        Args:
            user_id: User ID
            conversation_id: Optional existing conversation ID
            
        Returns:
            Conversation object
        """
        with Session(engine) as session:
            if conversation_id:
                conversation = session.get(Conversation, conversation_id)
                if conversation and conversation.user_id == user_id:
                    return conversation
                    
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            
            logger.info(f"Created new conversation {conversation.id} for user {user_id}")
            return conversation
    
    async def get_conversation_history(
        self, 
        conversation_id: int, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history formatted for Gemini.
        
        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries for Gemini
        """
        with Session(engine) as session:
            query = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc())
                .limit(limit)
            )
            
            messages = session.exec(query).all()
            
            # Format for Gemini chat
            history = []
            for msg in messages:
                history.append({
                    "role": "user" if msg.role == "user" else "model",
                    "parts": [msg.content]
                })
            
            return history
    
    async def save_message(
        self, 
        conversation_id: int, 
        user_id: str, 
        role: str, 
        content: str
    ) -> Message:
        """
        Save a message to the database.
        
        Args:
            conversation_id: Conversation ID
            user_id: User ID
            role: Message role ('user' or 'assistant')
            content: Message content
            
        Returns:
            Created message object
        """
        with Session(engine) as session:
            message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=role,
                content=content
            )
            
            session.add(message)
            
            # Update conversation updated_at
            conversation = session.get(Conversation, conversation_id)
            if conversation:
                conversation.updated_at = datetime.utcnow()
                session.add(conversation)
            
            session.commit()
            session.refresh(message)
            
            return message
    
    async def chat(
        self, 
        user_id: str, 
        message: str, 
        conversation_id: Optional[int] = None
    ) -> Tuple[int, str, List[Dict[str, Any]]]:
        """
        Process a chat message and return response using Google Gemini.
        
        Args:
            user_id: User ID
            message: User's message
            conversation_id: Optional existing conversation ID
            
        Returns:
            Tuple of (conversation_id, response_text, tool_calls)
        """
        try:
            # Get or create conversation
            conversation = await self.get_or_create_conversation(user_id, conversation_id)
            
            # Save user message
            await self.save_message(conversation.id, user_id, "user", message)
            
            # Get conversation history
            history = await self.get_conversation_history(conversation.id)
            
            # Create chat session with history (exclude current message from history)
            chat = self.model.start_chat(history=history[:-1] if len(history) > 1 else [])
            
            # Send message to Gemini
            response = chat.send_message(message)
            
            tool_calls_record = []
            final_response = ""
            
            # Handle function calls in a loop
            max_iterations = 5  # Prevent infinite loops
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                if not response.candidates or not response.candidates[0].content.parts:
                    break
                
                part = response.candidates[0].content.parts[0]
                
                # If it's a function call
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    logger.info(f"Function call: {function_name} with args: {function_args}")
                    
                    # Execute the MCP tool (automatically injects user_id)
                    result = await self.execute_mcp_tool(function_name, function_args, user_id)
                    
                    # Record the tool call
                    tool_calls_record.append({
                        "tool": function_name,
                        "arguments": function_args,
                        "result": result
                    })
                    
                    # Send function response back to Gemini
                    response = chat.send_message(
                        genai.protos.Content(
                            parts=[genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=function_name,
                                    response={"result": result}
                                )
                            )]
                        )
                    )
                
                # If it's text response
                elif hasattr(part, 'text') and part.text:
                    final_response = part.text
                    break
                else:
                    # No more parts to process
                    break
            
            # If no text response generated, create one
            if not final_response:
                if tool_calls_record:
                    final_response = "I've completed the requested actions."
                else:
                    final_response = "I'm ready to help you manage your tasks!"
            
            # Save assistant response
            await self.save_message(conversation.id, user_id, "assistant", final_response)
            
            logger.info(f"Chat completed for user {user_id} in conversation {conversation.id}")
            
            return conversation.id, final_response, tool_calls_record
            
        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)
            # Return a friendly error message
            error_response = "I'm sorry, I encountered an error processing your request. Please try again."
            return (
                conversation.id if 'conversation' in locals() else 0,
                error_response,
                []
            )


# Create singleton instance
ai_service = AIService()
