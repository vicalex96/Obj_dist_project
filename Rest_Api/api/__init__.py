from fastapi import APIRouter
from api.routes import router as blog_router

router = APIRouter()

router.include_router(blog_router, prefix="/objects", tags= ["Phones"])