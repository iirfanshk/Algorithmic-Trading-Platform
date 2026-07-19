from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect
)
import yfinance as yf

from app.auth.login import Login
from app.auth.register import Register

from app.services.dashboard_service import get_dashboard_data
from app.services.market_service import get_market_data
from app.services.models_service import get_model_prediction
from app.services.portfolio_service import (
    execute_trade,
    get_holdings,
    get_transactions
)
from app.services.backtest_service import run_backtest

from app.paper_trading.paper_service import (
    portfolio_summary,
    allocation_chart,
    buy_asset,
    sell_asset
)
from app.services.settings_service import (
    save_settings,
    load_settings
)
from app.alerts.alert_service import check_price_alert
from app.config.assets import ASSETS

app = Flask(
    __name__,
    template_folder="app/frontend",
    static_folder="app/frontend",
    static_url_path=""
)

app.secret_key = "algorithmic_trading_secret_key"

# =====================================================
# Global Settings
# =====================================================

@app.context_processor
def inject_settings():
    return {
        "settings": load_settings()
    }


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    if "user" in session:
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/signup")
def signup():

    return render_template("signup.html")


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    dashboard_data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        **dashboard_data
    )


# =====================================================
# MARKET
# =====================================================

@app.route("/market")
def market():

    if "user" not in session:
        return redirect("/")

    asset_class = request.args.get(
        "asset_class",
        "Stocks"
    )

    if asset_class not in ASSETS:
        asset_class = "Stocks"

    ticker = request.args.get(
        "ticker",
        ASSETS[asset_class][0]
    )

    market_data = get_market_data(
        asset_class,
        ticker
    )

    return render_template(
        "market.html",
        **market_data
    )


# =====================================================
# AI SIGNALS
# =====================================================

@app.route("/models")
def models():

    if "user" not in session:
        return redirect("/")

    asset_class = request.args.get(
        "asset_class",
        "Stocks"
    )

    if asset_class not in ASSETS:
        asset_class = "Stocks"

    asset = request.args.get(
        "asset",
        ASSETS[asset_class][0]
    )

    # Prevent invalid asset selection
    if asset not in ASSETS[asset_class]:
        asset = ASSETS[asset_class][0]

    prediction = get_model_prediction(asset)

    return render_template(
        "ai_signal.html",
        asset_classes=list(ASSETS.keys()),
        selected_asset_class=asset_class,
        assets=ASSETS[asset_class],
        asset=asset,
        **prediction
    )

# =====================================================
# PORTFOLIO
# =====================================================

@app.route("/portfolio")
def portfolio():

    if "user" not in session:
        return redirect("/")

    holdings = get_holdings()

    transactions = get_transactions()

    return render_template(
        "portfolio.html",
        holdings=holdings,
        transactions=transactions
    )


# =====================================================
# BACKTESTING
# =====================================================

@app.route("/backtesting")
def backtesting():

    if "user" not in session:
        return redirect("/")

    return render_template("backtesting.html")

# =====================================================
# SETTINGS PAGE
# =====================================================

@app.route("/settings")
def settings():

    if "user" not in session:
        return redirect("/login")

    settings = load_settings()

    return render_template(
        "settings.html",
        settings=settings
    )


# =====================================================
# SETTINGS
# =====================================================

@app.route("/api/settings", methods=["POST"])
def api_settings():

    if "user" not in session:
        return jsonify(
            success=False,
            message="Unauthorized"
        ), 401

    data = request.get_json()

    save_settings(data)

    return jsonify(
        success=True,
        message="Settings saved successfully."
    )


# =====================================================
# PAPER TRADING
# =====================================================

@app.route("/paper")
def paper():

    if "user" not in session:
        return redirect("/")

    chart = allocation_chart()

    return render_template(

        "paper_trading.html",

        allocation_chart=chart

    )


# =====================================================
# GET PAPER PORTFOLIO
# =====================================================

@app.route("/api/paper", methods=["GET"])
def api_paper():

    return jsonify(portfolio_summary())


# =====================================================
# BUY
# =====================================================

@app.route("/api/paper/buy", methods=["POST"])
def api_buy():

    data = request.get_json()

    return jsonify(

        buy_asset(

            data["asset"],

            int(data["quantity"])

        )

    )


# =====================================================
# SELL
# =====================================================

@app.route("/api/paper/sell", methods=["POST"])
def api_sell():

    data = request.json

    result = sell_asset(
        data["asset"],
        int(data["quantity"])
    )

    return jsonify(result)
    
    
# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =====================================================
# LOGIN API
# =====================================================

@app.route("/api/login", methods=["POST"])
def api_login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    login = Login()

    success, result = login.authenticate(
        username,
        password
    )

    if success:

        session["user"] = result["username"]

        return jsonify(
            success=True,
            user=result
        )

    return jsonify(
        success=False,
        message=result
    )
    
# =====================================================
# ALERTS PAGE
# =====================================================

@app.route("/alerts")
def alerts():

    if "user" not in session:
        return redirect("/")

    asset_class = request.args.get("asset_class", "Stocks")

    if asset_class not in ASSETS:
        asset_class = "Stocks"

    return render_template(

        "alert.html",

        asset_classes=list(ASSETS.keys()),

        selected_asset_class=asset_class,

        assets=ASSETS[asset_class]

    )


# =====================================================
# CHECK ALERT
# =====================================================

@app.route("/api/alerts", methods=["POST"])
def api_alerts():

    if "user" not in session:
        return jsonify(
            success=False,
            message="Unauthorized"
        ), 401

    data = request.get_json()

    result = check_price_alert(

        data["asset"],

        data["target_price"],

        data["condition"]

    )

    result["success"] = True

    return jsonify(result)


# =====================================================
# REGISTER API
# =====================================================

@app.route("/api/register", methods=["POST"])
def api_register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    register = Register()

    success, message = register.create_user(
        username,
        email,
        password
    )

    return jsonify(
        success=success,
        message=message
    )

@app.route("/api/trade", methods=["POST"])
def api_trade():

    try:

        if "user" not in session:
            return jsonify(
                success=False,
                message="Unauthorized"
            ), 401

        data = request.get_json()

        asset = data["asset"]
        trade_type = data["trade_type"]
        quantity = float(data["quantity"])

        ticker = yf.Ticker(asset)
        history = ticker.history(period="1d")

        if history.empty:
            return jsonify(
                success=False,
                message="Unable to fetch live market price."
            )

        price = float(history["Close"].iloc[-1])

        execute_trade(
            asset,
            trade_type,
            quantity,
            price
        )

        return jsonify(
            success=True,
            price=round(price, 2)
        )

    except Exception as e:

        print(e)

        return jsonify(
            success=False,
            message=str(e)
        ), 500
        
# =====================================================
# BACKTEST API
# =====================================================

@app.route("/api/backtest", methods=["POST"])
def api_backtest():

    if "user" not in session:
        return jsonify(success=False, message="Unauthorized"), 401

    data = request.get_json()

    result = run_backtest(
        asset=data["asset"],
        strategy=data["strategy"],
        capital=float(data["capital"]),
        start_date=data["start_date"],
        end_date=data["end_date"]
    )

    return jsonify(result)
    
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )