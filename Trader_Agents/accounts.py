from pydantic import BaseModel
import json
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from market import get_share_price
from database import write_account, read_account, write_log

load_dotenv(override=True)

INITIAL_BALANCE = 10_000.0
SPREAD = 0.002


class Transaction(BaseModel):
    symbol: str
    quantity: int
    price: float
    timestamp: str
    rationale: str

    def total(self) -> float:
        return self.quantity * self.price
    
    def __repr__(self):
        return f"{abs(self.quantity)} shares of {self.symbol} at {self.price} each."


class Account(BaseModel):
    name: str
    balance: float
    strategy: str
    holdings: Dict[str, int]
    transactions: List[Transaction]
    portfolio_value_time_series: List[Tuple[str, float]]

    @classmethod
    def get(cls, name: str) -> "Account":
        fields = read_account(name.lower())
        if not fields:
            fields = {
                "name": name.lower(),
                "balance": INITIAL_BALANCE,
                "strategy": "",
                "holdings": {},
                "transactions": [],
                "portfolio_value_time_series": []
            }
            write_account(name, fields)
        return cls(**fields)
    
    
    def save(self) -> None:
        write_account(self.name.lower(), self.model_dump())

    def reset(self, strategy: str) -> None:
        self.balance = INITIAL_BALANCE
        self.strategy = strategy
        self.holdings = {}
        self.transactions = []
        self.portfolio_value_time_series = []
        self.save()

    def deposit(self, amount: float) -> str:
        """Deposit funds into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()
        write_log(self.name, "account", f"Deposited {amount}")
        return f"Deposited {amount}. Balance: {self.balance}"

    def withdraw(self, amount: float) -> str:
        """Withdraw funds from the account, ensuring it doesn't go negative."""
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.save()
        write_log(self.name, "account", f"Withdrew {amount}")
        return f"Withdrew {amount}. Balance: {self.balance}"

    def buy_shares(self, symbol: str, quantity: int, rationale: str) -> str:
        """Buy shares of a stock if sufficient funds are available."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        price = get_share_price(symbol)
        buy_price = price * (1 + SPREAD)
        total_cost = buy_price * quantity
        
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        elif price==0:
            raise ValueError(f"Unrecognized symbol {symbol}")
        
        # Update holdings
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Record transaction
        transaction = Transaction(symbol=symbol, quantity=quantity, price=buy_price, timestamp=timestamp, rationale=rationale)
        self.transactions.append(transaction)
        
        # Update balance
        self.balance -= total_cost
        self.save()
        write_log(self.name, "account", f"Bought {quantity} of {symbol}")
        return "Completed. Latest details:\n" + self.report()

    def sell_shares(self, symbol: str, quantity: int, rationale: str) -> str:
        """Sell shares of a stock if the user has enough shares."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if self.holdings.get(symbol, 0) < quantity:
            raise ValueError(f"Cannot sell {quantity} shares of {symbol}. Not enough shares held.")
        
        price = get_share_price(symbol)
        sell_price = price * (1 - SPREAD)
        total_proceeds = sell_price * quantity
        
        # Update holdings
        self.holdings[symbol] -= quantity
        
        # If shares are completely sold, remove from holdings
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Record transaction
        transaction = Transaction(symbol=symbol, quantity=-quantity, price=sell_price, timestamp=timestamp, rationale=rationale)  # negative quantity for sell
        self.transactions.append(transaction)

        # Update balance
        self.balance += total_proceeds
        self.save()
        write_log(self.name, "account", f"Sold {quantity} of {symbol}")
        return "Completed. Latest details:\n" + self.report()

    def calculate_portfolio_value(self) -> float:
        """Calculate the total value of the user's portfolio."""
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        """Calculate profit/loss relative to cash injected and current holdings.

        Interprets PnL as current total portfolio value minus net cash invested.
        """
        portfolio_value = self.calculate_portfolio_value()
        cash_flows = 0.0
        for txn in self.transactions:
            # Positive quantity means cash outflow (buy), negative means inflow (sell)
            cash_flows += txn.total()
        # Net invested is cash outflows minus current cash balance increase from deposits/withdrawals.
        # As a simple approximation, we compute PnL as portfolio_value - (initial_balance + net_deposits)
        # Here we approximate net_deposits via balance movements captured in state; since we do not
        # track deposits/withdraws separately historically, we treat cash_flows as net position cost.
        return portfolio_value - (INITIAL_BALANCE + cash_flows)

    def get_holdings(self) -> Dict[str, int]:
        """Report the current holdings of the user."""
        return dict(self.holdings)

    def get_profit_loss(self) -> float:
        """Report the user's profit or loss at any point in time."""
        return self.calculate_profit_loss()

    def list_transactions(self) -> List[Dict[str, float | int | str]]:
        """List all transactions made by the user."""
        return [transaction.model_dump() for transaction in self.transactions]
    
    def report(self) -> str:
        """Return a json string representing the account."""
        portfolio_value = self.calculate_portfolio_value()
        self.portfolio_value_time_series.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), portfolio_value))
        self.save()
        pnl = self.calculate_profit_loss()
        data = self.model_dump()
        data["total_portfolio_value"] = portfolio_value
        data["total_profit_loss"] = pnl
        write_log(self.name, "account", f"Retrieved account details")
        return json.dumps(data)
    
    def get_strategy(self) -> str:
        """Return the strategy of the account."""
        write_log(self.name, "account", f"Retrieved strategy")
        return self.strategy
    
    def change_strategy(self, strategy: str) -> str:
        """Change investment strategy for future decisions."""
        self.strategy = strategy
        self.save()
        write_log(self.name, "account", f"Changed strategy")
        return "Changed strategy"

# Example of usage:
if __name__ == "__main__":
    account = Account("John Doe")
    account.deposit(1000)
    account.buy_shares("AAPL", 5)
    account.sell_shares("AAPL", 2)
    print(f"Current Holdings: {account.get_holdings()}")
    print(f"Total Portfolio Value: {account.calculate_portfolio_value()}")
    print(f"Profit/Loss: {account.get_profit_loss()}")
    print(f"Transactions: {account.list_transactions()}")