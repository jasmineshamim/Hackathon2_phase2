from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import html


class TaskBase(BaseModel):
    """
    Base schema for task with common fields.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (max 1000 characters)")
    completed: bool = Field(default=False, description="Whether the task is completed")
    user_id: str = Field(..., description="ID of the user who owns this task")

    def sanitize_fields(self):
        """Sanitize user input to prevent XSS and other injection attacks."""
        if self.title:
            self.title = html.escape(self.title.strip())
        if self.description:
            self.description = html.escape(self.description.strip())
        return self


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (max 1000 characters)")
    completed: bool = Field(default=False, description="Whether the task is completed")

    def sanitize_fields(self):
        """Sanitize user input to prevent XSS and other injection attacks."""
        if self.title:
            self.title = html.escape(self.title.strip())
        if self.description:
            self.description = html.escape(self.description.strip())
        return self


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (max 1000 characters)")
    completed: Optional[bool] = Field(None, description="Whether the task is completed")

    def sanitize_fields(self):
        """Sanitize user input to prevent XSS and other injection attacks."""
        if self.title:
            self.title = html.escape(self.title.strip()) if self.title else self.title
        if self.description:
            self.description = html.escape(self.description.strip()) if self.description else self.description
        return self


class TaskResponse(TaskBase):
    """
    Response schema for task with ID and timestamps.
    """
    id: int = Field(..., description="Unique identifier for the task")
    created_at: datetime = Field(..., description="Timestamp when the task was created")
    updated_at: datetime = Field(..., description="Timestamp when the task was last updated")


class TaskListResponse(BaseModel):
    """
    Response schema for list of tasks.
    """
    tasks: list[TaskResponse]


class TaskStatistics(BaseModel):
    """
    Response schema for task statistics.
    """
    total_count: int = Field(..., description="Total number of tasks")
    pending_count: int = Field(..., description="Number of pending (incomplete) tasks")
    completed_count: int = Field(..., description="Number of completed tasks")