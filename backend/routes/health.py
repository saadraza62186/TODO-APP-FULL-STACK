from fastapi import APIRouter
from datetime import datetime
from schemas import HealthResponse
from config import settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint.
    Returns API status and version.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=settings.APP_VERSION
    )
