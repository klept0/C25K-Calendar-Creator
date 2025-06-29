#!/usr/bin/env python3
"""
Couch to 5K ICS Generator

DISCLAIMER: This script is for informational purposes only and is not a
substitute for professional medical advice, diagnosis, or treatment.
Always consult your healthcare provider before starting any new exercise
program, especially if you have hypertension or other pre-existing health
conditions. Use this script at your own risk. The author assumes no
responsibility for any injury or health issues that may result from using
this script.

This script generates a personalized Couch to 5K calendar (.ics) file,
tailored for users with hypertension. It customizes the workout plan
based on your age, weight, and gender. If any required information is
missing, the script will prompt you and will not generate the calendar file.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any


def get_user_info() -> Optional[Dict[str, Any]]:
    """
    Prompt user for age, weight (metric or imperial), and gender.
    Returns a dict or None if incomplete.
    """
    try:
        unit = (
            input("Choose units: [M]etric (kg) or [I]mperial (lbs)? ".strip())
            .strip()
            .lower()
        )
        if unit not in ("m", "i"):
            print("Please enter 'M' for Metric or 'I' for Imperial.")
            return None
        age = int(input("Enter your age (years): ").strip())
        if unit == "m":
            weight = float(input("Enter your weight (kg): ").strip())
        else:
            weight = float(input("Enter your weight (lbs): ").strip())
            weight = weight * 0.453592  # Convert lbs to kg
        gender = input("Enter your gender (male/female): ").strip().lower()
        if gender not in ["male", "female"]:
            print("Gender must be 'male' or 'female'.")
            return None
        return {"age": age, "weight": weight, "gender": gender, "unit": unit}
    except (ValueError, TypeError):
        print("Invalid input. Please enter valid numbers for age and weight.")
        return None


def get_workout_plan(user: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Return a plan (list of dicts) based on age and weight.
    Adjusts session duration for older or heavier users.
    """
    plan: List[Dict[str, Any]] = []
    for week in range(10):
        for day_offset in (0, 2, 4):  # Mon, Wed, Fri
            description = (
                f"Follow the Couch to 5K plan - Week {week+1} session. "
                f"Note: This plan is tailored for an adult {user['gender']} "
                f"aged {user['age']} with hypertension. "
                "Please monitor your health and consult your doctor if needed."
            )
            plan.append(
                {
                    "week": week + 1,
                    "day": day_offset // 2 + 1,
                    "day_offset": day_offset,
                    "duration": 30,  # minutes
                    "description": description,
                }
            )
    if user["age"] >= 60 or user["weight"] >= 100:
        for session in plan:
            session["duration"] = 25
            session["description"] += " (Reduced session duration for safety.)"
    return plan


def format_ics_datetime(dt: datetime) -> str:
    """
    Format a datetime object for ICS file (YYYYMMDDTHHMMSS).
    """
    return dt.strftime("%Y%m%dT%H%M%S")


def generate_ics(plan: List[Dict[str, Any]], start_day: datetime) -> None:
    """
    Generate the ICS file from the workout plan and start date.
    """
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Couch to 5K//EN\n"
    for session in plan:
        session_date = start_day + timedelta(
            weeks=session["week"] - 1, days=session["day_offset"]
        )
        dt_start = session_date.replace(hour=7, minute=0)
        dt_end = dt_start + timedelta(minutes=session["duration"])
        event_name = f"C25K Week {session['week']} - Day {session['day']}"
        ics_content += (
            f"BEGIN:VEVENT\n"
            f"SUMMARY:{event_name}\n"
            f"DTSTART;TZID=America/New_York:{format_ics_datetime(dt_start)}\n"
            f"DTEND;TZID=America/New_York:{format_ics_datetime(dt_end)}\n"
            f"DESCRIPTION:{session['description']}\n"
            f"END:VEVENT\n"
        )
    ics_content += "END:VCALENDAR"
    with open("Couch_to_5K_Reminders.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)
    print("ICS file 'Couch_to_5K_Reminders.ics' created successfully.")


def main() -> None:
    """
    Main execution block for the Couch to 5K ICS Generator.
    """
    print("Couch to 5K ICS Generator (for users with hypertension)")
    print(
        "====================================================================",
        "\nDISCLAIMER: This script is for informational purposes only and is not a\n",
        "substitute for professional medical advice, diagnosis, or treatment.\n",
        "Always consult your healthcare provider before starting any new\n",
        "exercise program, especially if you have hypertension or other\n",
        "pre-existing health conditions. Use this script at your own risk.\n",
        "The author assumes no responsibility for any injury or health issues\n",
        "that may result from using this script.\n",
        "====================================================================",
        sep="",
    )
    user = get_user_info()
    if not user:
        print(
            "Missing or invalid information. "
            "Please provide all required details to generate your calendar."
        )
        return
    # === CUSTOMIZE YOUR START DATE HERE ===
    # Example: Start on July 15, 2025
    start_day = datetime(2025, 7, 15)  # Change as needed
    plan = get_workout_plan(user)
    generate_ics(plan, start_day)


if __name__ == "__main__":
    main()
