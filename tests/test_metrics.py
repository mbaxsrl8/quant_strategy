"""Tests for quant_strategy.utils.metrics."""

import numpy as np
import pandas as pd
import pytest

from quant_strategy.utils.metrics import (
    annualized_return,
    annualized_volatility,
    max_drawdown,
    sharpe_ratio,
)

TRADING_DAYS = 252


@pytest.fixture
def flat_returns():
    """Daily returns series that is entirely zero (no volatility)."""
    return pd.Series([0.0] * 100)


@pytest.fixture
def positive_returns():
    """Constant positive daily returns of 0.1 %."""
    return pd.Series([0.001] * TRADING_DAYS)


@pytest.fixture
def mixed_returns():
    """Alternating +1 % / -0.5 % daily returns."""
    rng = np.random.default_rng(42)
    return pd.Series(rng.normal(0.0005, 0.01, TRADING_DAYS))


class TestAnnualizedReturn:
    def test_empty_returns(self):
        assert annualized_return(pd.Series([], dtype=float)) == 0.0

    def test_zero_returns(self, flat_returns):
        result = annualized_return(flat_returns)
        assert result == pytest.approx(0.0, abs=1e-6)

    def test_positive_returns(self, positive_returns):
        result = annualized_return(positive_returns)
        expected = (1 + 0.001) ** TRADING_DAYS - 1
        assert result == pytest.approx(expected, rel=1e-4)


class TestAnnualizedVolatility:
    def test_empty_returns(self):
        assert annualized_volatility(pd.Series([], dtype=float)) == 0.0

    def test_zero_volatility(self, flat_returns):
        assert annualized_volatility(flat_returns) == pytest.approx(0.0, abs=1e-9)

    def test_positive_volatility(self, mixed_returns):
        result = annualized_volatility(mixed_returns)
        assert result > 0


class TestSharpeRatio:
    def test_zero_volatility_returns_zero(self, flat_returns):
        assert sharpe_ratio(flat_returns) == 0.0

    def test_positive_sharpe(self, positive_returns):
        result = sharpe_ratio(positive_returns)
        assert result > 0

    def test_risk_free_rate_reduces_sharpe(self, positive_returns):
        sharpe_no_rf = sharpe_ratio(positive_returns, risk_free_rate=0.0)
        sharpe_with_rf = sharpe_ratio(positive_returns, risk_free_rate=0.05)
        assert sharpe_no_rf > sharpe_with_rf


class TestMaxDrawdown:
    def test_empty_equity_curve(self):
        assert max_drawdown(pd.Series([], dtype=float)) == 0.0

    def test_always_increasing(self):
        equity = pd.Series([1.0, 1.1, 1.2, 1.3, 1.4])
        assert max_drawdown(equity) == pytest.approx(0.0, abs=1e-9)

    def test_known_drawdown(self):
        # Peak at 2.0, trough at 1.0 → drawdown of -50 %
        equity = pd.Series([1.0, 2.0, 1.0, 1.5])
        assert max_drawdown(equity) == pytest.approx(-0.5, rel=1e-4)
