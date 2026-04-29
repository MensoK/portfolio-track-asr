from typing import List

import typer

from portfolio_track_asr.controllers import portfolio_controller
from portfolio_track_asr.models.portfolio import Portfolio
from portfolio_track_asr.models.simulation import run_simulation
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
def view_portfolio(
    group_by: str = typer.Option(None, "--group-by", "-g", help="Group weights by: sector, asset-class"),
):
    portfolio = Portfolio.load(portfolio_controller.PORTFOLIO_PATH)
    prices = portfolio_controller.get_current_prices([a.ticker for a in portfolio.assets])
    total = portfolio.total_value(prices)

    if group_by == "sector":
        groups = portfolio.weights_by_group(prices, "sector")
        table_view.display_group_weights(groups, "Weights by Sector", total)
    elif group_by == "asset-class":
        groups = portfolio.weights_by_group(prices, "asset_class")
        table_view.display_group_weights(groups, "Weights by Asset Class", total)
    else:
        weights = portfolio.asset_weights(prices)
        table_view.display_portfolio(portfolio.assets, prices, weights, total)


@app.command()
def risk(
    period: str = typer.Option("1y", "--period", "-p"),
    risk_free_rate: float = typer.Option(0.02, "--risk-free-rate", "-r"),
):
    portfolio = Portfolio.load(portfolio_controller.PORTFOLIO_PATH)
    prices = portfolio_controller.get_current_prices([a.ticker for a in portfolio.assets])
    weights = portfolio.asset_weights(prices)
    history = portfolio_controller.get_history([a.ticker for a in portfolio.assets], period=period)
    volatilities = portfolio.asset_volatilities(history)
    sharpe = portfolio.sharpe_ratio(history, weights, risk_free_rate)
    table_view.display_risk_metrics(portfolio.assets, volatilities, sharpe)


@app.command()
def simulate(
    n_years: int = typer.Option(15, "--years", "-y"),
    n_paths: int = typer.Option(100_000, "--paths"),
):
    portfolio = Portfolio.load(portfolio_controller.PORTFOLIO_PATH)
    prices = portfolio_controller.get_current_prices([a.ticker for a in portfolio.assets])
    total = portfolio.total_value(prices)
    weights_dict = portfolio.asset_weights(prices)
    tickers = [a.ticker for a in portfolio.assets if a.ticker in prices]
    weights = [weights_dict[t] / 100 for t in tickers]
    w, mean_returns, cov_matrix = portfolio_controller.get_simulation_params(tickers, weights)
    paths = run_simulation(total, w, mean_returns, cov_matrix, n_paths=n_paths, n_years=n_years)
    chart_view.show_simulation_chart(paths, n_years, total)


if __name__ == "__main__":
    app()