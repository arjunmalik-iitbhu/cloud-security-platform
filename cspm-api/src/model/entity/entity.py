import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlmodel import Field, Relationship, SQLModel


class Actor(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("name::text <> ''::text", name="actor_name_check"),
        PrimaryKeyConstraint("id", name="actor_primary_key"),
        UniqueConstraint("name", name="actor_unique_name"),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    name: str = Field(sa_column=Column("name", String(200), nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    movie_to_actor: list["MovieToActor"] = Relationship(back_populates="actor")


class Director(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("name::text <> ''::text", name="director_name_check"),
        PrimaryKeyConstraint("id", name="director_primary_key"),
        UniqueConstraint("name", name="director_unique_name"),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    name: str = Field(sa_column=Column("name", String(200), nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    movie: list["Movie"] = Relationship(back_populates="director")


class Genre(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("name::text <> ''::text", name="genre_name_check"),
        PrimaryKeyConstraint("id", name="genre_primary_key"),
        UniqueConstraint("name", name="genre_unique_name"),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    name: str = Field(sa_column=Column("name", String(200), nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    movie_to_genre: list["MovieToGenre"] = Relationship(back_populates="genre")


class Movie(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("title::text <> ''::text", name="movie_title_check"),
        ForeignKeyConstraint(
            ["director_id"],
            ["director.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="movie_foreign_key_director_id",
        ),
        PrimaryKeyConstraint("id", name="movie_primary_key"),
        UniqueConstraint("title", name="movie_unique_title"),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    title: str = Field(sa_column=Column("title", String(1000), nullable=False))
    release_year: int = Field(sa_column=Column("release_year", Integer, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    director_id: Optional[int] = Field(
        default=None, sa_column=Column("director_id", BigInteger)
    )

    director: Optional["Director"] = Relationship(back_populates="movie")
    movie_rating: list["MovieRating"] = Relationship(back_populates="movie")
    movie_to_actor: list["MovieToActor"] = Relationship(back_populates="movie")
    movie_to_genre: list["MovieToGenre"] = Relationship(back_populates="movie")


class MovieRating(SQLModel, table=True):
    __tablename__ = "movie_rating"
    __table_args__ = (
        ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="movie_rating_foreign_key_movie_id",
        ),
        PrimaryKeyConstraint("id", name="movie_rating_primary_key"),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    comment: str = Field(
        sa_column=Column(
            "comment", Text, nullable=False, server_default=text("''::text")
        )
    )
    story: int = Field(
        sa_column=Column("story", Integer, nullable=False, server_default=text("4"))
    )
    direction: int = Field(
        sa_column=Column("direction", Integer, nullable=False, server_default=text("4"))
    )
    acting: int = Field(
        sa_column=Column("acting", Integer, nullable=False, server_default=text("4"))
    )
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    movie_id: Optional[int] = Field(
        default=None, sa_column=Column("movie_id", BigInteger)
    )

    movie: Optional["Movie"] = Relationship(back_populates="movie_rating")


class MovieToActor(SQLModel, table=True):
    __tablename__ = "movie_to_actor"
    __table_args__ = (
        ForeignKeyConstraint(
            ["actor_id"],
            ["actor.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="movie_to_actor_foreign_key_actor_id",
        ),
        ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="movie_to_actor_foreign_key_movie_id",
        ),
        PrimaryKeyConstraint("id", name="movie_to_actor_primary_key"),
        UniqueConstraint(
            "movie_id", "actor_id", name="movie_to_actor_unique_movie_id_actor_id"
        ),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    movie_id: int = Field(sa_column=Column("movie_id", BigInteger, nullable=False))
    actor_id: int = Field(sa_column=Column("actor_id", BigInteger, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    actor: Optional["Actor"] = Relationship(back_populates="movie_to_actor")
    movie: Optional["Movie"] = Relationship(back_populates="movie_to_actor")


class MovieToGenre(SQLModel, table=True):
    __tablename__ = "movie_to_genre"
    __table_args__ = (
        ForeignKeyConstraint(
            ["genre_id"],
            ["genre.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="movie_to_genre_foreign_key_genre_id",
        ),
        ForeignKeyConstraint(
            ["movie_id"],
            ["movie.id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="movie_to_genre_foreign_key_movie_id",
        ),
        PrimaryKeyConstraint("id", name="movie_to_genre_primary_key"),
        UniqueConstraint(
            "movie_id", "genre_id", name="movie_to_genre_unique_movie_id_genre_id"
        ),
    )

    id: int = Field(sa_column=Column("id", BigInteger, primary_key=True))
    movie_id: int = Field(sa_column=Column("movie_id", BigInteger, nullable=False))
    genre_id: int = Field(sa_column=Column("genre_id", BigInteger, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(
            "created_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            "updated_at",
            DateTime(True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )

    genre: Optional["Genre"] = Relationship(back_populates="movie_to_genre")
    movie: Optional["Movie"] = Relationship(back_populates="movie_to_genre")
