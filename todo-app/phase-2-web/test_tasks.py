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
            "email": "task_test@example.com",
            "password": "Pass123!",
            "name": "Task Test User"
        }

        # Make registration request
        response = client.post("/api/auth/register", json=test_user_data)
        print('Registration - Status code:', response.status_code)
        if response.status_code == 200:
            # Extract the token from the registration response
            token_data = response.json()
            access_token = token_data["access_token"]
            headers = {"Authorization": f"Bearer {access_token}"}
            
            print("Access token obtained for testing")
            
            # Test task creation (T043)
            print("\n--- Testing Task Creation (T043) ---")
            task_data = {
                "title": "Test Task",
                "description": "This is a test task"
            }
            create_response = client.post("/api/tasks/", json=task_data, headers=headers)
            print('Task Creation - Status code:', create_response.status_code)
            print('Task Creation - Response:', create_response.text)

            if create_response.status_code == 200:
                created_task = create_response.json()
                task_id = created_task["id"]
                print(f"Created task with ID: {task_id}")

                # Test task listing (T044)
                print("\n--- Testing Task Listing (T044) ---")
                list_response = client.get("/api/tasks/", headers=headers)
                print('Task Listing - Status code:', list_response.status_code)
                print('Task Listing - Response:', list_response.text)

                # Test task updating (T045)
                print("\n--- Testing Task Updating (T045) ---")
                update_data = {
                    "title": "Updated Test Task",
                    "description": "This is an updated test task",
                    "completed": False
                }
                update_response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=headers)
                print('Task Update - Status code:', update_response.status_code)
                print('Task Update - Response:', update_response.text)

                # Test task completion toggle (T047)
                print("\n--- Testing Task Completion Toggle (T047) ---")
                toggle_data = {"completed": True}
                toggle_response = client.patch(f"/api/tasks/{task_id}/complete", json=toggle_data, headers=headers)
                print('Task Completion Toggle - Status code:', toggle_response.status_code)
                print('Task Completion Toggle - Response:', toggle_response.text)

                # Test task deletion (T046)
                print("\n--- Testing Task Deletion (T046) ---")
                delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers)
                print('Task Deletion - Status code:', delete_response.status_code)
                print('Task Deletion - Response:', delete_response.text)
            else:
                print("Task creation failed, checking if it's due to validation error")
                # Check if the issue is with the TaskCreate schema
                # The error showed that user_id was required, but it should be added by the service
                task_data_fixed = {
                    "title": "Test Task",
                    "description": "This is a test task",
                    "completed": False
                }
                create_response = client.post("/api/tasks/", json=task_data_fixed, headers=headers)
                print('Task Creation (fixed) - Status code:', create_response.status_code)
                print('Task Creation (fixed) - Response:', create_response.text)
                if create_response.status_code == 200:
                    created_task = create_response.json()
                    task_id = created_task["id"]
                    print(f"Created task with ID: {task_id}")

                    # Test task listing (T044)
                    print("\n--- Testing Task Listing (T044) ---")
                    list_response = client.get("/api/tasks/", headers=headers)
                    print('Task Listing - Status code:', list_response.status_code)
                    print('Task Listing - Response:', list_response.text)

                    # Test task updating (T045)
                    print("\n--- Testing Task Updating (T045) ---")
                    update_data = {
                        "title": "Updated Test Task",
                        "description": "This is an updated test task",
                        "completed": False
                    }
                    update_response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=headers)
                    print('Task Update - Status code:', update_response.status_code)
                    print('Task Update - Response:', update_response.text)

                    # Test task completion toggle (T047)
                    print("\n--- Testing Task Completion Toggle (T047) ---")
                    toggle_data = {"completed": True}
                    toggle_response = client.patch(f"/api/tasks/{task_id}/complete", json=toggle_data, headers=headers)
                    print('Task Completion Toggle - Status code:', toggle_response.status_code)
                    print('Task Completion Toggle - Response:', toggle_response.text)

                    # Test task deletion (T046)
                    print("\n--- Testing Task Deletion (T046) ---")
                    delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers)
                    print('Task Deletion - Status code:', delete_response.status_code)
                    print('Task Deletion - Response:', delete_response.text)
                else:
                    print("Task creation (fixed) also failed, skipping remaining tests")
        else:
            print("Registration failed, unable to test task functionality")
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()