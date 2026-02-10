import requests
import sys

try:
    response = requests.get('http://localhost:8000/health')
    print(f"Backend is running! Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Backend might not be accessible: {e}")
    sys.exit(1)