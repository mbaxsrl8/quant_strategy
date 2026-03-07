"""Tests for quant_strategy.backtest.engine."""

import numpy as np
import pandas as pd
import pytest

from quant_strategy.backtest.engine import BacktestEngine, BacktestResult
from quant_strategy.strategy.base import MovingAverageCrossover


def make_price_data(n: int = 300, seed: int = 1) -> pd.DataFrame:
    """Create a synthetic Close-price DataFrame with n rows."""
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    return pd.DataFrame({"Close": close}, index=dates)


@pytest.fixture
def engine():
    strategy = MovingAverageCrossover(short_window=10, long_window=30)
    return BacktestEngine(strategy=strategy, initial_capital=10_000.0)


@pytest.fixture
def result(engine):
    data = make_price_data()
    return engine.run(data)


class TestBacktestEngine:
    def test_run_returns_backtest_result(self, result):
        assert isinstance(result, BacktestResult)

    def test_equity_curve_starts_at_initial_capital(self, engine):
        data = make_price_data()
        result = engine.run(data)
        # First value equals initial capital because the first signal is shifted
        assert result.equity_curve.iloc[0] == pytest.approx(10_000.0, rel=1e-6)

    def test_equity_curve_length_matches_data(self, engine):
        data = make_price_data(300)
        result = engine.run(data)
        assert len(result.equity_curve) == len(data)

    def test_signals_length_matches_data(self, engine):
        data = make_price_data(300)
        result = engine.run(data)
        assert len(result.signals) == len(data)


class TestBacktestResult:
    def test_metrics_keys_present(self, result):
        expected_keys = {
            "annualized_return",
            "annualized_volatility",
            "sharpe_ratio",
            "max_drawdown",
        }
        assert expected_keys == set(result.metrics.keys())

    def test_max_drawdown_non_positive(self, result):
        assert result.metrics["max_drawdown"] <= 0

    def test_annualized_volatility_non_negative(self, result):
        assert result.metrics["annualized_volatility"] >= 0
