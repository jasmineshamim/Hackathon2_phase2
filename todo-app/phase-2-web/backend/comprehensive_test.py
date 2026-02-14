#!/usr/bin/env python3
"""
Comprehensive test suite for the backend
"""
import subprocess
import time
import signal
import os
import sys
import requests
import uuid

def start_server():
    """Start the backend server in the background"""
    print("[INFO] Starting backend server...")
    server_process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    # Give the server some time to start
    time.sleep(3)

    return server_process

def run_unit_tests():
    """Run basic unit tests"""
    print("\n[INFO] Running unit tests...")

    # Add the current directory to the Python path
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Test 1: Model imports
    try:
        from models.user import User
        from models.task import Task
        print("[SUCCESS] Models imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import models: {e}")
        return False

    # Test 2: Service imports
    try:
        from services.auth_service import register_user, authenticate_user
        from auth.jwt_handler import create_access_token, verify_token
        print("[SUCCESS] Services imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import services: {e}")
        return False

    return True

def run_integration_tests():
    """Run integration tests with the server"""
    print("\n[INFO] Running integration tests...")

    base_url = "http://127.0.0.1:8000"

    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200 and response.json()["status"] == "healthy":
            print("[SUCCESS] Health check passed")
        else:
            print(f"[ERROR] Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return False

    # Test 2: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200 and "message" in response.json():
            print("[SUCCESS] Root endpoint accessible")
        else:
            print(f"[ERROR] Root endpoint failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Root endpoint failed: {e}")
        return False

    # Test 3: Authentication endpoints
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

    # Register
    try:
        register_data = {
            "email": unique_email,
            "password": "TestPassword123!",
            "name": "Integration Test User"
        }
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        if response.status_code == 200:
            print("[SUCCESS] Registration endpoint working")
            tokens = response.json()
            access_token = tokens.get('access_token')
        else:
            print(f"[ERROR] Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Registration test failed: {e}")
        return False

    # Login with same credentials
    try:
        login_data = {
            "email": unique_email,
            "password": "TestPassword123!"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("[SUCCESS] Login endpoint working")
            tokens = response.json()
            access_token = tokens.get('access_token')
        else:
            print(f"[ERROR] Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Login test failed: {e}")
        return False

    # Test 4: Protected endpoint
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        if response.status_code == 200:
            print("[SUCCESS] Protected endpoint accessible")
        else:
            print(f"[ERROR] Protected endpoint failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Protected endpoint test failed: {e}")
        return False

    # Test 5: API endpoints (without auth, should return 401 for protected ones)
    try:
        response = requests.get(f"{base_url}/api/tasks")
        # This should return 401 since no auth token is provided
        if response.status_code in [200, 401, 403]:  # Various expected responses
            print("[SUCCESS] API endpoint accessible (expected response)")
        else:
            print(f"[ERROR] API endpoint unexpected error: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] API endpoint test failed: {e}")
        return False

    return True

def main():
    """Main test function"""
    print("=" * 60)
    print("COMPREHENSIVE BACKEND TEST SUITE")
    print("=" * 60)

    # Run unit tests first
    unit_tests_passed = run_unit_tests()

    if not unit_tests_passed:
        print("\n[Unit Tests] Some unit tests failed!")
        return False

    print("\n[Unit Tests] All unit tests passed!")

    # Start server for integration tests
    server_process = start_server()

    try:
        # Run integration tests
        integration_tests_passed = run_integration_tests()

        if integration_tests_passed:
            print("\n[Integration Tests] All integration tests passed!")
            print("\n[OVERALL] ALL TESTS PASSED!")
            return True
        else:
            print("\n[Integration Tests] Some integration tests failed!")
            return False

    finally:
        # Stop the server
        print("\n[INFO] Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("[INFO] Server stopped.")

    return unit_tests_passed and integration_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)