#!/usr/bin/env python3
"""
Couch to 5K ICS Generator

DISCLAIMER: This script is for informational purposes only and is not a
substitute for professional medical advice, diagnosis, or treatment.
Always consult your healthcare provider before starting any new exercise
program, especially if you have hypertension or other pre-existing health
conditions. Use this script at your own risk. The author assumes no
responsibility for any injury or health issues that may result from using
this script.

Medical recommendations and plan structure are based on:
- NHS Couch to 5K:
  https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/
- CDC Physical Activity Guidelines:
  https://www.cdc.gov/physicalactivity/basics/index.htm
- American Heart Association:
  https://www.heart.org/en/healthy-living/fitness/fitness-basics

C25K Calendar Creator – Main Entrypoint

All logic is now modularized and accessible via the PyQt6 GUI only.
Legacy CLI and Tkinter code has been removed for clarity and maintainability.

For advanced export, analytics, and accessibility features, see the modules and README.
"""

if __name__ == "__main__":
    from modules.pyqt_gui import run_pyqt_gui

    run_pyqt_gui()
