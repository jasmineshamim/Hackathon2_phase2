from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class UserRegistrationRequest(BaseModel):
    """
    Schema for user registration request.
    """
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    name: Optional[str] = Field(default=None, max_length=100)

    @validator('password')
    def validate_password_strength(cls, v):
        """
        Validate password strength requirements.
        At least 8 characters, with at least one uppercase, lowercase, number, and special character.
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        # Check for at least one digit
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')

        return v

    @validator('name')
    def validate_name(cls, v):
        """
        Validate name field to prevent XSS and other injection attacks.
        """
        if v is not None:
            # Remove any HTML tags and escape special characters
            import html
            sanitized = html.escape(v.strip())

            # Check for potentially dangerous patterns
            dangerous_patterns = [
                r'<script',
                r'javascript:',
                r'on\w+\s*=',
                r'vbscript:',
                r'data:',
                r'<iframe',
                r'<object',
                r'<embed'
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, sanitized, re.IGNORECASE):
                    raise ValueError('Name contains invalid characters')

            return sanitized
        return v

    def sanitize_fields(self):
        """Sanitize user input to prevent XSS and other injection attacks."""
        if self.name:
            import html
            dangerous_patterns = [
                r'<script',
                r'javascript:',
                r'on\w+\s*=',
                r'vbscript:',
                r'data:',
                r'<iframe',
                r'<object',
                r'<embed'
            ]

            sanitized = html.escape(self.name.strip())
            for pattern in dangerous_patterns:
                if re.search(pattern, sanitized, re.IGNORECASE):
                    raise ValueError('Name contains invalid characters')
            self.name = sanitized
        return self


class UserLoginRequest(BaseModel):
    """
    Schema for user login request.
    """
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class TokenResponse(BaseModel):
    """
    Schema for token response after successful authentication.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Schema for JWT token payload contents.
    """
    sub: str  # Subject (user ID)
    email: str
    exp: int  # Expiration timestamp
    iat: int  # Issued at timestamp
    jti: str  # JWT ID for token identification


class RefreshTokenRequest(BaseModel):
    """
    Schema for refresh token request.
    """
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """
    Schema for initiating password reset.
    """
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """
    Schema for confirming password reset.
    """
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator('new_password')
    def validate_new_password_strength(cls, v):
        """
        Validate new password strength requirements.
        At least 8 characters, with at least one uppercase, lowercase, number, and special character.
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')

        # Check for at least one digit
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')

        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')

        return v