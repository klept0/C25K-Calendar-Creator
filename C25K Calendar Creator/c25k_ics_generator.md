# Couch to 5K ICS Generator

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

This script generates a personalized Couch to 5K calendar (.ics) file, tailored for users with hypertension. It customizes the workout plan based on your age, weight, gender, preferred language, session start time, and personal goal. The script supports multiple export formats for use with Apple/Google calendars, Google Fit, and other platforms. It also generates a Markdown checklist for tracking progress.

## Features

- **Customizable Start Date and Time:** Set your preferred program start date and session start time.
- **Personalized Plan:** Adjusts session duration for older or heavier users, based on safety recommendations from NHS, CDC, and AHA.
- **Health Reminder:** Includes a note to monitor health and consult a doctor if needed.
- **Localization:** Supports English and Spanish for all workout instructions.
- **Multiple Export Formats:**
  - `.ics` (standard calendar import, Apple/Google Calendar, Apple Health)
  - `.csv` (spreadsheet import)
  - `.json` (data import for other apps)
  - Google Fit compatible `.csv`
  - Markdown checklist for tracking
- **Hydration and Safety Reminders:** Each workout includes hydration and safety notes.
- **Beginner Tips:** Each day includes a motivational or safety tip (based on NHS, CDC, and AHA guidance).
- **Rest Days:** Rest days are included in all exports and the checklist.
- **Personal Goal:** Option to set a personal goal, included in the checklist.
- **Resource Link:** Checklist includes a link to a reputable C25K guide.
- **Customizable Alerts for ICS:** Set a custom notification time (in minutes) before each session when exporting to ICS. The calendar file will include a notification (VALARM) for each workout event.

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
     - **Alert time before session (minutes, for ICS export only)**
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
- **Customizable Alerts for ICS:** Set a custom notification time (in minutes) before each session when exporting to ICS. The calendar file will include a notification (VALARM) for each workout event.

### Usage Notes

- All advanced features are optional and can be accessed via prompts when running the script.
- Stubs indicate features that can be extended with real integrations.

## Progress Tracking Macros

The `progress.csv` file includes built-in spreadsheet macros to help you track your Couch to 5K journey:

- **Auto-fill Today’s Date:** Use `=TODAY()` in the `date_completed` column.
- **Total Completed Sessions:** `=COUNTIF(D2:D31,"Y")`
- **Progress Percentage:** `=COUNTIF(D2:D31,"Y")/COUNTA(D2:D31)`
- **Next Session to Complete:** `=MATCH("",D2:D31,0)+1`
- **Days Since Last Session:** `=TODAY()-MAX(C2:C31)`
- **Motivational Message:** `=IF(COUNTIF(D2:D31,"Y")=COUNTA(D2:D31),"Congratulations! You finished!","Keep going, you're doing great!")`

These macros work in Excel, Google Sheets, and most spreadsheet programs. See the comments in `progress.csv` for more details.

## Advanced Macros in Progress Tracker (Automated Columns)

The following advanced macros are now included as columns in `progress.csv`:

- **Current_Streak**: Tracks the current streak of completed sessions. Use `=IF(D2="Y",1,0)` in F2, then `=IF(D3="Y",F2+1,0)` down the column. Longest streak: `=MAX(F2:F31)`.
- **Missed**: Flags missed sessions. Use `=IF(AND(C2="",TODAY()-DATE(2025,7,15)+(ROW()-2)*2>2),"Missed","")` in G2.
- **Adjust_Plan**: Suggests plan adjustment if 3+ sessions are missed. Use `=IF(COUNTIF($D$2:$D$31,"N")>=3,"Consider repeating this week or shifting plan","On Track")` in H2.
- **Effort**: User rates each session (1-5 or Easy/Medium/Hard). Add conditional formatting for trends.
- **Milestone**: Celebrates milestones. Use `=IF(AND(A2=1,B2=3),"First week done!",IF(AND(A2=5,B2=3),"Halfway!",IF(AND(A2=10,B2=3),"C25K Complete!","")))` in J2.
- **Weather**: User logs weather/conditions for each session.

Other macros:

- **Goal Progress Visualization**: `=COUNTIF(D2:D31,"Y")/COUNTA(D2:D31)`
- **Weekly Summary**: Insert a row after each week and use `=COUNTIF(D2:D4,"Y")` for completed, `=COUNTIF(G2:G4,"Missed")` for missed, and a motivational message formula.
- **Auto-Backup/Versioning**: Use File > Version history (Google Sheets) or a VBA macro (Excel).

All formulas/macros are beginner-friendly and can be copy-pasted or are pre-filled in the CSV. See the tool and repo README for more details.

## Medical Sources and References

- NHS Couch to 5K: https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/
- CDC Physical Activity Guidelines: https://www.cdc.gov/physicalactivity/basics/index.htm
- American Heart Association: https://www.heart.org/en/healthy-living/fitness/fitness-basics

All medical and health-related logic in this script is for informational purposes only and is based on the above reputable sources. Always consult your healthcare provider before starting any new exercise program.

## Disclaimer

---

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

---

**Author:** [klept0]
**License:** MIT
