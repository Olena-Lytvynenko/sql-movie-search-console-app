import sqlite3
import os

# Handles logging search queries into the SQLite database.
class QueryLogger:
    DB_PATH = os.path.abspath(os.path.join("db", "queries_log.db"))

    QUERIES_LOG_TABLE = """
    CREATE TABLE IF NOT EXISTS queries_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT,  
        production_year INTEGER,  
        keyword TEXT,
        query_type TEXT NOT NULL,
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Adds a table for storing searched keywords.
    KEYWORDS_LOG_TABLE = """
    CREATE TABLE IF NOT EXISTS keywords_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_id INTEGER,
        keyword TEXT NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Initializes the connection to the SQLite database and ensures the tables exist.
    def __init__(self):
        try:
            self.connection = sqlite3.connect(self.DB_PATH)
            self.cursor = self.connection.cursor()
            with self.connection:
                self.cursor.execute(self.QUERIES_LOG_TABLE)  # Ensures queries_log exists
                self.cursor.execute(self.KEYWORDS_LOG_TABLE)  # Ensures keywords_log exists
        except sqlite3.Error as e:
            print(f"Database connection failed: {e}")
            self.connection = None

    # Logs a search query into the database and saves keywords if applicable.
    def log_query(self, genre: str = None, production_year: int = None, keyword: str = None, query_type: str = "") -> int:
        try:
            with self.connection:
                self.cursor.execute("""
                INSERT INTO queries_log (genre, production_year, keyword, query_type) 
                VALUES (?, ?, ?, ?);
                """, (genre, production_year, keyword, query_type))

                query_id = self.cursor.lastrowid  # Gets the ID of the inserted query
                return query_id  # Returns the query ID for further use.

        except sqlite3.Error as e:
            print(f"Failed to log query: {e}")
            return None  # Returns None if logging fails.

    # Logs a keyword search into the keywords_log table.
    def log_keyword(self, query_id: int, keyword: str) -> None:
        try:
            with self.connection:
                self.cursor.execute("""
                INSERT INTO keywords_log (query_id, keyword) 
                VALUES (?, ?);
                """, (query_id, keyword))
        except sqlite3.Error as e:
            print(f"Failed to log keyword: {e}")

    # Closes the database connection.
    def close(self) -> None:
        if self.connection:
            self.connection.close()