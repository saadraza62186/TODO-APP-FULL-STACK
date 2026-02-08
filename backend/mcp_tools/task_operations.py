"""
Task Operations
Simple functions for task management operations.
"""
from sqlmodel import Session, select
from typing import Optional, List, Dict, Any
import logging

from models import Task
from db import engine

logger = logging.getLogger(__name__)


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
            # "all" doesn't add any filter
            
            # Execute query
            tasks = session.exec(query).all()
            
            # Convert to dictionaries
            result = []
            for task in tasks:
                result.append({
                    "task_id": task.id,
                    "title": task.title,
                    "description": task.description or "",
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })
            
            logger.info(f"Retrieved {len(result)} tasks for user {user_id} (status: {status})")
            return result
            
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        return [{
            "error": True,
            "message": f"Failed to list tasks: {str(e)}",
            "code": "DATABASE_ERROR"
        }]


async def complete_task(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Mark a task as completed.
    
    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to complete
        
    Returns:
        Dictionary with task_id and status
    """
    try:
        with Session(engine) as session:
            # Find task
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
            ).first()
            
            if not task:
                return {
                    "error": True,
                    "message": f"Task {task_id} not found or you don't have permission",
                    "code": "NOT_FOUND"
                }
            
            # Update task
            task.completed = True
            session.add(task)
            session.commit()
            
            logger.info(f"Marked task {task_id} as completed for user {user_id}")
            
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


async def delete_task(
    user_id: str,
    task_id: int
) -> Dict[str, Any]:
    """
    Delete a task.
    
    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to delete
        
    Returns:
        Dictionary with status and message
    """
    try:
        with Session(engine) as session:
            # Find task
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
            ).first()
            
            if not task:
                return {
                    "error": True,
                    "message": f"Task {task_id} not found or you don't have permission",
                    "code": "NOT_FOUND"
                }
            
            # Delete task
            session.delete(task)
            session.commit()
            
            logger.info(f"Deleted task {task_id} for user {user_id}")
            
            return {
                "status": "deleted",
                "task_id": task_id,
                "message": f"Task '{task.title}' has been deleted"
            }
            
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        return {
            "error": True,
            "message": f"Failed to delete task: {str(e)}",
            "code": "DATABASE_ERROR"
        }


async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update task details.
    
    Args:
        user_id: ID of the user owning the task
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)
        
    Returns:
        Dictionary with updated task details
    """
    try:
        with Session(engine) as session:
            # Find task
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == user_id
                )
            ).first()
            
            if not task:
                return {
                    "error": True,
                    "message": f"Task {task_id} not found or you don't have permission",
                    "code": "NOT_FOUND"
                }
            
            # Update fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            logger.info(f"Updated task {task_id} for user {user_id}")
            
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title,
                "description": task.description or "",
                "completed": task.completed
            }
            
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return {
            "error": True,
            "message": f"Failed to update task: {str(e)}",
            "code": "DATABASE_ERROR"
        }


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get tool definitions in Gemini format.
    
    Returns:
        List of function declarations for Gemini
    """
    return [
        {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "title": {
                        "type_": "STRING",
                        "description": "Task title (required)"
                    },
                    "description": {
                        "type_": "STRING",
                        "description": "Task description (optional)"
                    }
                },
                "required": ["title"]
            }
        },
        {
            "name": "list_tasks",
            "description": "Retrieve all tasks or filter by status (pending/completed)",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "status": {
                        "type_": "STRING",
                        "description": "Filter by status: 'all', 'pending', or 'completed' (default: 'all')"
                    }
                },
                "required": []
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "task_id": {
                        "type_": "INTEGER",
                        "description": "ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "delete_task",
            "description": "Delete a task permanently",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "task_id": {
                        "type_": "INTEGER",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        },
        {
            "name": "update_task",
            "description": "Update task title and/or description",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "task_id": {
                        "type_": "INTEGER",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type_": "STRING",
                        "description": "New title (optional)"
                    },
                    "description": {
                        "type_": "STRING",
                        "description": "New description (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
    ]
