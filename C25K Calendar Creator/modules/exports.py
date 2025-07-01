import csv
import json
from typing import Any, Dict, List


def export_csv(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the plan to a CSV file."""
    if not plan:
        return
    keys = plan[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(plan)


def export_json(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the plan to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)


def export_google_fit_csv(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the plan to a Google Fit-compatible CSV file."""
    if not plan:
        return
    fieldnames = [
        "Title",
        "Description",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "All Day Event",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for session in plan:
            writer.writerow(
                {
                    "Title": session.get("title", ""),
                    "Description": session.get("description", ""),
                    "Start Date": session.get("date", ""),
                    "Start Time": session.get("start_time", ""),
                    "End Date": session.get("date", ""),
                    "End Time": session.get("end_time", ""),
                    "All Day Event": "False",
                }
            )


def export_markdown_checklist(plan: List[Dict[str, Any]], filename: str) -> None:
    """Export the plan as a Markdown checklist."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# C25K Plan Checklist\n\n")
        for session in plan:
            title = session.get("title", "")
            date = session.get("date", "")
            f.write(f"- [ ] {date}: {title}\n")
