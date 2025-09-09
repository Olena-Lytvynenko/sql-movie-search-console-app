import os
from dotenv import load_dotenv, find_dotenv
from pymysql.cursors import DictCursor

# Load environment variables from the .env file
os.environ.pop("USER", None) # Prevent conflict with system USER variable
load_dotenv(find_dotenv())

# MySQL database connection settings
MYSQL_CONFIG = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
    "cursorclass": DictCursor,
}

# SQLite database file path for query logging.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB_PATH = os.path.join(BASE_DIR, "db", "queries_log.db")

# Number of top queries to retrieve in GET_TOP_QUERIES.
TOP_QUERIES_LIMIT = 5

# Number of bubbles for the bubble chart of the most popular keywords.
MAX_KEYWORDS_BUBBLE = 10

# Default page size for paginated results
PAGE_SIZE = 10
