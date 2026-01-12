class MovieService:
    def __init__(self, repository):
        self.repository = repository

    async def create_movie(self, movie_data: MovieBaseModel):
        return await self.repository.create_movie(movie_data)

    async def read_movies(self):
        return await self.repository.get_all_movies()

    async def read_movie_by_email(self, movie_email: str):
        return await self.repository.get_movie_by_email(movie_email)

    async def update_movie(self, movie_id, movie_data: MovieBaseModel):
        return await self.repository.update_movie(movie_id, movie_data)

    async def delete_movie(self, movie_id: int):
        return await self.repository.delete_movie(movie_id)
