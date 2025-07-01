import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime

from modules.core import get_workout_plan


# --- Helpers ---
def _has_rest_day(plan, day):
    return any(s["workout"] == "Rest Day" and s["day"] == day for s in plan)


def _no_workouts_on_rest_days(plan, rest_days):
    for s in plan:
        if s["duration"] > 0 and isinstance(s["day"], str):
            assert s["day"] not in rest_days, f"Workout scheduled on rest day: {s['day']}"


def _all_workouts_have_fields(plan):
    for s in plan:
        if s["duration"] > 0:
            for field in ["week", "day", "day_offset", "duration", "description", "workout", "tip"]:
                assert field in s
            assert s["duration"] > 0


def _plan_sorted(plan):
    weeks_and_offsets = [(s["week"], s["day_offset"]) for s in plan]
    assert weeks_and_offsets == sorted(weeks_and_offsets)


def test_get_workout_plan_basic():
    # Basic plan with rest days
    user = {
        "name": "Test User",
        "age": 30,
        "weight": 70,
        "weight_unit": "m",
        "gender": "other",
        "unit": "m",
        "weeks": 2,
        "days_per_week": 3,
        "start_day": datetime(2025, 7, 1),
        "hour": 7,
        "minute": 0,
        "lang": "e",
        "export": "i",
        "goal": "",
        "high_contrast": False,
        "large_font": False,
        "dyslexia_font": False,
        "email": "",
        "location": "",
        "alert_minutes": 30,
        "rest_days": ["Sat", "Sun"],
        "anonymize": False,
    }
    plan = get_workout_plan(user)
    assert isinstance(plan, list)
    assert len(plan) > 0
    assert all("week" in s for s in plan)
    assert all("day_offset" in s for s in plan)
    # Rest days must be present and have duration 0
    rest_days = user["rest_days"]
    rest_entries = [s for s in plan if s["duration"] == 0]
    assert rest_entries, "No rest days found in plan"
    for entry in rest_entries:
        assert entry["workout"] == "Rest Day"
        assert any(
            day in entry["day"] for day in rest_days
        ), f"Rest day label mismatch: {entry['day']}"
    _no_workouts_on_rest_days(plan, rest_days)
    _all_workouts_have_fields(plan)
    _plan_sorted(plan)


def test_get_workout_plan_varied_rest_days():
    base_user = {
        "name": "Test User",
        "age": 30,
        "weight": 70,
        "weight_unit": "m",
        "gender": "other",
        "unit": "m",
        "weeks": 1,
        "days_per_week": 2,
        "start_day": datetime(2025, 7, 1),
        "hour": 7,
        "minute": 0,
        "lang": "e",
        "export": "i",
        "goal": "",
        "high_contrast": False,
        "large_font": False,
        "dyslexia_font": False,
        "email": "",
        "location": "",
        "alert_minutes": 30,
        "anonymize": False,
    }
    # Only Sunday as rest day
    user1 = dict(base_user)
    user1["rest_days"] = ["Sun"]
    plan1 = get_workout_plan(user1)
    assert any(s["workout"] == "Rest Day" and s["day"] == "Sun" for s in plan1)
    # No rest days
    user2 = dict(base_user)
    user2["rest_days"] = []
    plan2 = get_workout_plan(user2)
    assert not any(s["workout"] == "Rest Day" for s in plan2)
    # All days as rest days
    user3 = dict(base_user)
    user3["rest_days"] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    plan3 = get_workout_plan(user3)
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        assert any(s["workout"] == "Rest Day" and s["day"] == day for s in plan3)


def test_get_workout_plan_edge_cases():
    # 1 week, 1 day per week
    user = {
        "name": "Edge",
        "age": 25,
        "weight": 60,
        "weight_unit": "m",
        "gender": "f",
        "unit": "m",
        "weeks": 1,
        "days_per_week": 1,
        "start_day": datetime(2025, 7, 1),
        "hour": 6,
        "minute": 30,
        "lang": "e",
        "export": "i",
        "goal": "",
        "high_contrast": False,
        "large_font": False,
        "dyslexia_font": False,
        "email": "",
        "location": "",
        "alert_minutes": 15,
        "rest_days": ["Sun"],
        "anonymize": False,
    }
    plan = get_workout_plan(user)
    # Should have 1 workout and 1 rest day
    assert sum(1 for s in plan if s["duration"] > 0) == 1
    assert sum(1 for s in plan if s["duration"] == 0) == 1
