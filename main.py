import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILENAME = "cooking.db"
DB_PATH = BASE_DIR / DB_FILENAME


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL DEFAULT ''
    )
    """,
    )

    cur.execute("""
        INSERT INTO recipes (title, description)
        VALUES ('Pasta', 'Cheesy Pasta'),
               ('Brownie', 'Chocolate Brownie')
        """)

    conn.commit()

    res = cur.execute("SELECT * FROM recipes")
    for row in res.fetchall():
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
