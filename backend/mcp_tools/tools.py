"""
MCP Server for Task Management
Exposes task operations as MCP tools for AI agents.
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
import logging

from models import Task
from db import engine

logger = logging.getLogger(__name__)

# Create MCP server instance
mcp_server = Server("task-management-server")


# ============================================================================
# Tool 1: add_task
# ============================================================================

@mcp_server.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new task.
    
    Args:
        user_id: ID of the user creating the task
        title: Task title (required)
        description: Task description (optional)
        
    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        with Session(engine) as session:
            # Create new task
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"Created task {task.id} for user {user_id}: {title}")
            
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
            
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return {
            "error": True,
            "message": f"Failed to create task: {str(e)}",
            "code": "DATABASE_ERROR"
        }


# ============================================================================
# Tool 2: list_tasks
# ============================================================================

@mcp_server.tool()
async def list_tasks(
    user_id: str,
    status: str = "all"
) -> List[Dict[str, Any]]:
    """
    Retrieve tasks from the list.
    
    Args:
        user_id: ID of the user
        status: Filter by status - "all", "pending", or "completed" (default: "all")
        
    Returns:
        List of task dictionaries
    """
    try:
        with Session(engine) as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id)
            
            # Apply status filter
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            # "all" returns everything
            
            # Order by created_at descending
            query = query.order_by(Task.created_at.desc())
            
            tasks = session.exec(query).all()
            
            # Convert to dictionaries
            result = []
            for task in tasks:
                result.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                })
            
            logger.info(f"Retrieved {len(result)} tasks for user {user_id} with status {status}")
            
            return result
            
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return [{
            "error": True,
            "message": f"Failed to list tasks: {str(e)}",
            "code": "DATABASE_ERROR"
        }]


# ============================================================================
# Tool 3: complete_task
# ============================================================================

@mcp_server.tool()
async def complete_task(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Mark a task as complete.
    
    Args:
        user_id: ID of the user
        task_id: ID of the task to complete
        
    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        with Session(engine) as session:
            # Find the task
            task = session.get(Task, task_id)
            
            if not task:
                return {
                    "error": True,
                    "message": f"Task {task_id} not found",
                    "code": "TASK_NOT_FOUND"
                }
            
            # Check ownership
            if task.user_id != user_id:
                return {
                    "error": True,
                    "message": "You don't have access to this task",
                    "code": "UNAUTHORIZED"
                }
            
            # Mark as completed
            task.completed = True
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"Completed task {task_id} for user {user_id}")
            
            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
            
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return {
            "error": True,
            "message": f"Failed to complete task: {str(e)}",
            "code": "DATABASE_ERROR"
        }


# ============================================================================
# Tool 4: delete_task
# ============================================================================

@mcp_server.tool()
async def delete_task(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Remove a task from the list.
    
    Args:
        user_id: ID of the user
        task_id: ID of the task to delete
        
    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        with Session(engine) as session:
            # Find the task
            task = session.get(Task, task_id)
            
            if not task:
                return {
                    "error": True,
                    "message": f"Task {task_id} not found",
                    "code": "TASK_NOT_FOUND"
                }
            
            # Check ownership
            if task.user_id != user_id:
                return {
                    "error": True,
                    "message": "You don't have access to this task",
                    "code": "UNAUTHORIZED"
                }
            
            # Store title before deletion
            task_title = task.title
            
            # Delete the task
            session.delete(task)
            session.commit()
            
            logger.info(f"Deleted task {task_id} for user {user_id}")
            
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": task_title
            }
            
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return {
            "error": True,
            "message": f"Failed to delete task: {str(e)}",
            "code": "DATABASE_ERROR"
        }


# ============================================================================
# Tool 5: update_task
# ============================================================================

@mcp_server.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Modify task title or description.
    
    Args:
        user_id: ID of the user
        task_id: ID of the task to update
        title: New task title (optional)
        description: New task description (optional)
        
    Returns:
        Dictionary with task_id, status, and title
    """
    try:
        with Session(engine) as session:
            # Find the task
            task = session.get(Task, task_id)
            
            if not task:
                return {
                    "error": True,
                    "message": f"Task {task_id} not found",
                    "code": "TASK_NOT_FOUND"
                }
            
            # Check ownership
            if task.user_id != user_id:
                return {
                    "error": True,
                    "message": "You don't have access to this task",
                    "code": "UNAUTHORIZED"
                }
            
            # Update fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"Updated task {task_id} for user {user_id}")
            
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
            
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return {
            "error": True,
            "message": f"Failed to update task: {str(e)}",
            "code": "DATABASE_ERROR"
        }


# ============================================================================
# Import datetime (needed for update functions)
# ============================================================================
from datetime import datetime


# ============================================================================
# Helper Functions
# ============================================================================

def get_mcp_tools_list() -> List[Dict[str, Any]]:
    """
    Get list of all available MCP tools for the AI agent.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user creating the task"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional)"
                    }
                },
                "required": ["user_id", "title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "Retrieve tasks from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by status (default: all)"
                    }
                },
                "required": ["user_id"]
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to complete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Remove a task from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Modify task title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "ID of the user"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional)"
                    }
                },
                "required": ["user_id", "task_id"]
            }
        }
    ]
