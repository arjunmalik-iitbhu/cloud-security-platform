from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import GenreCreateReq, GenreRes
from src.model.entity import Genre

router = APIRouter(
    tags=["genres"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/genres", response_model=list[GenreRes])
async def read_genres(
    offset: int = 0,
    limit: int = 10,
    genre: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Genre)
    if genre:
        query = query.where(col(Genre.name).ilike(f"%{genre}%"))
    result = await session.exec(query.offset(offset).limit(limit))
    genres = result.all()
    return [GenreRes(**genre.model_dump()) for genre in genres]


@router.get("/genre/{genre_id}", response_model=GenreRes)
async def read_genre(genre_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Genre).where(Genre.id == int(genre_id)))
    genre = result.first()
    if not genre or not genre.id:
        raise HTTPException(status_code=404, detail=f"Genre {genre_id} not found")
    return GenreRes(**genre.model_dump())


@router.put(
    "/genre/{genre_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_genre(genre_id: str, session: AsyncSession = Depends(get_session)):
    return HTTPException(status_code=403, detail=f"Operation forbidden")


@router.post("/genre", response_model=Genre, status_code=status.HTTP_201_CREATED)
async def create_genre(
    genreReq: GenreCreateReq, session: AsyncSession = Depends(get_session)
):
    genre = Genre(**genreReq.model_dump(by_alias=False))
    session.add(genre)
    await session.commit()
    await session.refresh(genre)
    return genre
