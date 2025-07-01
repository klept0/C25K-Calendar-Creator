
# ℹ️ About This Project

This project began as a personal tool to help manage my own Couch to 5K journey. After finding it useful, I decided to share it with the community in hopes that others might benefit as well. Contributions, pull requests, and suggestions for enhancements are very welcome!

Feel free to open issues, submit pull requests, or suggest new features—let's make C25K Calendar Creator even better together.

## 🏃‍♀️ C25K Calendar Creator



![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)


### A modern, accessible Couch to 5K training plan generator with a beautiful PyQt6 GUI

Turn your fitness goals into reality with personalized workout calendars and comprehensive tracking tools.

## 🌟 Overview

The **C25K Calendar Creator** is a comprehensive desktop application that generates personalized Couch to 5K training plans. Built with Python and PyQt6, it offers a modern, accessible interface for creating customized workout schedules that adapt to your age, weight, fitness level, and health considerations.

> **⚠️ Medical Disclaimer:** This application is for informational purposes only and is NOT a substitute for professional medical advice. Always consult your healthcare provider before starting any new exercise program, especially if you have pre-existing health conditions.


## ✨ Key Features


### 🎯 **Personalized Training Plans**

- **Adaptive Workouts**: Plans adjust based on age, weight, and fitness level
- **Health-Conscious**: Special considerations for users with hypertension
- **Flexible Scheduling**: Choose your start date, session times, and rest days
- **Progressive Structure**: Follows NHS Couch to 5K guidelines


### 📅 Export Formats _(Implemented)_

- **📱 Calendar Integration**: `.ics` files for Apple Calendar, Google Calendar, and Outlook
- **📊 Excel Tracker**: Advanced progress tracking with macros and visual indicators
- **📄 Multiple Formats**: CSV, JSON, Markdown checklists
- **🔗 Google Fit**: CSV export compatible with Google Fit


### 📅 Advanced Export Features

- **🏃 Mobile Apps**: Direct export to Strava, RunKeeper, Garmin Connect, Apple Health, Intervals.icu
- **📊 QR Code Export**: Generate QR codes for easy plan sharing


### 🎨 Modern GUI Experience

- **Intuitive Interface**: Clean, user-friendly PyQt6 design
- **Accessibility Features**: High contrast mode, large fonts, dyslexia-friendly fonts, screen reader support
- **Persistent Preferences**: Your settings are automatically saved and restored
- **Real-time Calendar Preview**: See your workout schedule with color-coded days


### 🌍 Internationalization

- **Multi-language Support**: English, Spanish, French, German, Portuguese
- **Localized Content**: Workout instructions in multiple languages
- **Regional Settings**: Imperial/Metric units supported


### 🏥 Health & Safety

- **Medical Guidelines**: Based on NHS, CDC, and American Heart Association recommendations
- **Safety Reminders**: Hydration and health monitoring tips included
- **Beginner-Friendly**: Progressive difficulty with proper rest periods
- **Customizable Intensity**: Adjust based on your fitness level

## 🚀 Quick Start


### Installation


1. **Clone the repository**

```bash

git clone https://github.com/yourusername/C25K-Calendar-Creator.git
cd C25K-Calendar-Creator

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/Random-Scripts.git
    cd Random-Scripts
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Launch the application**

    ```bash
    python c25k_ics_generator.py
    ```

4. **🚀 Enable Advanced Features** *(Optional)*

    ```bash
    # Install advanced export dependencies
    pip install qrcode[pil] reportlab Pillow

    # Test advanced features
    python test_advanced_features.py
    ```

5. **🔑 Setup API Integrations** *(Optional)*

    - Create accounts with [Strava](https://developers.strava.com/), [Intervals.icu](https://intervals.icu/), [OpenWeatherMap](https://openweathermap.org/api)
    - Configure `api_credentials.json` (see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md))
    - Enable fitness platform exports and weather recommendations


### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: 256MB RAM minimum
- **Storage**: 50MB free space

## 🎯 Current Status

### ✅ Fully Implemented Features
- **Complete PyQt6 GUI** with modern interface
- **Core C25K Plan Generation** following NHS guidelines  
- **Multiple Export Formats**: ICS, CSV, JSON, Markdown, Excel tracker
- **Accessibility Features**: High contrast, large fonts, screen reader support
- **Persistent Preferences** with automatic save/restore
- **Interactive Calendar Preview** with color-coded workout days
- **Comprehensive Testing** with unit test coverage

### 🚀 Advanced Features - Ready to Deploy!
- **🌍 Multi-language Support**: Complete i18n system with 5 languages (English, Spanish, French, German, Portuguese)
- **📱 Fitness Platform APIs**: Full integration framework for Strava, RunKeeper, Garmin Connect, **Intervals.icu**
- **📄 PDF Export**: Comprehensive training guides with progress tracking and QR codes
- **📊 QR Code Generation**: Shareable plan summaries and weekly codes
- **🌤️ Weather Integration**: OpenWeatherMap API for workout recommendations
- **🔧 Advanced Export Manager**: Unified system with graceful fallbacks

### 🔧 Activation Required _(Install: `pip install qrcode[pil] reportlab`)_
- **Intervals.icu Integration**: Structured workouts with power/pace zones
- **PDF Training Guides**: Complete workout documentation 
- **QR Code Sharing**: Mobile-friendly plan distribution
- **Multi-language Interface**: Localized workout descriptions
- **Weather Recommendations**: Live conditions and safety advice

### 🔑 API Setup Required _(Credentials needed)_
- **Strava Integration**: OAuth2 + training calendar upload
- **RunKeeper Integration**: Activity import/export
- **Garmin Connect**: Training plan synchronization  
- **Weather Services**: Live forecast integration

## 📋 Dependencies


```text
PyQt6>=6.0.0          # Modern GUI framework
openpyxl>=3.1.0       # Excel file creation and macros
requests>=2.0.0       # Weather API integration (planned feature)
qrcode[pil]>=7.0.0    # QR code generation (planned feature)
reportlab>=4.0.0      # PDF export functionality (planned feature)
```

**Note**: Some dependencies support planned features that are not yet implemented.

## 🎮 How to Use


### 1. Launch & Setup

- Run the application and fill in your personal information
- Set your preferred start date and session times
- Choose your units (Imperial/Metric) and language
- Save your preferences for future use


### 2. Generate Your Plan

- Click "Generate C25K Plan" to create your personalized schedule
- Review the generated plan in the preview area
- The plan automatically adjusts based on your profile


### 3. Export Your Plan

- Choose from implemented export formats:
  - **📱 Calendar**: Import into your phone or computer calendar (ICS format)
  - **📊 Excel**: Track progress with advanced analytics
  - **📄 Checklist**: Print-friendly Markdown format
  - **📈 CSV**: Import into Google Sheets, Numbers, Excel, or Google Fit
  - **🔗 JSON**: Structured data for app integration
  
  - **Now Available**: Direct exports to Strava, RunKeeper, Garmin Connect, Apple Health, Intervals.icu, PDF, QR Codes, and more!


### 4. Track Progress

- Use the Excel tracker for detailed progress monitoring
- Check off completed workouts in your calendar
- Review analytics and adjust as needed


## 📊 Export Formats Explained

| Format | Use Case | Features | Status |
|--------|----------|----------|---------|
| **📱 ICS (Calendar)** | Phone/Computer calendars | Custom alerts, recurring events, timezone support | ✅ Implemented |
| **📊 Excel Tracker** | Progress monitoring | Macros, charts, analytics, visual progress indicators | ✅ Implemented |
| **📄 Markdown** | Print/Share | Clean checklist format, goal tracking | ✅ Implemented |
| **📈 CSV** | Spreadsheet apps | Import into Google Sheets, Numbers, Excel | ✅ Implemented |
| **🔗 JSON** | App integration | Structured data for other fitness apps | ✅ Implemented |
| **🏃 Google Fit** | Fitness tracking | CSV format compatible with Google Fit | ✅ Implemented |
| **📱 Strava/RunKeeper** | Popular running apps | Direct export to running platforms | 🚀 Ready to Deploy |
| **📊 QR Codes** | Easy sharing | QR codes containing plan summary | 🚀 Ready to Deploy |
| **📄 PDF Guide** | Comprehensive docs | Complete training guide with tips and tracking | 🔧 Ready to Deploy |
| **🎯 Intervals.icu** | Structured training | Power/pace zones, advanced workout structure | 🔧 Ready to Deploy |
| **🌤️ Weather Integration** | Smart recommendations | Live weather-based workout suggestions | 🔧 Ready to Deploy |
| **🌍 Multi-language** | Global accessibility | Spanish, French, German, Portuguese support | 🔧 Ready to Deploy |


## 🎯 Sample Training Plan


**Week 1**: Build the habit

- Run 60 seconds, walk 90 seconds (8 repetitions)
- Total workout time: ~20 minutes


**Week 5**: Building endurance  

- Run 20 minutes continuously
- Major milestone achievement!


**Week 9**: Race ready

- Run 30 minutes (5K distance)
- Graduation day! 🎉


## ⚙️ Advanced Features


### 🔧 Customization Options

- **Rest Day Patterns**: Choose which days work best for you
- **Session Duration**: Adjust based on your schedule  
- **Difficulty Scaling**: Automatic adjustments for age/weight
- **Weather Integration**: Demo weather suggestions *(Real API integration planned)*

**Note**: Weather suggestions are currently simulated for demonstration purposes. Future versions will integrate with live weather APIs.


### 📊 Analytics & Tracking _(Implemented)_

- **Excel Progress Tracker**: Comprehensive tracking with visual indicators
- **Calendar Integration**: Visual workout schedule with color coding
- **Plan Customization**: Adaptive plans based on personal profile


### 📊 Planned Analytics Features _(Coming Soon)_

- **Progress Charts**: Visual representation of improvement over time
- **Completion Rates**: Track consistency and adherence metrics
- **Performance Metrics**: Time, distance, and effort tracking
- **Goal Achievement**: Monitor progress toward 5K goals


### ♿ Accessibility Features _(Implemented)_

- **High Contrast Mode**: Enhanced visibility for low vision users
- **Large Font Support**: Adjustable text sizes
- **Dyslexia-Friendly Fonts**: Comic Sans MS option for dyslexic users
- **Screen Reader Compatible**: Enhanced descriptions for assistive technology
- **Keyboard Navigation**: Complete mouse-free operation with focus highlights
- **Increased Spacing**: Better readability with adjustable spacing


## 🛠️ Development


### Project Structure

```text
C25K-Calendar-Creator/
├── c25k_ics_generator.py          # Main application entry point
├── modules/                       # Core application modules
│   ├── core.py                   # Business logic and plan generation
│   ├── pyqt_gui.py               # PyQt6 user interface
│   ├── exports.py                # Export functionality
│   ├── api_integrations.py       # Fitness platform APIs
│   ├── advanced_exports.py       # PDF & QR code generation
│   ├── internationalization.py   # Multi-language support
│   └── utils.py                  # Utility functions
├── c25k_utils/                   # Specialized utilities
│   ├── accessibility.py          # Accessibility enhancements
│   └── mobile_export.py          # Mobile app integrations
├── tests/                        # Test suite
│   └── test_plan.py              # Unit tests for plan generation
├── test_advanced_features.py     # Advanced features test suite
├── IMPLEMENTATION_GUIDE.md       # Advanced setup instructions
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

### Running Tests

```bash
python -m pytest tests/ -v
```


### Code Quality

The project maintains high code quality with:

- **Type Hints**: Full type annotation coverage
- **Documentation**: Comprehensive docstrings
- **Testing**: Unit tests for core functionality
- **Linting**: Code formatting with Black and isort

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🐛 Report Bugs**: Create detailed issue reports
2. **💡 Suggest Features**: Share your ideas for improvements
3. **🔧 Submit PRs**: Fix bugs or add new features
4. **📖 Improve Docs**: Help make documentation clearer
5. **🌍 Translations**: Add support for new languages

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/yourusername/C25K-Calendar-Creator.git
cd C25K-Calendar-Creator
pip install -r requirements.txt
pip install black isort pytest  # Development tools

# Run tests
python -m pytest

# Format code
python -m black .
python -m isort .
```


## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.


## 🙏 Acknowledgments


### Medical Guidelines

- **NHS Couch to 5K**: Official UK health service program structure
- **CDC Physical Activity Guidelines**: Safety and progression recommendations  
- **American Heart Association**: Cardiovascular health considerations


### Technical Foundations

- **PyQt6**: Modern cross-platform GUI framework
- **Python Community**: Excellent ecosystem and libraries
- **Open Source Contributors**: Thank you for inspiration and tools


## 📞 Support


### Getting Help

- **📖 Documentation**: Check the built-in help and tooltips
- **🐛 Issues**: Report bugs on our GitHub Issues page
- **💬 Discussions**: Join community discussions for questions
- **📧 Contact**: Reach out for specific support needs

### Frequently Asked Questions

**Q: Can I modify the workout plan?**
A: Yes! The plan adjusts automatically based on your profile, and you can customize rest days and session times.

**Q: Is my data stored online?**
A: No! All data is stored locally on your device. No information is sent to external servers.

**Q: What if I miss a workout?**
A: The Excel tracker helps you reschedule and catch up. The plan is flexible and forgiving.

**Q: Can I use this with a fitness tracker?**
A: Absolutely! Export to popular fitness apps or use the calendar integration with your device's health apps.

---



---


---


---


---

#### 🏃‍♀️ Ready to start your fitness journey? Download C25K Calendar Creator today! 🏃‍♂️

_Made with ❤️ for the running community_

[⬆️ Back to Top](#-about-this-project)
