from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import DirectorCreateReq, DirectorRes
from src.model.entity import Director

router = APIRouter(
    tags=["directors"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/directors", response_model=list[DirectorRes])
async def read_directors(
    offset: int = 0,
    limit: int = 10,
    director: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Director)
    if director:
        query = query.where(col(Director.name).ilike(f"%{director}%"))
    result = await session.exec(query.offset(offset).limit(limit))
    directors = result.all()
    return [DirectorRes(**director.model_dump()) for director in directors]


@router.get("/director/{director_id}", response_model=DirectorRes)
async def read_director(director_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Director).where(Director.id == int(director_id)))
    director = result.first()
    if not director or not director.id:
        raise HTTPException(status_code=404, detail=f"Director {director_id} not found")
    return DirectorRes(**director.model_dump())


@router.put(
    "/director/{director_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_director(
    director_id: str, session: AsyncSession = Depends(get_session)
):
    return HTTPException(status_code=403, detail=f"Operation forbidden")


@router.post("/director", response_model=Director, status_code=status.HTTP_201_CREATED)
async def create_director(
    directorReq: DirectorCreateReq, session: AsyncSession = Depends(get_session)
):
    director = Director(**directorReq.model_dump(by_alias=False))
    session.add(director)
    await session.commit()
    await session.refresh(director)
    return director
