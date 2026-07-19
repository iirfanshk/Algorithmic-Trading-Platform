import sqlite3
from pathlib import Path

# Database Location
DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "users.db"


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_users_table()

    # ------------------------------------------
    # Create Users Table
    # ------------------------------------------

    def create_users_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            last_login TIMESTAMP

        );
        """

        self.cursor.execute(query)

        self.connection.commit()

    # ------------------------------------------
    # Execute Query
    # ------------------------------------------

    def execute(self, query, params=()):

        self.cursor.execute(query, params)

        self.connection.commit()

    # ------------------------------------------
    # Fetch One
    # ------------------------------------------

    def fetch_one(self, query, params=()):

        self.cursor.execute(query, params)

        return self.cursor.fetchone()

    # ------------------------------------------
    # Fetch All
    # ------------------------------------------

    def fetch_all(self, query, params=()):

        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    # ------------------------------------------
    # Close Connection
    # ------------------------------------------

    def close(self):

        self.connection.close()


db = Database()