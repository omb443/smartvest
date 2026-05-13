# storage.py
# saves each session to a CSV file and loads past profiles on request

import csv
import os
from datetime import datetime


PROFILES_FILE = "investor_profiles.csv"

# all fields written to the CSV, in the order they appear as column headers
FIELDNAMES = [
    "name", "age", "employment_status", "annual_income", "monthly_expenses",
    "current_savings", "monthly_investment", "existing_debt", "dependents",
    "investment_horizon", "goal", "risk_comfort", "loss_tolerance",
    "risk_score", "risk_category", "projected_value", "created_at"
]


def save_profile(profile, risk_score, risk_category, projected_value):
    # opens the file in append mode so previous sessions are never overwritten
    # writes the header only on the first run when the file does not exist yet
    try:
        file_exists = os.path.isfile(PROFILES_FILE)

        with open(PROFILES_FILE, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                "name": profile.get("name", ""),
                "age": profile.get("age", ""),
                "employment_status": profile.get("employment_status", ""),
                "annual_income": profile.get("annual_income", ""),
                "monthly_expenses": profile.get("monthly_expenses", ""),
                "current_savings": profile.get("current_savings", ""),
                "monthly_investment": profile.get("monthly_investment", ""),
                "existing_debt": profile.get("existing_debt", ""),
                "dependents": profile.get("dependents", ""),
                "investment_horizon": profile.get("investment_horizon", ""),
                "goal": profile.get("goal", ""),
                "risk_comfort": profile.get("risk_comfort", ""),
                "loss_tolerance": profile.get("loss_tolerance", ""),
                "risk_score": risk_score,
                "risk_category": risk_category,
                "projected_value": projected_value,
                "created_at": profile.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            })

        print(f"\nProfile saved to '{PROFILES_FILE}'")

    except PermissionError:
        print(f"Error: Permission denied writing to '{PROFILES_FILE}'.")
    except IOError as error:
        print(f"Error saving profile: {error}")
    except Exception as error:
        print(f"Unexpected error saving profile: {error}")


def load_profiles():
    # reads all rows from the CSV and returns them as a list of dictionaries
    # returns an empty list if the file does not exist yet
    try:
        if not os.path.isfile(PROFILES_FILE):
            print(f"No saved profiles found.")
            return []

        profiles = []
        with open(PROFILES_FILE, mode="r", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                profiles.append(row)

        print(f"Loaded {len(profiles)} saved profile(s).")
        return profiles

    except IOError as error:
        print(f"Error loading profiles: {error}")
        return []
    except Exception as error:
        print(f"Unexpected error loading profiles: {error}")
        return []


def display_saved_profiles():
    # prints a summary table of all past sessions
    # skips any row where projected_value cannot be converted to a float
    try:
        profiles = load_profiles()
        if not profiles:
            print("No profiles to display.")
            return

        print("\n" + "=" * 80)
        print("                 Saved Investor Profiles")
        print("=" * 80)
        print(f"{'Name':<20} {'Age':>4} {'Goal':<12} {'Category':<15} {'Score':>6} {'Projected':>18}")
        print("-" * 80)

        for p in profiles:
            try:
                projected = float(p.get("projected_value", 0))
                print(
                    f"{p.get('name', ''):<20} "
                    f"{p.get('age', ''):>4} "
                    f"{p.get('goal', '').title():<12} "
                    f"{p.get('risk_category', ''):<15} "
                    f"{p.get('risk_score', ''):>6} "
                    f"${projected:>16,.2f}"
                )
            except ValueError:
                continue

        print("=" * 80)

    except Exception as error:
        print(f"Error displaying profiles: {error}")