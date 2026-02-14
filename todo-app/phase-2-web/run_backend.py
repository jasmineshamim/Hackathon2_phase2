import os
import sys
import uvicorn

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Change to the backend directory
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

# Add the backend directory to the Python path
sys.path.insert(0, '.')

# Now import and run the app
from main import app

if __name__ == "__main__":
    print("Starting FastAPI server on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")
    uvicorn.run(app, host="0.0.0.0", port=8000)