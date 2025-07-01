from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QGroupBox, QCalendarWidget, QFrame, QMenuBar, QMenu, QFileDialog, QTextEdit, QDialog, QDialogButtonBox
)
from PyQt6.QtGui import QAction
import sys


import os
import json  # used for preferences

class C25KPyQtGUI(QWidget):
    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if self.focus_highlight.isChecked() and event.type() == QEvent.Type.FocusIn:
            obj.setStyleSheet(obj.styleSheet() + "; outline: 2px solid #0078d7;")
        elif self.focus_highlight.isChecked() and event.type() == QEvent.Type.FocusOut:
            # Remove only the outline, keep other styles
            obj.setStyleSheet(obj.styleSheet().replace("; outline: 2px solid #0078d7;", ""))
        return super().eventFilter(obj, event)
    def show_onboarding(self):
        steps = [
            ("Welcome to C25K Calendar Creator!", "This app helps you create a personalized Couch to 5K training plan with reminders, exports, and accessibility features."),
            ("Personal Information", "Fill in your name, age, gender, weight, and preferred units. These help customize your plan."),
            ("Plan Settings", "Choose how many weeks, days per week, and your preferred start date and time. Select your export format and (optionally) enter your email for reminders."),
            ("Accessibility Options", "Enable high contrast, large font, dyslexia font, and other options for a more accessible experience."),
            ("Calendar Preview", "The calendar on the right shows your workout schedule. Milestones and rest days are color-coded."),
            ("Export & Feedback", "Click 'Generate Plan and Exports' to create your files. Use the Feedback button to send suggestions or issues.")
        ]
        for title, msg in steps:
            QMessageBox.information(self, title, msg)
    def _set_invalid(self, widget, message=None):
        widget.setStyleSheet("border: 2px solid red;")
        if message:
            widget.setToolTip(message)

    def _set_valid(self, widget, default_tooltip=None):
        widget.setStyleSheet("")
        if default_tooltip:
            widget.setToolTip(default_tooltip)

    def _validate_email(self, email):
        import re
        if not email:
            return True
        return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

    def _validate_fields(self):
        valid = True
        # Name required
        if not self.name_edit.text().strip():
            self._set_invalid(self.name_edit, "Name is required.")
            valid = False
        else:
            self._set_valid(self.name_edit, "Enter your name (required)")
        # Age range
        if not (5 <= self.age_spin.value() <= 120):
            self._set_invalid(self.age_spin, "Age must be between 5 and 120.")
            valid = False
        else:
            self._set_valid(self.age_spin, "Enter your age (5-120)")
        # Email format (if provided)
        email = self.email_edit.text().strip()
        if email and not self._validate_email(email):
            self._set_invalid(self.email_edit, "Invalid email address.")
            valid = False
        else:
            self._set_valid(self.email_edit, "Enter your email for reminders (optional)")
        return valid
    PREFS_FILE = os.path.join(os.path.expanduser("~"), ".c25k_prefs.json")

    def __init__(self, submit_callback=None):
        super().__init__()
        self.submit_callback = submit_callback
        self.setWindowTitle("C25K Calendar Creator")
        self.prefs = self.load_preferences()
        self.init_ui()
        # Onboarding: show welcome dialog on first launch
        if not self.prefs.get("onboarded", False):
            self.show_onboarding()
            self.prefs["onboarded"] = True
            self.save_preferences(silent=True)

    def init_ui(self):
        # Install event filter for focus highlight
        for w in [self.name_edit, self.age_spin, self.unit_combo, self.weight_spin, self.gender_combo, self.weeks_spin, self.days_spin, self.start_date, self.time_edit, self.export_combo, self.email_edit, self.location_edit]:
            w.installEventFilter(self)

        # Screen Reader Mode: set accessible descriptions
        def update_accessible_descriptions():
            if self.screen_reader.isChecked():
                self.name_edit.setAccessibleDescription("Name: Enter your full name. Required.")
                self.age_spin.setAccessibleDescription("Age: Enter your age in years. Required.")
                self.unit_combo.setAccessibleDescription("Units: Select Imperial or Metric units.")
                self.weight_spin.setAccessibleDescription("Weight: Enter your weight in selected units.")
                self.gender_combo.setAccessibleDescription("Gender: Select your gender.")
                self.weeks_spin.setAccessibleDescription("Weeks: Number of weeks for your plan.")
                self.days_spin.setAccessibleDescription("Days per week: Number of workout days per week.")
                self.start_date.setAccessibleDescription("Start Date: Select the date to begin your plan.")
                self.time_edit.setAccessibleDescription("Session Time: Enter the time for your workouts.")
                self.export_combo.setAccessibleDescription("Export Format: Select the file format for export.")
                self.email_edit.setAccessibleDescription("Email: Enter your email for reminders (optional).")
                self.location_edit.setAccessibleDescription("Location: Enter your city or ZIP for weather (optional).")
            else:
                for w in [self.name_edit, self.age_spin, self.unit_combo, self.weight_spin, self.gender_combo, self.weeks_spin, self.days_spin, self.start_date, self.time_edit, self.export_combo, self.email_edit, self.location_edit]:
                    w.setAccessibleDescription("")
        self.screen_reader.stateChanged.connect(lambda _: update_accessible_descriptions())
        update_accessible_descriptions()
        # Preview Export Button
        preview_btn = QPushButton("Preview Export")
        preview_btn.setToolTip("Preview the export file before saving.")
        preview_btn.clicked.connect(self.show_export_preview)
        form_layout.addWidget(preview_btn)
    def show_export_preview(self):
        # Gather user input as in submit()
        from datetime import datetime
        try:
            user = {
                "name": self.name_edit.text(),
                "age": self.age_spin.value(),
                "weight": self.weight_spin.value(),
                "weight_unit": "i" if self.unit_combo.currentIndex() == 0 else "m",
                "gender": self.gender_combo.currentText(),
                "unit": "i" if self.unit_combo.currentIndex() == 0 else "m",
                "weeks": self.weeks_spin.value(),
                "days_per_week": self.days_spin.value(),
                "start_day": self.start_date.date().toPyDate() if hasattr(self.start_date.date(), 'toPyDate') else datetime.now().date(),
                "hour": 7,
                "minute": 0,
                "lang": "e",
                "export": "i",  # Will be mapped below
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
            export_map = {
                0: "i", 1: "c", 2: "j", 3: "g", 4: "m", 5: "s", 6: "a"
            }
            user["export"] = export_map.get(self.export_combo.currentIndex(), "i")
            from C25K_Calendar_Creator import c25k_ics_generator as c25k
            plan = c25k.get_workout_plan(user)
            preview_text = ""
            fmt = user["export"]
            if fmt == "i":
                # ICS preview
                from io import StringIO
                buf = StringIO()
                # Use a modified generate_ics to write to buffer
                ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Couch to 5K//EN\n"
                for session in plan[:3]:
                    event_name = session.get("title", f"C25K Week {session.get('week','?')} Day {session.get('day','?')}")
                    ics_content += f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDESCRIPTION:{session.get('description','')}\nEND:VEVENT\n"
                ics_content += "...\nEND:VCALENDAR"
                preview_text = ics_content
            elif fmt == "c":
                # CSV preview
                import csv
                from io import StringIO
                buf = StringIO()
                writer = csv.DictWriter(buf, fieldnames=plan[0].keys())
                writer.writeheader()
                for row in plan[:3]:
                    writer.writerow(row)
                preview_text = buf.getvalue() + "..."
            elif fmt == "j":
                # JSON preview
                import json
                preview_text = json.dumps(plan[:3], indent=2) + "\n..."
            elif fmt == "m":
                # Markdown preview
                lines = ["# C25K Plan Checklist\n"]
                for session in plan[:3]:
                    title = session.get('title', '')
                    date = session.get('date', '')
                    lines.append(f'- [ ] {date}: {title}')
                preview_text = "\n".join(lines) + "\n..."
            else:
                preview_text = "Preview not available for this format."
            # Show preview in dialog
            dlg = QDialog(self)
            dlg.setWindowTitle("Export Preview")
            layout = QVBoxLayout(dlg)
            label = QLabel("Preview of export file (first 3 entries):")
            layout.addWidget(label)
            text = QTextEdit()
            text.setReadOnly(True)
            text.setPlainText(preview_text)
            layout.addWidget(text)
            btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
            btns.accepted.connect(dlg.accept)
            layout.addWidget(btns)
            dlg.exec()
        except Exception as e:
            QMessageBox.critical(self, "Preview Error", f"Could not generate preview: {e}")
        # Keyboard shortcuts for major actions (set after widgets are created)
        # ...existing code...
        save_btn = QPushButton("Save Preferences")
        save_btn.setToolTip("Save your current settings as default.")
        save_btn.clicked.connect(self.save_preferences)
        form_layout.addWidget(save_btn)

        submit_btn = QPushButton("Generate Plan and Exports")
        submit_btn.setToolTip("Generate your plan and export files")
        submit_btn.clicked.connect(self.submit)
        submit_btn.setShortcut("Alt+E")  # Export/Generate
        form_layout.addWidget(submit_btn)

        feedback_btn.setShortcut("Alt+F")
        about_action = None
        for action in self.menu_bar.actions():
            if action.menu():
                for subaction in action.menu().actions():
                    if subaction.text() == "About":
                        about_action = subaction
                        break
        if about_action:
            about_action.setShortcut("Alt+H")
        # Set tab order for logical navigation
        self.setTabOrder(self.name_edit, self.age_spin)
        self.setTabOrder(self.age_spin, self.unit_combo)
        self.setTabOrder(self.unit_combo, self.weight_spin)
        self.setTabOrder(self.weight_spin, self.gender_combo)
        self.setTabOrder(self.gender_combo, self.weeks_spin)
        self.setTabOrder(self.weeks_spin, self.days_spin)
        self.setTabOrder(self.days_spin, self.start_date)
        self.setTabOrder(self.start_date, self.time_edit)
        self.setTabOrder(self.time_edit, self.export_combo)
        self.setTabOrder(self.export_combo, self.email_edit)
        self.setTabOrder(self.email_edit, self.location_edit)
        self.setTabOrder(self.location_edit, self.anonymize)
        # Real-time validation for required fields
        self.name_edit.textChanged.connect(lambda: self._validate_fields())
        self.age_spin.valueChanged.connect(lambda: self._validate_fields())
        self.email_edit.textChanged.connect(lambda: self._validate_fields())
        # Menu bar (Help, Screenshots, About)
        self.menu_bar = QMenuBar(self)
        help_menu = QMenu("Help", self)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_help)
        screenshots_action = QAction("Screenshots", self)
        screenshots_action.triggered.connect(self.show_screenshots)
        help_menu.addAction(about_action)
        help_menu.addAction(screenshots_action)
        self.menu_bar.addMenu(help_menu)

        # Main horizontal layout: form (left), calendar (right)
        main_layout = QHBoxLayout()
        form_layout = QVBoxLayout()
        form_layout.setMenuBar(self.menu_bar)
        # Feedback Button
        feedback_btn = QPushButton("Send Feedback")
        feedback_btn.setToolTip("Send feedback or suggestions to the developer.")
        feedback_btn.clicked.connect(self.show_feedback_dialog)
        form_layout.addWidget(feedback_btn)


        # --- Personal Information Group ---
        personal_group = QGroupBox("Personal Information")
        personal_layout = QVBoxLayout()
        # Name
        self.name_edit = QLineEdit()
        self.name_edit.setToolTip("Enter your name (required)")
        self.name_edit.setText(self.prefs.get("name", ""))
        personal_layout.addLayout(self._row("Name", self.name_edit))
        # Age
        self.age_spin = QSpinBox()
        self.age_spin.setRange(5, 120)
        self.age_spin.setValue(self.prefs.get("age", 30))
        self.age_spin.setToolTip("Enter your age (5-120)")
        personal_layout.addLayout(self._row("Age", self.age_spin))
        # Units (must be before weight for logic)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Imperial (i)", "Metric (m)"])
        self.unit_combo.setToolTip("Choose units: Imperial or Metric")
        self.unit_combo.setCurrentIndex(0 if self.prefs.get("unit", "i") == "i" else 1)
        self.unit_combo.currentIndexChanged.connect(self.update_weight_unit)
        personal_layout.addLayout(self._row("Units", self.unit_combo))
        # Weight
        self.weight_spin = QSpinBox()
        self.weight_label = QLabel()
        self.update_weight_unit()
        if self.unit_combo.currentIndex() == 0:
            self.weight_spin.setValue(self.prefs.get("weight", 150))
        else:
            self.weight_spin.setValue(self.prefs.get("weight", 70))
        personal_layout.addLayout(self._row(self.weight_label, self.weight_spin))
        # Gender
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["male", "female", "other"])
        gender_idx = self.gender_combo.findText(self.prefs.get("gender", "male"))
        self.gender_combo.setCurrentIndex(gender_idx if gender_idx >= 0 else 0)
        self.gender_combo.setToolTip("Select your gender")
        personal_layout.addLayout(self._row("Gender", self.gender_combo))
        personal_group.setLayout(personal_layout)
        form_layout.addWidget(personal_group)


        # --- Plan Settings Group ---
        plan_group = QGroupBox("Plan Settings")
        plan_layout = QVBoxLayout()
        # Weeks
        self.weeks_spin = QSpinBox()
        self.weeks_spin.setRange(1, 52)
        self.weeks_spin.setValue(self.prefs.get("weeks", 10))
        self.weeks_spin.setToolTip("Number of weeks in your plan (default 10)")
        plan_layout.addLayout(self._row("Weeks", self.weeks_spin))
        # Days per week
        self.days_spin = QSpinBox()
        self.days_spin.setRange(1, 7)
        self.days_spin.setValue(self.prefs.get("days_per_week", 3))
        self.days_spin.setToolTip("Days per week (default 3)")
        plan_layout.addLayout(self._row("Days/Week", self.days_spin))
        # Start Date
        from PyQt6.QtWidgets import QDateEdit
        from PyQt6.QtCore import QDate
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setToolTip("Select your plan start date")
        plan_layout.addLayout(self._row("Start Date", self.start_date))
        # Session Time
        self.time_edit = QLineEdit()
        self.time_edit.setPlaceholderText("07:00")
        self.time_edit.setToolTip("Session start time (HH:MM, 24h)")
        self.time_edit.setText(self.prefs.get("time", "07:00"))
        plan_layout.addLayout(self._row("Session Time", self.time_edit))
        # Export Format
        self.export_combo = QComboBox()
        self.export_combo.addItems([
            "ICS (Calendar)", "CSV", "JSON", "Google Fit CSV", "Markdown", "Strava/Runkeeper", "Apple Health"
        ])
        self.export_combo.setToolTip("Choose export format")
        plan_layout.addLayout(self._row("Export Format", self.export_combo))
        # Email (optional)
        self.email_edit = QLineEdit()
        self.email_edit.setToolTip("Enter your email for reminders (optional)")
        self.email_edit.setText(self.prefs.get("email", ""))
        plan_layout.addLayout(self._row("Email", self.email_edit))
        # Location (optional)
        self.location_edit = QLineEdit()
        self.location_edit.setToolTip("Enter your city or ZIP for weather (optional)")
        self.location_edit.setText(self.prefs.get("location", ""))
        plan_layout.addLayout(self._row("Location", self.location_edit))
        # Anonymize
        self.anonymize = QCheckBox("Anonymize Exports")
        self.anonymize.setToolTip("Remove personal info from all exports. If checked, your name and email will not appear in any export file.")
        self.anonymize.setChecked(self.prefs.get("anonymize", False))
        plan_layout.addWidget(self.anonymize)
        plan_group.setLayout(plan_layout)
        form_layout.addWidget(plan_group)

        # Accessibility Options (systematic, in a QGroupBox flyout)
        acc_group = QGroupBox("Accessibility Options")
        acc_layout = QVBoxLayout()
        self.high_contrast = QCheckBox("High Contrast")
        self.high_contrast.setToolTip("Enable high contrast mode for better visibility.")
        self.high_contrast.setChecked(self.prefs.get("high_contrast", False))
        self.large_font = QCheckBox("Large Font")
        self.large_font.setToolTip("Increase font size for readability.")
        self.large_font.setChecked(self.prefs.get("large_font", False))
        self.dyslexia_font = QCheckBox("Dyslexia Font")
        self.dyslexia_font.setToolTip("Use a dyslexia-friendly font (Comic Sans MS).")
        self.dyslexia_font.setChecked(self.prefs.get("dyslexia_font", False))
        self.light_mode = QCheckBox("Light Mode")
        self.light_mode.setToolTip("Enable a light color scheme for the app.")
        self.light_mode.setChecked(self.prefs.get("light_mode", False))
        self.light_mode.stateChanged.connect(self.apply_palette)
        self.screen_reader = QCheckBox("Screen Reader Mode")
        self.screen_reader.setToolTip("Enable extra descriptions for screen readers.")
        self.screen_reader.setChecked(self.prefs.get("screen_reader", False))
        self.increased_spacing = QCheckBox("Increased Spacing")
        self.increased_spacing.setToolTip("Add extra spacing between form elements.")
        self.increased_spacing.setChecked(self.prefs.get("increased_spacing", False))
        self.focus_highlight = QCheckBox("Focus Highlight")
        self.focus_highlight.setToolTip("Highlight focused fields for keyboard navigation.")
        self.focus_highlight.setChecked(self.prefs.get("focus_highlight", False))
        reset_btn = QPushButton("Reset Accessibility Settings")
        reset_btn.setToolTip("Reset all accessibility options to default.")
        reset_btn.clicked.connect(self.reset_accessibility)
        acc_layout.addWidget(self.high_contrast)
        acc_layout.addWidget(self.large_font)
        acc_layout.addWidget(self.dyslexia_font)
        acc_layout.addWidget(self.light_mode)
        acc_layout.addWidget(self.screen_reader)
        acc_layout.addWidget(self.increased_spacing)
        acc_layout.addWidget(self.focus_highlight)
        acc_layout.addWidget(reset_btn)
        acc_group.setLayout(acc_layout)
        form_layout.addWidget(acc_group)

        # Save/Restore Preferences Button
        save_btn = QPushButton("Save Preferences")
        save_btn.setToolTip("Save your current settings as default.")
        save_btn.clicked.connect(self.save_preferences)
        form_layout.addWidget(save_btn)

        # Submit Button
        submit_btn = QPushButton("Generate Plan and Exports")
        submit_btn.setToolTip("Generate your plan and export files")
        submit_btn.clicked.connect(self.submit)
        form_layout.addWidget(submit_btn)


        # --- Calendar Widget ---
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setToolTip("Visual calendar: workout days will be highlighted after you choose your plan options.")
        self.calendar.setMinimumWidth(350)
        self.calendar.clicked.connect(self.show_calendar_day_details)
        # Add a frame for visual separation
        calendar_frame = QFrame()
        calendar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        calendar_layout = QVBoxLayout()
        calendar_label = QLabel("Workout Calendar Preview")
        calendar_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        calendar_layout.addWidget(calendar_label)
        calendar_layout.addWidget(self.calendar)
        # Add legend below calendar
        legend_layout = QHBoxLayout()
        # Workout day color
        workout_color = QLabel()
        workout_color.setFixedSize(18, 18)
        workout_color.setStyleSheet("background: rgba(0,120,215,0.5); border: 1px solid #888;")
        legend_layout.addWidget(workout_color)
        legend_layout.addWidget(QLabel("Workout Day"))
        # Milestone color
        milestone_color = QLabel()
        milestone_color.setFixedSize(18, 18)
        milestone_color.setStyleSheet("background: rgba(255,215,0,0.7); border: 1px solid #888;")
        legend_layout.addWidget(milestone_color)
        legend_layout.addWidget(QLabel("Milestone (End of Week)"))
        # Rest day color
        rest_color = QLabel()
        rest_color.setFixedSize(18, 18)
        rest_color.setStyleSheet("background: rgba(180,180,180,0.5); border: 1px solid #888;")
        legend_layout.addWidget(rest_color)
        legend_layout.addWidget(QLabel("Rest Day"))
        legend_layout.addStretch(1)
        calendar_layout.addLayout(legend_layout)
        calendar_frame.setLayout(calendar_layout)

        # Add form and calendar to main layout
        main_layout.addLayout(form_layout, stretch=2)
        main_layout.addWidget(calendar_frame, stretch=1)

        self.setLayout(main_layout)

        # Connect signals to update calendar
        self.weeks_spin.valueChanged.connect(self.update_calendar_highlight)
        self.days_spin.valueChanged.connect(self.update_calendar_highlight)
        self.start_date.dateChanged.connect(self.update_calendar_highlight)
        self.unit_combo.currentIndexChanged.connect(self.update_calendar_highlight)
        # Initial highlight
        self.update_calendar_highlight()

    def update_calendar_highlight(self):
        """
        Highlight only the actual workout days, skipping user rest days, on the calendar.
        Add color-coding for milestones and tooltips for each workout day.
        """
        from PyQt6.QtGui import QTextCharFormat, QColor
        from PyQt6.QtCore import Qt
        # Clear all highlights in a wide range
        fmt_clear = QTextCharFormat()
        cal = self.calendar
        for offset in range(-180, 365):
            d = cal.selectedDate().addDays(offset)
            cal.setDateTextFormat(d, fmt_clear)
        # Get user selections
        weeks = self.weeks_spin.value()
        days_per_week = self.days_spin.value()
        start_qdate = self.start_date.date()
        rest_days = self.prefs.get("rest_days", ["Sat", "Sun"])
        weekday_map = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
        # Build workout days list, skipping rest days
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(0, 120, 215, 80))
        fmt.setForeground(QColor(0, 0, 0))
        milestone_fmt = QTextCharFormat()
        milestone_fmt.setBackground(QColor(255, 215, 0, 120))  # Gold for milestones
        milestone_fmt.setForeground(QColor(0, 0, 0))
        rest_fmt = QTextCharFormat()
        rest_fmt.setBackground(QColor(180, 180, 180, 80))
        rest_fmt.setForeground(QColor(80, 80, 80))
        workout_count = 0
        day_ptr = 0
        total_days = weeks * 7
        d = start_qdate
        self._calendar_tooltips = {}
        while workout_count < weeks * days_per_week and day_ptr < total_days * 2:
            weekday = weekday_map[d.dayOfWeek()]
            if weekday not in rest_days:
                # Color-code milestones (last day of week)
                if (workout_count + 1) % days_per_week == 0:
                    cal.setDateTextFormat(d, milestone_fmt)
                    self._calendar_tooltips[d.toString(Qt.DateFormat.ISODate)] = "Milestone: End of week!"
                else:
                    cal.setDateTextFormat(d, fmt)
                    self._calendar_tooltips[d.toString(Qt.DateFormat.ISODate)] = f"Workout Day {workout_count + 1}"
                workout_count += 1
            else:
                cal.setDateTextFormat(d, rest_fmt)
                self._calendar_tooltips[d.toString(Qt.DateFormat.ISODate)] = "Rest Day"
            d = d.addDays(1)
            day_ptr += 1
    def show_calendar_day_details(self, qdate):
        # Show a popup with details for the clicked day if it's a workout/milestone
        key = qdate.toString(qdate.Qt.DateFormat.ISODate)
        tip = self._calendar_tooltips.get(key)
        if tip:
            QMessageBox.information(self, "Workout Day Details", tip)
    def show_welcome(self):
        QMessageBox.information(self, "Welcome to C25K Calendar Creator",
            """
Welcome! This tool helps you create a personalized Couch to 5K plan with accessibility and export options.

• Fill out your info and preferences on the left.
• The calendar on the right shows your workout days.
• Use the Accessibility group to adjust the interface.
• Click 'Generate Plan and Exports' to create your plan.
• For help, use the Help menu or the README.
            """)

    def show_feedback_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Send Feedback")
        layout = QVBoxLayout(dialog)
        label = QLabel("Enter your feedback, suggestions, or issues:")
        layout.addWidget(label)
        textedit = QTextEdit()
        layout.addWidget(textedit)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)
        def submit():
            feedback = textedit.toPlainText().strip()
            if feedback:
                try:
                    feedback_path = os.path.join(os.path.expanduser("~"), "c25k_feedback.txt")
                    with open(feedback_path, "a", encoding="utf-8") as f:
                        import datetime
                        f.write(f"[{datetime.datetime.now().isoformat()}] {feedback}\n\n")
                    QMessageBox.information(self, "Thank you!", f"Feedback saved to {feedback_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not save feedback: {e}")
            dialog.accept()
        buttons.accepted.connect(submit)
        buttons.rejected.connect(dialog.reject)
        dialog.exec()

    def show_screenshots(self):
        # Try to open screenshots folder or a sample image
        screenshots_dir = os.path.join(os.path.dirname(__file__), "..", "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir, exist_ok=True)
        QFileDialog.getOpenFileName(self, "View Screenshot", screenshots_dir)


    def save_preferences(self, silent=False):
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
            "onboarded": self.prefs.get("onboarded", False),
        }
        try:
            with open(self.PREFS_FILE, "w", encoding="utf-8") as f:
                self.json.dump(prefs, f, indent=2)
            if not silent:
                QMessageBox.information(self, "Preferences Saved", "Your preferences have been saved and will be restored next time.")
        except Exception as e:
            if not silent:
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
        self.weight_label.repaint()

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
        if hasattr(self, '_validate_fields') and not self._validate_fields():
            QMessageBox.warning(self, "Invalid Input", "Please correct the highlighted fields before submitting.")
            return
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
