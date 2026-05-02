# Contributing to DODO CLI

Thank you for your interest in contributing to DODO CLI! This document provides guidelines for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Basic knowledge of robotics and/or machine learning

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/Dodo_CLI.V1.0.git
   cd Dodo_CLI.V1.0
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in Development Mode**
   ```bash
   pip install -e .[dev]
   ```

4. **Run Tests**
   ```bash
   pytest tests/
   ```

## 📝 Development Guidelines

### Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/
```

### Testing

- Write tests for new features in `tests/`
- Use descriptive test names
- Aim for high test coverage

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/dodo

# Run specific test
pytest tests/test_metadata.py
```

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Examples:
```
feat(cli): add export command
fix(metadata): handle empty sensor data
docs(readme): update installation instructions
```

## 🏗️ Project Structure

```
src/dodo/
├── cli.py              # Main CLI interface
├── metadata.py         # Metadata generation
├── alignment.py        # Sensor data alignment
├── models.py           # Pydantic models
├── config.py           # Configuration management
├── project.py          # Project utilities
├── security.py         # Authentication
├── validation.py       # Dataset validation
├── filter.py           # Data filtering
├── exporter.py         # Dataset export
├── importers/          # Data importers
│   ├── __init__.py
│   ├── rosbag.py
│   ├── json.py
│   └── mock.py
├── sensor_detection.py # Sensor type detection
└── alignment.py        # Temporal alignment
```

## 🐛 Bug Reports

When filing bug reports, please include:

1. **Environment Information**
   - Python version
   - DODO CLI version
   - Operating system

2. **Steps to Reproduce**
   - Detailed steps to reproduce the issue
   - Sample data (if applicable)

3. **Expected vs Actual Behavior**
   - What you expected to happen
   - What actually happened

4. **Error Messages**
   - Full error traceback

## 💡 Feature Requests

When requesting features, please:

1. **Describe the Use Case**
   - What problem are you trying to solve?
   - Why is this feature needed?

2. **Proposed Solution**
   - How should the feature work?
   - Any specific requirements?

3. **Alternatives Considered**
   - Other approaches you've considered

## 📤 Pull Requests

### Before Submitting

1. **Run Tests**
   ```bash
   pytest tests/
   ```

2. **Format Code**
   ```bash
   black src/
   ```

3. **Lint Code**
   ```bash
   flake8 src/
   ```

4. **Update Documentation**
   - Update README.md if needed
   - Add docstrings to new functions

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests for new functionality

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🏷️ Release Process

Releases are managed by the maintainers:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create Git tag
4. Publish to PyPI

## 🤝 Community

- Be respectful and inclusive
- Help newcomers learn
- Ask questions if unsure
- Participate in discussions

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discord**: For general discussion
- **Email**: team@dodo-robotics.com

Thank you for contributing to DODO CLI! 🎉
