"""Module for fetching and pre-processing market data."""

from __future__ import annotations

import pandas as pd


def load_csv(filepath: str, date_column: str = "Date") -> pd.DataFrame:
    """Load OHLCV data from a CSV file.

    Args:
        filepath: Path to the CSV file.
        date_column: Name of the column containing dates.

    Returns:
        DataFrame with a DatetimeIndex sorted in ascending order.
    """
    df = pd.read_csv(filepath, parse_dates=[date_column], index_col=date_column)
    df.sort_index(inplace=True)
    return df


def compute_returns(prices: pd.Series, period: int = 1) -> pd.Series:
    """Compute simple percentage returns from a price series.

    Args:
        prices: Series of asset prices.
        period: Look-back period for return calculation.

    Returns:
        Series of percentage returns.
    """
    return prices.pct_change(period).dropna()
