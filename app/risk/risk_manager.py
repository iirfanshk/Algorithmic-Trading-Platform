class RiskManager:
    """
    Handles Stop Loss and Take Profit.
    """

    def __init__(self,
                 stop_loss=0.05,
                 take_profit=0.10):
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def should_exit(self,
                    entry_price,
                    current_price):
        """
        Returns:
            "STOP_LOSS"
            "TAKE_PROFIT"
            None
        """

        if current_price <= entry_price * (1 - self.stop_loss):
            return "STOP_LOSS"

        if current_price >= entry_price * (1 + self.take_profit):
            return "TAKE_PROFIT"

        return None