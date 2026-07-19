import sqlite3

DB = "portfolio.db"


def connect():
    return sqlite3.connect(DB)


# ===========================
# BUY / SELL
# ===========================

def execute_trade(asset, trade_type, quantity, price):

    conn = connect()
    cur = conn.cursor()

    quantity = float(quantity)
    price = float(price)

    # Save transaction
    cur.execute(
        """
        INSERT INTO transactions
        (asset, trade_type, quantity, price)

        VALUES (?, ?, ?, ?)
        """,
        (asset, trade_type, quantity, price)
    )

    # Existing holding
    cur.execute(
        "SELECT quantity, average_price FROM portfolio WHERE asset=?",
        (asset,)
    )

    row = cur.fetchone()

    if trade_type == "BUY":

        if row:

            old_qty = row[0]
            old_avg = row[1]

            new_qty = old_qty + quantity

            new_avg = (
                (old_qty * old_avg) +
                (quantity * price)
            ) / new_qty

            cur.execute(
                """
                UPDATE portfolio
                SET quantity=?,
                    average_price=?
                WHERE asset=?
                """,
                (new_qty, new_avg, asset)
            )

        else:

            cur.execute(
                """
                INSERT INTO portfolio
                (asset, quantity, average_price)

                VALUES (?, ?, ?)
                """,
                (asset, quantity, price)
            )

    else:

        if row:

            remaining = row[0] - quantity

            if remaining <= 0:

                cur.execute(
                    "DELETE FROM portfolio WHERE asset=?",
                    (asset,)
                )

            else:

                cur.execute(
                    """
                    UPDATE portfolio
                    SET quantity=?
                    WHERE asset=?
                    """,
                    (remaining, asset)
                )

    conn.commit()
    conn.close()


# ===========================
# Holdings
# ===========================

def get_holdings():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        asset,
        quantity,
        average_price

        FROM portfolio
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ===========================
# Transactions
# ===========================

def get_transactions():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT
        trade_date,
        asset,
        trade_type,
        quantity,
        price

        FROM transactions

        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows