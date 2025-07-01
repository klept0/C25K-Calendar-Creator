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
    if not plan:
        return
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# 🏃‍♀️ C25K Training Plan Checklist\n\n")
        
        current_week = None
        for session in plan:
            week = session.get("week", 1)
            if week != current_week:
                f.write(f"\n## Week {week}\n\n")
                current_week = week
            
            f.write(f"- [ ] **{session.get('title', 'Training Session')}** - {session.get('date', 'TBD')}\n")
            f.write(f"  - {session.get('description', 'Training session')}\n")
            f.write(f"  - Duration: ~{session.get('duration', 30)} minutes\n\n")


class ExportManager:
    """Centralized export manager for all formats"""
    
    def __init__(self):
        self._check_advanced_features()
    
    def _check_advanced_features(self):
        """Check if advanced features are available"""
        try:
            from .advanced_exports import AdvancedExporter
            from .api_integrations import APIManager
            from .internationalization import InternationalizationManager
            
            self.advanced_exporter = AdvancedExporter()
            self.api_manager = APIManager()
            self.i18n_manager = InternationalizationManager()
            self.advanced_available = True
        except ImportError:
            self.advanced_available = False
            print("Advanced features not available. Install: pip install qrcode[pil] reportlab requests")
    
    def export_plan(self, plan_data: Dict[str, Any], export_format: str, filename: str, **kwargs) -> bool:
        """Export plan in the specified format, respecting integration preferences."""
        try:
            sessions = plan_data.get('sessions', [])

            # Helper to check integration preferences
            def integration_enabled(service: str) -> bool:
                import os, json
                prefs_path = os.path.join(os.path.expanduser("~"), ".c25k_prefs.json")
                if not os.path.exists(prefs_path):
                    return True
                try:
                    with open(prefs_path, "r", encoding="utf-8") as f:
                        prefs = json.load(f)
                    key_map = {
                        "strava": "strava_enabled",
                        "runkeeper": "runkeeper_enabled",
                        "garmin": "garmin_enabled",
                        "intervals.icu": "intervals_enabled",
                        "weather": "weather_enabled",
                    }
                    pref_key = key_map.get(service.lower())
                    if pref_key is not None:
                        return prefs.get(pref_key, True)
                except Exception:
                    return True
                return True

            if export_format.lower() == 'csv':
                export_csv(sessions, filename)
                return True
            elif export_format.lower() == 'json':
                export_json(sessions, filename)
                return True
            elif export_format.lower() == 'google_fit':
                export_google_fit_csv(sessions, filename)
                return True
            elif export_format.lower() == 'markdown':
                export_markdown_checklist(sessions, filename)
                return True
            elif export_format.lower() == 'pdf' and self.advanced_available:
                return self.advanced_exporter.export_comprehensive_pdf(plan_data, filename)
            elif export_format.lower() == 'qr' and self.advanced_available:
                results = self.advanced_exporter.export_with_qr_codes(plan_data, filename.replace('.png', ''))
                return any(results.values())
            elif export_format.lower() in ['strava', 'runkeeper', 'garmin', 'intervals.icu'] and self.advanced_available:
                if not integration_enabled(export_format.lower()):
                    print(f"Integration for {export_format} is disabled in preferences.")
                    return False
                from .api_integrations import convert_c25k_plan_to_workouts
                workouts = convert_c25k_plan_to_workouts(plan_data)
                return self.api_manager.export_to_platform(export_format.lower(), workouts)
            elif export_format.lower() == 'weather' and self.advanced_available:
                if not integration_enabled('weather'):
                    print("Weather integration is disabled in preferences.")
                    return False
                # Weather export logic would go here
                return True
            else:
                return False
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def get_available_formats(self) -> List[str]:
        """Get list of available export formats"""
        basic_formats = ['csv', 'json', 'google_fit', 'markdown']
        
        if self.advanced_available:
            advanced_formats = ['pdf', 'qr', 'strava', 'runkeeper', 'garmin', 'intervals.icu']
            return basic_formats + advanced_formats
        
        return basic_formats
    
    def get_format_descriptions(self) -> Dict[str, str]:
        """Get descriptions of available export formats"""
        descriptions = {
            'csv': 'Spreadsheet format for Excel, Google Sheets, Numbers',
            'json': 'Structured data format for developers and APIs',
            'google_fit': 'CSV format optimized for Google Fit import',
            'markdown': 'Printable checklist format'
        }
        
        if self.advanced_available:
            descriptions.update({
                'pdf': 'Comprehensive training guide with tips and tracking',
                'qr': 'QR codes for easy plan sharing and mobile access',
                'strava': 'Direct upload to Strava training calendar',
                'runkeeper': 'Direct upload to RunKeeper',
                'garmin': 'Direct upload to Garmin Connect',
                'intervals.icu': 'Structured workouts for intervals.icu'
            })
        
        return descriptions


# Create a global export manager instance
export_manager = ExportManager()
