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
from c25k_utils import (
    reminders,
    progress,
    plan_customization,
    accessibility,
    mobile_export,
    pdf_export,
    voice_prompts,
    community,
    start_date,
    weather,
)


def get_user_info() -> Optional[Dict[str, Any]]:
    """
    Prompt user for age, weight (metric or imperial), gender, session time, language, personal goal, and advanced options.
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
                "Export format: [I]CS (default), [C]SV, [J]SON, [G]oogle Fit CSV, [P]DF, [M]arkdown, [V]oice, [S]trava/Runkeeper? "
            )
            .strip()
            .lower()
        )
        if export not in ("i", "c", "j", "g", "p", "m", "v", "s", ""):
            print("Please enter a valid export option.")
            return None
        export = export if export else "i"
        # Personal goal
        goal = input("Enter your personal C25K goal (optional): ").strip()
        # Advanced: plan length
        weeks, days_per_week = plan_customization.get_custom_plan_length()
        # Advanced: accessibility
        high_contrast = (
            input("High-contrast mode? [Y/N] (default N): ").strip().lower() == "y"
        )
        large_font = (
            input("Large font mode? [Y/N] (default N): ").strip().lower() == "y"
        )
        # Advanced: dynamic start date
        start_option = (
            input("Start date: [D]efault, [N]ext Monday, or YYYY-MM-DD? ")
            .strip()
            .lower()
        )
        if start_option == "n":
            from datetime import datetime

            start_day = start_date.get_dynamic_start_date()
        elif start_option and start_option != "d":
            try:
                from datetime import datetime

                start_day = datetime.strptime(start_option, "%Y-%m-%d")
            except Exception:
                print("Invalid date format. Use YYYY-MM-DD.")
                return None
        else:
            start_day = None  # Use default in main
        # Advanced: email for reminders
        email = input("Enter your email for reminders (optional): ").strip()
        # Advanced: location for weather
        location = input(
            "Enter your city or ZIP for weather suggestions (optional): "
        ).strip()
        # Custom alert time for ICS
        alert_minutes = None
        if export == "i":
            alert_input = input(
                "Alert before session (minutes, default 30, 0=none): "
            ).strip()
            if alert_input == "":
                alert_minutes = 30
            else:
                try:
                    alert_minutes = int(alert_input)
                except Exception:
                    print("Invalid alert time. Using default 30 minutes.")
                    alert_minutes = 30
        return {
            "age": age,
            "weight": weight,
            "gender": gender,
            "unit": unit,
            "hour": hour,
            "minute": minute,
            "lang": lang,
            "export": export,
            "goal": goal,
            "weeks": weeks,
            "days_per_week": days_per_week,
            "high_contrast": high_contrast,
            "large_font": large_font,
            "start_day": start_day,
            "email": email,
            "location": location,
            "alert_minutes": alert_minutes,
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


def get_beginner_tip(day: int, lang: str = "e") -> str:
    """
    Return a motivational or safety tip for the given day.
    """
    tips_en = [
        "Remember to stretch before and after your workout!",
        "Wear comfortable shoes and clothing.",
        "Stay hydrated and listen to your body.",
        "Rest is as important as running. Take it easy on rest days!",
        "Track your progress and celebrate small wins.",
        "Invite a friend or family member to join you!",
        "If you feel pain, stop and consult a professional.",
        "Set a reminder so you don't miss your session.",
        "Smile and enjoy the journey!",
        "You're doing great—keep going!",
    ]
    tips_es = [
        "¡Recuerda estirar antes y después de tu entrenamiento!",
        "Usa calzado y ropa cómodos.",
        "Mantente hidratado y escucha a tu cuerpo.",
        "El descanso es tan importante como correr. ¡Tómalo con calma en los días de descanso!",
        "Registra tu progreso y celebra los pequeños logros.",
        "¡Invita a un amigo o familiar a unirse!",
        "Si sientes dolor, detente y consulta a un profesional.",
        "Pon una alarma para no perder tu sesión.",
        "¡Sonríe y disfruta el proceso!",
        "¡Lo estás haciendo genial, sigue así!",
    ]
    tips = tips_en if lang == "e" else tips_es
    return tips[(day - 1) % len(tips)]


def get_workout_plan(user: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Return a plan (list of dicts) based on age, weight, and plan customization.
    Adjusts session duration for older or heavier users.
    Adds actual workout details and tips for each session.
    """
    weeks = user.get("weeks", 10)
    days_per_week = user.get("days_per_week", 3)
    plan: List[Dict[str, Any]] = []
    for week in range(weeks):
        for day in range(days_per_week):
            day_offset = day * (7 // days_per_week)
            workout = get_workout_details(week + 1, day + 1, user.get("lang", "e"))
            tip = get_beginner_tip(day + 1, user.get("lang", "e"))
            description = (
                f"Follow the Couch to 5K plan - Week {week+1} session. "
                f"Note: This plan is tailored for an adult {user['gender']} "
                f"aged {user['age']} with hypertension. "
                f"Weight: {user['weight']:.1f} kg. "
                f"Session time: {user['hour']:02d}:{user['minute']:02d}. "
                "Please monitor your health and consult your doctor if needed.\n"
                f"Workout: {workout}\n"
                f"Tip: {tip}"
            )
            plan.append(
                {
                    "week": week + 1,
                    "day": day + 1,
                    "day_offset": day_offset,
                    "duration": 30,  # minutes
                    "description": description,
                    "workout": workout,
                    "tip": tip,
                }
            )
    if user["age"] >= 60 or user["weight"] >= 100:
        for session in plan:
            session["duration"] = 25
            session["description"] += " (Reduced session duration for safety.)"
    # Add rest days (remaining days of week)
    for week in range(weeks):
        for rest_offset in range(days_per_week, 7):
            rest_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][rest_offset]
            plan.append(
                {
                    "week": week + 1,
                    "day": rest_name,
                    "day_offset": rest_offset,
                    "duration": 0,
                    "description": (
                        f"Rest Day - Week {week+1} {rest_name}. "
                        "Rest and recover. Hydrate and stretch."
                    ),
                    "workout": "Rest Day",
                    "tip": get_beginner_tip(rest_offset, user.get("lang", "e")),
                }
            )
    return sorted(plan, key=lambda s: (s["week"], s["day_offset"]))


def format_ics_datetime(dt: datetime) -> str:
    """
    Format a datetime object for ICS file (YYYYMMDDTHHMMSS).
    """
    return dt.strftime("%Y%m%dT%H%M%S")


def generate_ics(
    plan: List[Dict[str, Any]],
    start_day: datetime,
    hour: int,
    minute: int,
    alert_minutes: int = 30,
) -> None:
    """
    Generate the ICS file from the workout plan and start date.
    Add the actual workout, tip, and rest days to the DESCRIPTION and NOTES fields.
    Add a VALARM block for custom alert time if alert_minutes > 0.
    """
    ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Couch to 5K//EN\n"
    for session in plan:
        session_date = start_day + timedelta(
            weeks=session["week"] - 1, days=session["day_offset"]
        )
        dt_start = session_date.replace(hour=hour, minute=minute)
        dt_end = dt_start + timedelta(minutes=session["duration"])
        if session["duration"] > 0:
            event_name = f"C25K Week {session['week']} - Day {session['day']}"
        else:
            event_name = f"C25K Week {session['week']} {session['day']} (Rest)"
        ics_content += (
            f"BEGIN:VEVENT\n"
            f"SUMMARY:{event_name}\n"
            f"DTSTART;TZID=America/New_York:{format_ics_datetime(dt_start)}\n"
            f"DTEND;TZID=America/New_York:{format_ics_datetime(dt_end)}\n"
            f"DESCRIPTION:{session['description']}\n"
            f"X-APPLE-NOTES:Workout: {session['workout']} | Tip: {session['tip']}\n"
        )
        # Add VALARM if alert_minutes > 0 and not a rest day
        if alert_minutes and session["duration"] > 0:
            ics_content += (
                "BEGIN:VALARM\n"
                f"TRIGGER:-PT{alert_minutes}M\n"
                "ACTION:DISPLAY\n"
                "DESCRIPTION:Time for your C25K session!\n"
                "END:VALARM\n"
            )
        ics_content += "END:VEVENT\n"
    ics_content += "END:VCALENDAR"
    with open("Couch_to_5K_Reminders.ics", "w", encoding="utf-8") as f:
        f.write(ics_content)
    print("ICS file 'Couch_to_5K_Reminders.ics' created successfully.")


def export_csv(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the workout plan to a CSV file, including tips and rest days."""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["week", "day", "duration", "description", "workout", "tip"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for session in plan:
            writer.writerow({k: session[k] for k in fieldnames})
    print(f"CSV file '{filename}' created successfully.")


def export_json(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the workout plan to a JSON file, including tips and rest days."""
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(plan, jsonfile, ensure_ascii=False, indent=2)
    print(f"JSON file '{filename}' created successfully.")


def export_google_fit_csv(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the workout plan to a Google Fit compatible CSV file, including tips."""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Activity Type", "Start Date", "End Date", "Description", "Tip"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for session in plan:
            writer.writerow(
                {
                    "Activity Type": "Running" if session["duration"] > 0 else "Rest",
                    "Start Date": f"Week {session['week']} Day {session['day']}",
                    "End Date": f"Week {session['week']} Day {session['day']}",
                    "Description": session["workout"],
                    "Tip": session["tip"],
                }
            )
    print(f"Google Fit CSV file '{filename}' created successfully.")


def export_markdown_checklist(
    plan: List[Dict[str, Any]], filename: str, user: Dict[str, Any]
) -> None:
    """Export the workout plan as a Markdown checklist file with tips and goal, with accessibility options if selected."""
    content = "# Couch to 5K Checklist\n\n"
    if user.get("goal"):
        content += f"**Personal Goal:** {user['goal']}\n\n"
    content += "**Resource:** [C25K Guide](https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/)\n\n"
    for session in plan:
        if session["duration"] > 0:
            content += (
                f"- [ ] Week {session['week']} Day {session['day']}: "
                f"{session['workout']}\n  - Tip: {session['tip']}\n  - Notes: _______\n"
            )
        else:
            content += f"- [ ] Week {session['week']} {session['day']}: Rest Day\n  - Tip: {session['tip']}\n  - Notes: _______\n"
    # Apply accessibility options if selected
    if user.get("high_contrast") or user.get("large_font"):
        content = accessibility.apply_accessibility_options(
            content, user.get("high_contrast"), user.get("large_font")
        )
    with open(filename, "w", encoding="utf-8") as mdfile:
        mdfile.write(content)
    print(f"Markdown checklist '{filename}' created successfully.")


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
    # Show summary before generating
    print("\nYour C25K Plan Summary:")
    print(f"  Weeks: {user['weeks']}  Days/Week: {user['days_per_week']}")
    print(f"  Start time: {user['hour']:02d}:{user['minute']:02d}")
    print(f"  Export format: {user['export'].upper()}")
    if user.get("start_day"):
        print(f"  Start date: {user['start_day']}")
    if user.get("goal"):
        print(f"  Goal: {user['goal']}")
    if user.get("high_contrast") or user.get("large_font"):
        print("  Accessibility: ", end="")
        if user["high_contrast"]:
            print("High-contrast ", end="")
        if user["large_font"]:
            print("Large font", end="")
        print()
    # Plan customization
    plan = get_workout_plan(user)
    # Dynamic start date
    if user.get("start_day"):
        start_day = user["start_day"]
    else:
        from datetime import datetime

        start_day = datetime(2025, 7, 15)  # Default
    # Weather suggestion (example for first workout)
    if user.get("location"):
        suggestion = weather.get_weather_suggestion(user["location"], str(start_day))
        print(f"Weather suggestion for your first workout: {suggestion}")
    # Export logic
    if user["export"] == "i":
        generate_ics(
            plan, start_day, user["hour"], user["minute"], user.get("alert_minutes", 30)
        )
    elif user["export"] == "c":
        export_csv(plan, "Couch_to_5K_Reminders.csv")
    elif user["export"] == "j":
        export_json(plan, "Couch_to_5K_Reminders.json")
    elif user["export"] == "g":
        export_google_fit_csv(plan, "Couch_to_5K_GoogleFit.csv")
    elif user["export"] == "p":
        pdf_export.export_to_pdf(str(plan), "Couch_to_5K_Plan.pdf")
    elif user["export"] == "m":
        export_markdown_checklist(plan, "Couch_to_5K_Checklist.md", user)
    elif user["export"] == "v":
        voice_prompts.export_voice_prompts(plan, user["lang"])
    elif user["export"] == "s":
        mobile_export.export_to_mobile_app(plan, "Strava/Runkeeper")
    # Always output a Markdown checklist with user info
    export_markdown_checklist(plan, "Couch_to_5K_Checklist.md", user)
    # Accessibility (example: print message)
    if user["high_contrast"] or user["large_font"]:
        print("Accessibility options enabled: ", end="")
        if user["high_contrast"]:
            print("High-contrast ", end="")
        if user["large_font"]:
            print("Large font", end="")
        print()
    # Reminders (stub)
    if user.get("email"):
        print(f"Sending reminder to {user['email']} for your first workout...")
        reminders.send_reminder(user["email"], plan[0], user["lang"])
    # Community/sharing (stub)
    community.share_plan(str(plan), platform="email")
    # Progress tracking (stub)
    progress_data = progress.import_progress("progress.csv")
    print(progress.generate_progress_summary(progress_data))
    print("\nAll done! Your personalized C25K plan and exports are ready. Good luck!")


if __name__ == "__main__":
    main()
