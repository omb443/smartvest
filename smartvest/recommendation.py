# Portfolio allocations per risk category
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

# Ticker symbols for each risk category
PORTFOLIO_TICKERS = {
    "Conservative": ["TLT", "LQD", "VYM", "SPY"],
    "Moderate": ["SPY", "VEA", "VNQ", "LQD", "VYM"],
    "Aggressive": ["QQQ", "VB", "EEM", "SPY", "XLK"]
}


def get_expected_return(risk_category):
    """
    Return expected annual return rate based on risk category.
    Based on historical long-term averages.
    """
    return_rates = {
        "Conservative": 0.045,
        "Moderate": 0.075,
        "Aggressive": 0.10
    }
    return return_rates.get(risk_category, 0.06)


def project_portfolio_growth(monthly_investment, annual_return_rate, years):
    """
    Project future portfolio value using compound interest formula
    with monthly contributions.

    Formula: FV = P * [((1 + r)^n - 1) / r]
    Where:
        P = monthly investment
        r = monthly return rate (annual rate / 12)
        n = total number of months
    """
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
    """
    Generate basic investment recommendations based on risk category.
    Returns allocation, tickers and projected portfolio value.
    """
    try:
        allocation = PORTFOLIO_ALLOCATIONS.get(risk_category, {})
        tickers = PORTFOLIO_TICKERS.get(risk_category, [])
        expected_return = get_expected_return(risk_category)
        horizon = profile.get("investment_horizon", 10)
        monthly_investment = profile.get("monthly_investment", 0)
        current_savings = profile.get("current_savings", 0)

        projected_value = (
            project_portfolio_growth(monthly_investment, expected_return, horizon)
            + current_savings * ((1 + expected_return) ** horizon)
        )

        return {
            "allocation": allocation,
            "tickers": tickers,
            "expected_return": expected_return,
            "projected_value": round(projected_value, 2),
            "horizon": horizon
        }

    except Exception as error:
        print(f"Error generating recommendations: {error}")
        return {}


def display_recommendations(recommendations, profile, risk_category):
    """
    Display portfolio allocation and basic projected growth.
    """
    try:
        if not recommendations:
            print("No recommendations available.")
            return

        print("\n" + "=" * 50)
        print("      Investment Recommendations")
        print("=" * 50)
        print(f"Risk Profile : {risk_category}")
        print(f"Horizon      : {recommendations['horizon']} years")

        print("\n--- Recommended Portfolio Allocation ---")
        for asset, weight in recommendations.get("allocation", {}).items():
            print(f"  {asset:<35} {weight*100:>5.1f}%")

        print("\n--- Projected Portfolio Growth ---")
        print(f"  Expected Annual Return : ~{recommendations.get('expected_return', 0)*100:.1f}%")
        print(f"  Projected Value        : ${recommendations.get('projected_value', 0):>15,.2f}")

        print("\n" + "=" * 50)
        print("  DISCLAIMER: Educational projections only.")
        print("  Consult a licensed financial advisor before investing.")
        print("=" * 50)

    except Exception as error:
        print(f"Error displaying recommendations: {error}")