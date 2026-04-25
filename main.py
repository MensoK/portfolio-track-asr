import typer

from portfolio_track_asr.models.asset import Asset
from portfolio_track_asr.controllers import portfolio_controller
from datetime import date

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


if __name__ == "__main__":
    app()