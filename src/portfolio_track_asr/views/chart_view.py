import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def show_simulation_chart(paths: np.ndarray, n_years: int, initial_value: float) -> None:
    pct = np.percentile(paths, [5, 25, 50, 75, 95], axis=0)
    time_axis = np.linspace(0, n_years, paths.shape[1])

    plt.figure()
    plt.fill_between(time_axis, pct[0], pct[4], alpha=0.15, label="5–95%")
    plt.fill_between(time_axis, pct[1], pct[3], alpha=0.25, label="25–75%")
    plt.plot(time_axis, pct[2], label="Median")
    plt.axhline(initial_value, linestyle="--", color="gray", label="Initial value")
    plt.title(f"Monte Carlo Simulation — {n_years} Years (100,000 paths)")
    plt.xlabel("Years")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.show()


def show_chart(history: pd.DataFrame, tickers: list[str], period: str) -> None:
    for ticker in tickers:
        if ticker in history.columns:
            plt.plot(history.index, history[ticker], label=ticker)

    plt.title(f"Price History ({period})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.show()
