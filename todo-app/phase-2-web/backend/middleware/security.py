from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    """
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        # Add security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response


# Rate limiting middleware would go here in the future
# For now, we'll just define a placeholder
class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to implement rate limiting.
    This is a basic implementation - in production, you'd want to use
    a more robust solution with Redis or similar for distributed rate limiting.
    """
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 3600):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next):
        # For now, just pass through - a full implementation would track
        # request counts per IP address
        response = await call_next(request)
        return response