# Random_Scripts

Random Things I Have Made - random ideas that may not be 100%

## Contents

- **C25K Calendar Creator**
  <details>
    <summary>Show details</summary>

  - `c25k_ics_generator.py`: Couch to 5K calendar and checklist generator with health, localization, and export features.
  - `c25k_ics_generator_readme.md`: Full documentation and usage guide for the C25K tool.
  - Output files: `.ics`, `.csv`, `.json`, Google Fit CSV, and Markdown checklist.

  </details>

---

<details>
<summary>Advanced Features</summary>

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

See the tool's README for details on each feature and how to use them.

</details>

<details>
<summary>Medical Sources and References</summary>

- NHS Couch to 5K: https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/
- CDC Physical Activity Guidelines: https://www.cdc.gov/physicalactivity/basics/index.htm
- American Heart Association: https://www.heart.org/en/healthy-living/fitness/fitness-basics

All medical and health-related logic in this script is for informational purposes only and is based on the above reputable sources. Always consult your healthcare provider before starting any new exercise program.

</details>

<details>
<summary>Progress Tracking Macros</summary>

The `progress.csv` file includes built-in spreadsheet macros to help you track your Couch to 5K journey:

- **Auto-fill Today’s Date:** Use `=TODAY()` in the `date_completed` column.
- **Total Completed Sessions:** `=COUNTIF(D2:D31,"Y")`
- **Progress Percentage:** `=COUNTIF(D2:D31,"Y")/COUNTA(D2:D31)`
- **Next Session to Complete:** `=MATCH("",D2:D31,0)+1`
- **Days Since Last Session:** `=TODAY()-MAX(C2:C31)`
- **Motivational Message:** `=IF(COUNTIF(D2:D31,"Y")=COUNTA(D2:D31),"Congratulations! You finished!","Keep going, you're doing great!")`

These macros work in Excel, Google Sheets, and most spreadsheet programs. See the comments in `progress.csv` for more details.

</details>

<details>
<summary>Advanced Macros in Progress Tracker (Automated Columns)</summary>

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

</details>

---

**Default Settings:**

- Units: Imperial (lbs)
- Temperature: Fahrenheit (°F)

The tool defaults to imperial units and Fahrenheit for weather. You can change these in the prompts or settings.
