# Stores raw SQL queries for various searches in the sakila database.
class RawQueries:

    # Retrieves all available genres from the category table.
    GET_GENRES = """
        SELECT name AS genre
        FROM category;
        """

    # Retrieves movies by genre.
    GET_MOVIES_BY_GENRE = """
        SELECT f.title, f.release_year, c.name AS genre
        FROM film AS f
        LEFT JOIN film_category AS fc ON f.film_id = fc.film_id
        LEFT JOIN category AS c ON fc.category_id = c.category_id
        WHERE LOWER(c.name) = LOWER(%s)
        ORDER BY f.release_year DESC;
        """

    # Retrieves movies by production year.
    GET_MOVIES_BY_YEAR = """
        SELECT title, release_year
        FROM film
        WHERE release_year = %s
        ORDER BY title ASC;
        """

    # Retrieves the minimum and maximum release years from the film table.
    GET_YEAR_RANGE = """
        SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year
        FROM film;
        """

    # Retrieves movies by keyword in title or description (case-insensitive, excludes partial matches).
    GET_MOVIES_BY_KEYWORD = """
        SELECT title, release_year, description
        FROM film
        WHERE title REGEXP CONCAT('(^| )', %s, '.*( |$)')
        OR description REGEXP CONCAT('(^| )', %s, '.*( |$)')
        ORDER BY release_year DESC;
        """

    # Retrieves movies by a single name (first or last).
    GET_MOVIES_BY_ACTOR_SINGLE = """
        SELECT f.title, f.release_year, a.first_name, a.last_name
        FROM film AS f
        JOIN film_actor AS fa ON f.film_id = fa.film_id
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE a.first_name LIKE %s OR a.last_name LIKE %s
        ORDER BY f.release_year DESC;
        """

    # Retrieves movies by full name (first AND last).
    GET_MOVIES_BY_ACTOR_FULL = """
        SELECT f.title, f.release_year, a.first_name, a.last_name
        FROM film AS f
        JOIN film_actor AS fa ON f.film_id = fa.film_id
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE a.first_name LIKE %s AND a.last_name LIKE %s
        ORDER BY f.release_year DESC;
        """

    # Retrieves a list of actors whose first name or last name matches the search input.
    GET_MATCHING_ACTORS = """
        SELECT CONCAT(first_name, ' ', last_name) AS full_name
        FROM actor
        WHERE first_name LIKE %s OR last_name LIKE %s;
        """

    # Retrieves the top N most searched queries from queries_log.
    GET_TOP_QUERIES = """
        SELECT query_type, 
            CASE 
                WHEN query_type = 'genre' THEN 'Genre: ' || genre
                WHEN query_type = 'year' THEN 'Year: ' || production_year
                WHEN query_type = 'keyword' THEN 'Keyword: ' || keyword
                WHEN query_type = 'genre_year' THEN 'Genre: ' || genre || ', Year: ' || production_year
                WHEN query_type = 'actor' THEN 'Actor: ' || keyword
            END AS search_text,
            COUNT(*) AS search_count
        FROM queries_log
        WHERE query_type IN ('genre', 'year', 'keyword', 'genre_year', 'actor') 
        GROUP BY query_type, search_text
        ORDER BY search_count DESC
        LIMIT ?;
        """

    # Retrieves top queries filtered by type.
    GET_TOP_QUERIES_BY_TYPE = """
            SELECT query_type, 
                CASE 
                    WHEN query_type = 'genre' THEN 'Genre: ' || genre
                    WHEN query_type = 'year' THEN 'Year: ' || production_year
                    WHEN query_type = 'keyword' THEN 'Keyword: ' || keyword
                    WHEN query_type = 'genre_year' THEN 'Genre: ' || genre || ', Year: ' || production_year
                    WHEN query_type = 'actor' THEN 'Actor: ' || keyword
                END AS search_text,
                COUNT(*) AS search_count
            FROM queries_log
            WHERE query_type = ?
            GROUP BY query_type, search_text
            ORDER BY search_count DESC
            LIMIT ?;
            """

    # Retrieves movie details (title, year, description, actors) by title (case-insensitive).
    GET_MOVIE_DETAILS = """
        SELECT 
            f.title AS title,
            f.release_year AS year,
            f.description AS description,
            GROUP_CONCAT(DISTINCT CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE LOWER(f.title) = LOWER(%s)
        GROUP BY f.film_id, f.title, f.release_year, f.description;
        """

    # Query for visualisation pie chart
    PIE_CHART_QUERY = """
            SELECT query_type, COUNT(*) AS count
            FROM queries_log
            GROUP BY query_type;
        """

    # Query for bubble chart (keyword frequency)
    BUBBLE_CHART_QUERY = """
        SELECT keyword, COUNT(*) AS count
        FROM keywords_log
        GROUP BY keyword
        ORDER BY count DESC
        LIMIT ?;
        """