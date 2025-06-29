"""
c25k_utils/start_date.py
Handles dynamic start date (e.g., next Monday).
Stub: To be implemented with start date logic.
"""

from datetime import date, timedelta


def get_dynamic_start_date(option: str = "next_monday") -> date:
    today = date.today()
    if option == "next_monday":
        days_ahead = 0 - today.weekday() + 7
        return today + timedelta(days=days_ahead)
    return today
