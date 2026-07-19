import json
from pathlib import Path
import yfinance as yf
from datetime import datetime
import plotly.express as px
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

    invested = 0

    unrealized = 0

    for position in portfolio["positions"]:

        current_price = get_live_price(position["asset"])

        invested += position["buy_price"] * position["quantity"]

        current_value = current_price * position["quantity"]

        total_value += current_value

        unrealized += current_value - (

            position["buy_price"] * position["quantity"]

        )

    total_return = ((total_value - 100000) / 100000) * 100

    return {

        "cash": round(portfolio["cash"],2),

        "portfolio_value": round(total_value,2),

        "unrealized": round(unrealized,2),

        "return_pct": round(total_return,2),

        "positions": len(portfolio["positions"]),

        "holdings": portfolio["positions"],

        "history": portfolio["history"]

    }
    
def allocation_chart():

    portfolio = load_portfolio()

    if len(portfolio["positions"]) == 0:
        return None

    allocation = {}

    for position in portfolio["positions"]:

        asset = position["asset"]

        price = get_live_price(asset)

        value = price * position["quantity"]

        allocation[asset] = allocation.get(asset, 0) + value

    labels = list(allocation.keys())
    values = list(allocation.values())
    
    print(labels)
    print(values)

    fig = px.pie(

        names=labels,

        values=values,

        hole=0.45,

        title="Portfolio Allocation"

    )

    fig.update_traces(
        textinfo="label+percent"
    )

    fig.update_layout(

        template="plotly_dark",

        margin=dict(l=20, r=20, t=40, b=20),

        legend_title="Assets"

    )

    return fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )