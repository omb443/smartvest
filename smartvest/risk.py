def calculate_risk_score(profile):
    """
    Calculate risk score with loss tolerance added in V3.

    Scoring breakdown:
    - Age factor         : up to 20 points
    - Income factor      : up to 20 points
    - Savings factor     : up to 15 points
    - Monthly investment : up to 10 points
    - Horizon factor     : up to 15 points
    - Risk comfort       : up to 15 points
    - Loss tolerance     : up to 10 points (new in V3)
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

        # Loss tolerance score (max 10) — added in V3
        if loss_tolerance == "buy":
            score += 10
        elif loss_tolerance == "hold":
            score += 5
        elif loss_tolerance == "sell":
            score += 0

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


def display_risk_result(score, category):
    """
    Display the final risk score and category.
    """
    try:
        print("\nRisk Assessment Result")
        print("----------------------")
        print(f"Risk Score    : {score}/100")
        print(f"Risk Category : {category}")

        if category == "Conservative":
            print("Explanation: This profile is better suited for safer investments with lower volatility.")
        elif category == "Moderate":
            print("Explanation: This profile can handle a balance between growth and safety.")
        elif category == "Aggressive":
            print("Explanation: This profile may be comfortable with higher-risk investments for higher growth.")
        else:
            print("Explanation: Risk category could not be calculated.")
    except Exception as error:
        print("An unexpected error occurred while displaying risk results.")
        print("Error:", error)
