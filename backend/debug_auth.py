"""
Debug script to test JWT authentication functionality
"""
import os
import sys
from datetime import timedelta
from jose import jwt

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from auth.jwt_handler import create_access_token, verify_token, get_user_id_from_token

def test_jwt_creation_and_verification():
    print("Testing JWT creation and verification...")

    # Test data
    user_data = {
        "sub": "test-user-id-123",
        "email": "test@example.com"
    }

    print(f"BETTER_AUTH_SECRET: {settings.BETTER_AUTH_SECRET}")
    print(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")
    print(f"JWT_REFRESH_SECRET_KEY: {settings.JWT_REFRESH_SECRET_KEY}")

    # Check if secrets are properly configured
    if settings.JWT_SECRET_KEY == "your-super-secret-jwt-key-here-change-in-production":
        print("WARNING: JWT_SECRET_KEY is using default value!")
    else:
        print("✓ JWT_SECRET_KEY is properly configured")

    if settings.BETTER_AUTH_SECRET == "your-super-secret-jwt-key-here":
        print("WARNING: BETTER_AUTH_SECRET is using default value!")
    else:
        print("✓ BETTER_AUTH_SECRET is properly configured")

    # Create a test token
    print("\nCreating access token...")
    try:
        token = create_access_token(data=user_data)
        print(f"✓ Token created: {token[:50]}...")
    except Exception as e:
        print(f"✗ Failed to create token: {e}")
        return False

    # Verify the token directly
    print("\nVerifying token directly...")
    try:
        payload = verify_token(token, "access")
        print(f"✓ Token verified, payload: {payload}")
    except Exception as e:
        print(f"✗ Failed to verify token: {e}")
        return False

    # Extract user ID from token
    print("\nExtracting user ID from token...")
    try:
        user_id = get_user_id_from_token(token)
        print(f"✓ User ID extracted: {user_id}")
    except Exception as e:
        print(f"✗ Failed to extract user ID: {e}")
        return False

    # Test with invalid token
    print("\nTesting with invalid token...")
    try:
        invalid_user_id = get_user_id_from_token("invalid.token.here")
        print(f"✗ Invalid token should have failed, but got: {invalid_user_id}")
        return False
    except Exception as e:
        print(f"✓ Correctly rejected invalid token: {e}")

    print("\n✓ All JWT tests passed!")
    return True

if __name__ == "__main__":
    success = test_jwt_creation_and_verification()
    if success:
        print("\nJWT authentication system is working correctly.")
    else:
        print("\nJWT authentication system has issues.")
        sys.exit(1)