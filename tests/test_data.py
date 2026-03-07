"""Tests for quant_strategy.data.fetcher."""

import os
import tempfile

import pandas as pd
import pytest

from quant_strategy.data.fetcher import compute_returns, load_csv


@pytest.fixture
def sample_csv(tmp_path):
    """Write a small OHLCV CSV to a temporary file and return its path."""
    data = pd.DataFrame(
        {
            "Date": pd.date_range("2023-01-01", periods=5, freq="B"),
            "Close": [100.0, 101.0, 102.0, 101.5, 103.0],
        }
    )
    filepath = tmp_path / "prices.csv"
    data.to_csv(filepath, index=False)
    return str(filepath)


class TestLoadCsv:
    def test_returns_dataframe(self, sample_csv):
        df = load_csv(sample_csv)
        assert isinstance(df, pd.DataFrame)

    def test_index_is_datetime(self, sample_csv):
        df = load_csv(sample_csv)
        assert isinstance(df.index, pd.DatetimeIndex)

    def test_index_is_sorted(self, sample_csv):
        df = load_csv(sample_csv)
        assert df.index.is_monotonic_increasing

    def test_correct_number_of_rows(self, sample_csv):
        df = load_csv(sample_csv)
        assert len(df) == 5


class TestComputeReturns:
    def test_returns_length(self):
        prices = pd.Series([100.0, 101.0, 102.0, 101.0, 103.0])
        returns = compute_returns(prices)
        assert len(returns) == len(prices) - 1

    def test_correct_first_return(self):
        prices = pd.Series([100.0, 110.0])
        returns = compute_returns(prices)
        assert returns.iloc[0] == pytest.approx(0.1, rel=1e-6)

    def test_period_parameter(self):
        prices = pd.Series([100.0, 105.0, 110.0, 115.0])
        returns = compute_returns(prices, period=2)
        assert len(returns) == len(prices) - 2
