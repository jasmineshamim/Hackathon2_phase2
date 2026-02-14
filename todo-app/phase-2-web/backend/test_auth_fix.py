#!/usr/bin/env python3
"""
Simple test to verify the authentication fix is working
"""
import subprocess
import time
import requests
import uuid

def test_authentication_fix():
    """Test that the authentication endpoints are working after the fix"""
    print("=" * 60)
    print("TESTING AUTHENTICATION FIX")
    print("=" * 60)

    # Start server
    print("\n[INFO] Starting backend server...")
    server_process = subprocess.Popen(
        ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Give the server time to start
    time.sleep(3)

    try:
        base_url = "http://127.0.0.1:8000"

        # Test 1: Verify server is running
        print("\n[TEST 1] Checking server availability...")
        try:
            response = requests.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✓ Server is running and accessible")
            else:
                print("✗ Server is not accessible")
                return False
        except Exception as e:
            print(f"✗ Server test failed: {e}")
            return False

        # Test 2: Test the fixed authentication endpoints
        print("\n[TEST 2] Testing authentication endpoints...")

        # Generate unique email for test
        unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        print(f"Using unique email: {unique_email}")

        # Test registration endpoint (was returning 404 before fix)
        print("  Testing /auth/register endpoint...")
        register_data = {
            "email": unique_email,
            "password": "TestPassword123!",
            "name": "Test User"
        }

        response = requests.post(f"{base_url}/auth/register", json=register_data)
        if response.status_code == 200:
            print("  ✓ /auth/register endpoint is working (was 404 before fix)")
        else:
            print(f"  ✗ /auth/register failed: {response.status_code} - {response.text}")
            return False

        # Test login endpoint (was returning 404 before fix)
        print("  Testing /auth/login endpoint...")
        login_data = {
            "email": unique_email,
            "password": "TestPassword123!"
        }

        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("  ✓ /auth/login endpoint is working (was 404 before fix)")
            tokens = response.json()
            access_token = tokens.get('access_token')
        else:
            print(f"  ✗ /auth/login failed: {response.status_code} - {response.text}")
            return False

        # Test protected endpoint
        print("  Testing protected /auth/me endpoint...")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        if response.status_code == 200:
            print("  ✓ Protected endpoint accessible with valid token")
        else:
            print(f"  ✗ Protected endpoint failed: {response.status_code} - {response.text}")
            return False

        # Test that API endpoints still work
        print("  Testing /api/tasks endpoint...")
        try:
            response = requests.get(f"{base_url}/api/tasks")
            # Expect 401 Unauthorized for protected endpoint without token, or 200 for accessible
            if response.status_code in [200, 401, 403]:
                print(f"  ✓ /api/tasks endpoint accessible (status: {response.status_code})")
            else:
                print(f"  ✗ /api/tasks unexpected status: {response.status_code}")
                return False
        except Exception as e:
            print(f"  ✗ /api/tasks failed: {e}")
            return False

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! AUTHENTICATION FIX IS WORKING")
        print("✓ Fixed the 404 error on /auth/register and /auth/login endpoints")
        print("✓ Authentication flow (register -> login -> protected access) works")
        print("✓ API endpoints remain accessible with /api prefix")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        return False

    finally:
        # Stop the server
        print("\n[INFO] Stopping server...")
        server_process.terminate()
        server_process.wait()
        print("[INFO] Server stopped.")

if __name__ == "__main__":
    success = test_authentication_fix()
    if success:
        print("\n🎉 Authentication fix verification completed successfully!")
    else:
        print("\n❌ Authentication fix verification failed!")

    exit(0 if success else 1)