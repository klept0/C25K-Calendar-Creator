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
- **Reminders:** Real email reminders for each session are now supported. Configure your SMTP server at the prompt or via environment variables. See the tool README for setup instructions.
- **Mobile App Export:** Real Strava/Runkeeper export is now supported. Enter your API token at the prompt to upload your plan. See the tool README for setup instructions.
- **Apple Health Export:** Apple Health CSV export is now supported. Import the CSV into Apple Health using Shortcuts or a 3rd-party app. See the tool README for setup instructions.
- **Voice Prompts Export:** Voice/text prompt export is now supported. Generates a text script and (optionally) audio files for each session. See the tool README for setup instructions.
- **Output Directory Logic:** All exports are saved in a user-specific folder inside the project.
- **Export Formats:** ICS, CSV, JSON, Google Fit CSV, Markdown, PDF, Excel, Apple Health CSV, Voice Prompts.
- **Markdown Checklist Export:** Always generated with user info and notes.
- **Colorized CLI Prompts and Feedback:** For a more user-friendly experience.
- **Weather Suggestions:** Real, actionable weather suggestions for your first workout are now provided using live forecast data. Enter your city or ZIP at the prompt to get advice (e.g., "Great weather for running!", "Rain expected, consider rescheduling or wear a rain jacket").
- **QR Code Export:** Instantly generate a QR code image containing a detailed summary of your C25K plan (all workouts/tips, not just a short string). The QR code is large and high-contrast if accessibility options are enabled, and a Markdown file is generated with the QR code and full plan summary for easy sharing and accessibility. Requires the `qrcode` Python package (`pip install qrcode[pil]`).
- **PDF Export:** Visually rich, accessible PDF export is now fully supported. The PDF includes a cover page, full plan table, accessibility options, motivational quotes, resource links, and privacy note. Requires the `reportlab` Python package (`pip install reportlab`).

</details>

<details>
<summary>Planned / Placeholder / Stub Features</summary>

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

## Weather Integration (OpenWeatherMap)

This tool can fetch real weather forecasts for your session dates if you provide a city or ZIP code. To enable this feature:

1. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api).
2. Set your API key as an environment variable before running the script:

   ```sh
   export OWM_API_KEY=your_openweathermap_api_key
   ```
   Or, replace the placeholder in the code with your API key.

3. If no API key is set, the tool will use a built-in weather stub for demo purposes.

See the code and documentation for more details.
