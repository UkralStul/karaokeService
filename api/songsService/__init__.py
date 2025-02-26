from fastapi import APIRouter
from .views import router as r
router = APIRouter()

router.include_router(r)