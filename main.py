import sqlite3
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict

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


class RecipeInsertParams(TypedDict):
    title: str
    description: str


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

    # dict_params = {
    #     "title": "Pancakes",
    #     "description": "Pancakes with syrup",
    # }
    dict_params = RecipeInsertParams(
        title="Pancakes",
        description="Pancakes with syrup",
    )
    res = cur.execute(
        """
        INSERT INTO recipes (title, description)
        VALUES (:title, :description)
        """,
        dict_params,
    )
    print("inserted", res.rowcount, "row")

    dict_many_params: Sequence[RecipeInsertParams] = [
        RecipeInsertParams(
            title="Fruit salad",
            description="bananas, apples, strawberries",
        ),
        RecipeInsertParams(
            title="Chicken salad",
            description="chicken, iceberg, mayo, cherry tomatoes",
        ),
        {
            "title": "Roastbeef salad",
            "description": "roasted beef, mayo, cherry tomatoes",
        },
    ]

    res = cur.executemany(
        """
        INSERT INTO recipes (title, description)
        VALUES (:title, :description)
        """,
        dict_many_params,
    )
    print("inserted", res.rowcount, "rows")

    cur.connection.commit()


def show_one_recipe(
    cur: sqlite3.Cursor,
    title: str,
) -> None:
    result = cur.execute(
        """
        SELECT title, description 
        FROM recipes
        WHERE title = ?
        LIMIT 1
    """,
        (title,),
    )
    row = result.fetchone()
    if not row:
        return

    print("Title:", row["title"])
    print("Description:", row["description"])


def update_data(
    cur: sqlite3.Cursor,
) -> None:
    title = "Chicken salad"
    show_one_recipe(cur, title)
    res = cur.execute(
        """
    UPDATE recipes
    SET description = :description
    WHERE title = :title
    """,
        {
            "title": title,
            "description": "chicken, iceberg salad, mayo, cherry tomatoes",
        },
    )
    print("updated", res.rowcount, "row(s)")
    show_one_recipe(cur, title)

    print()

    update_params = [
        {
            "title": "%burger%",
            "prefix": "[Burgers]",
        },
        {
            "title": "%soup%",
            "prefix": "[Soups]",
        },
        {
            "title": "%salad%",
            "prefix": "[Salads]",
        },
    ]
    res = cur.executemany(
        """
        UPDATE recipes
        SET description = :prefix || ' ' || description
        WHERE title like :title
        """,
        update_params,
    )

    print("updated", res.rowcount, "row(s)")

    cur.connection.commit()


def delete_data(
    cur: sqlite3.Cursor,
) -> None:
    title = "Pancakes"
    show_one_recipe(cur, title)
    res = cur.execute(
        """
    DELETE FROM recipes
    WHERE title = ?
    """,
        (title,),
    )
    print("deleted", res.rowcount, "row(s)")
    show_one_recipe(cur, title)

    res = cur.execute(
        """
        DELETE FROM recipes
        WHERE title like :title
        """,
        {
            "title": "%salad%",
        },
    )
    print("deleted", res.rowcount, "row(s)")

    cur.connection.commit()


def show_all_recipes(
    cur: sqlite3.Cursor,
) -> None:
    res = cur.execute("SELECT id, title, description FROM recipes")
    for row in res.fetchall():
        print("--- Recipe ---")
        print("#", row["id"])
        print("Title:", row["title"])
        print("Description:", row["description"])


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    create_table(cur, drop=True)
    insert_data(cur)
    update_data(cur)
    delete_data(cur)
    show_all_recipes(cur)
    conn.close()


if __name__ == "__main__":
    main()
