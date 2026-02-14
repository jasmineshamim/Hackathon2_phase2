#!/usr/bin/env python3
"""
Test to verify the complete task creation flow with authentication
"""
import requests
import uuid
import time

def test_complete_flow():
    """Test the complete flow: register -> login -> create task"""
    base_url = "http://127.0.0.1:8000"

    print("Testing complete authentication and task creation flow...")

    # Step 1: Generate unique email for test
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    print(f"Using unique email: {unique_email}")

    # Step 2: Register a new user
    print("\n1. Registering new user...")
    register_data = {
        "email": unique_email,
        "password": "TestPassword123!",
        "name": "Test User"
    }

    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        print(f"Registration response: {response.status_code}")

        if response.status_code == 200:
            print("✓ Registration successful")
            tokens = response.json()
            access_token = tokens.get('access_token')
            refresh_token = tokens.get('refresh_token')

            if not access_token:
                print("✗ No access token returned from registration")
                return False

            print("✓ Access token received")
        else:
            print(f"✗ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Registration request failed: {e}")
        return False

    # Step 3: Login to get a fresh token (optional, but good practice)
    print("\n2. Logging in to get fresh token...")
    login_data = {
        "email": unique_email,
        "password": "TestPassword123!"
    }

    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")

        if response.status_code == 200:
            print("✓ Login successful")
            tokens = response.json()
            access_token = tokens.get('access_token')

            if not access_token:
                print("✗ No access token returned from login")
                return False

            print("✓ Fresh access token received")
        else:
            print(f"✗ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Login request failed: {e}")
        return False

    # Step 4: Test protected endpoint to verify token works
    print("\n3. Testing protected endpoint (/auth/me)...")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        print(f"Protected endpoint response: {response.status_code}")

        if response.status_code == 200:
            user_data = response.json()
            print(f"✓ Protected endpoint works, user ID: {user_data.get('id')}")
        else:
            print(f"✗ Protected endpoint failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Protected endpoint request failed: {e}")
        return False

    # Step 5: Create a task using the authenticated user
    print("\n4. Creating a task with authenticated user...")
    task_data = {
        "title": "Test Task from Auth Flow",
        "description": "This is a test task created after successful authentication"
    }

    try:
        response = requests.post(f"{base_url}/tasks/", json=task_data, headers=headers)
        print(f"Create task response: {response.status_code}")

        if response.status_code == 200:
            task_response = response.json()
            print(f"✓ Task created successfully, ID: {task_response.get('id')}")
            print(f"✓ Task title: {task_response.get('title')}")
        elif response.status_code == 401:
            print(f"✗ Authentication failed when creating task: {response.text}")
            return False
        else:
            print(f"✗ Task creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Task creation request failed: {e}")
        return False

    # Step 6: Get all tasks to verify the task was saved
    print("\n5. Retrieving all tasks for the user...")
    try:
        response = requests.get(f"{base_url}/tasks/", headers=headers)
        print(f"Get tasks response: {response.status_code}")

        if response.status_code == 200:
            tasks = response.json()
            print(f"✓ Retrieved {len(tasks)} task(s)")
            for task in tasks:
                print(f"  - Task ID: {task['id']}, Title: {task['title']}")
        else:
            print(f"✗ Get tasks failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get tasks request failed: {e}")
        return False

    print("\n" + "="*60)
    print("ALL STEPS COMPLETED SUCCESSFULLY!")
    print("✓ User registration worked")
    print("✓ User login worked")
    print("✓ Authentication token validation worked")
    print("✓ Task creation worked (no 'Could not validate credentials' error)")
    print("✓ Task retrieval worked")
    print("="*60)

    return True

if __name__ == "__main__":
    print("=" * 70)
    print("COMPLETE AUTHENTICATION AND TASK CREATION FLOW TEST")
    print("=" * 70)

    success = test_complete_flow()

    if success:
        print("\n🎉 SUCCESS: Complete flow test passed!")
        print("The 'Could not validate credentials' error has been resolved.")
    else:
        print("\n❌ FAILURE: Complete flow test failed!")
        print("There may still be an issue with authentication.")

    print("=" * 70)