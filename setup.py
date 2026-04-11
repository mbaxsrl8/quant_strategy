from setuptools import setup, find_packages

setup(
    name="quant_strategy",
    version="0.1.0",
    description="A backbone project for quantitative trading strategy research",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.13.0",
        "yfinance>=0.2.18",
        "pandas-datareader>=0.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ]
    },
)
