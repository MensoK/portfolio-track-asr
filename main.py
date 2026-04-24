from portfolio_track_asr.models.asset import Asset
from datetime import date

if __name__ == "__main__":
    asset = Asset("MCRSFT", "Tech", "equity", 10, 400, date(2026, 4, 24))
    print(asset)
    print(f"Transaction value: ${asset.transaction_value:,.1f}")