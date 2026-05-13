# risk.py
# scores the investor from 0 to 100 and assigns a risk category

def calculate_risk_score(profile, ratios=None):
    # each factor adds points based on how much risk capacity it suggests
    # age, income, savings, monthly investment, horizon, and self-rated comfort
    # score is capped at 100 at the end
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

        # younger investors have more time to recover from a bad year
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

        # higher income means losses hurt less relative to total earnings
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

        # larger savings base provides a cushion if investments drop
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

        # higher monthly contribution shows financial discipline and capacity
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

        # longer horizon means more time for the portfolio to recover from dips
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

        # risk_comfort is 1 to 5, multiplied by 3 so it contributes up to 15 points
        score += risk_comfort * 3

        # buy means willing to invest more during a crash, sell means panic selling
        if loss_tolerance == "buy":
            score += 10
        elif loss_tolerance == "hold":
            score += 5
        elif loss_tolerance == "sell":
            score += 0

        # debt penalty: high debt reduces financial flexibility
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

        # more dependents means less room to take financial risks
        if dependents >= 4:
            score -= 10
        elif dependents == 3:
            score -= 7
        elif dependents == 2:
            score -= 4
        elif dependents == 1:
            score -= 2

        # having 6 months of expenses saved means you can afford to take more risk
        if ratios:
            efr = ratios.get("emergency_fund_ratio", 0)
            if efr >= 1.0:
                score += 5
            elif efr >= 0.5:
                score += 2

        # saving a high percentage of income signals discipline
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
    # thresholds: 0-35 conservative, 36-65 moderate, 66-100 aggressive
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
    # prints the score and a one-line explanation of what the category means
    try:
        print("\n" + "=" * 50)
        print("         Risk Assessment Result")
        print("=" * 50)
        print(f"Risk Score    : {score}/100")
        print(f"Risk Category : {category}")

        if category == "Conservative":
            print("\nExplanation:")
            print("  Your profile indicates a preference for capital preservation.")
            print("  Best suited for lower-risk investments that prioritize stability.")
        elif category == "Moderate":
            print("\nExplanation:")
            print("  Your profile indicates a balanced approach to investing.")
            print("  You can handle a mix of growth-oriented and stable assets.")
        elif category == "Aggressive":
            print("\nExplanation:")
            print("  Your profile indicates a high capacity for investment risk.")
            print("  You are well-positioned to pursue growth-focused investments.")
        else:
            print("  Risk category could not be determined.")

        if ratios:
            print("\n--- Financial Health Indicators ---")
            dti = ratios.get("debt_to_income", 0)
            efr = ratios.get("emergency_fund_ratio", 0)
            sr = ratios.get("savings_rate", 0)

            dti_status = "Good" if dti < 20 else ("Manageable" if dti < 40 else "High - consider reducing debt")
            efr_status = "Good" if efr >= 1.0 else ("Partial" if efr >= 0.5 else "Low - build emergency fund")
            sr_status = "Excellent" if sr >= 20 else ("Good" if sr >= 10 else ("Fair" if sr >= 5 else "Low"))

            print(f"  Debt-to-Income Ratio     : {dti}%  -> {dti_status}")
            print(f"  Emergency Fund Coverage  : {efr}x  -> {efr_status}")
            print(f"  Savings Rate             : {sr}%   -> {sr_status}")

    except Exception as error:
        print("An unexpected error occurred while displaying risk results.")
        print("Error:", error)