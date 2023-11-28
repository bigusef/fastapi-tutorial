from fastapi import APIRouter

from .location.router import router as location_router

root_router = APIRouter()
root_router.include_router(location_router)
