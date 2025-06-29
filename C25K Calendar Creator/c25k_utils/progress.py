"""
c25k_utils/progress.py
Handles progress tracking import and summary generation.
Stub: To be implemented with import and summary logic.
"""

import csv
from typing import List, Dict


def import_progress(file_path: str) -> List[Dict[str, str]]:
    """
    Import progress from a CSV file. Each row should have at least 'week', 'day', 'completed' columns.
    Returns a list of dicts.
    """
    progress = []
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                progress.append(row)
    except FileNotFoundError:
        return []
    return progress


def generate_progress_summary(progress_data: List[Dict[str, str]]) -> str:
    """
    Generate a summary of completed workouts from imported progress data.
    Expects 'completed' column to be 'yes' or 'no'.
    """
    if not progress_data:
        return "No progress data found."
    total = len(progress_data)
    completed = sum(
        1 for row in progress_data if row.get("completed", "").strip().lower() == "yes"
    )
    percent = (completed / total * 100) if total else 0
    return f"Progress: {completed}/{total} sessions completed ({percent:.1f}%)."
