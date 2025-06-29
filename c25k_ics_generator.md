# Couch to 5K ICS Generator

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

This script generates a calendar file (.ics) for the popular "Couch to 5K" running program, tailored for users with hypertension. The generated calendar will have three workout reminders per week (Monday, Wednesday, Friday) for 10 weeks, each session scheduled at 7:00 AM for 30 minutes. The plan is further customized based on your age, weight, and gender.

## Features

- **Customizable Start Date:** Easily set your preferred program start date.
- **Personalized Plan:** Adjusts session duration for older or heavier users.
- **Health Reminder:** Includes a note to monitor health and consult a doctor if needed.
- **Ready-to-Import:** Produces a standard `.ics` file compatible with Google Calendar, Apple Calendar, Outlook, and others.

## Usage

1. **Run the Script:**
   - Make sure you have Python 3 installed.
   - Run the script:
     ```bash
     python3 c25k_ics_generator.py
     ```
2. **Enter Your Information:**
   - The script will prompt you for your age, weight (in kg), and gender (male/female).
   - If any information is missing or invalid, the script will not generate the calendar.
3. **Import the Calendar:**
   - Locate the generated `Couch_to_5K_Reminders.ics` file.
   - Import it into your preferred calendar application.

## Example

To start the program on July 15, 2025, set in the script:

```python
start_day = datetime(2025, 7, 15)
```

## Customization

- **Session Time:** Change the `hour` and `minute` in the script to adjust workout times.
- **Days per Week:** Modify the `day_offset` list to change which days sessions occur.
- **Workout Duration:** The script automatically reduces session duration for users aged 60+ or weighing 100kg+.

## Disclaimer

---

**DISCLAIMER: This script is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your healthcare provider before starting any new exercise program, especially if you have hypertension or other pre-existing health conditions. Use this script at your own risk. The author assumes no responsibility for any injury or health issues that may result from using this script.**

---

**Author:** [klept0]
**License:** MIT
