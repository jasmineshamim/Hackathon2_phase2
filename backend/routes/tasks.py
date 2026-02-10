from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from ..auth.middleware import get_current_user, JWTBearer
from ..auth.authorization import verify_user_owns_task
from ..database.session import get_session
from ..models.task import Task
from ..models.user import User
from ..schemas.task import TaskResponse, TaskCreate, TaskUpdate, TaskStatistics
from ..services.task_service import (
    get_tasks_by_user_id,
    create_task_for_user,
    get_task_by_id_and_user_id,
    update_task,
    delete_task as delete_task_service,
    toggle_task_completion as toggle_task_completion_service,
    get_task_statistics
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


# Static routes (defined first to ensure precedence over dynamic routes)
@router.get("/statistics", response_model=TaskStatistics)
def get_task_statistics_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get task statistics for the currently authenticated user.
    Returns total, pending, and completed task counts.
    """
    stats = get_task_statistics(db, current_user.id)
    return TaskStatistics(**stats)


# Dynamic routes (defined after static routes to avoid conflicts)
@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for the currently authenticated user.
    """
    # Get all tasks for the authenticated user using the service
    tasks = get_tasks_by_user_id(db, current_user.id)

    # Convert to response format
    task_responses = []
    for task in tasks:
        task_responses.append(TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        ))

    return task_responses


@router.post("/", response_model=TaskResponse)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the currently authenticated user.
    """
    # Create a new task for the authenticated user
    db_task = create_task_for_user(db, current_user.id, task_create)

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        user_id=db_task.user_id,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the currently authenticated user.
    """
    # Get the specific task using the service
    task = get_task_by_id_and_user_id(db, task_id, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Update a task by ID for the currently authenticated user.
    """
    # Update the task using the service
    updated_task = update_task(db, task_id, current_user.id, task_update)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        user_id=updated_task.user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Delete a task by ID for the currently authenticated user.
    """
    # Delete the task using the service
    success = delete_task_service(db, task_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete")
def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task by ID for the currently authenticated user.
    """
    # Toggle the task completion using the service
    # For toggle, we just flip the current completion status
    task = get_task_by_id_and_user_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = toggle_task_completion_service(db, task_id, current_user.id, not task.completed)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=updated_task.id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        user_id=updated_task.user_id,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )