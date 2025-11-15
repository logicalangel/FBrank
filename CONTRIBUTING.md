# Contributing to InnerMatch

First off, thank you for considering contributing to InnerMatch! It's people like you that make InnerMatch such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible.
- **Provide specific examples to demonstrate the steps**.
- **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
- **Explain which behavior you expected to see instead and why**.
- **Include Python version, OS, and InnerMatch version**.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Provide specific examples to demonstrate the steps** or provide code snippets.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
- **Explain why this enhancement would be useful** to most InnerMatch users.

### Pull Requests

- Fill in the required template
- Do not include issue numbers in the PR title
- Follow the Python style guide (PEP 8)
- Include thoughtfully-worded, well-structured tests
- Document new code
- End all files with a newline

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/InnerMatch.git
cd InnerMatch
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=innermatch --cov-report=html

# Run specific test file
pytest tests/test_ranker.py

# Run specific test
pytest tests/test_ranker.py::TestFeedbackRanker::test_ranker_initialization
```

### Code Quality

```bash
# Format code with black
black innermatch/ tests/

# Check formatting
black --check innermatch/ tests/

# Lint with flake8
flake8 innermatch/ --max-line-length=100

# Type checking with mypy
mypy innermatch/
```

### Before Committing

Make sure your changes pass all checks:

```bash
# 1. Format code
black innermatch/ tests/

# 2. Run tests
pytest

# 3. Check coverage (should be > 90%)
pytest --cov=innermatch --cov-report=term

# 4. Lint
flake8 innermatch/ --max-line-length=100

# 5. Type check
mypy innermatch/ --ignore-missing-imports
```

## Style Guidelines

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to all public modules, functions, classes, and methods
- Use type hints for function arguments and return values

### Documentation Style

- Use Google-style docstrings:

```python
def function(arg1: str, arg2: int) -> bool:
    """
    Brief description of the function.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When something goes wrong
    """
    pass
```

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
- 🎨 `:art:` when improving the format/structure of the code
- 🐛 `:bug:` when fixing a bug
- ✨ `:sparkles:` when adding a new feature
- 📝 `:memo:` when writing docs
- 🚀 `:rocket:` when improving performance
- ✅ `:white_check_mark:` when adding tests
- 🔒 `:lock:` when dealing with security

Example:

```text
✨ Add support for custom learning rates

- Implement learning_rate parameter in FeedbackRanker
- Add tests for learning rate functionality
- Update documentation

Fixes #123
```

## Testing Guidelines

- Write tests for all new features
- Ensure all tests pass before submitting a PR
- Aim for > 90% code coverage
- Use descriptive test names
- Group related tests in classes
- Use fixtures for common setup

Example:

```python
class TestFeedbackRanker:
    """Test suite for FeedbackRanker class."""

    @pytest.fixture
    def ranker(self):
        """Create a FeedbackRanker instance for testing."""
        return FeedbackRanker("user", "pass", "session")

    def test_initialization(self, ranker):
        """Test that ranker initializes correctly."""
        assert ranker.user_id == "user"
```

## Documentation

- Update the README.md if you change functionality
- Add docstrings to new functions/classes
- Update the API reference if needed
- Add examples for new features

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. GitHub Actions will automatically publish to PyPI

## Questions?

Feel free to contact us:

- Open an issue for bug reports or feature requests
- Email: [synaptosearch@gmail.com](mailto:synaptosearch@gmail.com)
- GitHub Discussions: For general questions

## Recognition

Contributors will be recognized in:

- The project README
- Release notes
- The GitHub contributors page

Thank you for contributing to InnerMatch! 🎉
