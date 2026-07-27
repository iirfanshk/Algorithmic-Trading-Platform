import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env", override=True)


class Database:

    def __init__(self):

        database_url = os.getenv("DATABASE_URL")
        print("DATABASE_URL =", database_url)

        if not database_url:
            raise RuntimeError(
                f"DATABASE_URL not found in {BASE_DIR / '.env'}"
            )

        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()

        self.create_users_table()

    def create_users_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            username VARCHAR(255) UNIQUE NOT NULL,

            email VARCHAR(255) UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            last_login TIMESTAMP

        );
        """

        self.cursor.execute(query)
        self.connection.commit()

    def execute(self, query, params=()):

        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query, params=()):

        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):

        self.cursor.close()
        self.connection.close()


db = Database()