from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from redis import Redis
from app.core.config import settings
import time
from typing import Callable
import json

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        redis_client: Redis,
        rate_limit: int = 100,  # requests per window
        window: int = 60,  # window in seconds
    ):
        super().__init__(app)
        self.redis = redis_client
        self.rate_limit = rate_limit
        self.window = window

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate limiting for certain paths
        if request.url.path in ["/api/v1/health", "/metrics"]:
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        # Get current count
        current = self.redis.get(key)
        if current is None:
            # First request in window
            self.redis.setex(key, self.window, 1)
        else:
            current = int(current)
            if current >= self.rate_limit:
                return Response(
                    content=json.dumps({"detail": "Rate limit exceeded"}),
                    status_code=429,
                    media_type="application/json"
                )
            self.redis.incr(key)

        # Process request
        response = await call_next(request)
        return response 