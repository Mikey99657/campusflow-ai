from fastapi import APIRouter

from app.api.routes import health, tasks, agents

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
