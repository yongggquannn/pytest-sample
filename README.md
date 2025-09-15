# Pytest Sample

A simple Python project demonstrating pytest testing structure.

## Setup

```bash
pip install -r requirements.txt
```

**Alternative:** If you're using Python 3 specifically or the above command fails (common on macOS/Linux systems where `pip` points to Python 2):

```bash
pip3 install -r requirements.txt
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

**Alternative:** If `pytest` command is not found or you want to ensure you're using the correct Python version:

```bash
# Run all tests
python3 -m pytest

# Run with coverage
python3 -m pytest --cov=src

# Run specific test file
python3 -m pytest tests/test_calculator.py

# Verbose output
python3 -m pytest -v
```


## Project Structure

```
pytest-sample/
├── tests/                  # Test files
│   └── test_mock_api.py   # API testing with mocked responses
├── input/                  # Configuration and data files
│   └── testing.yml        # Test configuration data
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```