from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database import engine
from app.models.user import Base
from app.api.v1 import auth, users, health, admin
from app.core.logging import setup_logging
from app.core.errors import AppException
from app.core.monitoring import setup_monitoring
from app.core.rate_limit import RateLimitMiddleware
from app.core.cache import get_cache
import time
import logging
import redis

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize Redis client
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD or None,
    decode_responses=True
)

# Initialize cache
cache = get_cache()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="PulseBoard API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Setup monitoring
setup_monitoring(app)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware, redis_client=redis_client)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"Application error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers
    )

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    # Initialize any startup tasks here
    try:
        # Test Redis connection
        redis_client.ping()
        logger.info("Redis connection successful")
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")
    # Cleanup tasks
    redis_client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to PulseBoard API"}