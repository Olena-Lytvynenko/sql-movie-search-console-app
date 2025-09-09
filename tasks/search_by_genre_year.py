from db.db_connector import DBConnection
from db.raw_queries import RawQueries

# Handles search by genre, year, and their combination.
class SearchByGenreYear:
    def __init__(self, db: DBConnection):
        self.db = db

    # Retrieves all available genres.
    def get_all_genres(self):
        result = self.db.execute_select(RawQueries.GET_GENRES)
        return result

    # Searches for movies by genre.
    def search_by_genre(self, genre: str):
        result = self.db.execute_select(RawQueries.GET_MOVIES_BY_GENRE, (genre,))
        return result

    # Searches for movies by production year.
    def search_by_year(self, year: int):
        result = self.db.execute_select(RawQueries.GET_MOVIES_BY_YEAR, (year,))
        return result

    # Searches for movies by genre and production year.
    def search_by_genre_and_year(self, genre: str, year: int) -> list[dict] | None:
        results = self.db.execute_select(RawQueries.GET_MOVIES_BY_GENRE, (genre,))
        filtered_results = [movie for movie in results if movie['release_year'] == year]
        return filtered_results