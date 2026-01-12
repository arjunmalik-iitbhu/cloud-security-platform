from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import MovieRatingCreateReq, MovieRatingRes
from src.model.entity import MovieRating

router = APIRouter(
    tags=["movie_ratings"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/ratings", response_model=list[MovieRatingRes])
async def read_ratings(
    offset: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
):
    result = await session.exec(select(MovieRating).offset(offset).limit(limit))
    ratings = result.all()
    return [MovieRatingRes(**rating.model_dump()) for rating in ratings]


@router.get("/rating/{rating_id}", response_model=MovieRatingRes)
async def read_rating(rating_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(
        select(MovieRating).where(MovieRating.id == int(rating_id))
    )
    rating = result.first()
    if not rating or not rating.id:
        raise HTTPException(
            status_code=404, detail=f"MovieRating {rating_id} not found"
        )
    return MovieRatingRes(**rating.model_dump())


@router.put(
    "/rating/{rating_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_rating(rating_id: str, session: AsyncSession = Depends(get_session)):
    return HTTPException(status_code=403, detail=f"Operation forbidden")


@router.post("/rating", response_model=MovieRating, status_code=status.HTTP_201_CREATED)
async def create_rating(
    ratingReq: MovieRatingCreateReq, session: AsyncSession = Depends(get_session)
):
    rating = MovieRating(**ratingReq.model_dump(by_alias=False))
    session.add(rating)
    await session.commit()
    await session.refresh(rating)
    return rating
