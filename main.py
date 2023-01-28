"""
Main application module.
"""
from fastapi import FastAPI

from app.routers.poly_router import router

app = FastAPI()

app.include_router(
    router=router,
    prefix="/api/v1",
    tags=["polys"],
    responses={404: {"description": "Not found"}},
)
