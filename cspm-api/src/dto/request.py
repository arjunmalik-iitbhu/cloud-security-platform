from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, from_attributes=True
    )


class MovieCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new movie.
    """

    title: str
    release_year: int
    director_id: Optional[int] = None
    actor_ids: Optional[list[int]] = None
    genre_ids: Optional[list[int]] = None


class MovieUpdateDirectorReq(BaseSchema):
    """
    Data Transfer Object for updating director of a movie.
    """

    director_id: Optional[int] = None


class MovieUpdateActorReq(BaseSchema):
    """
    Data Transfer Object for updating actor of a movie.
    """

    actor_id: Optional[int] = None


class MovieUpdateGenreReq(BaseSchema):
    """
    Data Transfer Object for updating genre of a movie.
    """

    genre_id: Optional[int] = None


class MovieRatingCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new movie.
    """

    movie_id: int
    comment: str
    story: int
    direction: int
    acting: int


class ActorCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new actor.
    """

    name: str
    movie_ids: Optional[list[int]] = None


class DirectorCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new director.
    """

    name: str


class GenreCreateReq(BaseSchema):
    """
    Data Transfer Object for creating a new genre.
    """

    name: str
    movie_ids: Optional[list[int]] = None
