import sqlite3
from pathlib import Path

_db_path = Path(__file__).resolve().parent / "news.db"
conn = sqlite3.connect(str(_db_path))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS processed_urls(
    url TEXT PRIMARY KEY
)
""")
conn.commit()

def is_processed(url):
    cursor.execute("SELECT 1 FROM processed_urls WHERE url=?", (url,))
    return cursor.fetchone() is not None

def mark_processed(url):
    cursor.execute("INSERT OR IGNORE INTO processed_urls(url) VALUES(?)", (url,))
    conn.commit()
