from typing import List

import typer

from portfolio_track_asr.controllers import portfolio_controller
from portfolio_track_asr.models.portfolio import Portfolio
from portfolio_track_asr.views import table_view, chart_view

app = typer.Typer()

@app.command()
def add_asset(
    ticker: str = typer.Argument(...),
    sector: str = typer.Option(..., "--sector", "-s"),
    asset_class: str = typer.Option(..., "--asset-class", "-a"),
    quantity: float = typer.Option(..., "--quantity", "-q"),
    purchase_price: float = typer.Option(..., "--purchase-price", "-p"),
):
    asset = portfolio_controller.add_asset(ticker, sector, asset_class, quantity, purchase_price)
    typer.echo(f"Added {asset.ticker}: {asset.quantity} shares at ${asset.purchase_price:.1f}")


@app.command()
def prices():
    portfolio = Portfolio.load(portfolio_controller.PORTFOLIO_PATH)
    current_prices = portfolio_controller.get_current_prices([a.ticker for a in portfolio.assets])
    table_view.display_prices(portfolio.assets, current_prices)


@app.command()
def chart(
    tickers: List[str] = typer.Argument(...),
    period: str = typer.Option("1y", "--period", "-p"),
):
    history = portfolio_controller.get_history(tickers, period)
    chart_view.show_chart(history, tickers, period)


@app.command()
def view_portfolio():
    portfolio = Portfolio.load(portfolio_controller.PORTFOLIO_PATH)
    prices = portfolio_controller.get_current_prices([a.ticker for a in portfolio.assets])
    table_view.display_portfolio(portfolio.assets, prices)


if __name__ == "__main__":
    app()