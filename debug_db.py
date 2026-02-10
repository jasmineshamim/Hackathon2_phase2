import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv('./backend/.env')
print("DATABASE_URL from os.environ:", repr(os.environ.get('DATABASE_URL')))

sys.path.append('./backend')

from backend.config.settings import settings
print("DATABASE_URL from settings:", repr(settings.DATABASE_URL))

from sqlalchemy import create_engine
try:
    engine = create_engine(settings.DATABASE_URL)
    print("Engine created successfully")
except Exception as e:
    print(f"Error creating engine: {e}")

# Try to connect
try:
    with engine.connect() as conn:
        print("Connected to database successfully")
except Exception as e:
    print(f"Error connecting to database: {e}")