from config.settings import TRANSACTION_COST


class PortfolioState:
    """
    Maintains the current portfolio state.
    """

    def __init__(self, initial_capital):

        self.cash = initial_capital

        self.positions = {}

        self.average_price = {}

    # -------------------------------------------------
    # BUY
    # -------------------------------------------------

    def buy(self, asset, shares, price):

        if shares <= 0:
            return

        cost = shares * price

        commission = cost * TRANSACTION_COST

        total_cost = cost + commission

        self.cash -= total_cost

        if asset in self.positions:

            old_shares = self.positions[asset]
            old_avg = self.average_price[asset]

            new_shares = old_shares + shares

            new_avg = (
                (old_shares * old_avg) +
                (shares * price)
            ) / new_shares

            self.positions[asset] = new_shares
            self.average_price[asset] = new_avg

        else:

            self.positions[asset] = shares
            self.average_price[asset] = price

    # -------------------------------------------------
    # SELL
    # -------------------------------------------------

    def sell(self, asset, price):

        if asset not in self.positions:
            return 0

        shares = self.positions[asset]

        proceeds = shares * price

        commission = proceeds * TRANSACTION_COST

        cash_received = proceeds - commission

        self.cash += cash_received

        del self.positions[asset]
        del self.average_price[asset]

        return cash_received

    # -------------------------------------------------
    # HOLDINGS VALUE
    # -------------------------------------------------

    def holdings_value(self, prices):

        total = 0

        for asset, shares in self.positions.items():

            if asset in prices:

                total += shares * prices[asset]

        return total

    # -------------------------------------------------
    # TOTAL PORTFOLIO VALUE
    # -------------------------------------------------

    def portfolio_value(self, prices):

        return self.cash + self.holdings_value(prices)

    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    def summary(self):

        return {

            "Cash": round(self.cash, 2),

            "Positions": self.positions,

            "Average Prices": self.average_price

        }