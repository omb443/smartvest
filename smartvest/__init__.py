"""
SmartVest — Personalized Investment Advisory Package

Modules:
    profile - Investor profiling and financial ratio computation
    risk - Risk scoring and classification engine
    recommendation -Portfolio recommendations and growth projections
    analysis - yFinance data fetching and matplotlib visualisations
    storage - CSV-based profile saving and loading
"""

from smartvest.profile import collect_user_profile, compute_financial_ratios, display_profile
from smartvest.risk import calculate_risk_score, classify_risk, display_risk_result
from smartvest.recommendation import get_recommendations, display_recommendations
from smartvest.analysis import run_analysis
from smartvest.storage import save_profile, load_profiles, display_saved_profiles

__version__ = "1.0.0"
__authors__ = ["Vidhi Babariya", "Om Boghra"]
__course__ = "FE520 - Introduction to Python for Financial Applications"