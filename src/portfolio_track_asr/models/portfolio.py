import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from portfolio_track_asr.models.asset import Asset

@dataclass
class Portfolio:
    assets: list[Asset] = field(default_factory=list)

    def add_asset(self, asset: Asset) -> None: #function to add asset to list
        self.asset.append(asset)

    def save_asset(self, path: Path) -> None: #function to convert object Asset to json, helps against memory loss after running program
        data = [{"ticker": a.ticker,
                 "sector": a.sector,
                 "asset_class": a.asset_class,
                 "quantity": a.quantity,
                 "purchase_price": a.purchase_price,
                 "purchase_date": a.purchase_date}
                 for a in self.assets]
        path.write_text(json.dumps(data))

    @classmethod
    def load(cls, path:Path) -> "Portfolio":
        if not path.exists():
            return cls()
        data = json.load(path.read_text())
        assets = [Asset(
                    ticker=item["ticker"],
                    sector=item["sector"],
                    asset_class=item["asset_class"],
                    quantity=item["quantity"],
                    purchase_price=item["purchase_price"],
                    purchase_date=item["purchase_date"]
        ) for item in data]
        return cls(assets=assets)
    
