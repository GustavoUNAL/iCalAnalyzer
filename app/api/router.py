from fastapi import APIRouter
from app.api.endpoints import analysis, calendar_stats, productive_hours

api_router = APIRouter()

api_router.include_router(analysis.router, tags=["analysis"])
api_router.include_router(calendar_stats.router, tags=["calendar"])
api_router.include_router(productive_hours.router, tags=["productivity"])