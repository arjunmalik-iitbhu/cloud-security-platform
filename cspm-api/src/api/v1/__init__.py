from fastapi import APIRouter

from . import credential, analysis

router = APIRouter(
    prefix="/v1",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

router.include_router(credential.router)
router.include_router(analysis.router)
