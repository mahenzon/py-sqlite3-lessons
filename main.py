import sqlite3
from collections.abc import Sequence
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILENAME = "cooking.db"
DB_PATH = BASE_DIR / DB_FILENAME


def create_table(
    cur: sqlite3.Cursor,
    *,
    drop: bool = False,
) -> None:
    if drop:
        cur.execute("DROP TABLE recipes")

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT ''
    )
    """,
    )


type PositionalParams = tuple[str, ...]


def insert_data(
    cur: sqlite3.Cursor,
) -> None:
    cur.execute("""
        INSERT INTO recipes (title, description)
        VALUES ('Pasta', 'Cheesy Pasta'),
               ('Brownie', 'Chocolate Brownie')
        """)

    some_title = "Chicken Soup"
    some_description = "Grandma's Chicken Soup with noodles"
    parameters: PositionalParams = (some_title, some_description)
    cur.execute(
        """
        INSERT INTO recipes (title, description)
        VALUES (?, ?)
        """,
        parameters,
    )
    tomato_soup_params: PositionalParams = ("Tomato Soup",)
    cur.execute(
        """
        INSERT INTO recipes (title, description)
        VALUES (?, 'default-description')
        """,
        tomato_soup_params,
    )
    cur.execute(
        """
        INSERT INTO recipes (title)
        VALUES (?)
        """,
        ("Bean Soup",),
    )

    many_params: Sequence[PositionalParams] = [
        ("Burger", "Beef burger"),
        ("Cheeseburger", "Beef + cheese burger"),
        ("Chicken burger", "Classic chicken burger"),
    ]
    cur.executemany(
        """
        INSERT INTO recipes (title, description)
        VALUES (?, ?)
        """,
        many_params,
    )

    cur.connection.commit()


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    create_table(cur, drop=True)
    insert_data(cur)

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
