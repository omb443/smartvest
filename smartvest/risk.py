def calculate_risk_score(profile, ratios=None):
    """
    Calculate a comprehensive risk score from 0 to 100.

    Scoring breakdown:
    - Age factor           : up to 20 points
    - Income factor        : up to 20 points
    - Savings factor       : up to 15 points
    - Monthly investment   : up to 10 points
    - Investment horizon   : up to 15 points
    - Risk comfort         : up to 15 points
    - Loss tolerance       : up to 10 points
    - Debt penalty         : up to -15 points (new in V5)
    - Dependents penalty   : up to -10 points (new in V5)
    - Emergency fund bonus : up to +5 points  (new in V5)
    - Savings rate bonus   : up to +5 points  (new in V5)
    """
    try:
        score = 0

        age = profile["age"]
        annual_income = profile["annual_income"]
        current_savings = profile["current_savings"]
        monthly_investment = profile["monthly_investment"]
        investment_horizon = profile["investment_horizon"]
        risk_comfort = profile["risk_comfort"]
        loss_tolerance = profile["loss_tolerance"]
        dependents = profile["dependents"]

        # Age score (max 20)
        if age < 30:
            score += 20
        elif age <= 45:
            score += 15
        elif age <= 55:
            score += 10
        elif age <= 65:
            score += 5
        else:
            score += 2

        # Income score (max 20)
        if annual_income >= 150000:
            score += 20
        elif annual_income >= 100000:
            score += 17
        elif annual_income >= 60000:
            score += 13
        elif annual_income >= 30000:
            score += 8
        else:
            score += 4

        # Savings score (max 15)
        if current_savings >= 100000:
            score += 15
        elif current_savings >= 50000:
            score += 12
        elif current_savings >= 20000:
            score += 8
        elif current_savings >= 5000:
            score += 4
        else:
            score += 1

        # Monthly investment score (max 10)
        if monthly_investment >= 2000:
            score += 10
        elif monthly_investment >= 1000:
            score += 8
        elif monthly_investment >= 500:
            score += 5
        elif monthly_investment >= 100:
            score += 3
        else:
            score += 1

        # Horizon score (max 15)
        if investment_horizon >= 20:
            score += 15
        elif investment_horizon >= 15:
            score += 12
        elif investment_horizon >= 10:
            score += 9
        elif investment_horizon >= 5:
            score += 6
        elif investment_horizon >= 3:
            score += 3
        else:
            score += 1

        # Risk comfort score (max 15)
        score += risk_comfort * 3

        # Loss tolerance score (max 10)
        if loss_tolerance == "buy":
            score += 10
        elif loss_tolerance == "hold":
            score += 5
        elif loss_tolerance == "sell":
            score += 0

        # Debt penalty (up to -15) — new in V5
        if ratios:
            dti = ratios.get("debt_to_income", 0)
            if dti >= 50:
                score -= 15
            elif dti >= 35:
                score -= 10
            elif dti >= 20:
                score -= 5
            elif dti >= 10:
                score -= 2

        # Dependents penalty (up to -10) — new in V5
        if dependents >= 4:
            score -= 10
        elif dependents == 3:
            score -= 7
        elif dependents == 2:
            score -= 4
        elif dependents == 1:
            score -= 2

        # Emergency fund bonus (up to +5) — new in V5
        if ratios:
            efr = ratios.get("emergency_fund_ratio", 0)
            if efr >= 1.0:
                score += 5
            elif efr >= 0.5:
                score += 2

        # Savings rate bonus (up to +5) — new in V5
        if ratios:
            sr = ratios.get("savings_rate", 0)
            if sr >= 20:
                score += 5
            elif sr >= 10:
                score += 3
            elif sr >= 5:
                score += 1

        return max(0, min(100, score))

    except KeyError as error:
        print("Profile is missing required information for risk scoring.")
        print("Missing key:", error)
        return None
    except TypeError:
        print("Invalid data type found in profile. Please check your inputs.")
        return None
    except Exception as error:
        print("An unexpected error occurred while calculating risk score.")
        print("Error:", error)
        return None


def classify_risk(score):
    """
    Classify the investor into Conservative, Moderate, or Aggressive.
    """
    try:
        if score is None:
            return "Unknown"
        if score <= 35:
            return "Conservative"
        elif score <= 65:
            return "Moderate"
        else:
            return "Aggressive"
    except Exception as error:
        print("An unexpected error occurred while classifying risk.")
        print("Error:", error)
        return "Unknown"


def display_risk_result(score, category, ratios=None):
    """
    Display the final risk score, category and financial health indicators.
    """
    try:
        print("\n" + "=" * 50)
        print("         Risk Assessment Result")
        print("=" * 50)
        print(f"Risk Score    : {score}/100")
        print(f"Risk Category : {category}")

        if category == "Conservative":
            print("\nProfile Explanation:")
            print("  Your profile indicates a preference for capital preservation.")
            print("  Best suited for lower-risk investments that prioritize stability.")
        elif category == "Moderate":
            print("\nProfile Explanation:")
            print("  Your profile indicates a balanced approach to investing.")
            print("  You can handle a mix of growth-oriented and stable assets.")
        elif category == "Aggressive":
            print("\nProfile Explanation:")
            print("  Your profile indicates a high capacity for investment risk.")
            print("  You are well-positioned to pursue growth-focused investments.")
        else:
            print("  Risk category could not be determined.")

        if ratios:
            print("\n--- Financial Health Indicators ---")
            dti = ratios.get("debt_to_income", 0)
            efr = ratios.get("emergency_fund_ratio", 0)
            sr = ratios.get("savings_rate", 0)

            dti_status = "Good" if dti < 20 else ("Manageable" if dti < 40 else "High — consider reducing debt")
            efr_status = "Good" if efr >= 1.0 else ("Partial" if efr >= 0.5 else "Low — build emergency fund")
            sr_status = "Excellent" if sr >= 20 else ("Good" if sr >= 10 else ("Fair" if sr >= 5 else "Low"))

            print(f"  Debt-to-Income Ratio     : {dti}%  → {dti_status}")
            print(f"  Emergency Fund Coverage  : {efr}x  → {efr_status}")
            print(f"  Savings Rate             : {sr}%   → {sr_status}")

    except Exception as error:
        print("An unexpected error occurred while displaying risk results.")
        print("Error:", error)
