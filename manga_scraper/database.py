import sqlite3
import os
database_file = 'data/manga/data.db' 

USER_TABLE = """
CREATE TABLE IF NOT EXISTS user_subscriptions (
    manga_url TEXT,
    uid TEXT,
    provider TEXT,
    PRIMARY KEY (manga_url, uid)
);
"""

MANGA_TABLE = """
        CREATE TABLE IF NOT EXISTS manga (
            url TEXT PRIMARY KEY,
            rule TEXT,
            title TEXT,
            last_update TEXT,
            update_flag INTEGER DEFAULT 0
)"""


dir = os.path.dirname(database_file)
if not os.path.exists(dir):
    os.makedirs(dir, exist_ok=True)
    
conn = sqlite3.connect(database_file)
conn.execute(MANGA_TABLE)
conn.execute(USER_TABLE)
conn.close()