# quant_strategy

A backbone Python project for quantitative trading strategy research and backtesting.

## Project Structure

```
quant_strategy/
├── quant_strategy/          # Main package
│   ├── data/                # Market data loading & processing
│   │   └── fetcher.py
│   ├── strategy/            # Strategy implementations
│   │   └── base.py          # BaseStrategy ABC + MovingAverageCrossover
│   ├── backtest/            # Backtesting engine
│   │   └── engine.py
│   └── utils/               # Performance metrics
│       └── metrics.py
├── tests/                   # pytest test suite
│   ├── test_data.py
│   ├── test_strategy.py
│   ├── test_backtest.py
│   └── test_metrics.py
├── requirements.txt
├── setup.py
└── pytest.ini
```

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Running Tests

```bash
pytest
```

## Key Components

| Module | Description |
|---|---|
| `quant_strategy.data.fetcher` | Load CSV price data; compute returns |
| `quant_strategy.strategy.base` | `BaseStrategy` ABC; `MovingAverageCrossover` |
| `quant_strategy.backtest.engine` | `BacktestEngine` + `BacktestResult` |
| `quant_strategy.utils.metrics` | Annualized return, volatility, Sharpe ratio, max drawdown |