# Testing Documentation for Archimind API

This document describes how to run tests for the Archimind API project and the testing architecture.

## Test Structure

The test suite is organized into the following components:

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and their interactions
- **Configuration Tests**: Test configuration and environment setups

## Test Files

- `conftest.py`: Contains common fixtures and configurations for tests
- `test_main.py`: Tests for basic API endpoints and health checks
- `test_auth.py`: Tests for authentication routes
- `test_notifications.py`: Tests for notification routes
- `test_save.py`: Tests for save routes
- `test_stats.py`: Tests for statistics routes
- `test_user.py`: Tests for user routes
- `test_prompts_folders.py`: Tests for prompt folders routes
- `test_prompts_templates.py`: Tests for prompt templates routes

## Running Tests Locally

### Prerequisites

1. Make sure you have Python 3.10+ installed
2. Install the required packages:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pytest-mock
```

### Running All Tests

To run all tests with coverage:

```bash
pytest tests/ --cov=./ --cov-report=term
```

### Running Specific Test Files

To run a specific test file:

```bash
pytest tests/test_auth.py
```

### Running Specific Tests

To run a specific test:

```bash
pytest tests/test_auth.py::test_sign_in_success
```

## CI/CD Integration

Tests are automatically run in the CI/CD pipeline using GitHub Actions:

1. On every push to `main` and `develop` branches
2. On every pull request to `main` and `develop` branches

The GitHub Actions workflow:
1. Sets up Python
2. Installs dependencies
3. Runs tests with coverage
4. Uploads coverage reports

## Mocking Strategy

The test suite uses a comprehensive mocking strategy:

1. **Supabase Mocking**: All Supabase client interactions are mocked
2. **Authentication Mocking**: User authentication is mocked
3. **Environment Mocking**: Environment variables are mocked

## Coverage Goals

- Routes: 90%+ coverage
- Utility functions: 95%+ coverage
- Edge cases and error handling: 80%+ coverage

## Adding New Tests

When adding new features to the API, ensure you:

1. Create new test files for new routes
2. Add tests for both success and error cases
3. Mock external dependencies
4. Verify authentication requirements
5. Cover edge cases and validation

## Troubleshooting Tests

Common issues:

1. **Missing Mocks**: Ensure all external dependencies are properly mocked
2. **Authentication Issues**: Check that the authentication mock is properly configured
3. **Fixture Issues**: Verify that fixtures are correctly set up in `conftest.py`
4. **Environment Issues**: Ensure environment variables are properly mocked or set