import matplotlib.pyplot as plt
import numpy as np
from db.db_connector import DBConnection
from db.raw_queries import RawQueries
from config import MAX_KEYWORDS_BUBBLE


# Generates a bar chart of the most popular queries.
def generate_bar_chart(db: DBConnection):
    data = db.execute_sqlite_select(RawQueries.GET_TOP_QUERIES, (7,))

    if not data:
        print("No data available for visualization.")
        return

    queries = [f"{row[0].capitalize()}: {row[1].replace(row[0].capitalize() + ': ', '')}" for row in data]
    counts = [row[2] for row in data]

    plt.figure(figsize=(10, 5))
    plt.barh(queries[::-1], counts[::-1], color="purple")

    plt.xlabel("Search Count", fontsize=12)
    plt.ylabel("Query Type & Value", fontsize=12)
    plt.title(f"Top {len(queries)} Most Popular Queries", fontsize=14)

    plt.xticks(np.arange(0, max(counts) + 1, 1), fontsize=10)
    plt.yticks(fontsize=10, ha="right")

    plt.subplots_adjust(left=0.25)
    plt.tight_layout()

    plt.show()

# Generates a bubble chart for keyword frequency.
def generate_bubble_chart(db: DBConnection):
    data = db.execute_sqlite_select(RawQueries.BUBBLE_CHART_QUERY, (MAX_KEYWORDS_BUBBLE,))

    if not data:
        print("No data available for visualization.")
        return

    keywords = [row[0] for row in data]
    counts = [row[1] for row in data]
    sizes = [count * 1000 for count in counts]

    np.random.seed(42)
    x_positions = np.random.uniform(1, 9, len(keywords))
    y_positions = np.random.uniform(1, 9, len(keywords))

    plt.figure(figsize=(8, 6))
    plt.scatter(x_positions, y_positions, s=sizes, alpha=0.6, color="purple")

    for i, keyword in enumerate(keywords):
        plt.text(x_positions[i], y_positions[i], keyword, ha="center", va="center",
                 fontsize=10, color="black")

    plt.xlim(0, 10)
    plt.ylim(0, 10)

    plt.xticks([])
    plt.yticks([])
    plt.title(f"Top {MAX_KEYWORDS_BUBBLE} Keyword Searches (Bubble Size = Frequency)")
    plt.show()

# Generates a pie chart of search query distribution.
def generate_pie_chart(db: DBConnection):
    data = db.execute_sqlite_select(RawQueries.PIE_CHART_QUERY)

    if not data:
        print("No data available for visualization.")
        return

    labels = [row[0] for row in data]
    sizes = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes, labels=labels, autopct="%1.1f%%", startangle=140,
        colors=["#800080", "#9932CC", "#BA55D3", "#DA70D6", "#E6E6FA"]
    )
    plt.title("Search Query Distribution")
    plt.show()