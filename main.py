import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILENAME = "cooking.db"
DB_PATH = BASE_DIR / DB_FILENAME


def create_table(
    cur: sqlite3.Cursor,
) -> None:
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT ''
    )
    """,
    )


def insert_data(
    cur: sqlite3.Cursor,
) -> None:
    cur.execute("""
        INSERT INTO recipes (title, description)
        VALUES ('Pasta', 'Cheesy Pasta'),
               ('Brownie', 'Chocolate Brownie')
        """)

    cur.connection.commit()


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # create_table(cur)
    # insert_data(cur)

    res = cur.execute("SELECT id, title, description FROM recipes")
    for row in res.fetchall():
        # print("--- Recipe ---", row)
        # print("#", row[0])
        # print("Title:", row[1])
        # print("Description:", row[2])
        print("--- Recipe ---")
        print("#", row["id"])
        print("Title:", row["title"])
        print("Description:", row["description"])

    conn.close()


if __name__ == "__main__":
    main()
