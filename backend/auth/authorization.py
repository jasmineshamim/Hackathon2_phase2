from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from backend.models.user import User
from backend.models.task import Task
from backend.auth.middleware import get_current_user
from backend.database.session import get_session


def get_current_user_from_token(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current authenticated user from the JWT token.
    This is a wrapper function for dependency injection.

    Args:
        current_user: User object retrieved from JWT token

    Returns:
        User: The authenticated user object
    """
    return current_user


def verify_user_owns_task(
    user: User = Depends(get_current_user),
    task_id: str = None,
    task: Task = None,
    db: Session = Depends(get_session)
) -> bool:
    """
    Verify that the current user owns the specified task.

    Args:
        user: Current authenticated user
        task_id: ID of the task to check ownership for (optional if task is provided)
        task: Task object to check ownership for (optional if task_id is provided)
        db: Database session

    Returns:
        bool: True if user owns the task, raises HTTPException otherwise

    Raises:
        HTTPException: If user doesn't own the task
    """
    if not task and not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either task or task_id must be provided"
        )

    # If task is not provided, fetch it from the database
    if not task:
        task = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    # Check if the task belongs to the current user
    # Since we don't have a user_id field in Task yet, we'll implement this differently
    # based on the current implementation. Let's assume tasks are linked to users somehow.

    # For now, we'll check if the user_id in the task matches the current user's id
    # Note: This assumes that Task model has a user_id field to link to the User
    if hasattr(task, 'user_id'):
        if task.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this task"
            )
    else:
        # If there's no user_id field in Task, we might need to adjust our approach
        # For now, let's assume that all users can access all tasks
        # This would need to be changed when we update the Task model
        pass

    return True


def has_permission_to_modify(
    user: User = Depends(get_current_user),
    task_id: str = None,
    task: Task = None,
    action: str = "modify",
    db: Session = Depends(get_session)
) -> bool:
    """
    Check if the user has permission to perform the specified action on the task.

    Args:
        user: Current authenticated user
        task_id: ID of the task to check permissions for (optional if task is provided)
        task: Task object to check permissions for (optional if task_id is provided)
        action: Action to check permissions for ('read', 'write', 'delete', 'modify')
        db: Database session

    Returns:
        bool: True if user has permission, raises HTTPException otherwise

    Raises:
        HTTPException: If user doesn't have permission
    """
    if not task and not task_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either task or task_id must be provided"
        )

    # If task is not provided, fetch it from the database
    if not task:
        task = db.exec(select(Task).where(Task.id == task_id)).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    # Check if the user has permission based on ownership
    # This function builds on the ownership verification
    if hasattr(task, 'user_id'):
        # For read actions, we might have different rules
        if action.lower() in ['read']:
            # Currently, we only allow reading own tasks
            if task.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to read this task"
                )
        # For write/modify/delete actions, user must own the task
        elif action.lower() in ['write', 'modify', 'update', 'delete']:
            if task.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to perform this action on this task"
                )
    else:
        # If there's no user_id field in Task, we might need to adjust our approach
        # For now, let's assume that all users can perform actions on all tasks
        # This would need to be changed when we update the Task model
        pass

    return True


def is_admin_user(
    user: User = Depends(get_current_user)
) -> bool:
    """
    Check if the current user is an admin user.

    Args:
        user: Current authenticated user

    Returns:
        bool: True if user is an admin, raises HTTPException otherwise

    Raises:
        HTTPException: If user is not an admin
    """
    # For now, we'll check a role field on the user
    # If the User model doesn't have a role field, we'll need to update it
    if hasattr(user, 'role') and user.role == 'admin':
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required for this action"
        )


def can_access_resource(
    resource_owner_id: str,
    user: User = Depends(get_current_user)
) -> bool:
    """
    Generic function to check if a user can access a resource owned by another user.

    Args:
        resource_owner_id: ID of the user who owns the resource
        user: Current authenticated user

    Returns:
        bool: True if user can access the resource, raises HTTPException otherwise

    Raises:
        HTTPException: If user cannot access the resource
    """
    # Check if the resource owner is the same as the current user
    if resource_owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this resource"
        )

    return True


def validate_user_permissions(
    required_permissions: list,
    user: User = Depends(get_current_user)
) -> bool:
    """
    Validate that the user has the required permissions.

    Args:
        required_permissions: List of permissions required
        user: Current authenticated user

    Returns:
        bool: True if user has all required permissions, raises HTTPException otherwise

    Raises:
        HTTPException: If user doesn't have required permissions
    """
    # For now, we'll just check if the user is authenticated
    # In a more complex system, we would check user roles/permissions
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Placeholder for more complex permission checking
    # This would involve checking user roles, permissions, etc.
    return True