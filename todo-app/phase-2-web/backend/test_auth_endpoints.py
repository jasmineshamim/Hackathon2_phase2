#!/usr/bin/env python3
"""
Test script to verify authentication endpoints are working correctly
"""
import requests
import json
import subprocess
import time
import signal
import os

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

def test_auth_endpoints():
    """Test authentication endpoints"""
    base_url = "http://127.0.0.1:8000"

    print("\n[INFO] Testing authentication endpoints...")

    # Test 1: Register a new user
    import uuid
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    print(f"\n[TEST] Register endpoint with email: {unique_email}...")
    register_data = {
        "email": unique_email,
        "password": "TestPassword123!",
        "name": "Test User"
    }

    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        print(f"Register response: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Registration successful")
            tokens = response.json()
            access_token = tokens.get('access_token')
        else:
            print(f"[ERROR] Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to register endpoint: {e}")
        return False

    # Test 2: Login with the registered user
    print("\n[TEST] Login endpoint...")
    login_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!"
    }

    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Login successful")
            tokens = response.json()
            access_token = tokens.get('access_token')
        else:
            print(f"[ERROR] Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to login endpoint: {e}")
        return False

    # Test 3: Access protected endpoint (get current user)
    print("\n[TEST] Protected endpoint (/auth/me)...")
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        print(f"Protected endpoint response: {response.status_code}")
        if response.status_code == 200:
            print("[SUCCESS] Protected endpoint access successful")
            print(f"User data: {response.json()}")
        else:
            print(f"[ERROR] Protected endpoint failed: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Could not connect to protected endpoint: {e}")
        return False

    print("\n[SUCCESS] All authentication tests passed!")
    return True

def main():
    """Main test function"""
    print("=" * 60)
    print("Authentication Endpoints Test Suite")
    print("=" * 60)

    # Start server
    server_process = start_server()

    try:
        # Run tests
        success = test_auth_endpoints()

        if success:
            print("\n[OVERALL] All tests passed successfully!")
        else:
            print("\n[OVERALL] Some tests failed!")

    finally:
        # Stop the server
        print("\n[INFO] Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("[INFO] Server stopped.")

    return success

if __name__ == "__main__":
    main()