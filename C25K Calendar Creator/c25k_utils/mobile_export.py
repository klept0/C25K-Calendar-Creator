"""
c25k_utils/mobile_export.py
Handles mobile app export (e.g., Strava, Runkeeper) with proper data formatting.
"""

from typing import Any, Dict, List


def export_to_mobile_app(plan_data: Dict[str, Any], app_name: str) -> bool:
    """
    Export plan data to mobile app format.

    Args:
        plan_data: The workout plan data
        app_name: Target mobile app name

    Returns:
        Success status
    """
    app_name_lower = app_name.lower()

    if app_name_lower == "strava":
        return _export_to_strava(plan_data)
    elif app_name_lower == "runkeeper":
        return _export_to_runkeeper(plan_data)
    elif app_name_lower == "garmin":
        return _export_to_garmin(plan_data)
    else:
        return _export_generic_format(plan_data, app_name)


def _export_to_strava(plan_data: Dict[str, Any]) -> bool:
    """Export plan in Strava-compatible format."""
    # Strava uses GPX format for workouts
    # This would typically integrate with Strava API
    try:
        strava_format = {
            "training_plan": {
                "name": "Couch to 5K Training Plan",
                "description": "A progressive 9-week running program",
                "weeks": [],
            }
        }

        current_week = None
        week_data = {"week_number": 1, "workouts": []}

        for session in plan_data.get("sessions", []):
            if session.get("week") != current_week:
                if current_week is not None:
                    strava_format["training_plan"]["weeks"].append(week_data)
                current_week = session.get("week")
                week_data = {"week_number": current_week, "workouts": []}

            workout = {
                "day": session.get("day"),
                "type": "running" if "Run" in session.get("workout", "") else "rest",
                "description": session.get("workout", ""),
                "duration": _extract_duration(session.get("workout", "")),
                "notes": session.get("tip", ""),
            }
            week_data["workouts"].append(workout)

        if week_data["workouts"]:
            strava_format["training_plan"]["weeks"].append(week_data)

        # In a real implementation, this would be sent to Strava API
        return True

    except Exception:
        return False


def _export_to_runkeeper(plan_data: Dict[str, Any]) -> bool:
    """Export plan in RunKeeper-compatible format."""
    try:
        runkeeper_format = {
            "plan_name": "Couch to 5K",
            "plan_type": "running",
            "total_weeks": 9,
            "activities": [],
        }

        for session in plan_data.get("sessions", []):
            activity = {
                "week": session.get("week"),
                "day": session.get("day"),
                "activity_type": "running" if "Run" in session.get("workout", "") else "rest",
                "title": session.get("workout", ""),
                "description": session.get("tip", ""),
                "scheduled_date": session.get("date"),
            }
            runkeeper_format["activities"].append(activity)

        # In a real implementation, this would be sent to RunKeeper API
        return True

    except Exception:
        return False


def _export_to_garmin(plan_data: Dict[str, Any]) -> bool:
    """Export plan in Garmin Connect-compatible format."""
    try:
        garmin_format = {
            "trainingPlan": {
                "planName": "Couch to 5K",
                "planType": "RUNNING",
                "estimatedDurationInWeeks": 9,
                "workouts": [],
            }
        }

        for session in plan_data.get("sessions", []):
            if "Run" in session.get("workout", ""):
                workout = {
                    "workoutName": session.get("workout", ""),
                    "sport": "RUNNING",
                    "scheduledDate": session.get("date"),
                    "steps": _parse_workout_steps(session.get("workout", "")),
                    "notes": session.get("tip", ""),
                }
                garmin_format["trainingPlan"]["workouts"].append(workout)

        # In a real implementation, this would be sent to Garmin Connect API
        return True

    except Exception:
        return False


def _export_generic_format(plan_data: Dict[str, Any], app_name: str) -> bool:
    """Export plan in generic JSON format for other apps."""
    try:
        # Create generic format structure for validation
        _generic_format = {
            "app_target": app_name,
            "plan_name": "Couch to 5K",
            "export_date": plan_data.get("start_date", ""),
            "total_sessions": len(plan_data.get("sessions", [])),
            "sessions": plan_data.get("sessions", []),
        }

        # In a real implementation, this might be saved to a file
        # or sent to a generic API endpoint
        # For now, just validate the structure exists
        return len(_generic_format["sessions"]) > 0

    except Exception:
        return False


def _extract_duration(workout_text: str) -> int:
    """Extract workout duration in minutes from workout description."""
    # Simple extraction - look for minute patterns
    import re

    # Look for patterns like "30 minutes", "20 mins", etc.
    minute_patterns = [r"(\d+)\s*minutes?", r"(\d+)\s*mins?", r"(\d+)\s*min"]

    for pattern in minute_patterns:
        match = re.search(pattern, workout_text, re.IGNORECASE)
        if match:
            return int(match.group(1))

    # Default estimates based on workout type
    if "Walk" in workout_text:
        return 30
    elif "Run" in workout_text:
        return 35
    else:
        return 5  # Rest day


def _parse_workout_steps(workout_text: str) -> List[Dict[str, Any]]:
    """Parse workout text into structured steps for Garmin format."""
    steps = []

    # Simple parsing - split on common delimiters
    parts = workout_text.replace(" then ", " | ").split(" | ")

    for i, part in enumerate(parts):
        step = {
            "stepId": i + 1,
            "stepType": "INTERVAL",
            "description": part.strip(),
            "duration": {"durationType": "TIME", "value": _extract_duration(part)},
            "target": {"targetType": "PACE", "value": "EASY" if "Walk" in part else "MODERATE"},
        }
        steps.append(step)

    return steps
