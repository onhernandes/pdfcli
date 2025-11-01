.PHONY: test test-cov test-unit test-integration test-cli install install-dev clean

# Install package in development mode
install:
	pip install -e .

# Install with test dependencies
install-dev:
	pip install -e .[test]

# Run all tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=pdf_manager --cov-report=html --cov-report=term

# Run only unit tests
test-unit:
	pytest -m unit

# Run only integration tests
test-integration:
	pytest -m integration

# Run only CLI tests
test-cli:
	pytest -m cli

# Clean up test artifacts
clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete