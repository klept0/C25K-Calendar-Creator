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
import csv
import json


def get_user_info() -> Optional[Dict[str, Any]]:
    """
    Prompt user for age, weight (metric or imperial), gender, session time, and language.
    Returns a dict or None if incomplete.
    """
    try:
        unit = (
            input("Choose units: [M]etric (kg) or [I]mperial (lbs)? ").strip().lower()
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
        # Session time
        time_str = input(
            "Enter session start time (HH:MM, 24h, default 07:00): "
        ).strip()
        if time_str:
            try:
                hour, minute = map(int, time_str.split(":"))
            except Exception:
                print("Invalid time format. Use HH:MM (24h).")
                return None
        else:
            hour, minute = 7, 0
        # Language/localization
        lang = (
            input("Choose language: [E]nglish (default) or [S]panish: ").strip().lower()
        )
        if lang not in ("e", "s", ""):
            print("Please enter 'E' for English or 'S' for Spanish.")
            return None
        lang = lang if lang else "e"
        # Export option
        export = (
            input(
                "Export format: [I]CS (default), [C]SV, [J]SON, or [G]oogle Fit CSV? "
            )
            .strip()
            .lower()
        )
        if export not in ("i", "c", "j", "g", ""):
            print("Please enter 'I', 'C', 'J', or 'G'.")
            return None
        export = export if export else "i"
        return {
            "age": age,
            "weight": weight,
            "gender": gender,
            "unit": unit,
            "hour": hour,
            "minute": minute,
            "lang": lang,
            "export": export,
        }
    except (ValueError, TypeError):
        print("Invalid input. Please enter valid numbers for age and weight.")
        return None


def get_workout_details(week: int, day: int, lang: str = "e") -> str:
    """
    Return a string describing the actual workout for the given week and day.
    Supports English and Spanish.
    """
    workouts_en = [
        "Brisk 5-min warmup walk. Then alternate 60 sec jogging and 90 sec "
        "walking for 20 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Then alternate 90 sec jogging, 2 min walking "
        "for 20 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. 90 sec jog, 90 sec walk, 3 min jog, 3 min "
        "walk, repeat. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 3 min, walk 90 sec, jog 5 min, walk 2.5 "
        "min, jog 3 min, walk 90 sec, jog 5 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 5 min, walk 3 min, jog 5 min, walk 3 min, "
        "jog 5 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 8 min, walk 5 min, jog 8 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 25 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 28 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 30 min. Hydrate before and after.",
        "Brisk 5-min warmup walk. Jog 30 min. Hydrate before and after.",
    ]
    workouts_es = [
        "Camine rápido 5 min para calentar. Luego alterne 60 seg corriendo y 90 seg caminando durante 20 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Luego alterne 90 seg corriendo, 2 min caminando durante 20 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. 90 seg corra, 90 seg camine, 3 min corra, 3 min camine, repita. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 3 min, camine 90 seg, corra 5 min, camine 2.5 min, corra 3 min, camine 90 seg, corra 5 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 5 min, camine 3 min, corra 5 min, camine 3 min, corra 5 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 8 min, camine 5 min, corra 8 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 25 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 28 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 30 min. Hidratese antes y después.",
        "Camine rápido 5 min para calentar. Corra 30 min. Hidratese antes y después.",
    ]
    workouts = workouts_en if lang == "e" else workouts_es
    if 1 <= week <= 10:
        return workouts[week - 1]
    return workouts[0] if lang == "e" else workouts_es[0]


def get_workout_plan(user: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Return a plan (list of dicts) based on age and weight.
    Adjusts session duration for older or heavier users.
    Adds actual workout details for each session.
    """
    plan: List[Dict[str, Any]] = []
    for week in range(10):
        for day_offset in (0, 2, 4):  # Mon, Wed, Fri
            workout = get_workout_details(
                week + 1, day_offset // 2 + 1, user.get("lang", "e")
            )
            description = (
                f"Follow the Couch to 5K plan - Week {week+1} session. "
                f"Note: This plan is tailored for an adult {user['gender']} "
                f"aged {user['age']} with hypertension. "
                f"Weight: {user['weight']:.1f} kg. "
                f"Session time: {user['hour']:02d}:{user['minute']:02d}. "
                "Please monitor your health and consult your doctor if needed.\n"
                f"Workout: {workout}"
            )
            plan.append(
                {
                    "week": week + 1,
                    "day": day_offset // 2 + 1,
                    "day_offset": day_offset,
                    "duration": 30,  # minutes
                    "description": description,
                    "workout": workout,
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


def generate_ics(
    plan: List[Dict[str, Any]], start_day: datetime, hour: int, minute: int
) -> None:
    """
    Generate the ICS file from the workout plan and start date.
    Add the actual workout to the DESCRIPTION and NOTES fields for Apple Health.
    """
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Couch to 5K//EN\n"
    for session in plan:
        session_date = start_day + timedelta(
            weeks=session["week"] - 1, days=session["day_offset"]
        )
        dt_start = session_date.replace(hour=hour, minute=minute)
        dt_end = dt_start + timedelta(minutes=session["duration"])
        event_name = f"C25K Week {session['week']} - Day {session['day']}"
        # Add workout to both DESCRIPTION and X-APPLE-NOTES for Apple Health
        ics_content += (
            f"BEGIN:VEVENT\n"
            f"SUMMARY:{event_name}\n"
            f"DTSTART;TZID=America/New_York:{format_ics_datetime(dt_start)}\n"
            f"DTEND;TZID=America/New_York:{format_ics_datetime(dt_end)}\n"
            f"DESCRIPTION:{session['description']}\n"
            f"X-APPLE-NOTES:{session['workout']}\n"
            f"END:VEVENT\n"
        )
    ics_content += "END:VCALENDAR"
    with open("Couch_to_5K_Reminders.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)
    print("ICS file 'Couch_to_5K_Reminders.ics' created successfully.")


def export_csv(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the workout plan to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["week", "day", "duration", "description", "workout"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for session in plan:
            writer.writerow({k: session[k] for k in fieldnames})
    print(f"CSV file '{filename}' created successfully.")


def export_json(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the workout plan to a JSON file."""
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(plan, jsonfile, ensure_ascii=False, indent=2)
    print(f"JSON file '{filename}' created successfully.")


def export_google_fit_csv(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the workout plan to a Google Fit compatible CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Activity Type", "Start Date", "End Date", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for session in plan:
            # Use walking as the activity type for C25K beginner
            writer.writerow(
                {
                    "Activity Type": "Running",
                    "Start Date": f"Week {session['week']} Day {session['day']}",
                    "End Date": f"Week {session['week']} Day {session['day']}",
                    "Description": session["workout"],
                }
            )
    print(f"Google Fit CSV file '{filename}' created successfully.")


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
    if user["export"] == "i":
        generate_ics(plan, start_day, user["hour"], user["minute"])
    elif user["export"] == "c":
        export_csv(plan, "Couch_to_5K_Reminders.csv")
    elif user["export"] == "j":
        export_json(plan, "Couch_to_5K_Reminders.json")
    elif user["export"] == "g":
        export_google_fit_csv(plan, "Couch_to_5K_GoogleFit.csv")


if __name__ == "__main__":
    main()
