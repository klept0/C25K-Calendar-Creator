# Random_Scripts

Random Things I Have Made - random ideas that may not be 100%

## Contents

<details>
<summary><strong>C25K Calendar Creator</strong></summary>

- `c25k_ics_generator.py`: Couch to 5K calendar and checklist generator with health, localization, and export features.
- `c25k_ics_generator_readme.md`: Full documentation and usage guide for the C25K tool.
- `c25k_excel_macro_inserter.py`: Script to auto-insert macros and formulas into the Excel progress tracker.
- Output files: `.ics`, `.csv`, `.json`, Google Fit CSV, Markdown checklist, and Excel progress tracker with advanced macros and visual cues.

<details>
<summary>Implemented Features</summary>

- **Plan Customization:** Choose number of weeks and days per week for your plan.
- **Accessibility:** High-contrast and large-font options for Markdown and Excel outputs.
- **Dynamic Start Date:** Start on a specific date or next Monday.
- **Progress Tracking:** Excel tracker is auto-generated and includes all macros, formulas, and visual cues. Macros are auto-inserted using the included macro inserter script.
- **Motivational Quotes, Adaptive Plan, Custom Rest Days, Dashboard, Badges, Reminders, Weekly Review Prompts:** All included in the Excel tracker.
- **Output Directory Logic:** All exports are saved in a user-specific folder inside the project.
- **Export Formats:** ICS, CSV, JSON, Google Fit CSV, Markdown, PDF, Excel.
- **Markdown Checklist Export:** Always generated with user info and notes.
- **Colorized CLI Prompts and Feedback:** For a more user-friendly experience.

</details>

<details>
<summary>Planned / Placeholder / Stub Features</summary>

- **Reminders:** Email reminders are stubbed (no real email sending).
- **Weather Suggestions:** Weather integration is a stub (no real API call).
- **Mobile App Export:** Strava/Runkeeper and other mobile app exports are stubs.
- **Apple Health Export:** Documented as planned only.
- **QR Code Export:** Documented as planned only.
- **PDF Export:** PDF export is a stub (calls a module, may not be fully implemented).
- **Voice Prompts:** Voice/text prompt export is a stub.
- **Community/Sharing:** Sharing via email is a stub.
- **In-app FAQ/Help:** Documented as planned only.
- **Font Size/Dyslexia Font:** Documented as planned only.
- **Gamification (badges/level up):** Only visual/Excel, not interactive or tracked.
- **Data Privacy/Security:** Documented as planned only.
- **Customizable Plan Templates:** Documented as planned only.
- **Advanced Analytics (trend lines, analytics export):** Documented as planned only.
- **Wearables Integration:** Documented as planned only.
- **Feedback Loop:** Documented as planned only.

See the tool's README for details on each feature and how to use them. For planned features, refer to the documentation and Macros & Instructions sheet for future updates.

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

<details>
<summary>Medical Sources and References</summary>

- NHS Couch to 5K: https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/
- CDC Physical Activity Guidelines: https://www.cdc.gov/physicalactivity/basics/index.htm
- American Heart Association: https://www.heart.org/en/healthy-living/fitness/fitness-basics

All medical and health-related logic in this script is for informational purposes only and is based on the above reputable sources. Always consult your healthcare provider before starting any new exercise program.

</details>

---

**Default Settings:**

- Units: Imperial (lbs)
- Temperature: Fahrenheit (°F)

The tool defaults to imperial units and Fahrenheit for weather. You can change these in the prompts or settings.

</details>
