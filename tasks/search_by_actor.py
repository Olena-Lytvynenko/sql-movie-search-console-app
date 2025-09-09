from db.db_connector import DBConnection
from db.raw_queries import RawQueries

# Handles search for movies by actor.
class SearchByActor:
    def __init__(self, db: DBConnection):
        self.db = db

    # Searches for movies by actor (first name, last name, or both).
    def search_by_actor(self, actor_name: str):
        name_parts = actor_name.split()

        if len(name_parts) == 1:
            query = RawQueries.GET_MOVIES_BY_ACTOR_SINGLE
            params = (f"%{name_parts[0]}%", f"%{name_parts[0]}%")
        elif len(name_parts) == 2:
            query = RawQueries.GET_MOVIES_BY_ACTOR_FULL
            params = (f"%{name_parts[0]}%", f"%{name_parts[1]}%")
        else:
            return None  # Invalid input case is handled in `main.py`

        result = self.db.execute_select(query, params)
        return result


    # Retrieves a list of actors matching the input.
    def get_matching_actors(self, actor_name: str):
        query = RawQueries.GET_MATCHING_ACTORS
        params = (f"%{actor_name}%", f"%{actor_name}%")
        result = self.db.execute_select(query, params)
        return result


