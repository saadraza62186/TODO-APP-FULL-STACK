"""
Chat Routes for Phase III
Handles AI chatbot interactions through natural language.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import logging

from db import get_session
from middleware.auth import get_current_user
from schemas import (
    ChatRequest, ChatResponse, ToolCall,
    ConversationResponse, ConversationHistoryResponse, MessageResponse
)
from models import Conversation, Message
from services.ai_service import ai_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send chat message to AI assistant",
    description="Send a message to the AI chatbot and receive a response with task management capabilities"
)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a message to the AI chatbot.
    
    The bot can understand natural language commands to:
    - Add new tasks
    - List tasks (all, pending, completed)
    - Complete tasks
    - Delete tasks
    - Update tasks
    
    Example messages:
    - "Add a task to buy groceries"
    - "Show me all my tasks"
    - "Mark task 3 as complete"
    - "Delete the meeting task"
    """
    try:
        # Verify user matches authenticated user
        if current_user != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access another user's chat"
            )
        
        # Process chat through AI service
        conversation_id, response_text, tool_calls_data = await ai_service.chat(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        # Format tool calls for response
        tool_calls = [
            ToolCall(
                tool=tc["tool"],
                arguments=tc["arguments"],
                result=tc["result"]
            )
            for tc in tool_calls_data
        ]
        
        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            tool_calls=tool_calls
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your message"
        )


@router.get(
    "/{user_id}/conversations",
    response_model=List[ConversationResponse],
    summary="List user conversations",
    description="Get all conversations for the authenticated user"
)
async def list_conversations(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all conversations for a user."""
    try:
        # Verify user matches authenticated user
        if current_user != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access another user's conversations"
            )
        
        # Query conversations with message counts
        query = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        
        conversations = session.exec(query).all()
        
        # Add message counts
        result = []
        for conv in conversations:
            msg_count = session.exec(
                select(Message).where(Message.conversation_id == conv.id)
            ).all()
            
            result.append(
                ConversationResponse(
                    id=conv.id,
                    user_id=conv.user_id,
                    created_at=conv.created_at,
                    updated_at=conv.updated_at,
                    message_count=len(msg_count)
                )
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing conversations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving conversations"
        )


@router.get(
    "/{user_id}/conversations/{conversation_id}",
    response_model=ConversationHistoryResponse,
    summary="Get conversation history",
    description="Get all messages in a specific conversation"
)
async def get_conversation_history(
    user_id: str,
    conversation_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all messages in a conversation."""
    try:
        # Verify user matches authenticated user
        if current_user != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot access another user's conversations"
            )
        
        # Verify conversation exists and belongs to user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get messages
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        
        messages = session.exec(query).all()
        
        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=[
                MessageResponse(
                    id=msg.id,
                    conversation_id=msg.conversation_id,
                    user_id=msg.user_id,
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at
                )
                for msg in messages
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving conversation history"
        )


@router.delete(
    "/{user_id}/conversations/{conversation_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete conversation",
    description="Delete a conversation and all its messages"
)
async def delete_conversation(
    user_id: str,
    conversation_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a conversation and all its messages."""
    try:
        # Verify user matches authenticated user
        if current_user != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot delete another user's conversations"
            )
        
        # Verify conversation exists and belongs to user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Delete all messages (cascade should handle this, but being explicit)
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        
        for msg in messages:
            session.delete(msg)
        
        # Delete conversation
        session.delete(conversation)
        session.commit()
        
        return {
            "status": "deleted",
            "conversation_id": conversation_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting conversation"
        )
