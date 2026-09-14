import sqlite3


DATABASE_NAME = "linguaai.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            target_language TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_language(user_id: int, target_language: str):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, target_language)
        VALUES (?, ?)
    """, (user_id, target_language))

    connection.commit()
    connection.close()


def get_language(user_id: int):
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT target_language
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None
