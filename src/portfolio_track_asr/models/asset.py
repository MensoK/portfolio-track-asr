from dataclasses import dataclass, field
from datetime import date

@dataclass
class Asset:
    ticker: str
    sector: str
    asset_class: str
    quantity: float
    purchase_price: float
    purchase_date: date = field(default_factory=date.today)
    
    @property
    def transaction_value(self) -> float:
        return self.quantity * self.purchase_price

    def current_value(self, current_price: float) -> float:
        return self.quantity * current_price



