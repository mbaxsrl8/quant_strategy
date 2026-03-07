"""Tests for quant_strategy.strategy.base."""

import numpy as np
import pandas as pd
import pytest

from quant_strategy.strategy.base import BaseStrategy, MovingAverageCrossover


def make_price_data(n: int = 200, seed: int = 0) -> pd.DataFrame:
    """Create a synthetic OHLCV DataFrame with n rows."""
    rng = np.random.default_rng(seed)
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    dates = pd.date_range("2020-01-01", periods=n, freq="B")
    return pd.DataFrame({"Close": close}, index=dates)


class TestBaseStrategy:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            BaseStrategy()  # type: ignore[abstract]

    def test_subclass_must_implement_generate_signals(self):
        class IncompleteStrategy(BaseStrategy):
            pass

        with pytest.raises(TypeError):
            IncompleteStrategy()  # type: ignore[abstract]


class TestMovingAverageCrossover:
    def test_invalid_windows_raise(self):
        with pytest.raises(ValueError):
            MovingAverageCrossover(short_window=50, long_window=20)

    def test_equal_windows_raise(self):
        with pytest.raises(ValueError):
            MovingAverageCrossover(short_window=20, long_window=20)

    def test_signals_length_matches_data(self):
        data = make_price_data(200)
        strategy = MovingAverageCrossover(short_window=10, long_window=30)
        signals = strategy.generate_signals(data)
        assert len(signals) == len(data)

    def test_signals_contain_only_valid_values(self):
        data = make_price_data(200)
        strategy = MovingAverageCrossover(short_window=10, long_window=30)
        signals = strategy.generate_signals(data)
        assert set(signals.unique()).issubset({-1, 0, 1})

    def test_warmup_period_is_zero(self):
        long_window = 30
        data = make_price_data(200)
        strategy = MovingAverageCrossover(short_window=10, long_window=long_window)
        signals = strategy.generate_signals(data)
        assert (signals.iloc[: long_window - 1] == 0).all()

    def test_default_name(self):
        strategy = MovingAverageCrossover()
        assert strategy.name == "MovingAverageCrossover"
