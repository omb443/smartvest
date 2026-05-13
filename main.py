from smartvest.profile import collect_user_profile, compute_financial_ratios, display_profile
from smartvest.risk import calculate_risk_score, classify_risk, display_risk_result
from smartvest.recommendation import get_recommendations, display_recommendations
from smartvest.analysis import run_analysis


def main():
    """
    SmartVest - Personalized Investment Advisory Application
    
    Pipeline:
    1. Collect investor profile
    2. Compute financial ratios
    3. Calculate risk score and classify
    4. Generate investment recommendations
    5. Run market analysis and visualisations
    """

    # Step 1: Collect profile
    profile = collect_user_profile()
    
    # Step 2: Compute financial ratios
    ratios = compute_financial_ratios(profile)
    
    # Step 3: Display profile with ratios
    display_profile(profile, ratios)

    # Step 4: Risk scoring
    risk_score = calculate_risk_score(profile, ratios)
    risk_category = classify_risk(risk_score)
    display_risk_result(risk_score, risk_category, ratios)

    # Step 5: Recommendations
    recommendations = get_recommendations(risk_category, profile["goal"], profile)
    display_recommendations(recommendations, profile, risk_category)

    # Step 6: Market analysis and charts
    print("\nWould you like to see live market data and visualisation charts?")
    show_charts = input("Enter yes or no: ").strip().lower()

    if show_charts == "yes":
        run_analysis(profile, recommendations, risk_category)
    else:
        print("\nSkipping market analysis. You can run it anytime by restarting the app.")

    print("\nThank you for using SmartVest. Happy investing!")


if __name__ == "__main__":
    main()
