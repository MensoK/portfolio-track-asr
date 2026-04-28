import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from portfolio_track_asr.models.asset import Asset

@dataclass
class Portfolio:
    assets: list[Asset] = field(default_factory=list)

    def add_asset(self, asset: Asset) -> None: #function to add asset to list
        self.assets.append(asset)

    def save_asset(self, path: Path) -> None: #function to convert object Asset to json, helps against memory loss after running program
        data = [{"ticker": a.ticker,
                 "sector": a.sector,
                 "asset_class": a.asset_class,
                 "quantity": a.quantity,
                 "purchase_price": a.purchase_price,
                 "purchase_date": a.purchase_date}
                 for a in self.assets]
        path.write_text(json.dumps(data))

    def total_value(self, prices: dict[str, float]) -> float:
        return sum(a.current_value(prices[a.ticker]) for a in self.assets if a.ticker in prices)

    def asset_weights(self, prices: dict[str, float]) -> dict[str, float]:
        total = self.total_value(prices)
        if total == 0:
            return {}
        return {
            a.ticker: round(a.current_value(prices[a.ticker]) / total * 100, 2)
            for a in self.assets if a.ticker in prices
        }

    def weights_by_group(self, prices: dict[str, float], group_by: str) -> dict[str, float]:
        total = self.total_value(prices)
        if total == 0:
            return {}
        groups: dict[str, float] = {}
        for asset in self.assets:
            if asset.ticker not in prices:
                continue
            key = getattr(asset, group_by)
            groups[key] = groups.get(key, 0) + asset.current_value(prices[asset.ticker])
        return {k: round(v / total * 100, 2) for k, v in groups.items()}

    @classmethod
    def load(cls, path:Path) -> "Portfolio":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text())
        assets = [Asset(
                    ticker=item["ticker"],
                    sector=item["sector"],
                    asset_class=item["asset_class"],
                    quantity=item["quantity"],
                    purchase_price=item["purchase_price"],
                    purchase_date=item["purchase_date"]
        ) for item in data]
        return cls(assets=assets)
    
