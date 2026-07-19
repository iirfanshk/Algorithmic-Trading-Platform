from config.settings import TRANSACTION_COST


class ExecutionEngine:
    """
    Handles trade execution only.

    Responsibilities
    ----------------
    - Calculate shares to buy
    - Calculate commission
    - Calculate cash received after selling

    NOTE:
    PortfolioState is responsible for updating cash
    and holdings.
    """

    def __init__(self):

        self.transaction_cost = TRANSACTION_COST

    # -------------------------------------------------
    # BUY
    # -------------------------------------------------

    def buy(self, investment, price):

        if investment <= 0:

            return {

                "success": False,
                "shares": 0,
                "commission": 0,
                "investment": 0

            }

        commission = investment * self.transaction_cost

        investment_after_fee = investment - commission

        shares = investment_after_fee / price

        return {

            "success": True,

            "shares": shares,

            "commission": commission,

            "investment": investment_after_fee

        }

    # -------------------------------------------------
    # SELL
    # -------------------------------------------------

    def sell(self, shares, price):

        if shares <= 0:

            return {

                "success": False,

                "cash_received": 0,

                "commission": 0

            }

        gross = shares * price

        commission = gross * self.transaction_cost

        cash_received = gross - commission

        return {

            "success": True,

            "cash_received": cash_received,

            "commission": commission

        }