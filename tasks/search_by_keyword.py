from db.db_connector import DBConnection
from db.raw_queries import RawQueries

# Handles search by keyword in title or description.
class SearchByKeyword:
    def __init__(self, db: DBConnection):
        self.db = db

    # Searches for movies by keyword in title or description.
    def search_by_keyword(self, keyword: str):
        result = self.db.execute_select(RawQueries.GET_MOVIES_BY_KEYWORD, (keyword, keyword))
        return result