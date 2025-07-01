# Contributing to C25K Calendar Creator

First off, thank you for considering contributing to the C25K Calendar Creator! 🎉

## 🌟 How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title**: Summarize the issue in the title
- **Detailed description**: What happened vs. what you expected
- **Steps to reproduce**: Clear steps to reproduce the issue
- **Environment details**: OS, Python version, dependencies
- **Screenshots**: If applicable, add screenshots
- **Error messages**: Include full error messages and stack traces

### 💡 Suggesting Features

Feature requests are welcome! Please provide:

- **Clear use case**: Why would this feature be useful?
- **Detailed description**: How should it work?
- **Alternative solutions**: What alternatives have you considered?
- **Additional context**: Any other relevant information

### 🔧 Code Contributions

#### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/C25K-Calendar-Creator.git
   cd C25K-Calendar-Creator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install black isort pytest  # Development tools
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Standards

- **Python Version**: Support Python 3.8+
- **Code Style**: Use Black for formatting (`python -m black .`)
- **Import Sorting**: Use isort (`python -m isort .`)
- **Type Hints**: Include type hints for new functions
- **Documentation**: Add docstrings for public functions
- **Testing**: Include tests for new functionality

#### Testing

Run the test suite before submitting:
```bash
python -m pytest tests/ -v
```

For new features, add tests in the `tests/` directory following existing patterns.

#### Pull Request Process

1. **Update documentation**: Update README.md if needed
2. **Test your changes**: Ensure all tests pass
3. **Format your code**: Run black and isort
4. **Write clear commit messages**: Use descriptive, present-tense messages
5. **Create a pull request**: Include a clear description of changes

### 📚 Documentation Contributions

Documentation improvements are always welcome:

- **README updates**: Clarify instructions, add examples
- **Code comments**: Improve inline documentation
- **User guides**: Add tutorials or how-to guides
- **API documentation**: Enhance docstrings

### 🌍 Translation Contributions

Help make the app accessible to more users:

- **Language support**: Add new language translations
- **Improve existing translations**: Fix or enhance current translations
- **Cultural adaptations**: Suggest region-specific features

## 🎯 Project Structure

Understanding the codebase:

```
C25K Calendar Creator/
├── c25k_ics_generator.py          # Main application entry point
├── modules/                       # Core application modules
│   ├── core.py                   # Business logic (plan generation)
│   ├── pyqt_gui.py              # PyQt6 user interface
│   ├── exports.py               # Export functionality
│   └── utils.py                 # Utility functions
├── c25k_utils/                   # Specialized utilities
│   ├── accessibility.py         # Accessibility features
│   └── mobile_export.py         # Mobile app integrations
├── tests/                        # Test suite
└── docs/                         # Documentation files
```

### Key Components

- **`modules/core.py`**: Plan generation logic, workout definitions
- **`modules/pyqt_gui.py`**: Main GUI interface and user interactions
- **`modules/exports.py`**: Export functionality for different formats
- **`c25k_utils/`**: Specialized utilities for accessibility and mobile exports

## 📋 Contribution Guidelines

### Code Quality

- **Readability**: Write clear, self-documenting code
- **Performance**: Consider performance impact of changes
- **Security**: Avoid introducing security vulnerabilities
- **Accessibility**: Maintain and improve accessibility features

### Medical Content

When contributing medical or health-related content:

- **Evidence-based**: Base recommendations on reputable sources
- **Citations**: Include references to medical guidelines
- **Disclaimers**: Maintain appropriate medical disclaimers
- **Safety first**: Prioritize user safety in all recommendations

### UI/UX Contributions

For interface improvements:

- **Accessibility**: Ensure changes maintain accessibility standards
- **Consistency**: Follow existing design patterns
- **Usability**: Test changes with real users when possible
- **Responsive**: Consider different screen sizes and DPI settings

## 🚀 Release Process

### Version Management

- **Semantic Versioning**: Follow semver.org guidelines
- **CHANGELOG**: Update CHANGELOG.md for all changes
- **Testing**: Ensure comprehensive testing before releases

### Feature Development

1. **Discuss first**: For major features, create an issue for discussion
2. **Break down**: Split large features into smaller, reviewable PRs
3. **Incremental**: Submit incremental improvements rather than massive changes
4. **Backwards compatibility**: Maintain compatibility when possible

## 💬 Communication

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Code Review**: Engage constructively in code reviews

### Community Guidelines

- **Be respectful**: Treat all contributors with respect
- **Be constructive**: Provide helpful, actionable feedback
- **Be patient**: Remember that everyone is learning
- **Be inclusive**: Welcome contributors of all skill levels

## 🏆 Recognition

Contributors will be recognized in:

- **CHANGELOG.md**: Major contributions noted in release notes
- **README.md**: Contributors section (if implemented)
- **Release notes**: Acknowledgment in GitHub releases

## 📝 Legal

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

## Thank You! 🙏

Every contribution, no matter how small, makes this project better for everyone. Whether you're fixing a typo, adding a feature, or helping with documentation, your efforts are appreciated!

**Happy Contributing!** 🎉
