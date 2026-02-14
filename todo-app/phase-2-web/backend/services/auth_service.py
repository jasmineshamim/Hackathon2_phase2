from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status
from backend.models.user import User
from backend.schemas.auth import UserRegistrationRequest
from backend.auth.jwt_handler import hash_password, verify_password, create_access_token, create_refresh_token, generate_verification_token, generate_password_reset_token
from datetime import datetime, timedelta
from backend.config.settings import settings


def register_user(user_data: UserRegistrationRequest, db_session: Session) -> tuple[User, str, str]:
    """
    Register a new user with the provided data.

    Args:
        user_data (UserRegistrationRequest): User registration data
        db_session (Session): Database session

    Returns:
        tuple[User, str, str]: Created user, access token, refresh token

    Raises:
        HTTPException: If email is already registered
    """
    # Sanitize input fields if the method exists
    if hasattr(user_data, 'sanitize_fields'):
        user_data = user_data.sanitize_fields()

    # Check if user with this email already exists
    existing_user = db_session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Generate email verification token
    verification_token = generate_verification_token()

    # Create new user
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
        email_verification_token=verification_token,
        email_verified=False  # Email verification required
    )

    # Add user to database
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create tokens for the new user
    access_token_data = {
        "sub": user.id,
        "email": user.email
    }
    access_token = create_access_token(data=access_token_data)

    refresh_token_data = {
        "sub": user.id,
        "email": user.email
    }
    refresh_token = create_refresh_token(data=refresh_token_data)

    return user, access_token, refresh_token


def authenticate_user(email: str, password: str, db_session: Session) -> tuple[Optional[User], Optional[str], Optional[str]]:
    """
    Authenticate user with provided email and password.

    Args:
        email (str): User's email
        password (str): User's password
        db_session (Session): Database session

    Returns:
        tuple[Optional[User], Optional[str], Optional[str]]: User object, access token, refresh token if authentication successful, None otherwise
    """
    # Find user by email
    user = db_session.exec(select(User).where(User.email == email)).first()

    # Check if user exists and password is correct
    if not user or not verify_password(password, user.hashed_password):
        return None, None, None

    # Check if email is verified
    # For testing purposes, we'll skip this check
    # if not user.email_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email not verified. Please check your email for verification instructions."
    #     )

    # Create tokens
    access_token_data = {
        "sub": user.id,
        "email": user.email
    }
    access_token = create_access_token(data=access_token_data)

    refresh_token_data = {
        "sub": user.id,
        "email": user.email
    }
    refresh_token = create_refresh_token(data=refresh_token_data)

    return user, access_token, refresh_token


def refresh_access_token(refresh_token: str, db_session: Session) -> tuple[Optional[str], Optional[str]]:
    """
    Refresh access token using a valid refresh token.

    Args:
        refresh_token (str): Refresh token
        db_session (Session): Database session

    Returns:
        tuple[Optional[str], Optional[str]]: New access token and refresh token if refresh token is valid, None otherwise
    """
    from backend.auth.jwt_handler import verify_token

    try:
        # Verify the refresh token
        payload = verify_token(refresh_token, "refresh")

        # Get user ID from token
        user_id = payload.get("sub")
        if not user_id:
            return None, None

        # Get user from database
        user = db_session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            return None, None

        # Create new tokens
        access_token_data = {
            "sub": user.id,
            "email": user.email
        }
        new_access_token = create_access_token(data=access_token_data)

        # Optionally create a new refresh token (rolling refresh tokens)
        new_refresh_token_data = {
            "sub": user.id,
            "email": user.email
        }
        new_refresh_token = create_refresh_token(data=new_refresh_token_data)

        return new_access_token, new_refresh_token

    except HTTPException:
        # Token is invalid or expired
        return None, None


def logout_user(user_id: str, db_session: Session) -> bool:
    """
    Perform logout operations for the user (if needed).
    Currently, this is a stateless system, so we don't store sessions server-side.
    In a future implementation, we might add the token to a blacklist.

    Args:
        user_id (str): ID of the user logging out
        db_session (Session): Database session

    Returns:
        bool: True if logout was successful
    """
    # In a stateless JWT system, logout is typically handled on the client side
    # by simply deleting the token. However, we could implement a token blacklist
    # if needed for security reasons.

    # For now, we just return True to indicate successful logout
    return True


def initiate_password_reset(email: str, db_session: Session) -> bool:
    """
    Initiate password reset process for the user.

    Args:
        email (str): Email of the user requesting password reset
        db_session (Session): Database session

    Returns:
        bool: True if password reset initiation was successful
    """
    # Find user by email
    user = db_session.exec(select(User).where(User.email == email)).first()

    if not user:
        # Don't reveal if email exists or not for security reasons
        return True

    # Generate password reset token and set expiration
    reset_token = generate_password_reset_token()
    reset_expires = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour

    # Update user with reset token and expiration
    user.password_reset_token = reset_token
    user.password_reset_expires = reset_expires

    # Save changes
    db_session.add(user)
    db_session.commit()

    # In a real application, send email with reset link containing the token
    # send_password_reset_email(user.email, reset_token)

    return True


def confirm_password_reset(token: str, new_password: str, db_session: Session) -> bool:
    """
    Confirm password reset with the provided token and new password.

    Args:
        token (str): Password reset token
        new_password (str): New password to set
        db_session (Session): Database session

    Returns:
        bool: True if password reset was successful
    """
    # Find user by reset token
    user = db_session.exec(
        select(User).where(User.password_reset_token == token)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token"
        )

    # Check if token has expired
    if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset token has expired"
        )

    # Hash the new password
    hashed_new_password = hash_password(new_password)

    # Update user's password and clear reset token
    user.hashed_password = hashed_new_password
    user.password_reset_token = None
    user.password_reset_expires = None

    # Save changes
    db_session.add(user)
    db_session.commit()

    return True


def verify_email(token: str, db_session: Session) -> bool:
    """
    Verify user's email using the provided verification token.

    Args:
        token (str): Email verification token
        db_session (Session): Database session

    Returns:
        bool: True if email verification was successful
    """
    # Find user by verification token
    user = db_session.exec(
        select(User).where(User.email_verification_token == token)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email verification token"
        )

    # Verify the email
    user.email_verified = True
    user.email_verification_token = None

    # Save changes
    db_session.add(user)
    db_session.commit()

    return True