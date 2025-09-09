# Console Application for Movie Search Using SQL Databases

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Database](https://img.shields.io/badge/SQL-MySQL%20%2F%20SQLite-orange)]()

## Project Description

This is a modular Python console application designed for searching movies in an SQL database. The goal is to provide a flexible text search interface that works across various filters — keywords, actors, genres, and release years — and can be easily adapted to any SQL schema.

The project follows modular principles with low coupling. Each part of the code has a clearly defined responsibility and can be modified or reused independently. The architecture supports easy scalability without rewriting the entire application.

In addition to search functionality, the project logs **keyword-based search queries** into a local SQLite database. These logs are stored in a separate table and remain on the user’s device. This makes the project suitable not only as a search tool, but also as a base for analytics systems or user behavior tracking.

## Key Features

- Search movies by keyword  
- Search by actor name  
- Search by genre and release year  
- Log keyword searches into a dedicated SQLite table  
- Optional visualization of most frequent search terms

## How It Works

The application runs in the terminal. The user selects a search scenario and provides input. Results are printed as a formatted table. For keyword-based searches, queries are automatically saved to a local log database.

All connection parameters are stored in a `.env` file and loaded via `config.py`. The `.env` file is not included in the project, but an `.env.example` template is provided. On first run, the `queries_log.db` file is created automatically.

## Project Structure

```
sql-movie-search-console-app/
├── main.py               # Entry point: launch app and menu
├── config.py             # Loads environment variables from .env
├── requerements.txt      # Python dependency list
├── .env.example          # Template for environment variables
├── .gitignore            # Ignored files and folders

├── tasks/                # User-facing logic
│   ├── search_by_keyword.py       # Keyword-based search (logged)
│   ├── search_by_actor.py         # Search by actor name
│   ├── search_by_genre_year.py    # Search by genre and release year
│   ├── top_queries.py             # Retrieve most frequent keywords
│   ├── visualisation.py           # Optional bar chart (Matplotlib)
│   └── utils.py                   # Formatting and helper functions

├── db/                   # Database logic
│   ├── db_connector.py           # MySQL / SQLite connector
│   ├── raw_queries.py            # SQL queries for all search types
│   ├── query_logger.py           # Log table creation and updates
│   └── queries_log.db            # Local SQLite log file (auto-created)
```

## Installation and Run Instructions

1. Clone the repository  
2. Install dependencies:

```
pip install -r requerements.txt
```

3. Create your own `.env` file based on `.env.example` and enter your database credentials  
4. Run `main.py` via terminal

## How This Project Can Be Used

- As a base for custom SQL-based search tools  
- For user behavior analytics projects  
- As a teaching tool for Python architecture and modular design  
- As a starting point for MVPs that require local search + logging

## Who This Project Is For

If you're learning Python and want to build small but logically structured tools with real functionality, this project is a great practice base. You’ll work with architecture, imports, separation of logic into modules, and terminal interaction.

If you’re a data analyst, this can serve as a basic framework for logging and analyzing user search behavior.

If you’re practicing SQL, it’s a great way to reinforce SELECT queries, filters, grouping, and integrating SQL logic into Python.

And if you're prototyping an MVP — the core logic for filtering and logging is already implemented. You can easily extend it with a bot, interface, or API to build a complete microservice.

## License

This project is released under the MIT license.  
You are free to use, modify, and integrate the code into your own work — as long as proper attribution is given. All local data stays on the user’s device.
