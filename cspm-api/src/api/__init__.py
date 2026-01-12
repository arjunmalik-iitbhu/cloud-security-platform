from fastapi import APIRouter

from . import v1

router = APIRouter(
    prefix="/version",
    dependencies=[],
)

router.include_router(v1.router)
