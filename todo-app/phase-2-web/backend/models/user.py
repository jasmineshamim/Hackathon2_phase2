from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime
import re
import html
import uuid


def validate_email(email: str) -> str:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError('Invalid email format')
    return email.lower().strip()


def sanitize_text(text: str) -> str:
    """Sanitize text input to prevent XSS and other injection attacks."""
    return html.escape(text.strip())


def generate_uuid() -> str:
    """Generate a UUID string for user IDs."""
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    """
    User model representing a registered user with authentication credentials.
    """
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=100)
    hashed_password: str = Field(nullable=False)
    email_verified: bool = Field(default=False)
    email_verification_token: Optional[str] = Field(default=None, max_length=255)
    password_reset_token: Optional[str] = Field(default=None, max_length=255)
    password_reset_expires: Optional[datetime] = Field(default=None)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=datetime.utcnow)
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    )


class UserCreate(SQLModel):
    """
    Schema for creating a new user.
    """
    email: str
    name: Optional[str] = None
    password: str = Field(min_length=8, max_length=128, description="Password must be at least 8 characters long")

    def sanitize_fields(self):
        """Sanitize user input to prevent XSS and other injection attacks."""
        if self.email:
            self.email = validate_email(self.email)
        if self.name:
            self.name = sanitize_text(self.name)
        return self


class UserRead(SQLModel):
    """
    Schema for returning user information (without sensitive data).
    """
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime