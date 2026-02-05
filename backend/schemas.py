from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


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
