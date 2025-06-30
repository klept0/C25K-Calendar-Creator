from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox
)
import sys


import os
import json  # used for preferences

class C25KPyQtGUI(QWidget):
    PREFS_FILE = os.path.join(os.path.expanduser("~"), ".c25k_prefs.json")

    def __init__(self, submit_callback=None):
        super().__init__()
        self.submit_callback = submit_callback
        self.setWindowTitle("C25K Calendar Creator")
        self.prefs = self.load_preferences()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Name
        self.name_edit = QLineEdit()
        self.name_edit.setToolTip("Enter your name (required)")
        self.name_edit.setText(self.prefs.get("name", ""))
        layout.addLayout(self._row("Name", self.name_edit))
        # Age
        self.age_spin = QSpinBox()
        self.age_spin.setRange(5, 120)
        self.age_spin.setValue(self.prefs.get("age", 30))
        self.age_spin.setToolTip("Enter your age (5-120)")
        layout.addLayout(self._row("Age", self.age_spin))
        # Weight
        self.weight_spin = QSpinBox()
        self.weight_label = QLabel("Weight (kg)")
        self.weight_spin.setRange(30, 300)
        self.weight_spin.setValue(self.prefs.get("weight", 70))
        self.weight_spin.setToolTip("Enter your weight in kg (30-300)")
        layout.addLayout(self._row(self.weight_label, self.weight_spin))
        # Gender
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["male", "female", "other"])
        gender_idx = self.gender_combo.findText(self.prefs.get("gender", "male"))
        self.gender_combo.setCurrentIndex(gender_idx if gender_idx >= 0 else 0)
        self.gender_combo.setToolTip("Select your gender")
        layout.addLayout(self._row("Gender", self.gender_combo))
        # Units
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Imperial (i)", "Metric (m)"])
        self.unit_combo.setToolTip("Choose units: Imperial or Metric")
        self.unit_combo.currentIndexChanged.connect(self.update_weight_unit)
        self.unit_combo.setCurrentIndex(0 if self.prefs.get("unit", "i") == "i" else 1)
        layout.addLayout(self._row("Units", self.unit_combo))

        # Accessibility Options (systematic, in a QGroupBox flyout)
        # (QGroupBox, QVBoxLayout, QPushButton already imported at top)
        acc_group = QGroupBox("Accessibility Options")
        acc_layout = QVBoxLayout()
        # High Contrast
        self.high_contrast = QCheckBox("High Contrast")
        self.high_contrast.setToolTip("Enable high contrast mode for better visibility.")
        self.high_contrast.setChecked(self.prefs.get("high_contrast", False))
        # Large Font
        self.large_font = QCheckBox("Large Font")
        self.large_font.setToolTip("Increase font size for readability.")
        self.large_font.setChecked(self.prefs.get("large_font", False))
        # Dyslexia Font
        self.dyslexia_font = QCheckBox("Dyslexia Font")
        self.dyslexia_font.setToolTip("Use a dyslexia-friendly font (Comic Sans MS).")
        self.dyslexia_font.setChecked(self.prefs.get("dyslexia_font", False))
        # Light Mode
        self.light_mode = QCheckBox("Light Mode")
        self.light_mode.setToolTip("Enable a light color scheme for the app.")
        self.light_mode.setChecked(self.prefs.get("light_mode", False))
        self.light_mode.stateChanged.connect(self.apply_palette)
        # Screen Reader Mode
        self.screen_reader = QCheckBox("Screen Reader Mode")
        self.screen_reader.setToolTip("Enable extra descriptions for screen readers.")
        self.screen_reader.setChecked(self.prefs.get("screen_reader", False))
        # Increased Spacing
        self.increased_spacing = QCheckBox("Increased Spacing")
        self.increased_spacing.setToolTip("Add extra spacing between form elements.")
        self.increased_spacing.setChecked(self.prefs.get("increased_spacing", False))
        # Focus Highlight
        self.focus_highlight = QCheckBox("Focus Highlight")
        self.focus_highlight.setToolTip("Highlight focused fields for keyboard navigation.")
        self.focus_highlight.setChecked(self.prefs.get("focus_highlight", False))
        # Reset Button
        reset_btn = QPushButton("Reset Accessibility Settings")
        reset_btn.setToolTip("Reset all accessibility options to default.")
        reset_btn.clicked.connect(self.reset_accessibility)
        # Add all systematically
        acc_layout.addWidget(self.high_contrast)
        acc_layout.addWidget(self.large_font)
        acc_layout.addWidget(self.dyslexia_font)
        acc_layout.addWidget(self.light_mode)
        acc_layout.addWidget(self.screen_reader)
        acc_layout.addWidget(self.increased_spacing)
        acc_layout.addWidget(self.focus_highlight)
        acc_layout.addWidget(reset_btn)
        acc_group.setLayout(acc_layout)
        layout.addWidget(acc_group)

        # Save/Restore Preferences Button
        save_btn = QPushButton("Save Preferences")
        save_btn.setToolTip("Save your current settings as default.")
        save_btn.clicked.connect(self.save_preferences)
        layout.addWidget(save_btn)
    def save_preferences(self):
        prefs = {
            "name": self.name_edit.text(),
            "age": self.age_spin.value(),
            "weight": self.weight_spin.value(),
            "gender": self.gender_combo.currentText(),
            "unit": "i" if self.unit_combo.currentIndex() == 0 else "m",
            "high_contrast": self.high_contrast.isChecked(),
            "large_font": self.large_font.isChecked(),
            "dyslexia_font": self.dyslexia_font.isChecked(),
            "light_mode": self.light_mode.isChecked(),
            "screen_reader": self.screen_reader.isChecked(),
            "increased_spacing": self.increased_spacing.isChecked(),
            "focus_highlight": self.focus_highlight.isChecked(),
        }
        try:
            with open(self.PREFS_FILE, "w", encoding="utf-8") as f:
                self.json.dump(prefs, f, indent=2)
            QMessageBox.information(self, "Preferences Saved", "Your preferences have been saved and will be restored next time.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save preferences: {e}")

    def load_preferences(self):
        try:
            if self.os.path.exists(self.PREFS_FILE):
                with open(self.PREFS_FILE, "r", encoding="utf-8") as f:
                    return self.json.load(f)
        except Exception:
            pass
        return {}

    def update_weight_unit(self):
        # Update label and tooltip for weight based on selected unit
        if self.unit_combo.currentIndex() == 0:
            # Imperial
            self.weight_label.setText("Weight (lbs)")
            self.weight_spin.setToolTip("Enter your weight in lbs (65-660)")
            self.weight_spin.setRange(65, 660)
            if self.weight_spin.value() < 65 or self.weight_spin.value() > 660:
                self.weight_spin.setValue(150)
        else:
            # Metric
            self.weight_label.setText("Weight (kg)")
            self.weight_spin.setToolTip("Enter your weight in kg (30-300)")
            self.weight_spin.setRange(30, 300)
            if self.weight_spin.value() < 30 or self.weight_spin.value() > 300:
                self.weight_spin.setValue(70)

    def show_help(self):
        QMessageBox.information(self, "About C25K Calendar Creator",
            """
C25K Calendar Creator (PyQt6)
Create a personalized Couch to 5K training plan and export it in various formats.

Fields:
- Name, Age, Weight, Gender: Personal info for plan customization.
- Units: Imperial or Metric.
- Weeks/Days: Plan duration and frequency.
- Start Date/Time: When your plan begins.
- Export Format: Choose your preferred output.
- Accessibility: Enable options for better readability.
- Anonymize: Remove personal info from exports.

For help, visit the README or contact the author.
""")

    def _row(self, label, widget):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        row.addWidget(widget)
        return row

    def submit(self):
        import os
        try:
            # Validate required fields
            if not self.name_edit.text().strip():
                QMessageBox.critical(self, "Input Error", "Name is required.")
                return
            if not self.time_edit.text().strip():
                QMessageBox.critical(self, "Input Error", "Session time is required.")
                return
            # Map export combo to internal code
            export_map = {
                0: "i",  # ICS
                1: "c",  # CSV
                2: "j",  # JSON
                3: "g",  # Google Fit
                4: "m",  # Markdown
                5: "s",  # Strava/Runkeeper
                6: "a",  # Apple Health
            }
            export_code = export_map.get(self.export_combo.currentIndex(), "i")
            # Map units
            unit_code = "i" if self.unit_combo.currentIndex() == 0 else "m"
            user_input = {
                "name": self.name_edit.text(),
                "age": self.age_spin.value(),
                "weight": self.weight_spin.value(),
                "weight_unit": unit_code,
                "gender": self.gender_combo.currentText(),
                "unit": unit_code,
                "weeks": self.weeks_spin.value(),
                "days_per_week": self.days_spin.value(),
                "start_day": self.start_date.date().toPyDate(),
                "hour": None,
                "minute": None,
                "lang": "e",
                "export": export_code,
                "goal": "",
                "high_contrast": self.high_contrast.isChecked(),
                "large_font": self.large_font.isChecked(),
                "dyslexia_font": self.dyslexia_font.isChecked(),
                "email": self.email_edit.text(),
                "location": self.location_edit.text(),
                "alert_minutes": 30,
                "rest_days": ["Sat", "Sun"],
                "anonymize": self.anonymize.isChecked(),
            }
            # Parse time
            try:
                hour, minute = map(int, self.time_edit.text().split(":"))
                user_input["hour"] = hour
                user_input["minute"] = minute
            except Exception:
                QMessageBox.critical(self, "Input Error", "Session time must be in HH:MM format.")
                return
            # Import main logic from c25k_ics_generator
            import importlib.util
            main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "c25k_ics_generator.py"))
            spec = importlib.util.spec_from_file_location("c25k_main", main_path)
            if spec is None or spec.loader is None:
                QMessageBox.critical(self, "Error", "Could not load main logic (c25k_ics_generator.py not found or import failed).")
                return
            c25k_main = importlib.util.module_from_spec(spec)
            sys.modules["c25k_main"] = c25k_main
            spec.loader.exec_module(c25k_main)
            # Generate plan and outputs
            plan = c25k_main.get_workout_plan(user_input)
            outdir = c25k_main.get_output_dir(user_input)
            # Export logic for all types
            if export_code == "i":
                c25k_main.generate_ics(plan, user_input["start_day"], user_input["hour"], user_input["minute"], user_input["alert_minutes"], outdir)
            elif export_code == "c":
                c25k_main.export_csv(plan, os.path.join(outdir, "Couch_to_5K_Plan.csv"))
            elif export_code == "j":
                c25k_main.export_json(plan, os.path.join(outdir, "Couch_to_5K_Plan.json"))
            elif export_code == "g":
                c25k_main.export_google_fit_csv(plan, os.path.join(outdir, "Couch_to_5K_GoogleFit.csv"))
            elif export_code == "m":
                c25k_main.export_markdown_checklist(plan, os.path.join(outdir, "Couch_to_5K_Checklist.md"))
            elif export_code == "s":
                if hasattr(c25k_main, "export_strava_runkeeper_csv"):
                    c25k_main.export_strava_runkeeper_csv(plan, os.path.join(outdir, "Couch_to_5K_Strava_Runkeeper.csv"))
                else:
                    QMessageBox.warning(self, "Export Not Available", "Strava/Runkeeper export is not implemented.")
            elif export_code == "a":
                if hasattr(c25k_main, "export_apple_health_csv"):
                    c25k_main.export_apple_health_csv(plan, os.path.join(outdir, "Couch_to_5K_Apple_Health.csv"))
                else:
                    QMessageBox.warning(self, "Export Not Available", "Apple Health export is not implemented.")
            # Always create progress tracker
            c25k_main.create_progress_tracker(user_input, outdir)
            QMessageBox.information(self, "Success", f"Plan and exports generated in: {outdir}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def apply_palette(self):
        # Only import if available (for linting environments)
        QPalette = QColor = None
        try:
            from PyQt6.QtGui import QPalette as _QPalette, QColor as _QColor
            QPalette = _QPalette
            QColor = _QColor
        except ImportError:
            pass
        if QPalette is None or QColor is None:
            return
        app = QApplication.instance()
        if self.light_mode.isChecked():
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Base, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
            app.setPalette(palette)
        else:
            app.setPalette(app.style().standardPalette())

    def reset_accessibility(self):
        self.high_contrast.setChecked(False)
        self.large_font.setChecked(False)
        self.dyslexia_font.setChecked(False)
        self.light_mode.setChecked(False)
        self.screen_reader.setChecked(False)
        self.increased_spacing.setChecked(False)
        self.focus_highlight.setChecked(False)
        self.apply_palette()

def run_pyqt_gui(submit_callback=None):
    app = QApplication(sys.argv)
    win = C25KPyQtGUI(submit_callback)
    win.show()
    sys.exit(app.exec())
