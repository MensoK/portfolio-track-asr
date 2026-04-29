# Portfolio Tracker CLI

A command-line application to track and analyse an investment portfolio. Built with Python, Typer, yfinance, and matplotlib.

## Installation

```bash
poetry install
```

## Commands

### Add an asset

Add a position to your portfolio. The data is saved to `portfolio.json` so it persists between sessions.

```bash
poetry run python main.py add-asset AAPL --sector Technology --asset-class Stock --quantity 10 --purchase-price 150.00
```


| `--sector` | `-s` | Sector the asset belongs to |
| `--asset-class` | `-a` | Asset class (e.g. Stock, ETF, Bond) |
| `--quantity` | `-q` | Number of shares / units held |
| `--purchase-price` | `-p` | Price per share at time of purchase |

---

### View current prices

Shows each asset's current price alongside purchase price and gain/loss.

```bash
poetry run python main.py prices
```

---

### View portfolio

Shows the full portfolio with current values and relative weights. Optionally group by sector or asset class.

```bash
# Full portfolio table with weight per asset
poetry run python main.py view-portfolio

# Weights grouped by sector
poetry run python main.py view-portfolio --group-by sector

# Weights grouped by asset class
poetry run python main.py view-portfolio --group-by asset-class
```

---

### Price history chart

Plot the historical closing price of one or more tickers.

```bash
# Single ticker, default 1-year period
poetry run python main.py chart AAPL

# Multiple tickers with a custom period
poetry run python main.py chart AAPL MSFT TSLA --period 2y
```

Supported period values: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

---

### Risk metrics

Shows annualized volatility per asset and the portfolio-level Sharpe ratio. Volatility is calculated from daily log returns, annualized by multiplying by √252. The Sharpe ratio measures return earned per unit of risk above the risk-free rate: `(annualized_return − risk_free_rate) / annualized_volatility`.

```bash
# Default: 1-year history, 2% risk-free rate
poetry run python main.py risk

# Custom period and risk-free rate
poetry run python main.py risk --period 2y --risk-free-rate 0.03
```


| `--period` | `-p` | Historical period for return/vol estimation (default: `1y`) |
| `--risk-free-rate` | `-r` | Annual risk-free rate as a decimal (default: `0.02`) |

---

### Monte Carlo simulation

Simulates the portfolio value over the next 15 years across 100,000 random paths. Parameters (expected return, volatility, correlations) are estimated from the past 3 years of historical data.

The chart shows percentile bands: the dark band covers 25–75% of outcomes, the outer band covers 5–95%, and the line is the median path.

```bash
# Default: 15 years, 100,000 paths
poetry run python main.py simulate

# Custom duration and number of paths
poetry run python main.py simulate --years 10 --paths 50000
```


| `--years` / `-y` | Number of years to simulate (default: 15) |
| `--paths` | Number of simulated paths (default: 100,000) |
