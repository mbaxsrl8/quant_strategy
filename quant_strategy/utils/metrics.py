"""Performance metrics for strategy evaluation."""

from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def annualized_return(daily_returns: pd.Series) -> float:
    """Compute the annualized arithmetic return.

    Args:
        daily_returns: Series of daily percentage returns (as decimals).

    Returns:
        Annualized return as a decimal (e.g. 0.12 means 12 %).
    """
    if daily_returns.empty:
        return 0.0
    mean_daily = daily_returns.mean()
    return float((1 + mean_daily) ** TRADING_DAYS_PER_YEAR - 1)


def annualized_volatility(daily_returns: pd.Series) -> float:
    """Compute the annualized volatility (standard deviation).

    Args:
        daily_returns: Series of daily percentage returns (as decimals).

    Returns:
        Annualized volatility as a decimal.
    """
    if daily_returns.empty:
        return 0.0
    return float(daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR))


def sharpe_ratio(
    daily_returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """Compute the annualized Sharpe ratio.

    Args:
        daily_returns: Series of daily percentage returns (as decimals).
        risk_free_rate: Annual risk-free rate (default 0).

    Returns:
        Sharpe ratio.  Returns 0.0 when volatility is zero.
    """
    vol = annualized_volatility(daily_returns)
    if vol == 0.0:
        return 0.0
    excess = annualized_return(daily_returns) - risk_free_rate
    return float(excess / vol)


def max_drawdown(equity_curve: pd.Series) -> float:
    """Compute the maximum drawdown from an equity curve.

    Args:
        equity_curve: Series representing portfolio value over time.

    Returns:
        Maximum drawdown as a negative decimal (e.g. -0.25 means -25 %).
    """
    if equity_curve.empty:
        return 0.0
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    return float(drawdown.min())
