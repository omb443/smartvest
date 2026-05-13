# recommendation.py
# maps risk category and investment goal to portfolio allocations and growth projections

# allocations are fixed weights per risk category
# tickers are used by analysis.py to fetch live market data
PORTFOLIO_ALLOCATIONS = {
    "Conservative": {
        "Government Bonds (TLT)": 0.35,
        "Corporate Bond ETF (LQD)": 0.25,
        "Dividend Stocks (VYM)": 0.20,
        "S&P 500 Index (SPY)": 0.10,
        "Cash / Money Market": 0.10
    },
    "Moderate": {
        "S&P 500 Index (SPY)": 0.35,
        "International ETF (VEA)": 0.15,
        "REIT (VNQ)": 0.15,
        "Corporate Bond ETF (LQD)": 0.20,
        "Dividend Stocks (VYM)": 0.15
    },
    "Aggressive": {
        "Growth ETF (QQQ)": 0.30,
        "Small-Cap ETF (VB)": 0.20,
        "Emerging Markets (EEM)": 0.20,
        "S&P 500 Index (SPY)": 0.20,
        "Sector ETF (XLK - Tech)": 0.10
    }
}

PORTFOLIO_TICKERS = {
    "Conservative": ["TLT", "LQD", "VYM", "SPY"],
    "Moderate": ["SPY", "VEA", "VNQ", "LQD", "VYM"],
    "Aggressive": ["QQQ", "VB", "EEM", "SPY", "XLK"]
}

# one short paragraph of advice per goal, shown at the end of recommendations
GOAL_NOTES = {
    "retirement": (
        "For retirement, consistency and compounding are key. "
        "Maximize tax-advantaged accounts like 401(k) and IRA where possible. "
        "Gradually shift toward conservative allocations as you near retirement."
    ),
    "home": (
        "For a home purchase, prioritize liquidity and capital preservation. "
        "Avoid high-volatility assets if your horizon is under 5 years."
    ),
    "education": (
        "For education funding, align your horizon with when tuition is needed. "
        "Shift to conservative assets 2-3 years before the start date."
    ),
    "wealth": (
        "For wealth building, diversification is essential. "
        "Focus on low-cost index funds and reinvest dividends automatically."
    ),
    "emergency": (
        "For an emergency fund, prioritize capital preservation and liquidity. "
        "High-yield savings or money market funds are most appropriate. "
        "Target 6 months of living expenses kept highly liquid."
    ),
    "travel": (
        "For a travel goal with a shorter horizon, keep most funds in low-risk assets. "
        "Consider short-term bond ETFs to earn some return while keeping funds safe."
    ),
    "business": (
        "For a business funding goal, keep capital in stable liquid instruments. "
        "Only invest in equities with funds you won't need for 5+ years."
    )
}


def get_expected_return(risk_category):
    # based on long-term historical averages for each portfolio type
    # conservative is bond-heavy so lower, aggressive is equity-heavy so higher
    return_rates = {
        "Conservative": 0.045,
        "Moderate": 0.075,
        "Aggressive": 0.10
    }
    return return_rates.get(risk_category, 0.06)


def calculate_volatility_range(expected_return, risk_category):
    # adds and subtracts one standard deviation to get best and worst case returns
    # standard deviations are based on typical portfolio volatility for each risk level
    std_devs = {
        "Conservative": 0.05,
        "Moderate": 0.10,
        "Aggressive": 0.18
    }
    std = std_devs.get(risk_category, 0.10)
    return round(expected_return + std, 4), round(expected_return - std, 4)


def project_portfolio_growth(monthly_investment, annual_return_rate, years):
    # standard compound interest formula with monthly contributions
    # FV = P * [((1 + r)^n - 1) / r]
    # where r is the monthly rate and n is total months
    # current savings are compounded separately in get_recommendations
    try:
        if years <= 0 or monthly_investment < 0:
            return 0

        monthly_rate = annual_return_rate / 12
        n_months = years * 12

        if monthly_rate == 0:
            future_value = monthly_investment * n_months
        else:
            future_value = monthly_investment * (
                ((1 + monthly_rate) ** n_months - 1) / monthly_rate
            )

        return round(future_value, 2)

    except Exception as error:
        print(f"Error projecting portfolio growth: {error}")
        return 0


def get_recommendations(risk_category, goal, profile):
    # pulls together allocation, tickers, goal advice, and all three projection scenarios
    # current savings are compounded as a lump sum on top of the monthly contribution projection
    try:
        allocation = PORTFOLIO_ALLOCATIONS.get(risk_category, {})
        tickers = PORTFOLIO_TICKERS.get(risk_category, [])
        goal_note = GOAL_NOTES.get(
            goal, "Focus on building a diversified portfolio aligned with your goals."
        )
        expected_return = get_expected_return(risk_category)
        best_case, worst_case = calculate_volatility_range(expected_return, risk_category)

        horizon = profile.get("investment_horizon", 10)
        monthly_investment = profile.get("monthly_investment", 0)
        current_savings = profile.get("current_savings", 0)

        projected_value = (
            project_portfolio_growth(monthly_investment, expected_return, horizon)
            + current_savings * ((1 + expected_return) ** horizon)
        )
        best_projected = (
            project_portfolio_growth(monthly_investment, best_case, horizon)
            + current_savings * ((1 + best_case) ** horizon)
        )
        worst_projected = (
            project_portfolio_growth(monthly_investment, worst_case, horizon)
            + current_savings * ((1 + worst_case) ** horizon)
        )

        return {
            "allocation": allocation,
            "tickers": tickers,
            "goal_note": goal_note,
            "expected_return": expected_return,
            "projected_value": round(projected_value, 2),
            "best_projected": round(best_projected, 2),
            "worst_projected": round(worst_projected, 2),
            "horizon": horizon
        }

    except Exception as error:
        print(f"Error generating recommendations: {error}")
        return {}


def display_recommendations(recommendations, profile, risk_category):
    # prints allocation with a simple bar chart, goal advice, projections, and monthly breakdown
    try:
        if not recommendations:
            print("No recommendations available.")
            return

        print("\n" + "=" * 50)
        print("      Investment Recommendations")
        print("=" * 50)
        print(f"Risk Profile : {risk_category}")
        print(f"Goal         : {profile.get('goal', 'N/A').title()}")
        print(f"Horizon      : {recommendations['horizon']} years")

        print("\n--- Recommended Portfolio Allocation ---")
        for asset, weight in recommendations.get("allocation", {}).items():
            bar = "█" * int(weight * 40)
            print(f"  {asset:<35} {weight*100:>5.1f}%  {bar}")

        print("\n--- Goal-Specific Advice ---")
        print(f"  {recommendations.get('goal_note', '')}")

        print("\n--- Projected Portfolio Growth ---")
        expected = recommendations.get("expected_return", 0) * 100
        horizon = recommendations.get("horizon", 0)
        print(f"  Expected Annual Return  : ~{expected:.1f}%")
        print(f"  Projected Value ({horizon}yr)  : ${recommendations.get('projected_value', 0):>15,.2f}  (base case)")
        print(f"  Best Case Estimate      : ${recommendations.get('best_projected', 0):>15,.2f}  (+1 std dev)")
        print(f"  Worst Case Estimate     : ${recommendations.get('worst_projected', 0):>15,.2f}  (-1 std dev)")

        print("\n--- Monthly Investment Breakdown ---")
        monthly = profile.get("monthly_investment", 0)
        for asset, weight in recommendations.get("allocation", {}).items():
            print(f"  {asset:<35} ${monthly * weight:>8,.2f}/month")

        print("\n" + "=" * 50)
        print("  DISCLAIMER: Educational projections only.")
        print("  Consult a licensed financial advisor before investing.")
        print("=" * 50)

    except Exception as error:
        print(f"Error displaying recommendations: {error}")