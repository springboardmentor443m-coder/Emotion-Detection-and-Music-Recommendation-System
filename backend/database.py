import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "music.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            artist TEXT,
            mood TEXT,
            genre TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS mood_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_type TEXT NOT NULL,
            emotion TEXT NOT NULL,
            input_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def save_mood_history(input_type, emotion, input_text=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO mood_history (input_type, emotion, input_text)
        VALUES (?, ?, ?)
        """,
        (input_type, emotion, input_text),
    )
    conn.commit()
    conn.close()


def fetch_mood_history(limit=12):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, input_type, emotion, input_text, created_at
        FROM mood_history
        ORDER BY datetime(created_at) DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def clear_mood_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mood_history")
    conn.commit()
    conn.close()
