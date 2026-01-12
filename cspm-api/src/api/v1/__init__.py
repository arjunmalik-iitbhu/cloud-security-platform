from fastapi import APIRouter

from . import actor, director, genre, movie, movie_rating

router = APIRouter(
    prefix="/v1",
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

router.include_router(actor.router)
router.include_router(director.router)
router.include_router(genre.router)
router.include_router(movie.router)
router.include_router(movie_rating.router)
