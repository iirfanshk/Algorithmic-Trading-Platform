import json
from pathlib import Path
import yfinance as yf
from datetime import datetime
import plotly.express as px
import pandas as pd

PORTFOLIO_FILE = Path("paper_portfolio.json")


def load_portfolio():

    if PORTFOLIO_FILE.exists():

        with open(PORTFOLIO_FILE, "r") as f:

            portfolio = json.load(f)

        # Add history if an old portfolio file doesn't have it
        if "history" not in portfolio:
            portfolio["history"] = []

        return portfolio

    # Create a new portfolio if the file doesn't exist
    return {

        "cash": 100000,

        "positions": [],

        "history": []

    }


def save_portfolio(data):

    with open(PORTFOLIO_FILE, "w") as f:

        json.dump(data, f, indent=4)


def update_portfolio_history():

    portfolio = load_portfolio()

    total_value = portfolio["cash"]

    for position in portfolio["positions"]:

        current_price = get_live_price(position["asset"])

        total_value += current_price * position["quantity"]

    folder = Path("data/backtest")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / "portfolio_history.csv"

    new_row = pd.DataFrame({
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Portfolio_Value": [round(total_value, 2)]
    })

    try:
        history = pd.read_csv(file_path)
        history = pd.concat([history, new_row], ignore_index=True)

    except FileNotFoundError:
        history = new_row

    history.to_csv(file_path, index=False)


def get_live_price(asset):

    data = yf.download(asset, period="1d", progress=False)

    close = data["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    return float(close.iloc[-1])


def buy_asset(asset, quantity):

    portfolio = load_portfolio()

    quantity = int(quantity)

    price = get_live_price(asset)

    cost = price * quantity

    if cost > portfolio["cash"]:

        return {
            "success": False,
            "message": "Insufficient cash."
        }

    portfolio["cash"] -= cost

    # ===========================
    # If asset already exists,
    # increase quantity
    # ===========================

    existing = None

    for position in portfolio["positions"]:
        if position["asset"] == asset:
            existing = position
            break

    if existing:

        total_cost = (
            existing["buy_price"] * existing["quantity"]
            + price * quantity
        )

        existing["quantity"] += quantity

        existing["buy_price"] = round(
            total_cost / existing["quantity"], 2
        )

    else:

        portfolio["positions"].append({

            "asset": asset,

            "quantity": quantity,

            "buy_price": round(price, 2)

        })

    portfolio["history"].append({

        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),

        "asset": asset,

        "action": "BUY",

        "quantity": quantity,

        "price": round(price, 2),

        "total": round(cost, 2)

    })

    save_portfolio(portfolio)
    update_portfolio_history()

    return {

        "success": True,

        "message": f"Bought {quantity} {asset}"

    }


def sell_asset(asset, quantity):

    portfolio = load_portfolio()

    quantity = int(quantity)

    for position in portfolio["positions"]:

        if position["asset"] == asset:

            if quantity > position["quantity"]:
                raise Exception("Not enough shares to sell.")

            current_price = get_live_price(asset)

            proceeds = current_price * quantity

            portfolio["cash"] += proceeds

            # Save trade history
            portfolio["history"].append({

                "date": datetime.now().strftime("%d-%m-%Y %H:%M"),

                "asset": asset,

                "action": "SELL",

                "quantity": quantity,

                "price": round(current_price, 2),

                "total": round(proceeds, 2)

            })

            # Reduce quantity instead of deleting everything
            position["quantity"] -= quantity

            # Remove position only if quantity becomes zero
            if position["quantity"] == 0:
                portfolio["positions"].remove(position)

            save_portfolio(portfolio)
            update_portfolio_history()

            return {
                "success": True,
                "message": f"Sold {quantity} {asset}"
            }

    return {
        "success": False,
        "message": "Asset not found."
    }

def portfolio_summary():

    portfolio = load_portfolio()

    total_value = portfolio["cash"]
    unrealized = 0

    holdings = []

    for position in portfolio["positions"]:

        current_price = get_live_price(position["asset"])

        market_value = current_price * position["quantity"]

        pnl = (
            current_price - position["buy_price"]
        ) * position["quantity"]

        total_value += market_value
        unrealized += pnl

        holdings.append({

            "asset": position["asset"],

            "quantity": position["quantity"],

            "buy_price": round(position["buy_price"],2),

            "current_price": round(current_price,2),

            "market_value": round(market_value,2),

            "unrealized": round(pnl,2)

        })

    total_return = ((total_value - 100000) / 100000) * 100

    return {

        "cash": round(portfolio["cash"],2),

        "portfolio_value": round(total_value,2),

        "unrealized": round(unrealized,2),

        "return_pct": round(total_return,2),

        "positions": len(holdings),

        "holdings": holdings,

        "history": portfolio["history"]

    }

def allocation_chart():

    portfolio = load_portfolio()

    if len(portfolio["positions"]) == 0:
        return None

    labels = []
    values = []

    for position in portfolio["positions"]:

        try:

            asset = position["asset"]

            price = get_live_price(asset)

            value = price * position["quantity"]

            labels.append(asset)
            values.append(value)

        except Exception as e:

            print(f"Error fetching {asset}: {e}")

    if len(labels) == 0:
        return None

    print("Labels:", labels)
    print("Values:", values)

    fig = px.pie(

        names=labels,

        values=values,

        hole=0.45,

        title="Portfolio Allocation"

    )

    fig.update_traces(

        textinfo="label+percent",

        textposition="inside"

    )

    fig.update_layout(

        template="plotly_dark",

        height=450,

        margin=dict(l=20, r=20, t=40, b=20),

        legend_title="Assets"

    )

    return fig.to_html(

        full_html=False,

        include_plotlyjs=False

    )
    
def calculate_win_rate():

    portfolio = load_portfolio()

    history = portfolio["history"]

    buy_prices = {}

    wins = 0
    total = 0

    for trade in history:

        asset = trade["asset"]

        if trade["action"] == "BUY":
            buy_prices[asset] = trade["price"]

        elif trade["action"] == "SELL" and asset in buy_prices:

            buy_price = buy_prices.pop(asset)

            total += 1

            if trade["price"] > buy_price:
                wins += 1

    if total == 0:
        return 0.0

    return round((wins / total) * 100, 2)