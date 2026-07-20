import sqlite3
import yfinance as yf

DB = "portfolio.db"


def connect():
    return sqlite3.connect(DB)


# ==========================================================
# BUY / SELL
# ==========================================================

def execute_trade(asset, trade_type, quantity, price):

    conn = connect()
    cur = conn.cursor()

    quantity = float(quantity)
    price = float(price)

    cur.execute(
        """
        INSERT INTO transactions
        (asset, trade_type, quantity, price)
        VALUES (?, ?, ?, ?)
        """,
        (asset, trade_type, quantity, price)
    )

    cur.execute(
        """
        SELECT quantity, average_price
        FROM portfolio
        WHERE asset=?
        """,
        (asset,)
    )

    row = cur.fetchone()

    if trade_type == "BUY":

        if row:

            old_qty = row[0]
            old_avg = row[1]

            new_qty = old_qty + quantity

            new_avg = (
                (old_qty * old_avg)
                + (quantity * price)
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


# ==========================================================
# LIVE HOLDINGS
# ==========================================================

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

    holdings = []

    for asset, quantity, avg_price in rows:

        try:

            ticker = yf.Ticker(asset)

            try:
                current_price = ticker.fast_info["lastPrice"]
            except Exception:
                history = ticker.history(period="1d")
                current_price = float(history["Close"].iloc[-1])

        except Exception:

            current_price = None

        if current_price is not None:

            market_value = quantity * current_price
            unrealized = (current_price - avg_price) * quantity

            holdings.append({
                "asset": asset,
                "quantity": quantity,
                "average_price": round(avg_price, 2),
                "current_price": round(current_price, 2),
                "market_value": round(market_value, 2),
                "unrealized": round(unrealized, 2)
            })

        else:

            holdings.append({
                "asset": asset,
                "quantity": quantity,
                "average_price": round(avg_price, 2),
                "current_price": "-",
                "market_value": "-",
                "unrealized": "-"
            })

    return holdings


# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================

def get_portfolio_summary(initial_cash=100000):

    holdings = get_holdings()

    invested = 0
    market_value = 0
    unrealized = 0

    for h in holdings:

        invested += h["average_price"] * h["quantity"]

        if isinstance(h["market_value"], (int, float)):
            market_value += h["market_value"]

        if isinstance(h["unrealized"], (int, float)):
            unrealized += h["unrealized"]

    cash_balance = initial_cash - invested

    portfolio_value = cash_balance + market_value

    total_return = portfolio_value - initial_cash

    return {
        "portfolio_value": round(portfolio_value, 2),
        "cash_balance": round(cash_balance, 2),
        "invested": round(invested, 2),
        "market_value": round(market_value, 2),
        "unrealized": round(unrealized, 2),
        "total_return": round(total_return, 2),
        "return_pct": round((total_return / initial_cash) * 100, 2)
    }


# ==========================================================
# TRANSACTIONS
# ==========================================================

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