from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        """Validate title is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()
    
    @validator('description')
    def description_strip(cls, v):
        """Strip description whitespace."""
        if v:
            return v.strip() if v.strip() else None
        return v


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    
    @validator('title')
    def title_must_not_be_empty(cls, v):
        """Validate title is not just whitespace."""
        if v is not None:
            if not v.strip():
                raise ValueError('Title cannot be empty or whitespace')
            return v.strip()
        return v
    
    @validator('description')
    def description_strip(cls, v):
        """Strip description whitespace."""
        if v is not None:
            return v.strip() if v.strip() else None
        return v


class TaskToggleComplete(BaseModel):
    """Schema for toggling task completion status."""
    
    completed: bool = Field(..., description="Completion status")


class TaskResponse(BaseModel):
    """Schema for task response."""
    
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """Schema for health check response."""
    
    status: str
    timestamp: datetime
    version: str


# ============================================================================
# Chat Schemas (Phase III)
# ============================================================================

class ChatRequest(BaseModel):
    """Schema for chat message request."""
    
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID (creates new if not provided)")
    message: str = Field(..., min_length=1, description="User's natural language message")
    
    @validator('message')
    def message_must_not_be_empty(cls, v):
        """Validate message is not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Message cannot be empty or whitespace')
        return v.strip()


class ToolCall(BaseModel):
    """Schema for MCP tool invocation record."""
    
    tool: str = Field(..., description="Name of the MCP tool invoked")
    arguments: Dict[str, Any] = Field(..., description="Arguments passed to the tool")
    result: Any = Field(..., description="Result returned by the tool")


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    conversation_id: int = Field(..., description="The conversation ID (existing or newly created)")
    response: str = Field(..., description="AI assistant's response text")
    tool_calls: List[ToolCall] = Field(default=[], description="List of MCP tools invoked")


class MessageResponse(BaseModel):
    """Schema for message response."""
    
    id: int
    conversation_id: int
    user_id: str
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Schema for conversation response."""
    
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = None
    
    class Config:
        from_attributes = True


class ConversationHistoryResponse(BaseModel):
    """Schema for conversation history with messages."""
    
    conversation_id: int
    messages: List[MessageResponse]
