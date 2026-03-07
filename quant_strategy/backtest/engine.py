"""Simple event-driven backtesting engine."""

from __future__ import annotations

import pandas as pd

from quant_strategy.strategy.base import BaseStrategy
from quant_strategy.utils.metrics import (
    annualized_return,
    annualized_volatility,
    max_drawdown,
    sharpe_ratio,
)


class BacktestResult:
    """Container for the output produced by :class:`BacktestEngine`.

    Attributes:
        equity_curve: Cumulative portfolio value (starting from 1.0).
        signals: Raw signals produced by the strategy.
        metrics: Dictionary of summary performance metrics.
    """

    def __init__(
        self,
        equity_curve: pd.Series,
        signals: pd.Series,
    ) -> None:
        self.equity_curve = equity_curve
        self.signals = signals
        self.metrics = self._compute_metrics()

    def _compute_metrics(self) -> dict[str, float]:
        daily_returns = self.equity_curve.pct_change().dropna()
        return {
            "annualized_return": annualized_return(daily_returns),
            "annualized_volatility": annualized_volatility(daily_returns),
            "sharpe_ratio": sharpe_ratio(daily_returns),
            "max_drawdown": max_drawdown(self.equity_curve),
        }

    def __repr__(self) -> str:  # pragma: no cover
        lines = ["BacktestResult:"]
        for k, v in self.metrics.items():
            lines.append(f"  {k}: {v:.4f}")
        return "\n".join(lines)


class BacktestEngine:
    """Runs a strategy against historical price data.

    Args:
        strategy: An instance of :class:`~quant_strategy.strategy.base.BaseStrategy`.
        initial_capital: Starting portfolio value (default 10 000).
    """

    def __init__(
        self,
        strategy: BaseStrategy,
        initial_capital: float = 10_000.0,
    ) -> None:
        self.strategy = strategy
        self.initial_capital = initial_capital

    def run(self, data: pd.DataFrame) -> BacktestResult:
        """Execute the backtest on *data*.

        Args:
            data: DataFrame with at least a ``Close`` column and a
                  DatetimeIndex.

        Returns:
            A :class:`BacktestResult` instance containing the equity curve
            and performance metrics.
        """
        signals = self.strategy.generate_signals(data)
        daily_returns = data["Close"].pct_change().fillna(0)
        strategy_returns = signals.shift(1).fillna(0) * daily_returns
        equity_curve = (1 + strategy_returns).cumprod() * self.initial_capital
        return BacktestResult(equity_curve=equity_curve, signals=signals)
