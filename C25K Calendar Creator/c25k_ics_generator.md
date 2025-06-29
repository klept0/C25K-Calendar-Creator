# Couch to 5K ICS Generator

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

This script generates a personalized Couch to 5K calendar (.ics) file, tailored for users with hypertension. It customizes the workout plan based on your age, weight, gender, preferred language, session start time, and personal goal. The script supports multiple export formats for use with Apple/Google calendars, Google Fit, and other platforms. It also generates a Markdown checklist for tracking progress.

## Features

- **Customizable Start Date and Time:** Set your preferred program start date and session start time.
- **Personalized Plan:** Adjusts session duration for older or heavier users.
- **Health Reminder:** Includes a note to monitor health and consult a doctor if needed.
- **Localization:** Supports English and Spanish for all workout instructions.
- **Multiple Export Formats:**
  - `.ics` (standard calendar import, Apple/Google Calendar, Apple Health)
  - `.csv` (spreadsheet import)
  - `.json` (data import for other apps)
  - Google Fit compatible `.csv`
  - Markdown checklist for tracking
- **Hydration and Safety Reminders:** Each workout includes hydration and safety notes.
- **Beginner Tips:** Each day includes a motivational or safety tip.
- **Rest Days:** Rest days are included in all exports and the checklist.
- **Personal Goal:** Option to set a personal goal, included in the checklist.
- **Resource Link:** Checklist includes a link to a reputable C25K guide.

## Usage

1. **Run the Script:**
   - Make sure you have Python 3 installed.
   - Run the script:
     ```bash
     python3 c25k_ics_generator.py
     ```
2. **Enter Your Information:**
   - The script will prompt you for:
     - Units (Metric or Imperial)
     - Age
     - Weight
     - Gender
     - Session start time (24h format, e.g., 07:00)
     - Language (English or Spanish)
     - Export format (ICS, CSV, JSON, Google Fit CSV)
     - Personal goal (optional)
   - If any information is missing or invalid, the script will not generate the calendar.
3. **Import the Calendar or Data:**
   - Locate the generated file (e.g., `Couch_to_5K_Reminders.ics`, `.csv`, `.json`, `Couch_to_5K_GoogleFit.csv`, or `Couch_to_5K_Checklist.md`).
   - Import it into your preferred calendar, health application, or use the checklist for tracking.

## Example

To start the program on July 15, 2025, at 7:00 AM, set in the script or at the prompt:

```python
start_day = datetime(2025, 7, 15)
```

## Customization

- **Session Time:** Enter your preferred session time at the prompt.
- **Language:** Choose English or Spanish for all workout instructions.
- **Export Format:** Choose the format that best fits your needs (ICS, CSV, JSON, Google Fit CSV, Markdown).
- **Workout Duration:** The script automatically reduces session duration for users aged 60+ or weighing 100kg+.
- **Personal Goal:** Enter a goal to keep yourself motivated.

## Advanced Features

- **Plan Customization:** Choose number of weeks and days per week for your plan.
- **Accessibility:** High-contrast and large-font options for Markdown checklist.
- **Dynamic Start Date:** Start on a specific date or next Monday.
- **Reminders:** Optionally send an email reminder for your first workout (stub).
- **Weather Suggestions:** Get a weather suggestion for your first workout (stub).
- **Progress Tracking:** Import and summarize progress from a CSV (stub).
- **Mobile App Export:** Export to Strava/Runkeeper (stub).
- **PDF Export:** Export plan as a PDF (stub).
- **Voice Prompts:** Export voice/text prompts for workouts (stub).
- **Community/Sharing:** Share your plan via email (stub).

### Usage Notes

- All advanced features are optional and can be accessed via prompts when running the script.
- Stubs indicate features that can be extended with real integrations.

## Disclaimer

---

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

---

**Author:** [klept0]
**License:** MIT
