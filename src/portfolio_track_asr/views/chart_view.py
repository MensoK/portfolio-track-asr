import pandas as pd
import matplotlib.pyplot as plt


def show_chart(history: pd.DataFrame, tickers: list[str], period: str) -> None:
    for ticker in tickers:
        if ticker in history.columns:
            plt.plot(history.index, history[ticker], label=ticker)

    plt.title(f"Price History ({period})")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.show()
