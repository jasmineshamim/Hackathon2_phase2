from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from dotenv import load_dotenv

import sys
import os
# Add the parent directory to the path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try relative imports first (when running as part of the package)
    from .database.init_db import create_db_and_tables
    from .middleware.security import SecurityHeadersMiddleware
except ImportError:
    # Fall back to absolute imports (when running directly)
    from backend.database.init_db import create_db_and_tables
    from backend.middleware.security import SecurityHeadersMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    logger.info("Initializing database tables...")
    create_db_and_tables()
    logger.info("Database tables initialized!")
    yield
    # Cleanup on shutdown if needed
    logger.info("Shutting down...")


from fastapi.security import HTTPBearer

# Initialize security scheme for Swagger UI
security_scheme = HTTPBearer()

app = FastAPI(
    lifespan=lifespan,
    title="Todo API",
    description="Secure Todo application API with JWT authentication",
    version="1.0.0",
    docs_url="/docs",  # Enable Swagger UI documentation
    redoc_url="/redoc",  # Enable ReDoc documentation
    # Add security scheme for API docs
    root_path=""  # This helps with reverse proxy setups
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS middleware - add after security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
try:
    # Try relative imports first (when running as part of the package)
    from .routes import auth, tasks
except ImportError:
    # Fall back to absolute imports (when running directly)
    from backend.routes import auth, tasks

# Include authentication routes without the /api prefix to match standard auth endpoints
app.include_router(auth.router, tags=["authentication"])
# Include tasks routes without the /api prefix to match /tasks/ endpoint
app.include_router(tasks.router, tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API", "status": "running"}

@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "healthy", "message": "API is running"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)