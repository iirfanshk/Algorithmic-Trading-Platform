import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class Database:

    def __init__(self):

        self.connection = psycopg2.connect(
            os.getenv("DATABASE_URL")
        )

        self.cursor = self.connection.cursor()

        self.create_users_table()

    def create_users_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS users(

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