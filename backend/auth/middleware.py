from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.models.user import User
from backend.auth.jwt_handler import verify_token, get_user_id_from_token
from sqlmodel import Session, select
from backend.database.session import get_session
from jose import JWTError


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer authentication class that extends HTTPBearer.
    Validates JWT tokens and extracts user information from them.
    """
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        """
        Called when the middleware is used as a dependency.

        Args:
            credentials: HTTP authorization credentials

        Returns:
            str: The validated JWT token

        Raises:
            HTTPException: If token is invalid
        """
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme"
                )

            token = credentials.credentials

            # Just return the token to be used by get_current_user
            # The get_current_user function will validate the token
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No credentials provided"
            )


def get_current_user(
    token: str = Depends(JWTBearer()),
    db: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the JWT token.

    Args:
        token: JWT token from authentication middleware
        db: Database session

    Returns:
        User: The authenticated user object
    """
    try:
        # Extract user ID from token
        user_id = get_user_id_from_token(token)

        # Query the database for the user
        user = db.exec(select(User).where(User.id == user_id)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unable to get current user: {str(e)}"
        )


# Create a shortcut for dependency injection
JWTBearerAuth = JWTBearer