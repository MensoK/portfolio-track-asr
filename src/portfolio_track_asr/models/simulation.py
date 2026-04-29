import numpy as np


def run_simulation(
    initial_value: float,
    weights: np.ndarray,
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    n_paths: int = 100_000,
    n_years: int = 15,
    steps_per_year: int = 12,
) -> np.ndarray:
    n_steps = n_years * steps_per_year
    dt = 1 / steps_per_year

    portfolio_mean = weights @ mean_returns
    portfolio_var = float(weights @ cov_matrix @ weights)
    portfolio_vol = np.sqrt(portfolio_var)

    drift = (portfolio_mean - 0.5 * portfolio_var) * dt
    diffusion = portfolio_vol * np.sqrt(dt)

    eps = np.random.standard_normal((n_paths, n_steps))
    log_returns = drift + diffusion * eps

    cum = np.cumsum(log_returns, axis=1)
    values = initial_value * np.exp(np.hstack([np.zeros((n_paths, 1)), cum]))
    return values  
