from dataclasses import dataclass
from datetime import date

@dataclass

class Asset:
    ticker: str
    sector: str
    asset_class: str
    quantity: float
    purchase_price: float
    purchase_date: date = date.today
    
    @property
    def transaction_value(self) -> float:
        return self.quantity * self.purchase_price



