from sqlmodel import Session, select
from typing import List, Optional
from backend.models.task import Task
from backend.models.user import User
from backend.schemas.task import TaskCreate, TaskUpdate
from datetime import datetime


def get_tasks_by_user_id(db: Session, user_id: int) -> List[Task]:
    """
    Get all tasks for a specific user.
    """
    statement = select(Task).where(Task.user_id == user_id)
    return db.exec(statement).all()


def create_task_for_user(db: Session, user_id: int, task_create: TaskCreate) -> Task:
    """
    Create a new task for a specific user.
    """
    # Sanitize input fields
    task_create.sanitize_fields()

    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=getattr(task_create, 'completed', False),
        user_id=user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_by_id_and_user_id(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a specific task by its ID and user ID.
    """
    statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    return db.exec(statement).first()


def update_task(db: Session, task_id: int, user_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a task by its ID and user ID.
    """
    # Sanitize input fields
    task_update.sanitize_fields()

    db_task = get_task_by_id_and_user_id(db, task_id, user_id)
    if not db_task:
        return None

    # Update the task fields if they are provided
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a task by its ID and user ID.
    """
    db_task = get_task_by_id_and_user_id(db, task_id, user_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True


def toggle_task_completion(db: Session, task_id: int, user_id: int, completed: bool) -> Optional[Task]:
    """
    Toggle the completion status of a task by its ID and user ID.
    """
    db_task = get_task_by_id_and_user_id(db, task_id, user_id)
    if not db_task:
        return None

    # Update the completion status
    db_task.completed = completed

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task_statistics(db: Session, user_id: int) -> dict:
    """
    Get task statistics for a specific user.
    Returns total, pending, and completed task counts.
    """
    # Get all tasks for the user
    tasks = get_tasks_by_user_id(db, user_id)

    # Calculate statistics
    total_count = len(tasks)
    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = total_count - completed_count

    return {
        "total_count": total_count,
        "pending_count": pending_count,
        "completed_count": completed_count
    }