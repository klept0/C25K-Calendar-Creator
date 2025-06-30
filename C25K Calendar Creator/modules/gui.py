import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from typing import Any, Dict

# Import i18n dictionary and validation from main
from ..c25k_ics_generator import LANG_DICT, validate_user_input, get_output_dir, get_workout_plan, create_progress_tracker, export_csv, export_json, export_google_fit_csv, export_markdown_checklist

try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False

try:
    from c25k_utils.mobile_export import export_to_mobile_app, export_apple_health_csv
except ImportError:
    def export_to_mobile_app(*a, **kw):
        pass
    def export_apple_health_csv(*a, **kw):
        pass

def main_gui():
    # ...existing code for main_gui() from c25k_ics_generator.py...
    pass
