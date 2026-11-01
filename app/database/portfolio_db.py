import os
import sqlite3

DB = "/tmp/portfolio.db" if os.environ.get("VERCEL") else "portfolio.db"


def connect():
    return sqlite3.connect(DB)


def create_tables():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        asset TEXT,

        quantity REAL,

        average_price REAL

    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        asset TEXT,

        trade_type TEXT,

        quantity REAL,

        price REAL,

        trade_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


create_tables()