"""Base class for all trading strategies."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class BaseStrategy(ABC):
    """Abstract base class that every trading strategy must subclass.

    Subclasses must implement :meth:`generate_signals`.

    Attributes:
        name: Human-readable name for the strategy.
    """

    def __init__(self, name: str = "BaseStrategy") -> None:
        self.name = name

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals from market data.

        Args:
            data: DataFrame with at least a ``Close`` column.

        Returns:
            Series of integer signals aligned with *data*'s index:
            ``1`` = long, ``-1`` = short, ``0`` = flat.
        """

    def __repr__(self) -> str:  # pragma: no cover
        return f"{self.__class__.__name__}(name={self.name!r})"


class MovingAverageCrossover(BaseStrategy):
    """Simple moving-average crossover strategy.

    Generates a *long* signal when the short-window MA crosses above
    the long-window MA, and a *short* signal when it crosses below.

    Args:
        short_window: Look-back period for the fast moving average.
        long_window: Look-back period for the slow moving average.
    """

    def __init__(self, short_window: int = 20, long_window: int = 50) -> None:
        if short_window >= long_window:
            raise ValueError("short_window must be less than long_window")
        super().__init__(name="MovingAverageCrossover")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Return +1 / -1 signals based on MA crossover of ``Close`` prices."""
        close = data["Close"]
        short_ma = close.rolling(self.short_window).mean()
        long_ma = close.rolling(self.long_window).mean()
        signals = (short_ma > long_ma).astype(int) * 2 - 1
        signals.iloc[: self.long_window - 1] = 0
        return signals.rename("signal")
