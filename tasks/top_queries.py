from db.db_connector import DBConnection
from db.raw_queries import RawQueries
from config import TOP_QUERIES_LIMIT


# Handles retrieval and display of top search queries.
class TopQueries:
    def __init__(self, db: DBConnection):
        self.db = db

    # Retrieves the most popular search queries from the SQLite database.
    def get_top_queries(self):
        result = self.db.execute_sqlite_select(RawQueries.GET_TOP_QUERIES, (TOP_QUERIES_LIMIT,))
        return result

    # Fetches top queries filtered by type from SQLite.
    def get_top_queries_by_type(self, query_type: str):
        result = self.db.execute_sqlite_select(RawQueries.GET_TOP_QUERIES_BY_TYPE, (query_type, TOP_QUERIES_LIMIT))
        return result