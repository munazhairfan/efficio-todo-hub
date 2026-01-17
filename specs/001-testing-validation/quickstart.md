# Quickstart Guide: Testing & Validation for Chatbot-Based Todo System

**Feature**: Testing & Validation for Chatbot-Based Todo System
**Date**: 2026-01-17
**Branch**: 001-testing-validation

## Overview
This guide provides step-by-step instructions to set up and run the comprehensive testing suite for the chatbot-based todo system. The testing approach follows black-box principles using real database and OpenRouter AI integration.

## Prerequisites

### Environment Setup
1. **Python 3.11+** installed on your system
2. **Node.js 18+** for frontend testing
3. **PostgreSQL** database (or access to Neon PostgreSQL)
4. **OpenRouter API key** with appropriate permissions
5. **Git** for version control

### Required Configuration
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd efficio-todo-hub
   ```

2. Set up backend environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up frontend environment:
   ```bash
   cd ../frontend
   npm install
   ```

4. Configure environment variables:
   ```bash
   # backend/.env
   DATABASE_URL=postgresql://username:password@localhost:5432/test_db
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   SECRET_KEY=your_secret_key
   ```

## Running the Test Suite

### Phase 1: API Tests
Verify chat endpoint works with valid and invalid inputs.

```bash
# Navigate to backend
cd backend

# Run API-specific tests
pytest tests/api/ -v

# Or run specific chat endpoint tests
pytest tests/api/chat_tests.py -v
```

### Phase 2: Chatbot Logic Tests
Verify natural language → correct MCP tool mapping.

```bash
# Run chatbot logic tests
pytest tests/unit/agent_tests.py -v
pytest tests/integration/conversation_tests.py -v
```

### Phase 3: MCP Tools Tests
Verify each tool performs correct DB operations.

```bash
# Run MCP tools tests
pytest tests/integration/mcp_tool_tests.py -v
pytest tests/unit/service_tests.py -v
```

### Phase 4: Conversation Persistence Tests
Verify stateless requests still preserve context.

```bash
# Run conversation persistence tests
pytest tests/integration/conversation_tests.py -v
```

### Phase 5: Failure & Edge Case Tests
Verify system behavior under bad inputs and failures.

```bash
# Run error handling tests
pytest tests/integration/error_handling_tests.py -v
pytest tests/unit/error_tests.py -v
```

### Phase 6: Rate Limit Tests
Verify limits are enforced and reset correctly.

```bash
# Run rate limiting tests
pytest tests/integration/rate_limit_tests.py -v
```

## Complete Test Suite Execution

To run the entire test suite:

```bash
# Backend tests
cd backend
pytest tests/ --cov=src/ --cov-report=html

# Frontend tests
cd ../frontend
npm test

# Or run all tests with coverage
cd backend
pytest tests/ --cov=src/ --cov-report=term-missing -x
```

## Running Specific Test Categories

### API Tests Only
```bash
cd backend
pytest tests/api/ --tb=short
```

### Integration Tests Only
```bash
cd backend
pytest tests/integration/ --tb=short
```

### End-to-End Tests (Frontend)
```bash
cd frontend
npx playwright test
# Or for specific tests
npx playwright test chat_interface.test.ts
```

## Test Configuration

### Environment Variables for Testing
```bash
# Test-specific configurations
TEST_DATABASE_URL=postgresql://localhost:5432/test_todo_db
TEST_TIMEOUT=30
OPENROUTER_TEST_MODE=true
SKIP_SLOW_TESTS=false
```

### Custom pytest Configuration
Create `backend/pytest.ini`:
```ini
[tool:pytest]
testpaths = tests
python_files = *_test.py test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    api: marks tests as API tests
    chatbot: marks tests as chatbot logic tests
    mcp: marks tests as MCP tool tests
    rate_limit: marks tests as rate limiting tests
    error_handling: marks tests as error handling tests
```

## Viewing Test Results

### Console Output
Tests provide detailed output in the console showing pass/fail status and execution time.

### Coverage Reports
HTML coverage reports are generated in `backend/htmlcov/` after running tests with coverage.

### Test Logs
Detailed logs are available in `backend/tests/logs/` for debugging failed tests.

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure PostgreSQL is running
   - Verify `DATABASE_URL` is correctly set
   - Check database permissions

2. **OpenRouter API Errors**
   - Verify `OPENROUTER_API_KEY` is set correctly
   - Check API key permissions
   - Ensure internet connectivity

3. **Authentication Failures**
   - Verify `SECRET_KEY` is set
   - Check JWT token validity periods
   - Ensure proper authorization headers

4. **Rate Limiting Issues**
   - Adjust test delays if hitting API limits
   - Use test-specific API keys when possible

### Debugging Failed Tests

1. Run a specific test with maximum verbosity:
   ```bash
   pytest tests/path/to/test_file.py::test_specific_function -vvv -s
   ```

2. Use pytest's pdb debugger:
   ```bash
   pytest tests/path/to/test_file.py -s --pdb
   ```

3. Check test logs in the logs directory for detailed error information.

## Best Practices

### Writing New Tests
- Follow the existing test structure and naming conventions
- Use parametrized tests for multiple input scenarios
- Include proper assertions for expected outcomes
- Clean up test data after each test run

### Test Maintenance
- Regularly update tests when requirements change
- Monitor test execution time and performance
- Review and update test data periodically
- Maintain test coverage thresholds

### Continuous Integration
- Configure CI pipeline to run tests automatically
- Set up notifications for test failures
- Monitor test execution trends over time
- Implement flaky test detection and reporting