# Contributing to ETL Mapping Validator

Thank you for your interest in contributing!

## Filing an Issue

Found a bug or have a feature request? Please [open an issue](https://github.com/hkrishnan62/ETL_Parser/issues) on GitHub. Include a clear title, a description of the problem or request, steps to reproduce (for bugs), and any relevant error messages or screenshots. Check existing issues first to avoid duplicates.

## Submitting a Pull Request

1. Fork the repository and create a new branch from `main` (e.g., `git checkout -b fix/my-bug`).
2. Make your changes, including tests for any new behaviour.
3. Ensure all tests pass (`pytest tests/`).
4. Open a pull request against `main` with a clear description of what changed and why. Link to the related issue if one exists.

## Code Style

This project follows [PEP 8](https://peps.python.org/pep-0008/). Please run `flake8` before submitting. Keep lines to 120 characters or fewer and use descriptive variable names. No external linter configuration file is required beyond what is already in the repo.

## Running the Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full test suite
pytest tests/

# Run a specific test file
pytest tests/test_integration.py
```

All pull requests must pass the test suite before review.
