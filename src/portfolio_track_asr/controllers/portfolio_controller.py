from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf

from portfolio_track_asr.models.asset import Asset
from portfolio_track_asr.models.portfolio import Portfolio

PORTFOLIO_PATH = Path("portfolio.json")

def add_asset( #function to add asset to portfolio 
    ticker: str,
    sector: str,
    asset_class: str,
    quantity: float,
    purchase_price: float,
    purchase_date: date = None,
) -> Asset:
    portfolio = Portfolio.load(PORTFOLIO_PATH)
    asset = Asset(
        ticker=ticker,
        sector=sector,
        asset_class=asset_class,
        quantity=quantity,
        purchase_price=purchase_price,
        purchase_date=purchase_date
    )
    portfolio.add_asset(asset)
    portfolio.save_asset(PORTFOLIO_PATH)
    return asset

def get_current_prices(tickers: list[str]) -> dict[str, float]: #function to get live prices from ticker in porftfolio using yahoofinance
    prices = {}
    for ticker in tickers:
        prices[ticker] = yf.Ticker(ticker).fast_info.last_price
    return prices

def get_history(tickers: list[str]) -> pd.DataFrame: #function to get history of closing prices from yahoo finance over 5year period
    data = yf.download(tickers, period="5y")["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame(name=tickers[0])
    return data

