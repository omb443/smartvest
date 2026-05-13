# risk.py
# scores the investor from 0 to 100 and assigns a risk category

def calculate_risk_score(profile):
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

        # younger investors have more time to recover from a bad year
        if age < 30:
            score += 20
        elif age <= 45:
            score += 15
        elif age <= 60:
            score += 10
        else:
            score += 5

        # higher income means losses hurt less relative to total earnings
        if annual_income >= 100000:
            score += 20
        elif annual_income >= 60000:
            score += 15
        elif annual_income >= 30000:
            score += 10
        else:
            score += 5

        # larger savings base provides a cushion if investments drop
        if current_savings >= 50000:
            score += 15
        elif current_savings >= 20000:
            score += 10
        elif current_savings >= 5000:
            score += 5
        else:
            score += 2

        # higher monthly contribution shows financial discipline and capacity
        if monthly_investment >= 1000:
            score += 15
        elif monthly_investment >= 500:
            score += 10
        elif monthly_investment >= 100:
            score += 5
        else:
            score += 2

        # longer horizon means more time for the portfolio to recover from dips
        if investment_horizon >= 15:
            score += 15
        elif investment_horizon >= 7:
            score += 10
        elif investment_horizon >= 3:
            score += 5
        else:
            score += 2

        # risk_comfort is 1 to 5, multiplied by 3 so it contributes up to 15 points
        score += risk_comfort * 3

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
    # thresholds: 0-30 conservative, 31-60 moderate, 61-100 aggressive
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
    # prints the score and a one-line explanation of what the category means
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