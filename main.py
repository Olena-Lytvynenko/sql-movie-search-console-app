import logging
import time
from db.db_connector import DBConnection
from db.query_logger import QueryLogger
from tasks.search_by_actor import SearchByActor
from tasks.search_by_genre_year import SearchByGenreYear
from tasks.search_by_keyword import SearchByKeyword
from tasks.top_queries import TopQueries
from tasks.visualisation import generate_pie_chart, generate_bar_chart, generate_bubble_chart
from tasks.utils import paginate_movies, display_movie_details, is_valid_year, get_year_range
from config import MYSQL_CONFIG, PAGE_SIZE
from prettytable import PrettyTable

# Configure logger for console output
logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database connection
db_mysql = DBConnection(**MYSQL_CONFIG)  # MySQL
db_sqlite = DBConnection(use_mysql=False) # SQLite
logger_db = QueryLogger()

# Initialize search modules
actor_search = SearchByActor(db_mysql)
genre_year_search = SearchByGenreYear(db_mysql)
keyword_search = SearchByKeyword(db_mysql)
top_queries = TopQueries(db_sqlite)


# Handles searching for movies by actor.
def handle_actor_search():
    attempts = 3
    while attempts > 0:
        time.sleep(0.7)
        actor_name = input("\nEnter actor's name: ").strip()

        # Validate input: must be at least 3 characters and contain only letters
        if len(actor_name) >= 3 and all(part.isalpha() for part in actor_name.split()):
            logger_db.log_query(keyword=actor_name, query_type="actor")
            matching_actors = actor_search.get_matching_actors(actor_name)

            # If no matching actors are found, return to the menu
            if not matching_actors:
                logger.info(f"\nNo actor {actor_name} found.")
                return

            # If only one match is found, select it automatically
            if len(matching_actors) == 1:
                selected_actor = matching_actors[0]["full_name"]
            else:
                # Display matching actors in a table
                table = PrettyTable(["#", "Actor Name"])
                for idx, actor in enumerate(matching_actors, 1):
                    table.add_row([idx, actor["full_name"]])
                logger.info("\033[97m\n" + str(table) + "\033[0m")

                # Prompt user for selection
                while True:
                    time.sleep(0.7)
                    choice = input("\nSelect an actor by number (or 'n' to cancel): ").strip().lower()
                    if choice == 'n':
                        return
                    elif choice.isdigit() and 1 <= int(choice) <= len(matching_actors):
                        selected_actor = matching_actors[int(choice) - 1]["full_name"]
                        logger_db.log_query(keyword=selected_actor, query_type="actor")  # Log refined search
                        break
                    else:
                        logger.info("\n\033[91mInvalid choice. Please enter a valid number or 'n' to cancel.\033[0m")

            # If an actor is selected, perform a movie search
            if selected_actor:
                results = actor_search.search_by_actor(selected_actor)

                # If no movies are found for the actor, return to the menu
                if not results:
                    logger.info(f"\nNo movies found for actor: {selected_actor}")
                    return

                handle_paginated_movie_selection(results)
            return
        else:
            logger.info("\n\033[91mActor's name must have at least 3 letters and contain only alphabetic characters.\033[0m")
            attempts -= 1

    logger.info("\nToo many invalid attempts. Returning to the main menu.")
    return


# Handles searching for movies by genre.
def handle_genre_search():

    # Display available genres in a table
    genres = genre_year_search.get_all_genres()
    table = PrettyTable(["#", "Genre"])
    for idx, genre in enumerate(genres, start=1):
        table.add_row([idx, genre["genre"]])
    logger.info("\033[97m\n" + str(table) + "\033[0m")

    attempts = 3
    while attempts > 0:
        time.sleep(0.7)
        genre_input = input("\nSelect genre by number or enter name: ").strip().lower()

        # Check if input is a number within the valid range
        if genre_input.isdigit():
            genre_idx = int(genre_input)
            if 1 <= genre_idx <= len(genres):
                genre = genres[genre_idx - 1]["genre"]
            else:
                logger.info(f"\n\033[91mInvalid selection. Please enter a number between 1 and {len(genres)}.\033[0m")
                attempts -= 1
                continue
        else:
            genre = genre_input

            # Validate genre input
            available_genres = {g["genre"].lower() for g in genres}
            if genre not in available_genres:
                logger.info("\n\033[91mInvalid genre selection. Please choose from the available options.\033[0m")
                attempts -= 1
                continue

        # Log the selected genre
        logger_db.log_query(genre=genre, query_type="genre")

        # Execute search
        results = genre_year_search.search_by_genre(genre)
        if results:
            handle_paginated_movie_selection(results)
        else:
            logger.info(f"\nNo movies found for genre: {genre}")
        return

    # If all attempts fail, return to the main menu
    logger.info("\nToo many invalid attempts. Returning to the main menu.")
    return


# Handles searching for movies by production year with validation.
def handle_year_search():
    attempts = 3
    year_range = get_year_range(db_mysql)

    while attempts > 0:
        time.sleep(0.7)
        year = input(f"\nEnter production year ({year_range['min_year']} - {year_range['max_year']}): ").strip()

        if not is_valid_year(year, year_range):
            logger.info(f"\n\033[91mInvalid year. Please enter a value between {year_range['min_year']} and {year_range['max_year']}.\033[0m")
            attempts -= 1
            continue

        year = int(year)
        logger_db.log_query(production_year=year, query_type="year")

        results = genre_year_search.search_by_year(year)
        if results:
            handle_paginated_movie_selection(results)
        else:
            logger.info(f"\nNo movies found for year: {year}")
        return

    logger.info("\nToo many invalid attempts. Returning to the main menu.")
    return


# Handles searching for movies by both genre and year.
def handle_genre_year_search():
    # Retrieve the list of genres
    genres = genre_year_search.get_all_genres()
    table = PrettyTable(["#", "Genre"])
    for idx, genre in enumerate(genres, start=1):
        table.add_row([idx, genre["genre"]])
    logger.info("\033[97m\n" + str(table) + "\033[0m")

    # Retrieve the dynamic year range from the database
    year_range = get_year_range(db_mysql)

    attempts = 3
    while attempts > 0:
        time.sleep(0.7)
        genre_input = input("\nSelect genre by number or enter name: ").strip().lower()

        # Validate genre input
        if genre_input.isdigit():
            genre_idx = int(genre_input)
            if 1 <= genre_idx <= len(genres):
                genre = genres[genre_idx - 1]["genre"]
            else:
                logger.info(f"\n\033[91mInvalid selection. Please enter a number between 1 and {len(genres)}.\033[0m")
                attempts -= 1
                continue
        else:
            genre = genre_input

            # Validate genre input
            available_genres = {g["genre"].lower() for g in genres}
            if genre not in available_genres:
                logger.info("\n\033[91mInvalid genre selection. Please choose from the available options.\033[0m")
                attempts -= 1
                continue

        # User enters the production year
        year_attempts = 3
        while year_attempts > 0:
            time.sleep(0.7)
            year = input(f"\nEnter production year ({year_range['min_year']} - {year_range['max_year']}): ").strip()

            if is_valid_year(year, year_range):  # Validate year with dynamic range
                year = int(year)
                logger_db.log_query(genre=genre, production_year=year, query_type="genre_year")

                results = genre_year_search.search_by_genre_and_year(genre, year)
                if results:
                    handle_paginated_movie_selection(results)
                else:
                    logger.info(f"\nNo movies found for genre '{genre}' in year {year}.")
                return
            else:
                logger.info(f"\n\033[91mInvalid year. Please enter a value between {year_range['min_year']} and {year_range['max_year']}.\033[0m")
                year_attempts -= 1

        logger.info("\nToo many invalid attempts. Returning to the main menu.")
        return


# Handles searching for movies by keyword.
def handle_keyword_search():
    attempts = 3
    while attempts > 0:
        time.sleep(0.7)
        keyword = input("\nEnter keyword: ").strip()

        # Validate keyword: must be a single alphabetic word (no spaces, numbers, or symbols)
        if len(keyword) >= 3 and keyword.isalpha():
            query_id = logger_db.log_query(keyword=keyword, query_type="keyword")
            if query_id:
                logger_db.log_keyword(query_id, keyword)

            results = keyword_search.search_by_keyword(keyword)

            if results:
                handle_paginated_movie_selection(results)
            else:
                logger.info(f"\nNo movies found for keyword: {keyword}")
            return
        else:
            logger.info("\n\033[91mKeyword must be a single word with at least 3 alphabetic characters.\033[0m")
            attempts -= 1

    logger.info("\nToo many invalid attempts. Returning to the main menu.")
    return


# Handles user interaction for paginated movie selection.
def handle_paginated_movie_selection(results):
    index = 0

    while True:
        table, has_previous, has_next, start_index, end_index = paginate_movies(results, index)

        if not table:
            logger.info("\nNo movies found.")
            return

        logger.info("\033[97m\n" + str(table) + "\033[0m")

        # Navigation options
        commands = [f"Enter movie number ({start_index}-{end_index}) to view details"]
        if has_previous:
            commands.append("'p' for previous")
        if has_next:
            commands.append("'m' for more")
        commands.append("'n' to return")

        logger.info(f"\033[92m\n{', '.join(commands)}.\033[0m")

        # User input with limited attempts
        attempts = 3
        while attempts > 0:
            time.sleep(0.7)
            choice = input("\nEnter your choice: ").strip().lower()

            if choice == 'n':
                return

            elif choice == 'p' and has_previous:
                index = max(0, index - PAGE_SIZE)
                break  # Restart loop to update table

            elif choice == 'm' and has_next:
                index += PAGE_SIZE
                break  # Restart loop to update table

            elif choice.isdigit() and 1 <= int(choice) <= len(results):
                title = results[int(choice) - 1]["title"]
                display_movie_details(db_mysql, title)

                # Adding a dialog for returning to the movie list or exiting.
                back_attempts = 3
                while back_attempts > 0:
                    time.sleep(0.7)
                    back_choice = input("\nDo you want to return to the movie list? (y/n): ").strip().lower()
                    if back_choice == 'y':
                        break
                    elif back_choice == 'n':
                        logger.info("\n\033[92mReturning to the main menu.\033[0m")
                        return
                    else:
                        logger.info("\n\033[91mInvalid input. Please enter 'y' to return to the movie list or 'n' to exit.\033[0m")
                        back_attempts -= 1

                if back_attempts == 0:
                    logger.info("\nToo many invalid attempts. Returning to the main menu.")
                    return

                break
            else:
                logger.info("\n\033[91mInvalid input. Please enter a valid command.\033[0m")
                attempts -= 1

        if attempts == 0:
            logger.info("\nToo many invalid attempts. Returning to the main menu.")
            return

# Handles the menu for viewing top queries with retry limit and return option
def handle_statistics_menu():
    attempts = 3
    while attempts > 0:
        table = PrettyTable(["#", "View Top Queries"])
        table.add_row(["1", "Overall Top Queries"])
        table.add_row(["2", "Top Queries by Actor"])
        table.add_row(["3", "Top Queries by Genre"])
        table.add_row(["4", "Top Queries by Year"])
        table.add_row(["5", "Top Queries by Genre & Year"])
        table.add_row(["6", "Top Queries by Keyword"])
        table.add_row(["n", "Return to Main Menu"])
        logger.info("\033[97m\n" + str(table) + "\033[0m")

        time.sleep(0.7)
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "n":
            return  # Exit to main menu

        if not choice.isdigit() or not (1 <= int(choice) <= 6):
            logger.info(f"\n\033[91mInvalid input. Please enter a number between 1 and 6.\033[0m")
            attempts -= 1
            if attempts == 0:
                logger.info("\nToo many invalid attempts. Returning to the main menu.")
                return
            continue

        # Map choices to corresponding query functions
        query_options = {
            "1": top_queries.get_top_queries,
            "2": lambda: top_queries.get_top_queries_by_type("actor"),
            "3": lambda: top_queries.get_top_queries_by_type("genre"),
            "4": lambda: top_queries.get_top_queries_by_type("year"),
            "5": lambda: top_queries.get_top_queries_by_type("genre_year"),
            "6": lambda: top_queries.get_top_queries_by_type("keyword"),
        }

        results = query_options[choice]()

        if not results:
            logger.info("\nNo data available for this category.")
        else:
            # Display results in PrettyTable
            result_table = PrettyTable(["#", "Query", "Count"])
            for idx, row in enumerate(results, start=1):
                result_table.add_row([idx, row[1], row[2]])

            logger.info("\033[97m\n" + str(result_table) + "\033[0m")

        # Ask user if they want to continue
        retry_attempts = 3
        while retry_attempts > 0:
            time.sleep(0.7)
            retry_choice = input("\nWould you like to view another top query? (y/n): ").strip().lower()
            if retry_choice == "y":
                break  # Restart menu loop
            elif retry_choice == "n":
                logger.info("\033[92mReturning to the main menu.\033[0m")
                return
            else:
                retry_attempts -= 1
                logger.info(f"\n\033[91mInvalid input. Please enter 'y' to continue or 'n' to return.\033[0m")

        if retry_attempts == 0:
            logger.info("\nToo many invalid attempts. Returning to the main menu.")
            return


# Handles the menu for viewing graphical visualizations of search data
def handle_visualization_menu():
    attempts = 3
    while attempts > 0:
        table = PrettyTable(["#", "Visualization"])
        table.add_row(["1", "Pie Chart (Query Types)"])
        table.add_row(["2", "Bar Chart (Top Queries)"])
        table.add_row(["3", "Bubble Chart (Keyword Frequency)"])
        table.add_row(["n", "Return to Main Menu"])
        logger.info("\033[97m\n" + str(table) + "\033[0m")

        time.sleep(0.7)
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "n":
            return

        if not choice.isdigit() or not (1 <= int(choice) <= 3):
            logger.info(f"\n\033[91mInvalid input. Please enter a number between 1 and 3.\033[0m")
            attempts -= 1
            if attempts == 0:
                logger.info("\nToo many invalid attempts. Returning to the main menu.")
                return
            continue

        # Map choices to visualization functions
        visualization_options = {
            "1": generate_pie_chart,
            "2": generate_bar_chart,
            "3": generate_bubble_chart,
        }

        logger.info("\n\033[92mGenerating visualization...\033[0m")
        visualization_options[choice](db_sqlite)

        # Ask user if they want to view another visualization
        retry_attempts = 3
        while retry_attempts > 0:
            time.sleep(0.7)
            retry_choice = input("\nWould you like to view another visualization? (y/n): ").strip().lower()
            if retry_choice == "y":
                break
            elif retry_choice == "n":
                logger.info("\033[92mReturning to the main menu.\033[0m")
                return
            else:
                retry_attempts -= 1
                logger.info(f"\n\033[91mInvalid input. Please enter 'y' to continue or 'n' to return.\033[0m")

        if retry_attempts == 0:
            logger.info("\nToo many invalid attempts. Returning to the main menu.")
            return


def main():
    try:
        logger.info("\n\033[92mWelcome to CineScope!\033[0m")
        logger.info("\033[92mFind movies by actor, genre, year, or keyword.\033[0m")

        options = {
            "1": handle_actor_search,
            "2": handle_genre_search,
            "3": handle_year_search,
            "4": handle_genre_year_search,
            "5": handle_keyword_search,
            "6": handle_statistics_menu,
            "7": handle_visualization_menu,
        }

        while True:
            table = PrettyTable(["#", "Main Menu"])
            table.add_row(["1", "Search by Actor"])
            table.add_row(["2", "Search by Genre"])
            table.add_row(["3", "Search by Year"])
            table.add_row(["4", "Search by Genre & Year"])
            table.add_row(["5", "Search by Keyword"])
            table.add_row(["6", "View Top Queries"])
            table.add_row(["7", "View Visualizations"])
            table.add_row(["n", "Exit"])
            logger.info("\033[97m\n" + str(table) + "\033[0m")

            time.sleep(0.7)
            choice = input("\nEnter your choice (1-7 or 'n' to exit): ").strip()

            if choice.lower() == "n":
                logger.info("\n\033[92mExiting CineScope. Goodbye!\033[0m")
                break
            elif choice in options:
                options[choice]()  # Call the corresponding function
            else:
                logger.info("\n\033[91mInvalid choice. Please enter a number between 1 and 7, or 'n' to exit.\033[0m")
    finally:
        db_mysql.close()
        db_sqlite.close()


if __name__ == "__main__":
    main()
