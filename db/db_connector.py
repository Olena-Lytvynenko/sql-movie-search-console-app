import sqlite3
from pymysql import connect
from pymysql.err import OperationalError
from config import SQLITE_DB_PATH


# Handles MySQL and SQLite database connections and operations.
class DBConnection:
    # Now MySQL can be disabled if not needed
    def __init__(self, use_mysql=True, **kwargs):
        self.connection = None

        if use_mysql:
            try:
                self.connection = connect(**kwargs)
            except OperationalError as e:
                print(f"Database connection failed: {e}")

    # Executes a SELECT query in MySQL
    def execute_select(self, query: str, params: tuple = ()):
        if not self.connection:
            print("MySQL connection not available.")
            return []
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    # Executes a SELECT query in SQLite
    def execute_sqlite_select(self, query: str, params: tuple = ()):
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH)
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return []

    # Closes the database connection.
    def close(self):
        if self.connection:
            self.connection.close()
