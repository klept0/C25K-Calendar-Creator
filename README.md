# Random_Scripts

Random Things I Have Made - random ideas that may not be 100%

## Contents

- **C25K Calendar Creator**
  <details>
    <summary>Show details</summary>

  - `c25k_ics_generator.py`: Couch to 5K calendar and checklist generator with health, localization, and export features.
  - `c25k_ics_generator_readme.md`: Full documentation and usage guide for the C25K tool.
  - `c25k_excel_macro_inserter.py`: Script to auto-insert macros and formulas into the Excel progress tracker.
  - Output files: `.ics`, `.csv`, `.json`, Google Fit CSV, Markdown checklist, and Excel progress tracker with advanced macros and visual cues.

  </details>

---

<details>
<summary>Advanced Features</summary>

- **Plan Customization:** Choose number of weeks and days per week for your plan.
- **Accessibility:** High-contrast and large-font options for Markdown and Excel outputs.
- **Dynamic Start Date:** Start on a specific date or next Monday.
- **Reminders:** Optionally send an email reminder for your first workout (stub).
- **Weather Suggestions:** Get a weather suggestion for your first workout (stub).
- **Progress Tracking:** Excel tracker is auto-generated and includes all macros, formulas, and visual cues. Macros are auto-inserted using the included macro inserter script.
- **Mobile App Export:** Export to Strava/Runkeeper (stub).
- **PDF Export:** Export plan as a PDF (stub).
- **Voice Prompts:** Export voice/text prompts for workouts (stub).
- **Community/Sharing:** Share your plan via email (stub).

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
<summary>Excel Progress Tracker & Macros</summary>

The progress tracker Excel file (`<name>_progress_tracker.xlsx`) is automatically generated and includes built-in spreadsheet macros and instructions to help you track your Couch to 5K journey:

- **Macros & Instructions Sheet:** All advanced macros, formulas, and usage instructions are included in a dedicated sheet. You can copy-paste or review them directly in Excel.
- **Auto-Insertion:** Macros and formulas are auto-inserted using the included `c25k_excel_macro_inserter.py` script. You can run this script manually if needed.
- **Advanced Visual Cues:** The tracker includes checkmarks, rest day highlighting, overdue alerts, sparklines, milestone badges, weekly progress bars, goal gauge, weather icons/colors, accessibility macro, and notes highlighting.
- **Improved Formatting:** Columns are auto-sized, all cells are wrapped and aligned, code blocks use a monospaced font and shading, and the top row is frozen for easy navigation.
- **Accessibility:** High-contrast and large-font options are available for improved readability.

All formulas/macros are beginner-friendly and can be copy-pasted or are pre-filled in the Excel file. See the "Macros & Instructions" sheet in your progress tracker for more details.

</details>

---

**Default Settings:**

- Units: Imperial (lbs)
- Temperature: Fahrenheit (°F)

The tool defaults to imperial units and Fahrenheit for weather. You can change these in the prompts or settings.
