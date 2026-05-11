from smartvest.profile import collect_user_profile, display_profile


def main():
    profile = collect_user_profile()
    display_profile(profile)


if __name__ == "__main__":
    main()