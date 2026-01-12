from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import joinedload
from sqlmodel import col, insert, select, update
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.dto import (
    ActorRes,
    DirectorRes,
    GenreRes,
    MovieCreateReq,
    MovieRatingRes,
    MovieRes,
    MovieUpdateActorReq,
    MovieUpdateDirectorReq,
    MovieUpdateGenreReq,
)
from src.model.entity import Actor, Director, Genre, Movie, MovieToActor, MovieToGenre

router = APIRouter(
    tags=["movies"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


def _get_movie_res(movie: Movie):
    movie_res = MovieRes(**movie.model_dump())
    movie_res.genres = [
        GenreRes(**movie_to_genre_row.genre.model_dump())
        for movie_to_genre_row in movie.movie_to_genre
        if movie_to_genre_row.genre
    ]
    movie_res.actors = [
        ActorRes(**movie_to_actor_row.actor.model_dump())
        for movie_to_actor_row in movie.movie_to_actor
        if movie_to_actor_row.actor
    ]
    if movie.director:
        movie_res.director = DirectorRes(**movie.director.model_dump())
    movie_res.ratings = [
        MovieRatingRes(**movie_rating_row.model_dump())
        for movie_rating_row in movie.movie_rating
    ]
    return movie_res


@router.get("/movies", response_model=list[MovieRes])
async def read_movies(
    offset: int = 0,
    limit: int = 10,
    movie: Optional[str] = None,
    genre: Optional[str] = None,
    actor: Optional[str] = None,
    director: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    query = select(Movie).options(
        joinedload(Movie.movie_to_genre).joinedload(MovieToGenre.genre),
        joinedload(Movie.movie_to_actor).joinedload(MovieToActor.actor),
        joinedload(Movie.director),
        joinedload(Movie.movie_rating),
    )
    if movie:
        query = query.where(col(Movie.title).ilike(f"%{movie}%"))
    if genre:
        query = query.where(col(Genre.name).ilike(f"%{genre}%"))
    if actor:
        query = query.where(col(Actor.name).ilike(f"%{actor}%"))
    if director:
        query = query.where(col(Director.name).ilike(f"%{director}%"))
    result = await session.exec(query.offset(offset).limit(limit))
    movies = result.unique().all()
    return [_get_movie_res(movie) for movie in movies]


@router.get("/movie/{movie_id}", response_model=MovieRes)
async def read_movie(movie_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.exec(
        select(Movie)
        .options(
            joinedload(Movie.movie_to_genre).joinedload(MovieToGenre.genre),
            joinedload(Movie.movie_to_actor).joinedload(MovieToActor.actor),
            joinedload(Movie.director),
            joinedload(Movie.movie_rating),
        )
        .where(Movie.id == int(movie_id))
    )
    movie = result.first()
    if not movie or not movie.id:
        raise HTTPException(status_code=404, detail=f"Movie {movie_id} not found")
    return _get_movie_res(movie)


@router.put(
    "/movie/{movie_id}/director",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_movie_director(
    movie_id: str,
    movieReq: MovieUpdateDirectorReq,
    session: AsyncSession = Depends(get_session),
):
    await session.exec(
        update(Movie)
        .where(Movie.id == int(movie_id))
        .values(director_id=movieReq.director_id)
    )
    await session.commit()
    return movie_id


@router.put(
    "/movie/{movie_id}/actor",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_movie_actor(
    movie_id: str,
    movieReq: MovieUpdateActorReq,
    session: AsyncSession = Depends(get_session),
):
    await session.exec(
        insert(MovieToActor).values(movie_id=int(movie_id), actor_id=movieReq.actor_id)
    )
    await session.commit()
    return movie_id


@router.put(
    "/movie/{movie_id}/genre",
    responses={403: {"description": "Operation forbidden"}},
)
async def update_movie_genre(
    movie_id: str,
    movieReq: MovieUpdateGenreReq,
    session: AsyncSession = Depends(get_session),
):
    await session.exec(
        insert(MovieToGenre).values(movie_id=int(movie_id), genre_id=movieReq.genre_id)
    )
    await session.commit()
    return movie_id


@router.post("/movie", response_model=Movie, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movieReq: MovieCreateReq, session: AsyncSession = Depends(get_session)
):
    movie = Movie(**movieReq.model_dump(by_alias=False))
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return movie
