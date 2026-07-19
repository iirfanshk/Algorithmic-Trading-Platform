class PositionSizer:
    """
    Calculates how many shares to buy.
    """

    def __init__(self,
                 risk_per_trade=0.02):
        self.risk_per_trade = risk_per_trade

    def calculate_position_size(
        self,
        capital,
        entry_price
    ):
        risk_amount = capital * self.risk_per_trade

        shares = risk_amount / entry_price

        return int(shares)