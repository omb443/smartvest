from smartvest.profile import collect_user_profile, display_profile
from smartvest.risk import calculate_risk_score, classify_risk, display_risk_result
from smartvest.recommendation import get_recommendations, display_recommendations
from smartvest.analysis import run_analysis


def main():
    """
    SmartVest - Version 4
    Pipeline: profile → risk → recommendations → live market analysis
    """
    profile = collect_user_profile()
    display_profile(profile)

    risk_score = calculate_risk_score(profile)
    risk_category = classify_risk(risk_score)
    display_risk_result(risk_score, risk_category)

    recommendations = get_recommendations(risk_category, profile["goal"], profile)
    display_recommendations(recommendations, profile, risk_category)

    print("\nWould you like to see live market data for your portfolio?")
    show_analysis = input("Enter yes or no: ").strip().lower()

    if show_analysis == "yes":
        run_analysis(profile, recommendations, risk_category)
    else:
        print("\nSkipping market analysis.")

    print("\nThank you for using SmartVest. Happy investing!")


if __name__ == "__main__":
    main()