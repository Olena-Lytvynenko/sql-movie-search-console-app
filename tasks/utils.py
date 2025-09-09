import logging
from db.db_connector import DBConnection
from db.raw_queries import RawQueries
from config import PAGE_SIZE
from prettytable import PrettyTable

# Configure logger for console output.
logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Formats movies into a PrettyTable and returns it.
def paginate_movies(movies: list, index: int = 0):
    if not movies:
        return None, None, None

    page = movies[index:index + PAGE_SIZE]
    start_index = index + 1
    end_index = min(index + PAGE_SIZE, len(movies))

    table = PrettyTable(["#", "Title", "Year"])
    for i, movie in enumerate(page, start=start_index):
        table.add_row([i, movie["title"], movie["release_year"]])

    has_previous = index > 0
    has_next = index + PAGE_SIZE < len(movies)

    return table, has_previous, has_next, start_index, end_index

# Retrieves and displays movie details based on user selection.
def display_movie_details(db: DBConnection, title: str):

    movie = db.execute_select(RawQueries.GET_MOVIE_DETAILS, (title,))[0]

    # PrettyTable for structured output
    table = PrettyTable(["Field", "Value"])
    table.add_row(["Title", movie["title"]])
    table.add_row(["Year", movie["year"]])
    table.add_row(["Description", movie["description"]])
    table.add_row(["Actors", movie["actors"]])

    logger.info("\033[97m\n" + str(table) + "\033[0m")

# Retrieves the minimum and maximum release years from the database
def get_year_range(db):
    result = db.execute_select(RawQueries.GET_YEAR_RANGE)
    return result[0]

def is_valid_year(year: str, year_range: dict) -> bool:
    if not year.isdigit():
        return False
    year = int(year)
    return year_range["min_year"] <= year <= year_range["max_year"]

# Validates that the input consists of only letters and spaces.
def is_valid_input(text):
    text = text.strip()
    return all(word.isalpha() for word in text.split())
