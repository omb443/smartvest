# profile.py
# collects investor information through a questionnaire and computes financial ratios

from datetime import datetime


def get_valid_int(prompt, min_value=None, max_value=None):
    # keeps asking until the user enters a whole number within the allowed range
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value greater than or equal to {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Please enter a value less than or equal to {max_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_valid_float(prompt, min_value=None):
    # same idea as get_valid_int but for decimal values like income and savings
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Please enter a value greater than or equal to {min_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_valid_choice(prompt, choices):
    # loops until the user picks one of the accepted options
    # comparison is case-insensitive so "Employed" and "employed" both work
    choices_lower = [choice.lower() for choice in choices]
    while True:
        try:
            value = input(prompt).strip().lower()
            if value in choices_lower:
                return choices[choices_lower.index(value)]
            print("Invalid choice. Please choose from:", ", ".join(choices))
        except Exception as error:
            print("Something went wrong:", error)


def collect_user_profile():
    # walks the user through the full questionnaire
    # every field is validated before being stored in the profile dictionary
    print("\n" + "=" * 50)
    print("   Welcome to SmartVest - Investor Profile Setup")
    print("=" * 50)

    name = input("Enter your name: ").strip()
    age = get_valid_int("Enter your age: ", min_value=18, max_value=100)

    employment_status = get_valid_choice(
        "Enter your employment status (employed / self-employed / student / retired): ",
        ["employed", "self-employed", "student", "retired"]
    )

    annual_income = get_valid_float(
        "Enter your gross annual income (before tax): $", min_value=0
    )

    # monthly expenses and debt are needed to compute financial ratios
    monthly_expenses = get_valid_float(
        "Enter your total monthly expenses (rent, food, bills, etc.): $", min_value=0
    )
    current_savings = get_valid_float("Enter your current total savings: $", min_value=0)
    monthly_investment = get_valid_float(
        "Enter how much you can invest monthly: $", min_value=0
    )
    existing_debt = get_valid_float(
        "Enter your total existing debt (student loans, credit cards, etc.): $", min_value=0
    )
    dependents = get_valid_int(
        "How many financial dependents do you have? ", min_value=0, max_value=20
    )
    investment_horizon = get_valid_int(
        "Enter your investment time horizon in years: ", min_value=1, max_value=50
    )

    goal = get_valid_choice(
        "Choose your main investment goal\n"
        "(retirement / home / education / wealth / emergency / travel / business): ",
        ["retirement", "home", "education", "wealth", "emergency", "travel", "business"]
    )

    risk_comfort = get_valid_int(
        "On a scale of 1 to 5, how comfortable are you with investment risk? ",
        min_value=1, max_value=5
    )

    # loss tolerance captures how the user behaves when markets drop
    loss_tolerance = get_valid_choice(
        "\nIf your portfolio dropped 20%, what would you do?\n"
        "  sell / hold / buy\n"
        "Your choice: ",
        ["sell", "hold", "buy"]
    )

    profile = {
        "name": name,
        "age": age,
        "employment_status": employment_status,
        "annual_income": annual_income,
        "monthly_expenses": monthly_expenses,
        "current_savings": current_savings,
        "monthly_investment": monthly_investment,
        "existing_debt": existing_debt,
        "dependents": dependents,
        "investment_horizon": investment_horizon,
        "goal": goal,
        "risk_comfort": risk_comfort,
        "loss_tolerance": loss_tolerance,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return profile


def compute_financial_ratios(profile):
    # four ratios that measure financial health
    # savings rate: how much of monthly income goes toward investing
    # debt to income: total debt as a percentage of annual income
    # emergency fund: how many months of expenses are covered by savings
    # investment capacity: monthly investment as a percentage of monthly expenses
    try:
        monthly_income = profile["annual_income"] / 12 if profile["annual_income"] > 0 else 1

        savings_rate = (profile["monthly_investment"] / monthly_income) * 100

        debt_to_income = (
            (profile["existing_debt"] / profile["annual_income"]) * 100
            if profile["annual_income"] > 0 else 0
        )

        six_month_expenses = profile["monthly_expenses"] * 6
        emergency_fund_ratio = (
            profile["current_savings"] / six_month_expenses
            if six_month_expenses > 0 else 0
        )

        investment_capacity = (
            (profile["monthly_investment"] / profile["monthly_expenses"]) * 100
            if profile["monthly_expenses"] > 0 else 0
        )

        return {
            "savings_rate": round(savings_rate, 2),
            "debt_to_income": round(debt_to_income, 2),
            "emergency_fund_ratio": round(emergency_fund_ratio, 2),
            "investment_capacity": round(investment_capacity, 2)
        }

    except ZeroDivisionError:
        print("Warning: Could not compute some ratios due to zero values.")
        return {}
    except KeyError as error:
        print(f"Profile missing field for ratio calculation: {error}")
        return {}
    except Exception as error:
        print(f"Unexpected error during ratio computation: {error}")
        return {}


def display_profile(profile, ratios=None):
    # prints the full profile and optionally the financial ratios if they were computed
    try:
        print("\n" + "=" * 50)
        print("         Investor Profile Summary")
        print("=" * 50)
        print(f"Name                 : {profile['name']}")
        print(f"Age                  : {profile['age']}")
        print(f"Employment Status    : {profile['employment_status'].title()}")
        print(f"Annual Income        : ${profile['annual_income']:,.2f}")
        print(f"Monthly Expenses     : ${profile['monthly_expenses']:,.2f}")
        print(f"Current Savings      : ${profile['current_savings']:,.2f}")
        print(f"Monthly Investment   : ${profile['monthly_investment']:,.2f}")
        print(f"Existing Debt        : ${profile['existing_debt']:,.2f}")
        print(f"Dependents           : {profile['dependents']}")
        print(f"Investment Horizon   : {profile['investment_horizon']} years")
        print(f"Investment Goal      : {profile['goal'].title()}")
        print(f"Risk Comfort Level   : {profile['risk_comfort']} out of 5")
        print(f"Loss Tolerance       : {profile['loss_tolerance'].title()}")
        print(f"Profile Created At   : {profile['created_at']}")

        if ratios:
            print("\n--- Key Financial Ratios ---")
            print(f"Savings Rate             : {ratios.get('savings_rate')}% of monthly income")
            print(f"Debt-to-Income Ratio     : {ratios.get('debt_to_income')}%")
            print(f"Emergency Fund Coverage  : {ratios.get('emergency_fund_ratio')}x (6-month target)")
            print(f"Investment Capacity      : {ratios.get('investment_capacity')}% of monthly expenses")

    except KeyError as error:
        print("Profile is missing required information.")
        print("Missing key:", error)
    except Exception as error:
        print("An unexpected error occurred while displaying the profile.")
        print("Error:", error)