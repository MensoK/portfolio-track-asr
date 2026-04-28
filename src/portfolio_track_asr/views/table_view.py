import matplotlib.pyplot as plt

from portfolio_track_asr.models.asset import Asset


def display_portfolio(assets: list[Asset], prices: dict[str, float], weights: dict[str, float], total: float) -> None:
    columns = ["Ticker", "Sector", "Asset Class", "Quantity", "Purchase Price", "Transaction Value", "Current Value", "Weight %"]
    values = []

    for asset in assets:
        current = prices.get(asset.ticker)
        if current is None:
            continue
        values.append([
            asset.ticker, asset.sector, asset.asset_class, asset.quantity,
            asset.purchase_price, asset.transaction_value,
            asset.current_value(current), weights.get(asset.ticker, 0),
        ])

    _, ax = plt.subplots()
    ax.axis("off")
    ax.table(cellText=values, colLabels=columns, loc="center")
    plt.show()


def display_group_weights(groups: dict[str, float], title: str, total: float) -> None:
    columns = ["Group", "Weight %"]
    values = [[k, v] for k, v in groups.items()]

    _, ax = plt.subplots()
    ax.axis("off")
    ax.table(cellText=values, colLabels=columns, loc="center")
    plt.show()


def display_prices(assets: list[Asset], prices: dict[str, float]) -> None: #function to display a table with added assets and their components
    columns = ["Ticker", "Quantity", "Purchase Price", "Current Price", "Gain/Loss $", "Gain/Loss %"]
    values = []

    for asset in assets:
        current = prices.get(asset.ticker)
        if current is None:
            continue
        gain = (current - asset.purchase_price) * asset.quantity
        gain_pct = (current - asset.purchase_price) / asset.purchase_price * 100
        values.append([asset.ticker, asset.quantity, asset.purchase_price, current,
                       round(gain, 2), round(gain_pct, 2)])

    _, ax = plt.subplots()
    ax.axis("off")
    ax.table(cellText=values, colLabels=columns, loc="center")
    plt.show()
