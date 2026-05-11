from smartvest.profile import collect_user_profile, display_profile
from smartvest.risk import calculate_risk_score, classify_risk, display_risk_result


def main():
    profile = collect_user_profile()
    display_profile(profile)

    risk_score = calculate_risk_score(profile)
    risk_category = classify_risk(risk_score)
    display_risk_result(risk_score, risk_category)


if __name__ == "__main__":
    main()