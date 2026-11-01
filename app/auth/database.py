import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env", override=True)


class Database:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def get_connection(self):
        if self.connection is None or getattr(self.connection, "closed", 1) != 0:
            database_url = os.getenv("DATABASE_URL")
            if not database_url:
                raise RuntimeError("DATABASE_URL environment variable is not set.")
            self.connection = psycopg2.connect(database_url)
            self.cursor = self.connection.cursor()
            self.create_users_table()
        return self.connection

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
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception:
            if self.connection:
                self.connection.rollback()
            raise

    def execute(self, query, params=()):
        self.get_connection()
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query, params=()):
        self.get_connection()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.get_connection()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


db = Database()
