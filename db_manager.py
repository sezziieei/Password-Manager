import sqlite3

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("vault.db")
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def add_entry(self, website, username, password):
        self.cursor.execute(
            "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
            (website, username, password)
        )
        self.conn.commit()

    def get_all_entries(self):
        self.cursor.execute("SELECT website, username, password FROM passwords")
        return self.cursor.fetchall()