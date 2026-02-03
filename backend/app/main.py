from fastapi import FastAPI

from app.routers import players, teams, health
from app.core.logging_config import setup_logging


def create_app() -> FastAPI:
    """
    FastAPI application factory.
    """
    setup_logging()

    app = FastAPI(
        title="HoopsPredictor API",
        version="0.1.0",
        description="AI-Driven Performance Analyst for NBA data.",
    )

    # Include routers
    app.include_router(health.router, prefix="/health", tags=["health"])
    app.include_router(players.router, prefix="/players", tags=["players"])
    app.include_router(teams.router, prefix="/teams", tags=["teams"])

    return app


app = create_app()

