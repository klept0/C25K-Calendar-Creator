# Random_Scripts

[![Accessibility](https://img.shields.io/badge/accessibility-AA-blue)](./C25K%20Calendar%20Creator/c25k_ics_generator_readme.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/yourusername/yourrepo/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/yourrepo/actions)

Random Things I Have Made - random ideas that may not be 100%

---

**License:** MIT. See [LICENSE](LICENSE).

**Changelog:** See [CHANGELOG.md](CHANGELOG.md).

**Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md).

**Code Style:**
- This project uses [black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/) for formatting. Run `black .` and `isort .` before submitting a pull request.
- All functions should have type hints and docstrings.

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
- **Customizable Plan Templates:** Save and load custom plan templates for different goals or fitness levels. You can now save your current plan as a template, load a template at the start, and select from built-in or custom templates. *(Newly implemented)*
- **Advanced Analytics:** The Excel tracker now includes an Analytics sheet with summary statistics (totals, averages, streaks, missed sessions, effort trends, goal progress) and instructions for creating charts (progress over time, effort trends, weather vs. performance). *(Newly implemented)*
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
- **Colorized Feedback in GUI:** For a more user-friendly experience, the GUI provides colorized feedback and status messages.
- **Weather Suggestions:** Real, actionable weather suggestions for your first workout are now provided using live forecast data. Enter your city or ZIP at the prompt to get advice (e.g., "Great weather for running!", "Rain expected, consider rescheduling or wear a rain jacket").
- **QR Code Export:** Instantly generate a QR code image containing a detailed summary of your C25K plan (all workouts/tips, not just a short string). The QR code is large and high-contrast if accessibility options are enabled, and a Markdown file is generated with the QR code and full plan summary for easy sharing and accessibility. Requires the `qrcode` Python package (`pip install qrcode[pil]`).
- **PDF Export:** Visually rich, accessible PDF export is now fully supported. The PDF includes a cover page, full plan table, accessibility options, motivational quotes, resource links, and privacy note. Requires the `reportlab` Python package (`pip install reportlab`).
- **Wearables Integration:** Direct export/import for popular fitness trackers and smartwatches is now supported. Export your plan as Apple Health CSV, Google Fit CSV, or upload directly to Strava/Runkeeper via API. See below for import instructions. *(Newly implemented)*

</details>

<details>
<summary>Planned / Placeholder / Stub Features</summary>

- **Feedback Loop:** Planned.
- **Further Accessibility Polish:** Planned.
- **Gamification Enhancements:** Planned.
- **Privacy/Export Options:** Planned.

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
2. **Set your API key as an environment variable (recommended for security and convenience):**

   For macOS/zsh users, add this line to your `~/.zshrc` file:
   ```sh
   export OWM_API_KEY="your_actual_api_key_here"
   ```
   Then reload your shell configuration:
   ```sh
   source ~/.zshrc
   ```
   Replace `your_actual_api_key_here` with your real OpenWeatherMap API key.

   Alternatively, for a one-off run, you can set the variable inline:
   ```sh
   OWM_API_KEY="your_actual_api_key_here" python3 c25k_ics_generator.py
   ```

3. The script will automatically use the API key from the `OWM_API_KEY` environment variable. You do not need to type it in each time.

4. If no API key is set, the tool will use a built-in weather stub for demo purposes.

**Security note:** Never commit your API key to version control or share it in plaintext. Environment variables are only visible to your user and processes you run.

See the code and documentation for more details.

<details>
<summary>Wearables Import Instructions</summary>

- **Apple Health:** Export your plan as a Health-compatible CSV file. Import into Apple Health using the Shortcuts app or a 3rd-party tool (e.g., Health Importer). Map columns to "Running" workouts as needed.
- **Google Fit:** Export your plan as a Google Fit CSV file. Import into Google Fit using the web interface or a compatible app.
- **Strava/Runkeeper:** Export your plan directly to Strava or Runkeeper by entering your API token at the prompt. Each session will be uploaded as a planned activity. Your token is used only for export and is not stored.

See the tool README for more details and troubleshooting tips.

</details>

---

# C25K Calendar Creator (GUI Edition)

## Quick Start (GUI Only)

- **Install dependencies:**
  - Run `pip install -r requirements.txt` to install all required packages (PyQt6, openpyxl, requests, qrcode[pil], reportlab).
- **Launch the PyQt6 GUI:**
  - Run `python c25k_ics_generator.py` to launch the GUI.
  - All plan creation, export, and accessibility features are available via the GUI.
  - The GUI is accessible, user-friendly, and supports all export types (ICS, CSV, JSON, Google Fit, Markdown, Strava/Runkeeper, Apple Health, PDF, QR, and Excel tracker).

- **Persistent Preferences:**
  - Your settings (name, age, weight, accessibility, etc.) are saved automatically to `.c25k_prefs.json` in your home directory.
  - Click "Save Preferences" in the GUI to save your current settings. They will be restored next time you launch the app.

- **Accessibility:**
  - All accessibility features (high-contrast, large font, dyslexia font, light mode, screen reader, increased spacing, focus highlight) are grouped in a dedicated Accessibility flyout in the GUI.
  - Accessibility options apply to all exports and the GUI itself.

- **Onboarding & Help:**
  - On first launch, a welcome dialog explains the workflow and accessibility options.
  - A Help menu provides access to About and Screenshots.

- **Feedback:**
  - Use the "Send Feedback" button in the GUI to submit suggestions or issues. Feedback is saved locally for privacy.

- **Export Success Dialogs:**
  - After each export, a dialog confirms success and shows a clickable path to the output file.

- **Calendar Widget:**
  - The right side of the GUI features a visual calendar that highlights only actual workout days, skipping rest days.
  - Milestone days (end of each week) are color-coded gold, and tooltips are shown for each workout/milestone day.
  - Click any highlighted day to see session details in a popup.

- **Screenshots:**
  - Use the Help menu to view screenshots of the GUI. (Add your own screenshots to the `screenshots/` folder.)



- **Advanced Features:**
  - All export types, analytics, and accessibility features are available from the GUI.
  - See the tool README (`c25k_ics_generator_readme.md`) for full details on export formats, analytics, and advanced options.

---

**Platform Support:**

- The GUI is cross-platform and works on Windows, macOS, and Linux. If you encounter issues with PyQt6 installation, see the troubleshooting section below.

---

**Troubleshooting:**

- If you see errors about missing modules, run `pip install -r requirements.txt`.
- For PyQt6 installation issues on Linux, you may need to install system Qt libraries (see PyQt6 docs).
- If you have permission issues saving preferences, ensure you have write access to your home directory.
- For OpenWeatherMap API errors, check your API key and internet connection.
- For any other issues, see the tool README or open an issue on GitHub.

---

**Accessibility:**

- High-contrast mode (GUI, Markdown, Excel, PDF)
- Large font and dyslexia-friendly font options (Comic Sans MS or OpenDyslexic if available)
- Semantic headings and ARIA roles in Markdown export
- PDF export includes an explicit accessibility note, semantic headings, and high-contrast/large font/dyslexia-friendly font options
- Screen reader compatibility: Markdown and Excel exports are optimized for screen readers (avoid merged cells, clear headers, semantic structure). PDF accessibility is improved but may be limited by PDF readers—see the accessibility note in the PDF export for details.
- All accessibility features are documented in the README and in the Excel tracker’s "Macros & Instructions" sheet.

---

## Screenshots

*Add screenshots or a GIF of the GUI here for visual reference. The GUI now features onboarding, a Help menu, feedback dialog, export success dialogs, and a polished calendar widget with color-coded milestones and tooltips.*

---

## Contributing

Contributions are welcome! Please open an issue or pull request on GitHub. See the tool README for guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
