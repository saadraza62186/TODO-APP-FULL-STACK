from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List
from datetime import datetime
import logging

from db import get_session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskToggleComplete, TaskResponse
from middleware.auth import get_current_user, verify_user_access

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/{user_id}/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    user_id: str,
    status_filter: str = Query("all", alias="status", description="Filter by status: all, pending, completed"),
    sort_by: str = Query("created", alias="sort", description="Sort by: created, title, updated"),
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """
    Get all tasks for authenticated user.
    
    Query Parameters:
    - status: Filter by status (all, pending, completed)
    - sort: Sort order (created, title, updated)
    """
    # Verify user has access
    verify_user_access(user_id, current_user_id)
    
    # Build query
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply status filter
    if status_filter == "pending":
        statement = statement.where(Task.completed == False)
    elif status_filter == "completed":
        statement = statement.where(Task.completed == True)
    
    # Apply sorting
    if sort_by == "title":
        statement = statement.order_by(Task.title)
    elif sort_by == "updated":
        statement = statement.order_by(Task.updated_at.desc())
    else:  # default: created
        statement = statement.order_by(Task.created_at.desc())
    
    tasks = session.exec(statement).all()
    logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """
    Create a new task for authenticated user.
    
    Request Body:
    - title: Task title (required, 1-200 chars)
    - description: Task description (optional, max 1000 chars)
    """
    # Verify user has access
    verify_user_access(user_id, current_user_id)
    
    # Create task
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    logger.info(f"Created task {task.id} for user {user_id}")
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """
    Get details of a specific task.
    
    Path Parameters:
    - user_id: User ID
    - task_id: Task ID
    """
    # Verify user has access
    verify_user_access(user_id, current_user_id)
    
    # Get task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        logger.warning(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """
    Update a task.
    
    Path Parameters:
    - user_id: User ID
    - task_id: Task ID
    
    Request Body:
    - title: New task title (optional)
    - description: New task description (optional)
    """
    # Verify user has access
    verify_user_access(user_id, current_user_id)
    
    # Get task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        logger.warning(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    logger.info(f"Updated task {task_id} for user {user_id}")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """
    Delete a task.
    
    Path Parameters:
    - user_id: User ID
    - task_id: Task ID
    """
    # Verify user has access
    verify_user_access(user_id, current_user_id)
    
    # Get task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        logger.warning(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Delete task
    session.delete(task)
    session.commit()
    
    logger.info(f"Deleted task {task_id} for user {user_id}")
    return None


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    task_id: int,
    completion_data: TaskToggleComplete,
    session: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
):
    """
    Toggle task completion status.
    
    Path Parameters:
    - user_id: User ID
    - task_id: Task ID
    
    Request Body:
    - completed: New completion status (true/false)
    """
    # Verify user has access
    verify_user_access(user_id, current_user_id)
    
    # Get task
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        logger.warning(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update completion status
    task.completed = completion_data.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    logger.info(f"Toggled completion for task {task_id} to {task.completed}")
    return task
