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
        # Test the health check endpoint
        print("--- Testing Health Check Endpoint ---")
        health_response = client.get("/health")
        print(f"Health Check - Status code: {health_response.status_code}")
        print(f"Health Check - Response: {health_response.json()}")
        
        if health_response.status_code == 200:
            print("PASS: Health check endpoint is working")
        else:
            print("FAIL: Health check endpoint failed")

        # Test the root endpoint
        print("\n--- Testing Root Endpoint ---")
        root_response = client.get("/")
        print(f"Root - Status code: {root_response.status_code}")
        print(f"Root - Response: {root_response.json()}")

        if root_response.status_code == 200:
            print("PASS: Root endpoint is working")
        else:
            print("FAIL: Root endpoint failed")

        # Test the full user journey: register, login, create task, list tasks, update task, delete task
        print("\n--- Testing Full User Journey ---")

        # 1. Register a user
        print("1. Registering user...")
        user_data = {
            "email": "test@example.com",
            "password": "Pass123!",
            "name": "Test User"
        }
        register_response = client.post("/api/auth/register", json=user_data)
        print(f"Registration - Status: {register_response.status_code}")

        if register_response.status_code != 200:
            print(f"FAIL: Registration failed: {register_response.text}")
            exit(1)

        # Extract tokens
        tokens = register_response.json()
        access_token = tokens["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        print("PASS: User registered successfully")

        # 2. Create a task
        print("2. Creating a task...")
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        create_task_response = client.post("/api/tasks/", json=task_data, headers=headers)
        print(f"Task Creation - Status: {create_task_response.status_code}")

        if create_task_response.status_code != 200:
            print(f"FAIL: Task creation failed: {create_task_response.text}")
            exit(1)

        task = create_task_response.json()
        task_id = task["id"]
        print(f"PASS: Task created with ID: {task_id}")

        # 3. List tasks
        print("3. Listing tasks...")
        list_response = client.get("/api/tasks/", headers=headers)
        print(f"Task Listing - Status: {list_response.status_code}")

        if list_response.status_code != 200:
            print(f"FAIL: Task listing failed: {list_response.text}")
            exit(1)

        tasks = list_response.json()
        print(f"PASS: Retrieved {len(tasks)} tasks")

        # 4. Update the task
        print("4. Updating the task...")
        update_data = {
            "title": "Updated Test Task",
            "description": "This is an updated test task",
            "completed": True
        }
        update_response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=headers)
        print(f"Task Update - Status: {update_response.status_code}")

        if update_response.status_code != 200:
            print(f"FAIL: Task update failed: {update_response.text}")
            exit(1)

        updated_task = update_response.json()
        print(f"PASS: Task updated, completed: {updated_task['completed']}")

        # 5. Toggle task completion
        print("5. Toggling task completion...")
        toggle_data = {"completed": False}
        toggle_response = client.patch(f"/api/tasks/{task_id}/complete", json=toggle_data, headers=headers)
        print(f"Task Toggle - Status: {toggle_response.status_code}")

        if toggle_response.status_code != 200:
            print(f"FAIL: Task toggle failed: {toggle_response.text}")
            exit(1)

        toggled_task = toggle_response.json()
        print(f"PASS: Task completion toggled, completed: {toggled_task['completed']}")

        # 6. Delete the task
        print("6. Deleting the task...")
        delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers)
        print(f"Task Deletion - Status: {delete_response.status_code}")

        if delete_response.status_code != 200:
            print(f"FAIL: Task deletion failed: {delete_response.text}")
            exit(1)

        print("PASS: Task deleted successfully")

        print("\nPASSED: All tests passed! The application is working correctly.")
        
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()