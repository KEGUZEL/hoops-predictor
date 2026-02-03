from fastapi import APIRouter

from app.core.config import get_settings


router = APIRouter()


@router.get("/")
def health_check() -> dict:
    """
    Basit health endpoint'i. DevOps monitoring için kullanılabilir.
    """
    settings = get_settings()
    return {
        "status": "ok",
        "environment": settings.environment,
        "app_name": settings.app_name,
    }

