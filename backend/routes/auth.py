from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
try:
    # Try relative imports first (when running as part of the package)
    from ..database.session import get_session
except ImportError:
    # Fall back to absolute imports (when running directly)
    from backend.database.session import get_session
from ..schemas.auth import (
    UserRegistrationRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm
)
from ..services.auth_service import (
    register_user,
    authenticate_user,
    refresh_access_token,
    logout_user,
    initiate_password_reset,
    confirm_password_reset,
    verify_email
)
from ..models.user import User
from ..auth.middleware import JWTBearer, get_current_user
from typing import Dict, Any
import time


router = APIRouter(prefix="/auth", tags=["authentication"])

# In-memory storage for rate limiting (in production, use Redis or similar)
login_attempts: Dict[str, list] = {}


def check_rate_limit(ip_address: str) -> bool:
    """
    Check if the IP address has exceeded the login attempt limit.

    Args:
        ip_address (str): IP address to check

    Returns:
        bool: True if within limit, False if exceeded
    """
    current_time = time.time()
    window_start = current_time - 60  # 1 minute window

    # Clean up old attempts
    if ip_address in login_attempts:
        login_attempts[ip_address] = [
            attempt_time for attempt_time in login_attempts[ip_address]
            if attempt_time > window_start
        ]
    else:
        login_attempts[ip_address] = []

    # Check if limit exceeded
    if len(login_attempts[ip_address]) >= 5:  # 5 attempts per minute
        return False

    return True


def record_failed_attempt(ip_address: str):
    """
    Record a failed login attempt for rate limiting.

    Args:
        ip_address (str): IP address of the attempt
    """
    current_time = time.time()
    if ip_address not in login_attempts:
        login_attempts[ip_address] = []
    login_attempts[ip_address].append(current_time)


@router.post("/register", response_model=TokenResponse)
async def register(request: Request, user_data: UserRegistrationRequest, db: Session = Depends(get_session)):
    """
    Register a new user with email and password.
    """
    try:
        # Sanitize user input
        user_data = user_data.sanitize_fields()

        # Register the user and get tokens
        user, access_token, refresh_token = register_user(user_data, db)

        # In a real application, send verification email
        # await send_verification_email(user.email, user.email_verification_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, user_credentials: UserLoginRequest, db: Session = Depends(get_session)):
    """
    Authenticate user with email and password.
    """
    # Get client IP for rate limiting
    client_ip = request.client.host

    # Check rate limit
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )

    try:
        # Authenticate user
        user, access_token, refresh_token = authenticate_user(
            user_credentials.email,
            user_credentials.password,
            db
        )

        if not user:
            # Record failed attempt
            record_failed_attempt(client_ip)

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    except HTTPException:
        # Record failed attempt if it's a 401 (wrong credentials)
        if "Incorrect email or password" in str(HTTPException):
            record_failed_attempt(client_ip)
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )


@router.post("/logout")
async def logout(request: Request, current_user: User = Depends(JWTBearer()), db: Session = Depends(get_session)):
    """
    Log out the current user.
    """
    try:
        success = logout_user(current_user.id, db)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error during logout"
            )

        return {"message": "Successfully logged out"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during logout: {str(e)}"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest, db: Session = Depends(get_session)):
    """
    Refresh access token using a valid refresh token.
    """
    try:
        new_access_token, new_refresh_token = refresh_access_token(refresh_request.refresh_token, db)

        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during token refresh: {str(e)}"
        )


@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_session)):
    """
    Initiate password reset process.
    """
    try:
        success = initiate_password_reset(request.email, db)

        if success:
            # In a real application, this would send an email with reset instructions
            return {"message": "If an account with this email exists, a password reset link has been sent."}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error initiating password reset"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during password reset initiation: {str(e)}"
        )


@router.post("/reset-password")
async def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_session)):
    """
    Confirm password reset with token and new password.
    """
    try:
        success = confirm_password_reset(request.token, request.new_password, db)

        if success:
            return {"message": "Password has been reset successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error resetting password"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during password reset: {str(e)}"
        )


@router.get("/verify-email/{token}")
async def verify_email_endpoint(token: str, db: Session = Depends(get_session)):
    """
    Verify user's email using the provided token.
    """
    try:
        success = verify_email(token, db)

        if success:
            return {"message": "Email has been verified successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error verifying email"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during email verification: {str(e)}"
        )


# Add a test endpoint to check if auth is working
@router.get("/me", response_model=Dict[str, Any])
async def get_current_user(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at
    }