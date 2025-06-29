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

Medical recommendations and plan structure are based on:
- NHS Couch to 5K: https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/
- CDC Physical Activity Guidelines: https://www.cdc.gov/physicalactivity/basics/index.htm
- American Heart Association: https://www.heart.org/en/healthy-living/fitness/fitness-basics
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import csv
import json
import os
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


# --- Advanced Macros Implementation for progress.csv ---
# These are formulas and macro instructions for spreadsheet users.
# Add these as columns or sheets in progress.csv as appropriate.
#
# 1. Streak Counter (formula for Google Sheets/Excel):
#    Add a column 'Current_Streak'. In row 2 (first data row):
#      =IF([@completed]="Y",1,0)
#    In row 3 and down:
#      =IF([@completed]="Y",OFFSET([@Current_Streak],-1,0)+1,0)
#    Longest streak: =MAX(Current_Streak)
#
# 2. Missed Sessions Alert:
#    Add a column 'Missed'. Formula:
#      =IF(AND([@date_completed]="",TODAY()-[@date_scheduled]>2),"Missed","")
#    (Assumes a 'date_scheduled' column exists.)
#
# 3. Adaptive Plan Adjuster:
#    Add a column 'Adjust_Plan'. Formula:
#      =IF(COUNTIF([completed],"N")>=3,"Consider repeating this week or shifting plan","On Track")
#
# 4. Weekly Summary Generator:
#    At the end of each week, insert a summary row with formulas:
#      Sessions Completed: =COUNTIF([completed],"Y")
#      Sessions Missed: =COUNTIF([Missed],"Missed")
#      Motivational Msg: =IF([Sessions Completed]=[Total Sessions],"Great job!","Keep going!")
#
# 5. Effort/Feeling Tracker:
#    Add a column 'Effort' (1-5 or Easy/Medium/Hard). Use conditional formatting for trends.
#    For chart: Insert a bar/line chart of Effort vs. Date.
#
# 6. Goal Progress Visualization:
#    Add a cell for progress percent:
#      =COUNTIF([completed],"Y")/COUNTA([completed])
#    Insert a progress bar chart using this value.
#
# 7. Custom Milestone Celebrations:
#    Add a column 'Milestone'. Formula:
#      =IF(AND([@week]=1,[@day]=3),"First week done!",IF(AND([@week]=5,[@day]=3),"Halfway!",IF(AND([@week]=10,[@day]=3),"C25K Complete!","") ) )
#    Use conditional formatting to highlight these rows.
#
# 8. Weather/Condition Log:
#    Add a column 'Weather'. User logs weather/conditions for each session.
#    For trends: Insert a pivot table or chart by weather type.
#
# 9. Auto-Backup/Versioning:
#    Use spreadsheet's built-in version history, or set up a macro/script to copy the sheet weekly:
#      (Google Sheets: File > Version history > Name current version)
#      (Excel: VBA macro to copy sheet to a new tab with timestamp)
#
# All formulas/macros are beginner-friendly and can be copy-pasted into the spreadsheet. See README for more details.


def colorize(text, color, bold=False):
    colors = {
        "cyan": "\033[96m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "magenta": "\033[95m",
        "blue": "\033[94m",
        "white": "\033[97m",
        "reset": "\033[0m",
        "bold": "\033[1m",
    }
    prefix = colors.get(color, "")
    if bold:
        prefix = colors["bold"] + prefix
    return f"{prefix}{text}{colors['reset']}"


def get_user_info() -> Optional[Dict[str, Any]]:
    """
    Prompt user for name, age, weight (metric or imperial), gender,
    session time, language, personal goal, and advanced options.
    Returns a dict or None if incomplete.
    """
    try:
        name = input(colorize("Enter your name: ", "green", bold=True)).strip()
        if not name:
            print(colorize("Name is required.", "red", bold=True))
            return None
        unit = (
            input(
                colorize(
                    "Choose units: [M]etric (kg) or [I]mperial (lbs)? ",
                    "blue",
                    bold=True,
                )
            )
            .strip()
            .lower()
        )
        if unit not in ("m", "i"):
            print(
                colorize(
                    "Please enter 'M' for Metric or 'I' for Imperial.",
                    "red",
                    bold=True,
                )
            )
            return None
        age = int(
            input(
                colorize(
                    "Enter your age (years): ",
                    "yellow",
                    bold=True,
                )
            ).strip()
        )
        if unit == "m":
            weight = float(
                input(
                    colorize("Enter your weight (kg): ", "magenta", bold=True)
                ).strip()
            )
        else:
            weight = float(
                input(
                    colorize("Enter your weight (lbs): ", "magenta", bold=True)
                ).strip()
            )
            weight = weight * 0.453592  # Convert lbs to kg
        gender = (
            input(
                colorize(
                    "Enter your gender ([M]ale/[F]emale): ",
                    "cyan",
                    bold=True,
                )
            )
            .strip()
            .lower()
        )
        if gender in ["m", "male"]:
            gender = "male"
        elif gender in ["f", "female"]:
            gender = "female"
        else:
            print(
                colorize(
                    "Gender must be 'M'/'F' or 'male'/'female'.",
                    "red",
                    bold=True,
                )
            )
            return None
        # Session time
        time_str = input(
            colorize(
                "Enter session start time (HH:MM, 24h, default 07:00): ",
                "blue",
                bold=True,
            )
        ).strip()
        if time_str:
            try:
                hour, minute = map(int, time_str.split(":"))
            except Exception:
                print(
                    colorize(
                        "Invalid time format. Use HH:MM (24h).",
                        "red",
                        bold=True,
                    )
                )
                return None
        else:
            hour, minute = 7, 0
        # Language/localization
        lang = (
            input(
                colorize(
                    "Choose language: [E]nglish (default) or [S]panish: ",
                    "green",
                    bold=True,
                )
            )
            .strip()
            .lower()
        )
        if lang not in ("e", "s", ""):
            print(
                colorize(
                    "Please enter 'E' for English or 'S' for Spanish.",
                    "red",
                    bold=True,
                )
            )
            return None
        lang = lang if lang else "e"
        # Export option
        export = (
            input(
                colorize(
                    "Export format: [I]CS (default), [C]SV, [J]SON, [G]oogle Fit CSV, [P]DF, [M]arkdown, [V]oice, [S]trava/Runkeeper? ",
                    "yellow",
                    bold=True,
                )
            )
            .strip()
            .lower()
        )
        if export not in ("i", "c", "j", "g", "p", "m", "v", "s", ""):
            print(colorize("Please enter a valid export option.", "red", bold=True))
            return None
        export = export if export else "i"
        # Personal goal
        goal = input(
            colorize("Enter your personal C25K goal (optional): ", "magenta", bold=True)
        ).strip()
        # Advanced: plan length
        weeks, days_per_week = plan_customization.get_custom_plan_length()
        # Advanced: accessibility
        high_contrast = (
            input(
                colorize("High-contrast mode? [Y/N] (default N): ", "white", bold=True)
            )
            .strip()
            .lower()
            == "y"
        )
        large_font = (
            input(colorize("Large font mode? [Y/N] (default N): ", "white", bold=True))
            .strip()
            .lower()
            == "y"
        )
        # Advanced: dynamic start date
        start_option = (
            input(
                colorize(
                    "Start date: [D]efault, [N]ext Monday, or YYYY-MM-DD? ",
                    "blue",
                    bold=True,
                )
            )
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
                print(
                    colorize("Invalid date format. Use YYYY-MM-DD.", "red", bold=True)
                )
                return None
        else:
            start_day = None  # Use default in main
        # Advanced: email for reminders
        email = input(
            colorize("Enter your email for reminders (optional): ", "green", bold=True)
        ).strip()
        # Advanced: location for weather
        location = input(
            colorize(
                "Enter your city or ZIP for weather suggestions (optional): ",
                "cyan",
                bold=True,
            )
        ).strip()
        # Custom alert time for ICS
        alert_minutes = None
        if export == "i":
            alert_input = input(
                colorize(
                    "Alert before session (minutes, default 30, 0=none): ",
                    "magenta",
                    bold=True,
                )
            ).strip()
            if alert_input == "":
                alert_minutes = 30
            else:
                try:
                    alert_minutes = int(alert_input)
                except Exception:
                    print(
                        colorize(
                            "Invalid alert time. Using default 30 minutes.",
                            "red",
                            bold=True,
                        )
                    )
                    alert_minutes = 30
        return {
            "name": name,
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
    Workouts are based on the NHS Couch to 5K program.
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
    Tips are based on NHS, CDC, and AHA recommendations for beginners.
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
    Adjusts session duration for older or heavier users (age >= 60 or weight >= 100kg) for safety.
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
    outdir: str = ".",
) -> None:
    """
    Generate the ICS file from the workout plan and start date.
    Add the actual workout, tip, and rest days to the DESCRIPTION and NOTES fields.
    Add a VALARM block for custom alert time if alert_minutes > 0.
    ICS format is compatible with Apple/Google Calendar and most calendar apps.
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
    filename = os.path.join(outdir, "Couch_to_5K_Reminders.ics")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ics_content)
    print(f"ICS file '{filename}' created successfully.")


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
    content = f"# Couch to 5K Checklist\n\n**Name:** {user['name']}\n\n**Age:** {user['age']}\n\n**Start Date:** {user['start_day'].strftime('%Y-%m-%d') if user.get('start_day') else 'default'}\n\n"
    if user.get("goal"):
        content += f"**Personal Goal:** {user['goal']}\n\n"
    content += "**Resource:** [C25K Guide](https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/)\n\n"
    for session in plan:
        if session["duration"] > 0:
            content += (
                f"- [ ] Week {session['week']} Day {session['day']}: "
                f"{session['workout']}\n  - Tip: {session['tip']}\n  - Notes: ________________________________\n    ________________________________\n    ________________________________\n"
            )
        else:
            content += f"- [ ] Week {session['week']} {session['day']}: Rest Day\n  - Tip: {session['tip']}\n  - Notes: ________________________________\n    ________________________________\n    ________________________________\n"
    # Apply accessibility options if selected
    if user.get("high_contrast") or user.get("large_font"):
        content = accessibility.apply_accessibility_options(
            content, user.get("high_contrast"), user.get("large_font")
        )
    with open(filename, "w", encoding="utf-8") as mdfile:
        mdfile.write(content)
    print(f"Markdown checklist '{filename}' created successfully.")


def get_output_dir(user):
    # Use YYYY-MM-DD for start date
    start_str = (
        user["start_day"].strftime("%Y-%m-%d") if user.get("start_day") else "default"
    )
    safe_name = user["name"].replace(" ", "_")
    outdir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "created",
        f"{safe_name}-{user['age']}-{start_str}",
    )
    os.makedirs(outdir, exist_ok=True)
    return outdir


def main() -> None:
    """
    Main execution block for the Couch to 5K ICS Generator.
    """
    print(
        colorize(
            "Couch to 5K ICS Generator (for users with hypertension)",
            "magenta",
            bold=True,
        )
    )
    print(colorize("=" * 68, "yellow", bold=True))
    print(
        colorize(
            "\nDISCLAIMER: This script is for informational purposes only and is not a\n"
            "substitute for professional medical advice, diagnosis, or treatment.\n"
            "Always consult your healthcare provider before starting any new\n"
            "exercise program, especially if you have hypertension or other\n"
            "pre-existing health conditions. Use this script at your own risk.\n"
            "The author assumes no responsibility for any injury or health issues\n"
            "that may result from using this script.\n",
            "red",
            bold=True,
        )
    )
    print(colorize("=" * 68, "yellow", bold=True))
    user = get_user_info()
    if not user:
        print(
            "Missing or invalid information. "
            "Please provide all required details to generate your calendar."
        )
        return
    # Show summary before generating
    print(colorize("\nYour C25K Plan Summary:", "cyan", bold=True))
    print(
        colorize(
            f"  Weeks: {user['weeks']}  Days/Week: {user['days_per_week']}",
            "green",
            bold=True,
        )
    )
    print(
        colorize(
            f"  Start time: {user['hour']:02d}:{user['minute']:02d}",
            "yellow",
            bold=True,
        )
    )
    print(colorize(f"  Export format: {user['export'].upper()}", "magenta", bold=True))
    if user.get("start_day"):
        print(colorize(f"  Start date: {user['start_day']}", "blue", bold=True))
    if user.get("goal"):
        print(colorize(f"  Goal: {user['goal']}", "green", bold=True))
    if user.get("high_contrast") or user.get("large_font"):
        print(colorize("  Accessibility: ", "white", bold=True), end="")
        if user["high_contrast"]:
            print(colorize("High-contrast ", "yellow", bold=True), end="")
        if user["large_font"]:
            print(colorize("Large font", "yellow", bold=True), end="")
        print()
    # Plan customization
    plan = get_workout_plan(user)
    # Dynamic start date
    if user.get("start_day"):
        start_day = user["start_day"]
    else:
        from datetime import datetime

        start_day = datetime(2025, 7, 15)  # Default
    user["start_day"] = start_day  # Ensure always set
    outdir = get_output_dir(user)
    # Weather suggestion (example for first workout)
    if user.get("location"):
        suggestion = weather.get_weather_suggestion(user["location"], str(start_day))
        print(
            colorize(
                f"Weather suggestion for your first workout: {suggestion}",
                "cyan",
                bold=True,
            )
        )
    # Export logic
    if user["export"] == "i":
        generate_ics(
            plan,
            start_day,
            user["hour"],
            user["minute"],
            user.get("alert_minutes", 30),
            outdir=outdir,
        )
    elif user["export"] == "c":
        export_csv(plan, os.path.join(outdir, "Couch_to_5K_Reminders.csv"))
    elif user["export"] == "j":
        export_json(plan, os.path.join(outdir, "Couch_to_5K_Reminders.json"))
    elif user["export"] == "g":
        export_google_fit_csv(plan, os.path.join(outdir, "Couch_to_5K_GoogleFit.csv"))
    elif user["export"] == "p":
        pdf_export.export_to_pdf(
            str(plan), os.path.join(outdir, "Couch_to_5K_Plan.pdf")
        )
    elif user["export"] == "m":
        export_markdown_checklist(
            plan, os.path.join(outdir, "Couch_to_5K_Checklist.md"), user
        )
    elif user["export"] == "v":
        voice_prompts.export_voice_prompts(plan, user["lang"])
    elif user["export"] == "s":
        mobile_export.export_to_mobile_app(plan, "Strava/Runkeeper")
    # Always output a Markdown checklist with user info
    export_markdown_checklist(
        plan, os.path.join(outdir, "Couch_to_5K_Checklist.md"), user
    )
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
    print(
        colorize(
            "\nAll done! Your personalized C25K plan and exports are ready. Good luck!",
            "green",
            bold=True,
        )
    )


if __name__ == "__main__":
    main()
