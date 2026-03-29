import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILENAME = "cooking.db"
DB_PATH = BASE_DIR / DB_FILENAME


def main() -> None:
    # conn = sqlite3.connect("cooking.sqlite3")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    res = cur.execute("SELECT 1;")
    print(res)
    print(res.fetchall())

    res = cur.execute("SELECT 1, 2, 3;")
    print(res)
    print(res.fetchall())

    res = cur.execute("SELECT 7;")
    row = res.fetchone()
    print("row:", row)
    print("row result:", row[0])

    res = cur.execute("SELECT 'hello', 42;")
    row = res.fetchone()
    print("hello result row:", row)
    print("hello result str:", row[0])
    print("hello result int:", row[1])


if __name__ == "__main__":
    main()
