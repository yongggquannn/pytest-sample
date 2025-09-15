# Pytest Sample

A simple Python project demonstrating pytest testing structure.

## Setup

```bash
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_calculator.py

# Verbose output
pytest -v
```

## Project Structure

```
pytest-sample/
├── src/
│   ├── __init__.py
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
├── requirements.txt
└── README.md
```