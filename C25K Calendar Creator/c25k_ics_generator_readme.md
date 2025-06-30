# Couch to 5K ICS Generator

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

This script generates a personalized Couch to 5K calendar (.ics) file, tailored for users with hypertension. It customizes the workout plan based on your age, weight, gender, preferred language, session start time, and personal goal. The script supports multiple export formats for use with Apple/Google calendars, Google Fit, and other platforms. It also generates a Markdown checklist and an advanced Excel progress tracker for tracking progress.

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
  - **Excel progress tracker** with advanced macros and visual cues
- **Hydration and Safety Reminders:** Each workout includes hydration and safety notes.
- **Beginner Tips:** Each day includes a motivational or safety tip (based on NHS, CDC, and AHA guidance).
- **Rest Days:** Rest days are included in all exports and the checklist.
- **Personal Goal:** Option to set a personal goal, included in the checklist.
- **Resource Link:** Checklist includes a link to a reputable C25K guide.
- **Customizable Alerts for ICS:** Set a custom notification time (in minutes) before each session when exporting to ICS. The calendar file will include a notification (VALARM) for each workout event.
- **Advanced Excel Progress Tracker:** Automatically generated with all macros, formulas, and visual cues. Macros and instructions are included in a dedicated sheet. Formatting is optimized for readability and accessibility.
- **Community/Sharing Export:** Instantly generate a Markdown summary and an email draft of your plan, both formatted for easy sharing. The Markdown file is suitable for social media or group sharing, and the email draft is ready to send to friends or a support group. Both are saved in your output folder. No data is sent to any server; all files are generated locally.
- **QR Code Export:** Instantly generate a QR code image containing a detailed summary of your C25K plan (name, start date, goal, weeks, days/week, and all workouts/tips). The QR code is:
  - Saved as both a PNG image and a Markdown file with alt text and the full plan summary for easy sharing and accessibility
  - Larger and high-contrast if accessibility options are enabled
  - Includes a shareable link if provided
  - **Requires:** `qrcode[pil]` Python package (`pip install qrcode[pil]`).

## Defaults

- **Units:** Imperial (lbs, °F) unless Metric is selected
- **Session Start Time:** 07:00 (7:00 AM)
- **Language:** English
- **Plan Length:** 10 weeks, 3 days per week
- **Start Date:** July 15, 2025 (if not specified)
- **Alert Time (ICS):** 30 minutes before session
- **Accessibility:** Off (can enable high-contrast or large font)
- **Personal Goal:** Optional (blank by default)
- **Weather:** Fahrenheit (°F) for all weather integration
- **Output Directory:** `created/<name>-<age>-<start_date>/`
- **Progress Tracker:** Excel file auto-generated and macros auto-inserted

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
     - Export format (ICS, CSV, JSON, Google Fit CSV, Excel, Markdown)
     - **Alert time before session (minutes, for ICS export only)**
     - Personal goal (optional)
   - If any information is missing or invalid, the script will not generate the calendar.
3. **Import the Calendar or Data:**
   - Locate the generated file (e.g., `Couch_to_5K_Reminders.ics`, `.csv`, `.json`, `Couch_to_5K_GoogleFit.csv`, `Couch_to_5K_Checklist.md`, or your Excel tracker).
   - Import it into your preferred calendar, health application, or use the checklist/tracker for progress.

## Example

To start the program on July 15, 2025, at 7:00 AM, set in the script or at the prompt:

```python
start_day = datetime(2025, 7, 15)
```

## Customization

- **Session Time:** Enter your preferred session time at the prompt.
- **Language:** Choose English or Spanish for all workout instructions.
- **Export Format:** Choose the format that best fits your needs (ICS, CSV, JSON, Google Fit CSV, Markdown, Excel).
- **Workout Duration:** The script automatically reduces session duration for users aged 60+ or weighing 100kg+.
- **Personal Goal:** Enter a goal to keep yourself motivated.
- **Plan Length:** Choose number of weeks and days per week for your plan.
- **Accessibility:** Enable high-contrast or large-font options for Markdown and Excel outputs.

## Advanced Features

- **Dynamic Start Date:** Start on a specific date or next Monday.
- **Reminders:** Optionally send real email reminders for each workout session. Configure your SMTP server (Gmail, Outlook, etc.) at the prompt or via environment variables. Your credentials are used only to send reminders and are not stored.
- **Mobile App Export:** Export your plan directly to Strava or Runkeeper. Enter your API access token at the prompt. Each session will be uploaded as a planned activity. Your token is used only for export and is not stored.
- **Apple Health Export:** Export your plan as a Health-compatible CSV file. Import into Apple Health using the Shortcuts app or a 3rd-party tool (see below).
- **Voice Prompts Export:** Export session-by-session voice/text prompts as a text script and (optionally) audio files. Audio requires the `gTTS` package. Supports English and Spanish.
- **Community/Sharing Export:** Export a shareable summary of your plan as Markdown and an email draft. Share with friends, a group, or on social media.
- **Weather Suggestions:** Get a real, actionable weather suggestion for your first workout based on the forecast for your city or ZIP code. The script provides advice (e.g., "Great weather for running!", "Rain expected, consider rescheduling or wear a rain jacket") using real-time data. If no forecast is available, a fallback message is shown. See the Weather Integration section below for setup.
- **Progress Tracking:** Excel tracker is auto-generated and includes all macros, formulas, and visual cues. Macros are auto-inserted using the included macro inserter script.
- **PDF Export:** Export plan as a visually rich, accessible PDF. The PDF includes:
  - Cover page with your name, age, start date, and personal goal
  - Full plan table (week, day, date, workout, tip, weather, motivation, rest day)
  - Accessibility options (large font, dyslexia-friendly font, high-contrast)
  - Motivational quotes section
  - Resource links and privacy note
  - All content is formatted for readability and printability
  - **Requires:** `reportlab` Python package (`pip install reportlab`)
- **QR Code Export:** Instantly generate a QR code image containing a detailed summary of your C25K plan (name, start date, goal, weeks, days/week, and all workouts/tips). The QR code is:
  - Saved as both a PNG image and a Markdown file with alt text and the full plan summary for easy sharing and accessibility
  - Larger and high-contrast if accessibility options are enabled
  - Includes a shareable link if provided
  - **Requires:** `qrcode[pil]` Python package (`pip install qrcode[pil]`).

### Data Privacy & Security (New!)

- **Privacy Prompt:** When you run the script, you will be prompted to choose whether to anonymize your data in all exports. If you select this option, your name and email will be replaced with generic values (e.g., "Anonymous") in all generated files.
- **No Data Sent:** All data processing and export generation happens locally on your device. No personal data, credentials, or tokens are sent to any server or third party.
- **Anonymization Option:** If you enable anonymization, your name and email will not appear in any exported file (ICS, CSV, JSON, Excel, Markdown, PDF, QR, etc.).
- **Privacy Note in Exports:** Every export file includes a privacy note explaining that your data is only used locally and never sent or stored externally. See the privacy note in each file for details.
- **Credentials & Tokens:** Any credentials or API tokens (for email reminders, Strava, Runkeeper, etc.) are used in-memory only and never saved to disk or sent anywhere except the intended service for export.
- **Full Details:** For more information, see the privacy note in each export and the script source code.

---

### Voice Prompts Export (New!)

- Choose the Voice Prompts export option at the prompt to generate a text script and (optionally) audio files for each session.
- The text script is always generated. Audio files require the `gTTS` package (`pip install gTTS`).
- Supports English and Spanish. Accessibility options (large font, dyslexia-friendly font) apply to the text script.
- **Privacy:** No data is sent to any server; all files are generated locally. If anonymization is enabled, your name/email will not appear in the export.
- **Usage:**
  1. Select the Voice Prompts export option when prompted.
  2. Find the generated text script and (if available) audio files in your output folder.
  3. Play the audio files on your device or use the text script for manual prompts.
- **Privacy:** No data is sent to any server; all files are generated locally. If anonymization is enabled, your name/email will not appear in the export.

### Apple Health Export (New!)

- Choose the Apple Health export option at the prompt to generate a Health-compatible CSV file.
- The CSV includes columns for Type, Start, End, Distance, Duration, and Source.
- **Import Instructions:**
  1. Open the Shortcuts app on your iPhone.
  2. Use a shortcut or 3rd-party app (e.g., Health Importer) to import the CSV into Apple Health.
  3. You may need to map columns to "Running" workouts and adjust distance/duration as needed.
- **Privacy:** No data is sent to Apple or any server; the CSV is generated locally. If anonymization is enabled, your name/email will not appear in the export.

### Community/Sharing Export (Updated!)

- Choose the Community/Sharing export option at the prompt to generate a Markdown summary and an email draft of your plan.
- The Markdown summary is formatted for easy sharing on social media, with your name, goal, and a full session-by-session breakdown.
- The email draft is pre-filled with a friendly invitation and your full plan, ready to copy-paste or send.
- Both files are saved in your output folder for convenience.
- **Privacy:** No data is sent to any server; all files are generated locally. If anonymization is enabled, your name/email will not appear in the export.

### QR Code Export (Updated!)

- Choose the QR Code export option at the prompt to generate a PNG image containing a **detailed summary** of your C25K plan (name, start date, goal, weeks, days/week, and all workouts/tips).
- The QR code is saved in your output folder as both a PNG image and a Markdown file with alt text and the full plan summary for easy sharing and accessibility.
- If accessibility options are enabled, the QR code is larger and high-contrast for easier scanning.
- Optionally, a shareable link can be included in the QR code if provided.
- **Requires:** `qrcode[pil]` Python package (`pip install qrcode[pil]`).
- **Privacy:** No data is sent to any server; all files are generated locally. If anonymization is enabled, your name/email will not appear in the export.

## Using Templates (Save & Load Your Info)

You can save your user information and plan as a template for easy reuse:

1. **Create a Template:**
   - When prompted after entering your info, answer `Y` to "Save your settings as a template for future use?" and provide a template name.
   - Your info and plan will be saved in the `templates/` folder as `<template_name>.json`.

2. **Load a Template:**
   - On future runs, answer `Y` to "Load a saved plan template?" at the start.
   - Select your template by number or name. Your saved info will be loaded automatically.

3. **Edit or Delete Templates:**
   - Templates are stored as JSON files in the `templates/` directory. You can edit them with a text editor or delete them manually if needed.

**Tip:** Templates store your user info (name, age, weight, etc.) and plan settings. This saves time if you want to generate new calendars or trackers with the same info.

## Accessibility Features

- **High-Contrast Mode:** Available for CLI, Markdown, Excel, and PDF exports. PDF and Markdown exports use high-contrast colors for improved visibility if selected.
- **Large Font & Dyslexia-Friendly Font:** All major exports (Markdown checklist, Excel tracker, PDF, and voice prompt scripts) support large font and Comic Sans MS or OpenDyslexic (if available) for easier reading. Enable these options at the prompt.
- **Semantic Structure & ARIA Roles:** Markdown export uses semantic headings and ARIA roles for better screen reader compatibility. Table headers and section headings are clearly marked in all exports.
- **PDF Accessibility:** PDF export includes an explicit accessibility note at the top, semantic headings, and all font/contrast options. Note: PDF accessibility for screen readers is improved, but may be limited by your PDF reader—see the accessibility note in the PDF export for details.
- **Screen Reader Compatibility:** Markdown and Excel exports are optimized for screen readers (avoid merged cells, clear headers, semantic structure). All accessibility features are documented in this README and in the Excel tracker’s "Macros & Instructions" sheet.
- **Accessibility Documentation:** All accessibility features and options are described in this README and in the Excel tracker’s Macros & Instructions sheet.

---

## Excel Progress Tracker & Macros

The Excel progress tracker (`<name>_progress_tracker.xlsx`) is automatically generated in your output folder. It includes:

- **Macros & Instructions Sheet:** All advanced macros, formulas, and usage instructions are included in a dedicated sheet. You can copy-paste or review them directly in Excel.
- **Auto-Insertion:** Macros and formulas are auto-inserted using the included `c25k_excel_macro_inserter.py` script. You can run this script manually if needed.
- **Advanced Visual Cues:** The tracker includes checkmarks, rest day highlighting, overdue alerts, sparklines, milestone badges, weekly progress bars, goal gauge, weather icons/colors, accessibility macro, and notes highlighting.
- **Improved Formatting:** Columns are auto-sized, all cells are wrapped and aligned, code blocks use a monospaced font and shading, and the top row is frozen for easy navigation.
- **Accessibility:** High-contrast and large-font options are available for improved readability.

**Note:** The old CSV-based macros are no longer used. All macros and formulas are now in the Excel file.

## Planned & Upcoming Features

The following features are planned or partially implemented and will be added in future updates:

- **Customizable Plan Templates:** Save and load custom plan templates for different goals or fitness levels. *(Planned)*
- **Advanced Analytics:** In-depth statistics, charts, and insights on your progress and trends. *(Planned)*
- **Wearables Integration:** Direct export/import for popular fitness trackers and smartwatches. *(Planned)*
- **Feedback Loop:** In-app feedback and improvement suggestions based on your progress. *(Planned)*
- **Further Accessibility Polish:** Additional font and style options for Markdown and PDF, improved compatibility with screen readers. *(Planned)*
- **Gamification Enhancements:** More badges, levels, and interactive rewards. *(Planned)*
- **Privacy/Export Options:** More granular control over what data is included in each export. *(Planned)*

If you have suggestions or requests for new features, please open an issue or contact the author.

---

## Feature Implementation Status

All features listed above the 'Planned & Upcoming Features' section are fully implemented and documented, including:

- Data Privacy & Security (privacy prompt, anonymization, privacy note in all exports)
- All advanced export formats (ICS, CSV, JSON, Excel, PDF, Markdown, Google Fit, Apple Health, Strava/Runkeeper, Voice Prompts, QR Code, Community/Sharing)
- Accessibility options (large font, dyslexia-friendly font, high-contrast)
- Adaptive plan logic, custom rest days, motivational quotes, badges, dashboard, and weekly review
- In-app FAQ/help system
- Weather integration and suggestions
- Email reminders (with privacy safeguards)
- All tracker macros, formulas, and visual cues

For details on each feature, see the relevant section above.

---

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

**Tool README:** See `c25k_ics_generator_readme.md` in this folder for full usage, features, and advanced options.

## Weather API Key Setup (OpenWeatherMap)

To enable real weather suggestions for your workouts:

1. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api).
2. **Set your API key as an environment variable (recommended):**

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
