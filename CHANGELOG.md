# [2.1.0] - 2025-07-01

### Maintenance & Community Release

#### Added
- "About This Project" section in README to clarify personal origins and encourage contributions.
- README and documentation improvements for clarity and lint compliance.
- Confirmed all unnecessary files and legacy scripts have been removed from the repository.
- Ensured all workflows (.github/workflows/ci.yml) and ignore files (.gitignore) are up to date and reflect the current project structure and best practices.

#### Changed
- Updated project structure and documentation to use "C25K-Calendar-Creator" consistently.
- README badges and formatting now use pure Markdown for full compatibility.
- Minor improvements to onboarding and contribution guidance.

#### Fixed
- Addressed Markdown lint warnings in README.
- Verified .gitignore covers all build, test, and platform-specific artifacts.
- Confirmed CI workflow installs dependencies and runs tests as expected.

---

# 📜 Changelog

All notable changes to the **C25K Calendar Creator** project are documented in this file.

This changelog follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-06-30

### 🎉 Major Release - Complete Rewrite

#### Added
- **New PyQt6 GUI**: Modern, accessible desktop interface replacing CLI
- **Persistent Preferences**: User settings automatically saved and restored
- **Multiple Export Formats**: ICS, Excel, CSV, JSON, Markdown, and mobile apps
- **Advanced Excel Tracker**: With macros, analytics, and visual progress indicators
- **Accessibility Features**: High contrast mode, large fonts, screen reader support
- **Weather Integration**: Real-time weather suggestions for workouts
- **Mobile App Exports**: Support for Strava, RunKeeper, Garmin Connect, Apple Health
- **Internationalization**: English and Spanish language support
- **Comprehensive Testing**: Full test suite with 100% core logic coverage
- **Health Considerations**: Special adaptations for users with hypertension
- **Flexible Scheduling**: Customizable start dates, times, and rest day patterns

#### Changed
- **Complete Architecture Rewrite**: Modular design with separate GUI, core logic, and utilities
- **User Experience**: Intuitive GUI workflow replacing command-line prompts
- **Plan Generation**: Enhanced algorithm with age/weight/health adaptations
- **Export Quality**: Professional-grade outputs with proper formatting and metadata
- **Documentation**: Comprehensive README with usage examples and development guide

#### Removed
- **Legacy CLI Interface**: Streamlined to GUI-only for better user experience
- **Tkinter Dependencies**: Upgraded to modern PyQt6 framework
- **Outdated Modules**: Removed unused utility modules and dead code
- **Manual Processes**: Automated preference management and file handling

#### Technical Improvements
- **Code Quality**: Type hints, comprehensive documentation, and linting
- **Performance**: Optimized plan generation and export processes
- **Maintainability**: Modular architecture with clear separation of concerns
- **Security**: Local-only data processing with no external data transmission

### 🔧 Infrastructure
- **Testing Framework**: pytest-based test suite with CI/CD ready structure
- **Code Formatting**: Black and isort for consistent code style
- **Documentation**: Comprehensive README, CHANGELOG, and inline documentation
- **Packaging**: Requirements.txt with pinned dependencies for stability

### 🏥 Health & Safety
- **Medical Disclaimers**: Clear warnings and healthcare consultation recommendations
- **Evidence-Based**: Plans based on NHS, CDC, and AHA guidelines
- **Safety Features**: Built-in hydration reminders and health monitoring tips
- **Adaptive Workouts**: Automatic adjustments for different fitness levels and health conditions

### 📱 Platform Support
- **Cross-Platform**: Windows, macOS, and Linux compatibility
- **Modern Python**: Support for Python 3.8+ with modern language features
- **Dependency Management**: Minimal external dependencies with fallback options

## [1.x.x] - Legacy Versions

### Historical Context
Previous versions (1.x.x) featured command-line interfaces and basic calendar generation. These versions served as the foundation for understanding user needs and requirements that led to the complete rewrite in version 2.0.0.

#### Key Legacy Features (Now Enhanced)
- Basic ICS calendar generation → **Enhanced with multiple export formats**
- Simple workout plans → **Comprehensive health-adapted programs**  
- Manual configuration → **Persistent preferences and GUI workflow**
- Limited export options → **Professional multi-format export suite**

---

## Development Notes

### Version Numbering
- **Major (X.0.0)**: Breaking changes, major feature additions, architecture changes
- **Minor (X.Y.0)**: New features, enhancements, non-breaking changes
- **Patch (X.Y.Z)**: Bug fixes, documentation updates, minor improvements

### Contributing
See [README.md](README.md#contributing) for contribution guidelines and development setup instructions.

### Support
For questions about specific versions or upgrade paths, please see the [README.md](README.md#support) support section.
