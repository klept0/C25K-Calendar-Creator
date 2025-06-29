# Couch to 5K ICS Generator

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

This script generates a personalized Couch to 5K calendar (.ics) file, tailored for users with hypertension. It customizes the workout plan based on your age, weight, gender, preferred language, and session start time. The script supports multiple export formats for use with Apple/Google calendars, Google Fit, and other platforms.

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
- **Hydration and Safety Reminders:** Each workout includes hydration and safety notes.

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
     - Export format (ICS, CSV, JSON, or Google Fit CSV)
   - If any information is missing or invalid, the script will not generate the calendar.
3. **Import the Calendar or Data:**
   - Locate the generated file (e.g., `Couch_to_5K_Reminders.ics`, `.csv`, `.json`, or `Couch_to_5K_GoogleFit.csv`).
   - Import it into your preferred calendar or health application.

## Example

To start the program on July 15, 2025, at 7:00 AM, set in the script or at the prompt:

```python
start_day = datetime(2025, 7, 15)
```

## Customization

- **Session Time:** Enter your preferred session time at the prompt.
- **Language:** Choose English or Spanish for all workout instructions.
- **Export Format:** Choose the format that best fits your needs (ICS, CSV, JSON, Google Fit CSV).
- **Workout Duration:** The script automatically reduces session duration for users aged 60+ or weighing 100kg+.

## Disclaimer

---

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

---

**Author:** [klept0]
**License:** MIT
