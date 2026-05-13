from datetime import datetime


def get_valid_int(prompt, min_value=None, max_value=None):
    """
    Ask the user for an integer input and validate it.
    """
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
    """
    Ask the user for a decimal number input and validate it.
    """
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
    """
    Ask the user to choose one option from a list.
    """
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
    """
    Collect investor information including employment status
    and expanded investment goals.
    """
    print("\nWelcome to SmartVest Investor Profile Setup")
    print("------------------------------------------")

    name = input("Enter your name: ").strip()
    age = get_valid_int("Enter your age: ", min_value=18, max_value=100)

    # Employment status added in V2
    employment_status = get_valid_choice(
        "Enter your employment status (employed / self-employed / student / retired): ",
        ["employed", "self-employed", "student", "retired"]
    )

    annual_income = get_valid_float("Enter your annual income: $", min_value=0)
    current_savings = get_valid_float("Enter your current savings: $", min_value=0)
    monthly_investment = get_valid_float("Enter how much you can invest monthly: $", min_value=0)
    investment_horizon = get_valid_int(
        "Enter your investment time horizon in years: ", min_value=1, max_value=50
    )

    # Expanded to 7 goals in V2
    goal = get_valid_choice(
        "Choose your main investment goal\n"
        "(retirement / home / education / wealth / emergency / travel / business): ",
        ["retirement", "home", "education", "wealth", "emergency", "travel", "business"]
    )

    risk_comfort = get_valid_int(
        "On a scale of 1 to 5, how comfortable are you with investment risk? ",
        min_value=1, max_value=5
    )

    profile = {
        "name": name,
        "age": age,
        "employment_status": employment_status,
        "annual_income": annual_income,
        "current_savings": current_savings,
        "monthly_investment": monthly_investment,
        "investment_horizon": investment_horizon,
        "goal": goal,
        "risk_comfort": risk_comfort,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return profile


def display_profile(profile):
    """
    Display the user profile in a clean format.
    """
    try:
        print("\nInvestor Profile Summary")
        print("------------------------")
        print(f"Name               : {profile['name']}")
        print(f"Age                : {profile['age']}")
        print(f"Employment Status  : {profile['employment_status'].title()}")
        print(f"Annual Income      : ${profile['annual_income']:,.2f}")
        print(f"Current Savings    : ${profile['current_savings']:,.2f}")
        print(f"Monthly Investment : ${profile['monthly_investment']:,.2f}")
        print(f"Investment Horizon : {profile['investment_horizon']} years")
        print(f"Investment Goal    : {profile['goal'].title()}")
        print(f"Risk Comfort Level : {profile['risk_comfort']} out of 5")
        print(f"Profile Created At : {profile['created_at']}")
    except KeyError as error:
        print("Profile is missing required information.")
        print("Missing key:", error)
    except Exception as error:
        print("An unexpected error occurred while displaying the profile.")
        print("Error:", error)