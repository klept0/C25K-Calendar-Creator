import json  # used for preferences
import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFormLayout

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


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
            (
                "Welcome to C25K Calendar Creator!",
                "This app helps you create a personalized Couch to 5K training plan with reminders, exports, and accessibility features.",
            ),
            (
                "Personal Information",
                "Fill in your name, age, gender, weight, and preferred units. These help customize your plan.",
            ),
            (
                "Plan Settings",
                "Choose how many weeks, days per week, and your preferred start date and time. Select your export format and (optionally) enter your email for reminders.",
            ),
            (
                "Accessibility Options",
                "Enable high contrast, large font, dyslexia font, and other options for a more accessible experience.",
            ),
            (
                "Calendar Preview",
                "The calendar on the right shows your workout schedule. Milestones and rest days are color-coded.",
            ),
            (
                "Export & Feedback",
                "Click 'Generate Plan and Exports' to create your files. Use the Feedback button to send suggestions or issues.",
            ),
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
        # Set a minimum and default window size to ensure main content is visible
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)
        # Initialize attributes for OS and json modules
        self.os = os
        self.json = json
        self._calendar_tooltips = {}
        # Load preferences first
        self.prefs = self.load_preferences()
        # Initialize units based on preferences
        self._current_unit = "imperial" if self.prefs.get("unit", "i") == "i" else "metric"
        self.init_ui()  # This creates self.weight_spin and other widgets
        # Only call set_units after confirming weight_spin exists
        if hasattr(self, "weight_spin"):
            self.set_units(self._current_unit)
        # Onboarding: show welcome dialog on first launch
        if not self.prefs.get("onboarded", False):
            self.show_onboarding()
            self.prefs["onboarded"] = True
            self.save_preferences(silent=True)


    def init_ui(self):
        print("[DEBUG] init_ui: start")
        try:
            # Main horizontal layout: form (left), calendar (right)
            main_layout = QHBoxLayout()
            form_layout = QVBoxLayout()

            # Menu bar (Help, Screenshots, About, Units, Integrations, Feedback)
            self.menu_bar = QMenuBar(self)
            # Help menu
            help_menu = QMenu("Help", self)
            about_action = QAction("About", self)
            about_action.triggered.connect(self.show_help)
            screenshots_action = QAction("Screenshots", self)
            screenshots_action.triggered.connect(self.show_screenshots)
            help_menu.addAction(about_action)
            help_menu.addAction(screenshots_action)
            self.menu_bar.addMenu(help_menu)
            # Units dropdown in menu bar
            units_menu = QMenu("Units", self)
            self.imperial_action = QAction("Imperial (lbs, °F)", self)
            self.imperial_action.setCheckable(True)
            self.metric_action = QAction("Metric (kg, °C)", self)
            self.metric_action.setCheckable(True)
            self.imperial_action.triggered.connect(lambda: self.set_units("imperial"))
            self.metric_action.triggered.connect(lambda: self.set_units("metric"))
            # Set initial state
            if self.prefs.get("unit", "i") == "i":
                self.imperial_action.setChecked(True)
            else:
                self.metric_action.setChecked(True)
            units_menu.addAction(self.imperial_action)
            units_menu.addAction(self.metric_action)
            self.menu_bar.addMenu(units_menu)
            # Integrations menu
            integrations_menu = QMenu("Integrations", self)
            manage_integrations_action = QAction("Enable/Disable Integrations...", self)
            manage_integrations_action.triggered.connect(self.show_integrations_dialog)
            integrations_menu.addAction(manage_integrations_action)
            self.menu_bar.addMenu(integrations_menu)
            # Feedback menu
            feedback_menu = QMenu("Feedback", self)
            send_feedback_action = QAction("Send Feedback", self)
            send_feedback_action.triggered.connect(self.show_feedback_dialog)
            feedback_menu.addAction(send_feedback_action)
            self.menu_bar.addMenu(feedback_menu)
            form_layout.setMenuBar(self.menu_bar)

            print("[DEBUG] init_ui: menu bar and form_layout created")

            # ...existing code for adding widgets to form_layout and main_layout...
            # Feedback button removed from form layout (now in menu)
            print("[DEBUG] init_ui: feedback button added")
            # --- Personal Information Group ---
            personal_group = QGroupBox("Personal Information")
            personal_form = QFormLayout()
            personal_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            personal_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            personal_form.setHorizontalSpacing(18)
            personal_form.setVerticalSpacing(12)
            self.name_edit = QLineEdit()
            self.name_edit.setToolTip("Enter your name (required)")
            self.name_edit.setText(self.prefs.get("name", ""))
            personal_form.addRow("Name", self.name_edit)
            self.age_spin = QSpinBox()
            self.age_spin.setRange(5, 120)
            self.age_spin.setValue(self.prefs.get("age", 30))
            self.age_spin.setToolTip("Enter your age (5-120)")
            personal_form.addRow("Age", self.age_spin)
            self.weight_spin = QSpinBox()
            self.weight_spin.setRange(50, 500)
            self.weight_spin.setValue(self.prefs.get("weight", 150))
            self.weight_spin.setToolTip("Enter your weight")
            personal_form.addRow("Weight (lbs)", self.weight_spin)
            self.gender_combo = QComboBox()
            self.gender_combo.addItems(["male", "female", "other"])
            gender_idx = self.gender_combo.findText(self.prefs.get("gender", "male"))
            self.gender_combo.setCurrentIndex(gender_idx if gender_idx >= 0 else 0)
            self.gender_combo.setToolTip("Select your gender")
            personal_form.addRow("Gender", self.gender_combo)
            personal_group.setLayout(personal_form)
            personal_group.setMinimumHeight(180)
            personal_group.setStyleSheet("QGroupBox { margin-top: 12px; margin-bottom: 8px; padding: 16px 16px 12px 16px; font-size: 14px; } QLabel { margin-bottom: 6px; }")
            form_layout.addWidget(personal_group)
            form_layout.addSpacing(22)

            # --- Plan Settings Group ---
            plan_group = QGroupBox("Plan Settings")
            plan_group.setMinimumHeight(200)
            plan_form = QFormLayout()
            plan_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            plan_form.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            plan_form.setHorizontalSpacing(18)
            plan_form.setVerticalSpacing(12)
            self.weeks_spin = QSpinBox()
            self.weeks_spin.setRange(1, 52)
            self.weeks_spin.setValue(self.prefs.get("weeks", 10))
            self.weeks_spin.setToolTip("Number of weeks in your plan (default 10)")
            plan_form.addRow("Weeks", self.weeks_spin)
            self.days_spin = QSpinBox()
            self.days_spin.setRange(1, 7)
            self.days_spin.setValue(self.prefs.get("days_per_week", 3))
            self.days_spin.setToolTip("Days per week (default 3)")
            plan_form.addRow("Days/Week", self.days_spin)
            from PyQt6.QtCore import QDate
            from PyQt6.QtWidgets import QDateEdit
            self.start_date = QDateEdit()
            self.start_date.setCalendarPopup(True)
            self.start_date.setDate(QDate.currentDate())
            self.start_date.setToolTip("Select your plan start date")
            plan_form.addRow("Start Date", self.start_date)
            self.time_edit = QLineEdit()
            self.time_edit.setPlaceholderText("07:00")
            self.time_edit.setToolTip("Session start time (HH:MM, 24h)")
            self.time_edit.setText(self.prefs.get("time", "07:00"))
            plan_form.addRow("Session Time", self.time_edit)
            self.export_combo = QComboBox()
            self.export_combo.addItems([
                "ICS (Calendar)",
                "CSV",
                "JSON",
                "Google Fit CSV",
                "Markdown",
                "Strava/Runkeeper",
                "Apple Health",
            ])
            self.export_combo.setToolTip("Choose export format")
            plan_form.addRow("Export Format", self.export_combo)
            self.email_edit = QLineEdit()
            self.email_edit.setToolTip("Enter your email for reminders (optional)")
            self.email_edit.setText(self.prefs.get("email", ""))
            plan_form.addRow("Email", self.email_edit)
            self.location_edit = QLineEdit()
            self.location_edit.setToolTip("Enter your city or ZIP for weather (optional)")
            self.location_edit.setText(self.prefs.get("location", ""))
            plan_form.addRow("Location", self.location_edit)
            self.anonymize = QCheckBox("Anonymize Exports")
            self.anonymize.setToolTip("Remove personal info from all exports. If checked, your name and email will not appear in any export file.")
            self.anonymize.setChecked(self.prefs.get("anonymize", False))
            plan_form.addRow("", self.anonymize)
            plan_group.setLayout(plan_form)
            plan_group.setStyleSheet("QGroupBox { margin-top: 12px; margin-bottom: 8px; padding: 16px 16px 12px 16px; font-size: 14px; } QLabel { margin-bottom: 6px; } QLineEdit, QComboBox, QSpinBox { min-height: 28px; font-size: 13px; } QCheckBox { margin-top: 4px; margin-bottom: 4px; }")
            form_layout.addWidget(plan_group)
            form_layout.addSpacing(22)

            # --- Accessibility Options Group ---
            acc_group = QGroupBox("Accessibility Options")
            acc_group.setMinimumHeight(180)
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
            acc_layout.setSpacing(10)
            acc_group.setLayout(acc_layout)
            acc_group.setStyleSheet("QGroupBox { margin-top: 12px; margin-bottom: 8px; padding: 16px 16px 12px 16px; font-size: 14px; } QCheckBox { margin-top: 6px; margin-bottom: 6px; font-size: 13px; } QPushButton { margin-top: 10px; margin-bottom: 0px; min-height: 28px; }")
            form_layout.addWidget(acc_group)
            form_layout.addSpacing(22)

            # Add remaining buttons
            # (Feedback, Preview Export, Save Preferences, Generate Plan)
            # These are already added in the full code

            # Add stretch to push content to the top and prevent crowding
            form_layout.addStretch(1)

            # Optionally set a minimum width for the left panel
            left_panel = QWidget()
            left_panel.setLayout(form_layout)
            left_panel.setMinimumWidth(480)
            left_panel.setStyleSheet("QWidget { font-size: 13px; } QPushButton { margin-top: 10px; margin-bottom: 10px; min-height: 28px; } QLineEdit, QComboBox, QSpinBox { margin-bottom: 8px; min-height: 28px; } QGroupBox { border-radius: 8px; border: 1.5px solid #555; } QLabel { color: #e0e0e0; }")

            # --- Calendar Widget ---
            self.calendar = QCalendarWidget()
            self.calendar.setGridVisible(True)
            self.calendar.setToolTip(
                "Visual calendar: workout days will be highlighted after you choose your plan options."
            )
            self.calendar.setMinimumWidth(350)
            # Add a frame for visual separation
            calendar_frame = QFrame()
            calendar_frame.setFrameShape(QFrame.Shape.StyledPanel)
            calendar_layout = QVBoxLayout()
            calendar_label = QLabel("Workout Calendar Preview")
            calendar_label.setStyleSheet("font-weight: bold; font-size: 14px;")
            calendar_layout.addWidget(calendar_label)
            calendar_layout.addWidget(self.calendar)
            legend_layout = QHBoxLayout()
            workout_color = QLabel()
            workout_color.setFixedSize(18, 18)
            workout_color.setStyleSheet("background: rgba(0,120,215,0.5); border: 1px solid #888;")
            legend_layout.addWidget(workout_color)
            legend_layout.addWidget(QLabel("Workout Day"))
            milestone_color = QLabel()
            milestone_color.setFixedSize(18, 18)
            milestone_color.setStyleSheet("background: rgba(255,215,0,0.7); border: 1px solid #888;")
            legend_layout.addWidget(milestone_color)
            legend_layout.addWidget(QLabel("Milestone (End of Week)"))
            rest_color = QLabel()
            rest_color.setFixedSize(18, 18)
            rest_color.setStyleSheet("background: rgba(180,180,180,0.5); border: 1px solid #888;")
            legend_layout.addWidget(rest_color)
            legend_layout.addWidget(QLabel("Rest Day"))
            legend_layout.addStretch(1)
            calendar_layout.addLayout(legend_layout)
            calendar_frame.setLayout(calendar_layout)

            # Add form and calendar to main layout
            main_layout.addWidget(left_panel, stretch=2)
            main_layout.addWidget(calendar_frame, stretch=1)

            # At the end, set the layout
            self.setLayout(main_layout)
            print("[DEBUG] init_ui: main_layout set")
        except Exception as e:
            import traceback
            print(f"[ERROR] Exception in init_ui: {e}")
            traceback.print_exc()

    def show_integrations_dialog(self):
        # Ensure base form widgets are always visible
        if not self.isVisible():
            self.show()
        """Show a dialog to enable/disable integrations (Strava, RunKeeper, Garmin, Intervals.icu, Weather)."""
        integrations = [
            ("Strava", "strava_enabled", "strava_api_key", "Enter your Strava API key:"),
            ("RunKeeper", "runkeeper_enabled", "runkeeper_api_key", "Enter your RunKeeper API key:"),
            ("Garmin Connect", "garmin_enabled", "garmin_api_key", "Enter your Garmin Connect API key:"),
            ("Intervals.icu", "intervals_enabled", "intervals_api_key", "Enter your Intervals.icu API key:"),
            ("Weather Integration", "weather_enabled", "weather_api_key", "Enter your OpenWeatherMap API key:"),
        ]
        dialog = QDialog(self)
        dialog.setWindowTitle("Manage Integrations")
        layout = QVBoxLayout(dialog)
        label = QLabel("Enable or disable integrations. Changes are saved automatically.")
        layout.addWidget(label)
        checkboxes = {}
        for name, key, _, _ in integrations:
            cb = QCheckBox(name)
            cb.setChecked(self.prefs.get(key, True))
            layout.addWidget(cb)
            checkboxes[key] = cb
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btns.accepted.connect(dialog.accept)
        layout.addWidget(btns)

        def prompt_api_key(api_key_pref, prompt_text):
            # Only prompt if not already set
            if self.prefs.get(api_key_pref):
                return
            key_dialog = QDialog(self)
            key_dialog.setWindowTitle("API Key Required")
            key_layout = QVBoxLayout(key_dialog)
            key_label = QLabel(prompt_text)
            key_layout.addWidget(key_label)
            key_edit = QLineEdit()
            # Show API key as plaintext so user can confirm accuracy
            key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            key_layout.addWidget(key_edit)
            key_btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            key_layout.addWidget(key_btns)
            def accept_key():
                val = key_edit.text().strip()
                if val:
                    self.prefs[api_key_pref] = val
                    # Save only the API key to disk, not the full preferences (avoid widget dependency)
                    try:
                        with open(self.PREFS_FILE, "w", encoding="utf-8") as f:
                            json.dump(self.prefs, f, indent=2)
                    except Exception as e:
                        print(f"[ERROR] Could not save API key: {e}")
                key_dialog.accept()
            key_btns.accepted.connect(accept_key)
            key_btns.rejected.connect(key_dialog.reject)
            key_dialog.exec()

        def save_integrations():
            for name, key, api_key_pref, prompt_text in integrations:
                enabled = checkboxes[key].isChecked()
                self.prefs[key] = enabled
                if enabled:
                    prompt_api_key(api_key_pref, prompt_text)
            # Save only the integration preferences directly to disk (avoid widget dependency)
            try:
                with open(self.PREFS_FILE, "w", encoding="utf-8") as f:
                    json.dump(self.prefs, f, indent=2)
            except Exception as e:
                print(f"[ERROR] Could not save integration preferences: {e}")
        dialog.accepted.connect(save_integrations)
        dialog.exec()

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
        # Weight (will be updated by unit combo later)
        self.weight_spin = QSpinBox()
        self.weight_spin.setRange(50, 500)  # Covers both lbs and kg ranges
        self.weight_spin.setValue(self.prefs.get("weight", 150))
        self.weight_spin.setToolTip("Enter your weight")
        personal_layout.addLayout(self._row("Weight (lbs)", self.weight_spin))
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
        from PyQt6.QtCore import QDate
        from PyQt6.QtWidgets import QDateEdit

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
        self.export_combo.addItems(
            [
                "ICS (Calendar)",
                "CSV",
                "JSON",
                "Google Fit CSV",
                "Markdown",
                "Strava/Runkeeper",
                "Apple Health",
            ]
        )
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
        self.anonymize.setToolTip(
            "Remove personal info from all exports. If checked, your name and email will not appear in any export file."
        )
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

        # Preview Export Button
        preview_btn = QPushButton("Preview Export")
        preview_btn.setToolTip("Preview the export file before saving.")
        preview_btn.clicked.connect(self.show_export_preview)
        form_layout.addWidget(preview_btn)

        # Save/Restore Preferences Button
        save_btn = QPushButton("Save Preferences")
        save_btn.setToolTip("Save your current settings as default.")
        save_btn.clicked.connect(self.save_preferences)
        form_layout.addWidget(save_btn)

        # Main submit button
        submit_btn = QPushButton("Generate Plan and Exports")
        submit_btn.setToolTip("Generate your plan and export files")
        submit_btn.clicked.connect(self.submit)
        submit_btn.setShortcut("Alt+E")  # Export/Generate
        form_layout.addWidget(submit_btn)

        # Now that all widgets are created, set up event filters and configurations
        # Install event filter for focus highlight
        for w in [
            self.name_edit,
            self.age_spin,
            self.weight_spin,
            self.gender_combo,
            self.weeks_spin,
            self.days_spin,
            self.start_date,
            self.time_edit,
            self.export_combo,
            self.email_edit,
            self.location_edit,
        ]:
            w.installEventFilter(self)

        # Screen Reader Mode: set accessible descriptions
        def update_accessible_descriptions():
            if self.screen_reader.isChecked():
                self.name_edit.setAccessibleDescription("Name: Enter your full name. Required.")
                self.age_spin.setAccessibleDescription("Age: Enter your age in years. Required.")
                self.weight_spin.setAccessibleDescription(
                    "Weight: Enter your weight in selected units."
                )
                self.gender_combo.setAccessibleDescription("Gender: Select your gender.")
                self.weeks_spin.setAccessibleDescription("Weeks: Number of weeks for your plan.")
                self.days_spin.setAccessibleDescription(
                    "Days per week: Number of workout days per week."
                )
                self.start_date.setAccessibleDescription(
                    "Start Date: Select the date to begin your plan."
                )
                self.time_edit.setAccessibleDescription(
                    "Session Time: Enter the time for your workouts."
                )
                self.export_combo.setAccessibleDescription(
                    "Export Format: Select the file format for export."
                )
                self.email_edit.setAccessibleDescription(
                    "Email: Enter your email for reminders (optional)."
                )
                self.location_edit.setAccessibleDescription(
                    "Location: Enter your city or ZIP for weather (optional)."
                )
            else:
                for w in [
                    self.name_edit,
                    self.age_spin,
                    self.weight_spin,
                    self.gender_combo,
                    self.weeks_spin,
                    self.days_spin,
                    self.start_date,
                    self.time_edit,
                    self.export_combo,
                    self.email_edit,
                    self.location_edit,
                ]:
                    w.setAccessibleDescription("")

        self.screen_reader.stateChanged.connect(lambda _: update_accessible_descriptions())
        update_accessible_descriptions()

        # Set keyboard shortcuts
        feedback_btn.setShortcut("Alt+F")
        # about_action is not in this scope; shortcut is set above where it's defined

        # Set tab order for logical navigation
        self.setTabOrder(self.name_edit, self.age_spin)
        self.setTabOrder(self.age_spin, self.weight_spin)
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

        # --- Calendar Widget ---
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setToolTip(
            "Visual calendar: workout days will be highlighted after you choose your plan options."
        )
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
        # Initial highlight
        self.update_calendar_highlight()

    def update_calendar_highlight(self):
        """
        Highlight only the actual workout days, skipping user rest days, on the calendar.
        Add color-coding for milestones and tooltips for each workout day.
        """
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QColor, QTextCharFormat

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
                    self._calendar_tooltips[d.toString(Qt.DateFormat.ISODate)] = (
                        "Milestone: End of week!"
                    )
                else:
                    cal.setDateTextFormat(d, fmt)
                    self._calendar_tooltips[d.toString(Qt.DateFormat.ISODate)] = (
                        f"Workout Day {workout_count + 1}"
                    )
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
        QMessageBox.information(
            self,
            "Welcome to C25K Calendar Creator",
            """
Welcome! This tool helps you create a personalized Couch to 5K plan with accessibility and export options.

• Fill out your info and preferences on the left.
• The calendar on the right shows your workout days.
• Use the Accessibility group to adjust the interface.
• Click 'Generate Plan and Exports' to create your plan.
• For help, use the Help menu or the README.
            """,
        )

    def show_feedback_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Send Feedback")
        layout = QVBoxLayout(dialog)
        label = QLabel("Enter your feedback, suggestions, or issues:")
        layout.addWidget(label)
        textedit = QTextEdit()
        layout.addWidget(textedit)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(buttons)

        def submit():
            feedback = textedit.toPlainText().strip()
            if feedback:
                try:
                    feedback_path = os.path.join(os.path.expanduser("~"), "c25k_feedback.txt")
                    with open(feedback_path, "a", encoding="utf-8") as f:
                        import datetime

                        f.write(f"[{datetime.datetime.now().isoformat()}] {feedback}\n\n")
                    QMessageBox.information(
                        self, "Thank you!", f"Feedback saved to {feedback_path}"
                    )
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
            "unit": "i" if self.get_current_unit() == "imperial" else "m",
            "weeks": self.weeks_spin.value(),
            "days_per_week": self.days_spin.value(),
            "time": self.time_edit.text(),
            "email": self.email_edit.text(),
            "location": self.location_edit.text(),
            "anonymize": self.anonymize.isChecked(),
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
                json.dump(prefs, f, indent=2)
            if not silent:
                QMessageBox.information(
                    self,
                    "Preferences Saved",
                    "Your preferences have been saved and will be restored next time.",
                )
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
        """Update weight field based on current unit selection."""
        current_unit = self.get_current_unit()
        if current_unit == "imperial":
            self.weight_spin.setRange(50, 500)
            self.weight_spin.setSuffix(" lbs")
            self.weight_spin.setToolTip("Enter your weight in pounds")
        else:
            self.weight_spin.setRange(30, 200)
            self.weight_spin.setSuffix(" kg")
            self.weight_spin.setToolTip("Enter your weight in kilograms")

    def set_units(self, unit_type):
        """Set units to imperial or metric and update UI accordingly."""
        if unit_type == "imperial":
            self.imperial_action.setChecked(True)
            self.metric_action.setChecked(False)
            # Update weight field for imperial (lbs)
            current_weight = self.weight_spin.value()
            if hasattr(self, "_current_unit") and self._current_unit == "metric":
                # Convert kg to lbs
                self.weight_spin.setValue(int(current_weight * 2.205))
            self.weight_spin.setRange(50, 500)
            self.weight_spin.setSuffix(" lbs")
            self._current_unit = "imperial"
        else:  # metric
            self.imperial_action.setChecked(False)
            self.metric_action.setChecked(True)
            # Update weight field for metric (kg)
            current_weight = self.weight_spin.value()
            if hasattr(self, "_current_unit") and self._current_unit == "imperial":
                # Convert lbs to kg
                self.weight_spin.setValue(int(current_weight / 2.205))
            self.weight_spin.setRange(30, 200)
            self.weight_spin.setSuffix(" kg")
            self._current_unit = "metric"

        # Update weight label in the row layout
        self.update_weight_labels()

    def update_weight_labels(self):
        """Update the weight field labels and ranges based on current units."""
        if hasattr(self, "_current_unit") and self._current_unit == "metric":
            self.weight_spin.setToolTip("Enter your weight in kilograms")
        else:
            self.weight_spin.setToolTip("Enter your weight in pounds")

    def get_current_unit(self):
        """Get the current unit setting."""
        if hasattr(self, "_current_unit"):
            return self._current_unit
        return "imperial" if self.imperial_action.isChecked() else "metric"

    def show_help(self):
        QMessageBox.information(
            self,
            "About C25K Calendar Creator",
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
""",
        )

    def _row(self, label, widget):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        row.addWidget(widget)
        return row

    def submit(self):
        if hasattr(self, "_validate_fields") and not self._validate_fields():
            QMessageBox.warning(
                self, "Invalid Input", "Please correct the highlighted fields before submitting."
            )
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
            unit_code = "i" if self.get_current_unit() == "imperial" else "m"
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

            # Import core logic functions
            from modules.core import (
                generate_apple_health_csv,
                generate_csv,
                generate_excel_tracker,
                generate_ics,
                generate_json,
                generate_markdown,
                generate_strava_csv,
                get_workout_plan,
            )

            # Generate plan and outputs
            plan = get_workout_plan(user_input)
            outdir = os.path.join(os.path.expanduser("~"), "C25K_Exports")
            os.makedirs(outdir, exist_ok=True)

            # Export logic for all types
            if export_code == "i":
                generate_ics(
                    plan,
                    user_input["start_day"],
                    user_input["hour"],
                    user_input["minute"],
                    user_input.get("alert_minutes", 30),
                    outdir,
                )
            elif export_code == "c":
                generate_csv(plan, outdir)
            elif export_code == "j":
                generate_json(plan, outdir)
            elif export_code == "g":
                # Google Fit CSV - use regular CSV for now
                generate_csv(plan, outdir)
            elif export_code == "m":
                generate_markdown(plan, user_input, outdir)
            elif export_code == "s":
                # Strava/Runkeeper export
                generate_strava_csv(plan, outdir)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    "Strava CSV export completed! You can import this file into Strava or Runkeeper.",
                )
            elif export_code == "a":
                # Apple Health export
                generate_apple_health_csv(plan, outdir)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    "Apple Health CSV export completed! Import this file using the Apple Health app or a compatible tool.",
                )

            # Always create Excel progress tracker
            generate_excel_tracker(plan, user_input, outdir)

            QMessageBox.information(
                self,
                "Success",
                f"Plan and exports generated in: {outdir}\n\nIncludes:\n- Selected export format\n- Excel progress tracker\n- All necessary files for your C25K journey!",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def apply_palette(self):
        # Only import if available (for linting environments)
        QPalette = QColor = None
        try:
            from PyQt6.QtGui import QColor as _QColor
            from PyQt6.QtGui import QPalette as _QPalette

            QPalette = _QPalette
            QColor = _QColor
        except ImportError:
            pass
        if QPalette is None or QColor is None:
            return
        app = QApplication.instance()
        if app is None:
            return
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

    def show_export_preview(self):
        """Show a preview of the export file before generating."""
        from datetime import datetime

        try:
            user = {
                "name": self.name_edit.text(),
                "age": self.age_spin.value(),
                "weight": self.weight_spin.value(),
                "weight_unit": "i" if self.get_current_unit() == "imperial" else "m",
                "gender": self.gender_combo.currentText(),
                "unit": "i" if self.get_current_unit() == "imperial" else "m",
                "weeks": self.weeks_spin.value(),
                "days_per_week": self.days_spin.value(),
                "start_day": (
                    self.start_date.date().toPyDate()
                    if hasattr(self.start_date.date(), "toPyDate")
                    else datetime.now().date()
                ),
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
            export_map = {0: "i", 1: "c", 2: "j", 3: "g", 4: "m", 5: "s", 6: "a"}
            user["export"] = export_map.get(self.export_combo.currentIndex(), "i")
            from modules.core import get_workout_plan

            plan = get_workout_plan(user)
            preview_text = ""
            fmt = user["export"]
            if fmt == "i":
                # ICS preview
                ics_content = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Couch to 5K//EN\n"
                for session in plan[:3]:
                    event_name = f"C25K Week {session.get('week','?')} Day {session.get('day','?')}"
                    ics_content += f"BEGIN:VEVENT\nSUMMARY:{event_name}\nDESCRIPTION:{session.get('description','')}\nEND:VEVENT\n"
                ics_content += "...\nEND:VCALENDAR"
                preview_text = ics_content
            elif fmt == "c":
                # CSV preview
                import csv
                from io import StringIO

                buf = StringIO()
                writer = csv.DictWriter(buf, fieldnames=list(plan[0].keys()) if plan else [])
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
                    date = session.get("date", "")
                    workout = session.get("workout", "")
                    lines.append(f"- [ ] {date}: {workout}")
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


def run_pyqt_gui(submit_callback=None):
    print("[DEBUG] Starting QApplication...")
    app = QApplication(sys.argv)
    try:
        print("[DEBUG] Creating main window...")
        win = C25KPyQtGUI(submit_callback)
        print("[DEBUG] Main window created. Showing window...")
        win.show()
    except Exception as e:
        import traceback
        print("[ERROR] Exception during GUI initialization:", e)
        traceback.print_exc()
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Startup Error", f"Could not start GUI: {e}")
        sys.exit(1)
    print("[DEBUG] Entering Qt event loop...")
    sys.exit(app.exec())
