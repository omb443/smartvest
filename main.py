# main.py
# entry point for SmartVest, runs the full session from start to finish

from smartvest.profile import collect_user_profile, compute_financial_ratios, display_profile
from smartvest.risk import calculate_risk_score, classify_risk, display_risk_result
from smartvest.recommendation import get_recommendations, display_recommendations
from smartvest.analysis import run_analysis
from smartvest.storage import save_profile, display_saved_profiles


def main():
    print("\n" + "=" * 50)
    print("        Welcome to SmartVest")
    print("   Your Personalized Investment Advisor")
    print("=" * 50)

    # let the user check past sessions before starting a new one
    print("\nWould you like to view previously saved profiles?")
    if input("Enter yes or no: ").strip().lower() == "yes":
        display_saved_profiles()

    profile = collect_user_profile()
    ratios = compute_financial_ratios(profile)
    display_profile(profile, ratios)

    risk_score = calculate_risk_score(profile, ratios)
    risk_category = classify_risk(risk_score)
    display_risk_result(risk_score, risk_category, ratios)

    recommendations = get_recommendations(risk_category, profile["goal"], profile)
    display_recommendations(recommendations, profile, risk_category)

    # save before asking about charts so the session is not lost if the user skips
    save_profile(profile, risk_score, risk_category, recommendations.get("projected_value", 0))

    print("\nWould you like to see live market data and charts?")
    if input("Enter yes or no: ").strip().lower() == "yes":
        run_analysis(profile, recommendations, risk_category)
    else:
        print("\nSkipping market analysis.")

    print("\nThank you for using SmartVest. Happy investing!")
    print("=" * 50)


if __name__ == "__main__":
    main()