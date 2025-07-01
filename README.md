# 🏃‍♀️ C25K Calendar Creator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)

**A modern, accessible Couch to 5K training plan generator with a beautiful PyQt6 GUI**

*Turn your fitness goals into reality with personalized workout calendars and comprehensive tracking tools*

</div>

## 🌟 Overview

The **C25K Calendar Creator** is a comprehensive desktop application that generates personalized Couch to 5K training plans. Built with Python and PyQt6, it offers a modern, accessible interface for creating customized workout schedules that adapt to your age, weight, fitness level, and health considerations.

> **⚠️ Medical Disclaimer:** This application is for informational purposes only and is NOT a substitute for professional medical advice. Always consult your healthcare provider before starting any new exercise program, especially if you have pre-existing health conditions.

## ✨ Key Features

### 🎯 **Personalized Training Plans**
- **Adaptive Workouts**: Plans adjust based on age, weight, and fitness level
- **Health-Conscious**: Special considerations for users with hypertension
- **Flexible Scheduling**: Choose your start date, session times, and rest days
- **Progressive Structure**: Follows NHS Couch to 5K guidelines

### 📅 **Multiple Export Formats**
- **📱 Calendar Integration**: `.ics` files for Apple Calendar, Google Calendar, and Outlook
- **📊 Excel Tracker**: Advanced progress tracking with macros and visual indicators
- **📄 Multiple Formats**: CSV, JSON, Markdown checklists, and more
- **🔗 Mobile Apps**: Export to Strava, RunKeeper, Garmin Connect, and Apple Health

### 🎨 **Modern GUI Experience**
- **Intuitive Interface**: Clean, user-friendly PyQt6 design
- **Accessibility First**: High contrast mode, large fonts, screen reader support
- **Persistent Preferences**: Your settings are automatically saved and restored
- **Real-time Preview**: See your plan before exporting

### 🌍 **Internationalization**
- **Multi-language Support**: English and Spanish interfaces
- **Localized Content**: Workout instructions and tips in your preferred language
- **Regional Settings**: Imperial/Metric units, date formats

### 🏥 **Health & Safety**
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
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**
   ```bash
   python c25k_ics_generator.py
   ```

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Memory**: 256MB RAM minimum
- **Storage**: 50MB free space

## 📋 Dependencies

```
PyQt6>=6.0.0          # Modern GUI framework
requests>=2.0.0        # Weather API integration  
qrcode[pil]>=7.0.0     # QR code generation
reportlab>=4.0.0       # PDF export functionality
openpyxl>=3.1.0        # Excel file creation and macros
```

## 🎮 How to Use

### 1. **Launch & Setup**
- Run the application and fill in your personal information
- Set your preferred start date and session times
- Choose your units (Imperial/Metric) and language
- Save your preferences for future use

### 2. **Generate Your Plan**
- Click "Generate C25K Plan" to create your personalized schedule
- Review the generated plan in the preview area
- The plan automatically adjusts based on your profile

### 3. **Export Your Plan**
- Choose from multiple export formats:
  - **📱 Calendar**: Import into your phone or computer calendar
  - **📊 Excel**: Track progress with advanced analytics
  - **📄 Checklist**: Print-friendly Markdown format
  - **🔗 Apps**: Export to fitness platforms

### 4. **Track Progress**
- Use the Excel tracker for detailed progress monitoring
- Check off completed workouts in your calendar
- Review analytics and adjust as needed

## 📊 Export Formats Explained

| Format | Use Case | Features |
|--------|----------|----------|
| **📱 ICS (Calendar)** | Phone/Computer calendars | Custom alerts, recurring events, timezone support |
| **📊 Excel Tracker** | Progress monitoring | Macros, charts, analytics, visual progress indicators |
| **📄 Markdown** | Print/Share | Clean checklist format, goal tracking |
| **📈 CSV** | Spreadsheet apps | Import into Google Sheets, Numbers, Excel |
| **🔗 JSON** | App integration | Structured data for other fitness apps |
| **🏃 Fitness Apps** | Strava, RunKeeper, etc. | Direct export to popular running platforms |

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

### 🔧 **Customization Options**
- **Rest Day Patterns**: Choose which days work best for you
- **Session Duration**: Adjust based on your schedule
- **Difficulty Scaling**: Automatic adjustments for age/weight
- **Weather Integration**: Get weather-based workout suggestions

### 📊 **Analytics & Tracking**
- **Progress Charts**: Visual representation of your improvement
- **Completion Rates**: Track consistency and adherence
- **Performance Metrics**: Time, distance, and effort tracking
- **Goal Achievement**: Monitor progress toward your 5K goal

### ♿ **Accessibility Features**
- **High Contrast Mode**: Enhanced visibility for low vision users
- **Large Font Support**: Adjustable text sizes
- **Screen Reader Compatible**: Full ARIA support
- **Keyboard Navigation**: Complete mouse-free operation

## 🛠️ Development

### Project Structure
```
C25K Calendar Creator/
├── c25k_ics_generator.py          # Main application entry point
├── modules/                       # Core application modules
│   ├── core.py                   # Business logic and plan generation
│   ├── pyqt_gui.py              # PyQt6 user interface
│   ├── exports.py               # Export functionality
│   └── utils.py                 # Utility functions
├── c25k_utils/                   # Specialized utilities
│   ├── accessibility.py         # Accessibility enhancements
│   └── mobile_export.py         # Mobile app integrations
├── tests/                        # Test suite
│   └── test_plan.py             # Unit tests for plan generation
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

<div align="center">

**🏃‍♀️ Ready to start your fitness journey? Download C25K Calendar Creator today! 🏃‍♂️**

*Made with ❤️ for the running community*

[⬆️ Back to Top](#-c25k-calendar-creator)

</div>
