def calculate_risk_score(profile):
    """
    Calculate a risk score from 0 to 100 based on the investor profile.

    Higher score means the investor can take more risk.
    Lower score means the investor should stay more conservative.
    """
    try:
        score = 0

        age = profile["age"]
        annual_income = profile["annual_income"]
        current_savings = profile["current_savings"]
        monthly_investment = profile["monthly_investment"]
        investment_horizon = profile["investment_horizon"]
        risk_comfort = profile["risk_comfort"]

        # Age score: younger investors usually have more time to recover from losses
        if age < 30:
            score += 20
        elif age <= 45:
            score += 15
        elif age <= 60:
            score += 10
        else:
            score += 5

        # Income score: higher income can support more investment risk
        if annual_income >= 100000:
            score += 20
        elif annual_income >= 60000:
            score += 15
        elif annual_income >= 30000:
            score += 10
        else:
            score += 5

        # Savings score: more savings can provide a stronger financial base
        if current_savings >= 50000:
            score += 15
        elif current_savings >= 20000:
            score += 10
        elif current_savings >= 5000:
            score += 5
        else:
            score += 2

        # Monthly investment score
        if monthly_investment >= 1000:
            score += 15
        elif monthly_investment >= 500:
            score += 10
        elif monthly_investment >= 100:
            score += 5
        else:
            score += 2

        # Investment horizon score: longer time horizon allows more risk
        if investment_horizon >= 15:
            score += 15
        elif investment_horizon >= 7:
            score += 10
        elif investment_horizon >= 3:
            score += 5
        else:
            score += 2

        # Risk comfort score: user's own comfort level matters a lot
        score += risk_comfort * 3

        # Make sure score does not go above 100
        if score > 100:
            score = 100

        return score

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

        if score <= 30:
            return "Conservative"
        elif score <= 60:
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
        print(f"Risk Score: {score}/100")
        print(f"Risk Category: {category}")

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