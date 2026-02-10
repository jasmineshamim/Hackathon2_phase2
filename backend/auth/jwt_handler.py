from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from backend.config.settings import settings
import secrets
import string


# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token with the provided data and expiration time.

    Args:
        data (dict): Data to encode in the token (typically user info)
        expires_delta (timedelta, optional): Token expiration time

    Returns:
        str: Encoded JWT access token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 15 minutes if no expiration is provided
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})

    # Generate a unique JWT ID for the token
    jti = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    to_encode.update({"jti": jti})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a refresh token with the provided data and expiration time.

    Args:
        data (dict): Data to encode in the token (typically user info)
        expires_delta (timedelta, optional): Token expiration time

    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 7 days if no expiration is provided
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    # Generate a unique JWT ID for the token
    jti = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    to_encode.update({"jti": jti})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access"):
    """
    Verify and decode a JWT token.

    Args:
        token (str): JWT token to verify
        token_type (str): Type of token ("access" or "refresh")

    Returns:
        dict: Decoded token payload if valid

    Raises:
        HTTPException: If token is invalid, expired, or tampered with
    """
    try:
        if token_type == "access":
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        elif token_type == "refresh":
            payload = jwt.decode(token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        # Check if token type matches
        token_type_claim = payload.get("type")
        if token_type_claim != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type: expected {token_type}, got {token_type_claim}"
            )

        # Check if token has expired
        exp = payload.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_user_id_from_token(token: str) -> str:
    """
    Extract user ID from a JWT token.

    Args:
        token (str): JWT token to extract user ID from

    Returns:
        str: User ID if token is valid

    Raises:
        HTTPException: If token is invalid or user ID not found
    """
    try:
        payload = verify_token(token, "access")
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials - no user ID (sub) in token"
            )

        return user_id
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )


def get_email_from_token(token: str) -> str:
    """
    Extract email from a JWT token.

    Args:
        token (str): JWT token to extract email from

    Returns:
        str: User email if token is valid

    Raises:
        HTTPException: If token is invalid or email not found
    """
    payload = verify_token(token, "access")
    email: str = payload.get("email")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    return email


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): Plain text password to hash

    Returns:
        str: Hashed password
    """
    # Ensure password is not longer than 72 bytes for bcrypt
    if len(password.encode('utf-8')) > 72:
        password = password[:72]

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Previously hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_verification_token():
    """
    Generate a random verification token for email verification.

    Returns:
        str: Random verification token
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))


def generate_password_reset_token():
    """
    Generate a random token for password reset.

    Returns:
        str: Random password reset token
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))