# analysis.py
# fetches live market data via yfinance and generates three matplotlib charts
# each chart is saved with the investor's name in the filename

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
    # downloads adjusted closing prices for the given tickers
    # yfinance returns a MultiIndex when you pass multiple tickers
    # and a flat DataFrame for a single ticker, so we handle both cases
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
            # single ticker comes back as a flat DataFrame
            close_data = data[["Close"]]
            close_data.columns = tickers

        close_data.dropna(how="all", inplace=True)
        print(f"Successfully fetched data for {len(close_data.columns)} ticker(s).")
        return close_data

    except Exception as error:
        print(f"Error fetching ticker data: {error}")
        return pd.DataFrame()


def calculate_performance_metrics(price_data):
    # calculates four metrics for each ticker:
    # total return, annualised return, volatility, and Sharpe Ratio
    # risk-free rate is set to 4.5% (approximate 3-month T-bill rate)
    # 252 trading days used to annualise daily standard deviation
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
    # prints a formatted table of all ticker metrics
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


def plot_portfolio_allocation(allocation, risk_category, profile):
    # pie chart showing how the portfolio is split across asset classes
    # legend sits to the right so the labels do not overlap the slices
    # saved with the investor's name so each profile has its own chart
    try:
        labels = list(allocation.keys())
        sizes = [v * 100 for v in allocation.values()]
        colors = plt.cm.Set3.colors[:len(labels)]

        fig, ax = plt.subplots(figsize=(9, 6))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=None, autopct="%1.1f%%", colors=colors,
            startangle=140, pctdistance=0.82,
            wedgeprops=dict(edgecolor="white", linewidth=1.5)
        )
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight("bold")

        ax.legend(
            wedges,
            [f"{l} ({s:.1f}%)" for l, s in zip(labels, sizes)],
            title="Asset Classes", loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9
        )
        ax.set_title(
            f"Recommended Portfolio Allocation\n"
            f"{risk_category} Profile | Goal: {profile.get('goal', '').title()} | "
            f"Horizon: {profile.get('investment_horizon', 0)} years",
            fontsize=12, fontweight="bold", pad=15
        )
        plt.tight_layout()
        name = profile.get("name", "investor").replace(" ", "_")
        filename = f"{name}_portfolio_allocation.png"
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.show()
        print(f"\nChart saved as '{filename}'")

    except Exception as error:
        print(f"Error generating allocation chart: {error}")


def plot_historical_performance(price_data, risk_category, profile):
    # normalises all tickers to 100 at the start date
    # so you can compare performance regardless of price differences
    # e.g. SPY at $500 and TLT at $90 become directly comparable
    try:
        if price_data.empty:
            print("No price data for historical chart.")
            return

        normalised = (price_data / price_data.iloc[0]) * 100
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.tab10.colors

        for i, ticker in enumerate(normalised.columns):
            ax.plot(
                normalised.index, normalised[ticker],
                label=ticker, color=colors[i % len(colors)], linewidth=2
            )

        # dashed line at 100 shows the starting point for reference
        ax.axhline(y=100, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
        ax.set_title(
            f"Historical Performance - {risk_category} Portfolio\n(Normalised to 100 at Start)",
            fontsize=13, fontweight="bold"
        )
        ax.set_xlabel("Date", fontsize=11)
        ax.set_ylabel("Normalised Price (Base = 100)", fontsize=11)
        ax.legend(loc="upper left", fontsize=9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        name = profile.get("name", "investor").replace(" ", "_")
        filename = f"{name}_historical_performance.png"
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.show()
        print(f"Chart saved as '{filename}'")

    except Exception as error:
        print(f"Error generating historical chart: {error}")


def plot_projected_growth(profile, recommendations):
    # plots three lines: base case, best case, and worst case
    # best and worst are +/- one standard deviation from the expected return
    # the shaded area between them shows the realistic range of outcomes
    try:
        horizon = profile.get("investment_horizon", 10)
        monthly = profile.get("monthly_investment", 0)
        savings = profile.get("current_savings", 0)
        risk_category = recommendations.get("risk_category", "Moderate")

        expected_return = get_expected_return(risk_category)
        best_case, worst_case = calculate_volatility_range(expected_return, risk_category)

        years = list(range(0, horizon + 1))
        base_values, best_values, worst_values = [], [], []

        for y in years:
            base = project_portfolio_growth(monthly, expected_return, y) + savings * ((1 + expected_return) ** y)
            best = project_portfolio_growth(monthly, best_case, y) + savings * ((1 + best_case) ** y)
            worst = project_portfolio_growth(monthly, worst_case, y) + savings * ((1 + worst_case) ** y)
            base_values.append(base)
            best_values.append(best)
            worst_values.append(worst)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(years, base_values, color="#2196F3", linewidth=2.5, label="Base Case", zorder=3)
        ax.plot(years, best_values, color="#4CAF50", linewidth=1.5, linestyle="--", label="Best Case (+1s)", zorder=2)
        ax.plot(years, worst_values, color="#F44336", linewidth=1.5, linestyle="--", label="Worst Case (-1s)", zorder=2)
        ax.fill_between(years, worst_values, best_values, alpha=0.12, color="#2196F3", label="Projection Range")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        ax.set_title(
            f"Projected Portfolio Growth Over {horizon} Years\n"
            f"Monthly Investment: ${monthly:,.0f}   |   Starting Savings: ${savings:,.0f}",
            fontsize=13, fontweight="bold"
        )
        ax.set_xlabel("Years", fontsize=11)
        ax.set_ylabel("Portfolio Value (USD)", fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        name = profile.get("name", "investor").replace(" ", "_")
        filename = f"{name}_projected_growth.png"
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        plt.show()
        print(f"Chart saved as '{filename}'")

    except Exception as error:
        print(f"Error generating projected growth chart: {error}")


def run_analysis(profile, recommendations, risk_category):
    # entry point called from main.py
    # fetches data, prints the metrics table, then draws all three charts
    try:
        tickers = recommendations.get("tickers", [])
        allocation = recommendations.get("allocation", {})
        recommendations["risk_category"] = risk_category

        price_data = fetch_ticker_data(tickers, period="1y")
        if not price_data.empty:
            metrics = calculate_performance_metrics(price_data)
            display_performance_metrics(metrics)
        else:
            print("\nSkipping live market analysis (data unavailable).")

        print("\nGenerating charts...")
        plot_portfolio_allocation(allocation, risk_category, profile)
        if not price_data.empty:
            plot_historical_performance(price_data, risk_category, profile)
        plot_projected_growth(profile, recommendations)

    except Exception as error:
        print(f"Error during analysis: {error}")