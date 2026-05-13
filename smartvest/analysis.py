import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from smartvest.recommendation import (
    project_portfolio_growth,
    get_expected_return,
    calculate_volatility_range
)

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not installed. Live market data unavailable.")


def fetch_ticker_data(tickers, period="1y"):
    """
    Fetch historical adjusted closing prices for a list of tickers
    using yfinance.

    Parameters:
        tickers (list): Ticker symbols e.g. ["SPY", "QQQ"]
        period (str)  : Time period e.g. "1y", "3y", "5y"

    Returns:
        pd.DataFrame: Adjusted closing prices or empty DataFrame on failure.
    """
    if not YFINANCE_AVAILABLE:
        print("yfinance not available. Skipping market data fetch.")
        return pd.DataFrame()

    try:
        if not tickers:
            print("No tickers provided.")
            return pd.DataFrame()

        print(f"\nFetching market data for: {', '.join(tickers)} ...")
        data = yf.download(tickers, period=period, auto_adjust=True, progress=False)

        if data.empty:
            print("No data returned from yfinance.")
            return pd.DataFrame()

        if isinstance(data.columns, pd.MultiIndex):
            close_data = data["Close"]
        else:
            close_data = data[["Close"]]
            close_data.columns = tickers

        close_data.dropna(how="all", inplace=True)
        print(f"Successfully fetched data for {len(close_data.columns)} ticker(s).")
        return close_data

    except Exception as error:
        print(f"Error fetching ticker data: {error}")
        return pd.DataFrame()


def calculate_performance_metrics(price_data):
    """
    Calculate performance metrics for each ticker.

    Metrics:
    - Total Return (%)      : (Last - First) / First * 100
    - Annualised Return (%) : Geometric annualised return
    - Volatility (%)        : Annualised standard deviation of daily returns
    - Sharpe Ratio          : (Ann. Return - Risk Free Rate) / Volatility
                              Risk-free rate = 4.5% (approx T-bill rate)
    """
    try:
        if price_data.empty:
            return {}

        metrics = {}
        risk_free_rate = 0.045

        for ticker in price_data.columns:
            series = price_data[ticker].dropna()
            if len(series) < 2:
                continue

            total_return = ((series.iloc[-1] - series.iloc[0]) / series.iloc[0]) * 100
            daily_returns = series.pct_change().dropna()
            trading_days = len(daily_returns)
            years = trading_days / 252
            annualised_return = (
                ((1 + total_return / 100) ** (1 / years) - 1) * 100
                if years > 0 else 0
            )
            volatility = daily_returns.std() * np.sqrt(252) * 100
            sharpe = (
                (annualised_return / 100 - risk_free_rate) / (volatility / 100)
                if volatility > 0 else 0
            )

            metrics[ticker] = {
                "total_return": round(total_return, 2),
                "annualised_return": round(annualised_return, 2),
                "volatility": round(volatility, 2),
                "sharpe_ratio": round(sharpe, 2),
                "latest_price": round(series.iloc[-1], 2)
            }

        return metrics

    except Exception as error:
        print(f"Error calculating performance metrics: {error}")
        return {}


def display_performance_metrics(metrics):
    """
    Display performance metrics in a formatted table.
    """
    try:
        if not metrics:
            print("No performance metrics to display.")
            return

        print("\n" + "=" * 70)
        print("          Live Market Performance (Past 1 Year)")
        print("=" * 70)
        print(f"{'Ticker':<8} {'Price':>8} {'Total Ret':>10} {'Ann. Ret':>10} {'Volatility':>12} {'Sharpe':>8}")
        print("-" * 70)

        for ticker, m in metrics.items():
            ret_sign = "+" if m["total_return"] >= 0 else ""
            ann_sign = "+" if m["annualised_return"] >= 0 else ""
            print(
                f"{ticker:<8} "
                f"${m['latest_price']:>7.2f} "
                f"{ret_sign}{m['total_return']:>8.2f}% "
                f"{ann_sign}{m['annualised_return']:>8.2f}% "
                f"{m['volatility']:>10.2f}% "
                f"{m['sharpe_ratio']:>8.2f}"
            )

        print("-" * 70)
        print("Note: Sharpe Ratio uses ~4.5% risk-free rate.")

    except Exception as error:
        print(f"Error displaying metrics: {error}")


def run_analysis(profile, recommendations, risk_category):
    """
    Run the analysis pipeline:
    1. Fetch live market data
    2. Calculate and display performance metrics
    """
    try:
        tickers = recommendations.get("tickers", [])
        price_data = fetch_ticker_data(tickers, period="1y")

        if not price_data.empty:
            metrics = calculate_performance_metrics(price_data)
            display_performance_metrics(metrics)
        else:
            print("\nSkipping live market analysis (data unavailable).")

    except Exception as error:
        print(f"Error during analysis: {error}")