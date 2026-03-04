# Contributing to Desktop Organizer

Thank you for your interest in contributing to Desktop Organizer! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/desktop-organizer.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
5. Install in development mode: `pip install -e ".[dev]"`
6. Install pre-commit hooks: `pre-commit install`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Run linting: `ruff check src/ && ruff format src/`
5. Run type checking: `mypy src/desktop_organizer`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings in Google format
- Keep functions focused and small
- Add tests for new features

## Testing

- Write tests using pytest
- Maintain or improve code coverage
- Test edge cases
- Mock external dependencies

## Reporting Issues

When reporting issues, please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Feature Requests

We welcome feature requests! Please:
- Check if the feature already exists
- Describe the use case
- Explain why it would be useful

## Code of Conduct

Be respectful and constructive in all interactions.

## Questions?

Feel free to open an issue for any questions!
