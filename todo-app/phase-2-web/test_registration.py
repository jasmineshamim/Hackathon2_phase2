import sys
import os
from unittest.mock import patch
import tempfile

# Create a temporary SQLite database for testing
temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
temp_db_path = f"sqlite:///{temp_db.name}"

# Mock the database URL to use the temporary database
with patch.dict(os.environ, {
    'DATABASE_URL': temp_db_path,
    'BETTER_AUTH_SECRET': 'test-secret-key-for-testing',
    'BETTER_AUTH_URL': 'http://localhost:3000',
    'JWT_SECRET_KEY': 'test-jwt-secret',
    'JWT_REFRESH_SECRET_KEY': 'test-jwt-refresh-secret'
}):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

    # Import after patching environment variables
    from backend.main import app
    from backend.database.init_db import create_db_and_tables
    from fastapi.testclient import TestClient
    import traceback

    # Create the database tables
    create_db_and_tables()

    client = TestClient(app)

    try:
        # First, register a user
        test_user_data = {
            "email": "test@example.com",
            "password": "Pass123!",
            "name": "Test User"
        }

        # Make registration request
        response = client.post("/api/auth/register", json=test_user_data)
        print('Registration - Status code:', response.status_code)
        print('Registration - Response text:', response.text)

        # Now test login with the same credentials
        login_data = {
            "email": "test@example.com",
            "password": "Pass123!"
        }

        login_response = client.post("/api/auth/login", json=login_data)
        print('Login - Status code:', login_response.status_code)
        print('Login - Response text:', login_response.text)
        print('Login - Response JSON:', login_response.json() if login_response.content else 'No content')
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()