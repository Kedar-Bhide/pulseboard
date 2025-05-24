from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.errors import AppException
import redis
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies:
    1. Database connection
    2. Redis connection
    3. Application status
    """
    health_status = {
        "status": "healthy",
        "components": {
            "database": "healthy",
            "redis": "healthy",
            "application": "healthy"
        }
    }

    # Check database connection
    try:
        db.execute("SELECT 1")
    except Exception as e:
        health_status["components"]["database"] = "unhealthy"
        health_status["status"] = "unhealthy"

    # Check Redis connection
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True
        )
        redis_client.ping()
    except Exception as e:
        health_status["components"]["redis"] = "unhealthy"
        health_status["status"] = "unhealthy"

    if health_status["status"] == "unhealthy":
        raise AppException(
            status_code=503,
            detail="Service Unavailable",
            headers={"X-Health-Check": "failed"}
        )

    return health_status 