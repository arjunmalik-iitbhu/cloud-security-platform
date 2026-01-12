from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import ActorCreateReq, ActorRes
from src.model.entity import Actor

router = APIRouter(
    tags=["actors"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/actors", response_model=list[ActorRes])
async def read_actors(
    offset: int = 0,
    limit: int = 10,
    actor: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Actor)
    if actor:
        query = query.where(col(Actor.name).ilike(f"%{actor}%"))
    result = await session.exec(query.offset(offset).limit(limit))
    actors = result.all()
    return [ActorRes(**actor.model_dump()) for actor in actors]


@router.get("/actor/{actor_id}", response_model=ActorRes)
async def read_actor(actor_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Actor).where(Actor.id == int(actor_id)))
    actor = result.first()
    if not actor or not actor.id:
        raise HTTPException(status_code=404, detail=f"Actor {actor_id} not found")
    return ActorRes(**actor.model_dump())


@router.put(
    "/actor/{actor_id}",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_actor(actor_id: str, session: AsyncSession = Depends(get_session)):
    return HTTPException(status_code=403, detail=f"Operation forbidden")


@router.post("/actor", response_model=Actor, status_code=status.HTTP_201_CREATED)
async def create_actor(
    actorReq: ActorCreateReq, session: AsyncSession = Depends(get_session)
):
    actor = Actor(**actorReq.model_dump(by_alias=False))
    session.add(actor)
    await session.commit()
    await session.refresh(actor)
    return actor
