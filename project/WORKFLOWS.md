# Common Development Workflows

Quick reference for typical development tasks and how to execute them.

## Setup & Environment

### One-Time Setup
```bash
# Clone or navigate to project
cd project

# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
python -m task_manager.main --help
```

### Start Development
```bash
# Activate environment
.\.venv\Scripts\activate

# Run web app
python task_manager/app.py

# In another terminal, run CLI
python task_manager/main.py
```

## Common Workflows

### Workflow: Fixing a Bug

1. **Identify the bug**
   - Check error message or reproduction steps
   - Determine which component is affected

2. **Create a test that reproduces it**
   ```python
   # tests/test_bug_fix.py
   def test_bug_reproduction():
       """Reproduce the bug."""
       # Setup
       # Execute
       # Assert - verify bug exists
   ```

3. **Run the test to confirm it fails**
   ```bash
   pytest tests/test_bug_fix.py::test_bug_reproduction -v
   ```

4. **Fix the bug**
   - Identify root cause in relevant file
   - Make minimal change to fix it
   - Follow code style and patterns

5. **Verify the test passes**
   ```bash
   pytest tests/test_bug_fix.py::test_bug_reproduction -v
   ```

6. **Run full test suite**
   ```bash
   pytest --cov=task_manager
   ```

7. **Test manually** through UI/CLI where applicable

### Workflow: Adding a New API Endpoint

1. **Document the endpoint**
   - Method: GET, POST, PUT, DELETE
   - Path: `/api/tasks/...`
   - Request body (if POST/PUT)
   - Response format
   - Error cases

2. **Add to app.py**
   ```python
   @app.route('/api/tasks/<int:id>/new-action', methods=['POST'])
   def perform_action(id):
       # Validate input
       # Perform action
       # Return JSON response
   ```

3. **Add test in tests/test_app.py**
   ```python
   def test_new_endpoint_success(client):
       # Test successful case
   
   def test_new_endpoint_validation(client):
       # Test invalid input
   
   def test_new_endpoint_not_found(client):
       # Test when resource doesn't exist
   ```

4. **Test the endpoint**
   ```bash
   pytest tests/test_app.py::test_new_endpoint_success -v
   
   # Manual test with curl
   curl -X POST http://localhost:5000/api/tasks/1/new-action \
     -H "Content-Type: application/json" \
     -d '{"param": "value"}'
   ```

5. **Add to frontend if needed**
   - Update `static/app.js` with JavaScript fetch call
   - Update template to trigger the action

### Workflow: Adding a New Task Field

Follow the [Feature Guide](FEATURE_GUIDE.md) for detailed steps, or summary:

1. **Add to Task dataclass (task.py)**
   ```python
   new_field: FieldType = default_value
   ```

2. **Update database schema (database.py)**
   - Add column to CREATE TABLE
   - Handle migration for existing databases
   - Update `_row_to_task()` mapping

3. **Update TaskManager if needed (main.py)**

4. **Update Flask if exposing via API (app.py)**

5. **Write tests**
   - Test field creation
   - Test field persistence
   - Test field validation

6. **Update UI if needed**
   - templates/tasks_list.html - Display field
   - static/app.js - Handle form input

### Workflow: Writing Tests

1. **Create test file** (if needed)
   ```bash
   # Organize by component
   tests/test_component_name.py
   ```

2. **Add test class**
   ```python
   class TestComponentFeature:
       """Test specific feature of component."""
       
       @pytest.fixture
       def setup(self):
           """Setup test data."""
           # Return resource
       
       def test_happy_path(self, setup):
           """Test successful case."""
           # Arrange
           # Act
           # Assert
       
       def test_error_case(self, setup):
           """Test error handling."""
           # Arrange
           # Act with invalid data
           # Assert error occurs
   ```

3. **Run tests**
   ```bash
   # Run specific test
   pytest tests/test_component.py::TestClass::test_method -v
   
   # Run all tests for component
   pytest tests/test_component.py -v
   
   # Run with coverage
   pytest --cov=task_manager --cov-report=html
   ```

4. **Improve coverage**
   - Check coverage report: `htmlcov/index.html`
   - Add tests for uncovered lines
   - Aim for >80% coverage

### Workflow: Refactoring Code

1. **Ensure test coverage exists**
   ```bash
   pytest --cov=task_manager --cov-report=html
   # Check coverage report
   ```

2. **Write tests for edge cases** (if needed)
   ```python
   def test_edge_case_1(): pass
   def test_edge_case_2(): pass
   ```

3. **Make refactoring changes** to target file/function

4. **Run related tests**
   ```bash
   pytest tests/test_relevant_module.py -v
   ```

5. **Run full test suite**
   ```bash
   pytest --cov=task_manager
   ```

6. **Manual testing** if UI affected

7. **Commit with clear message**
   ```
   Refactor: Extract method X from Y for clarity
   
   - Benefits: Better readability, easier testing
   - No behavior changes (all tests pass)
   ```

### Workflow: Debugging a Test Failure

1. **Run failing test with verbose output**
   ```bash
   pytest tests/test_file.py::test_failing_test -vv
   ```

2. **Print debug info**
   ```bash
   # Show print() statements in test
   pytest tests/test_file.py::test_name -s
   
   # Show extra verbose output
   pytest tests/test_file.py::test_name -vv
   ```

3. **Drop into debugger**
   ```bash
   # Add breakpoint in test
   pytest --pdb tests/test_file.py::test_name
   ```

4. **Check test assumptions**
   - Verify test data is correct
   - Verify mocks are set up properly
   - Check for race conditions (async code)

5. **Identify the actual bug**
   - Is it in the test or the code?
   - If in code: fix it and rerun
   - If in test: fix test assumptions

### Workflow: Code Review Checklist

Before committing code:

- [ ] Tests written and passing
- [ ] Code coverage maintained or improved (70%+)
- [ ] No hardcoded values (use constants)
- [ ] Type hints on all functions
- [ ] Docstrings on public methods
- [ ] PEP 8 style followed
- [ ] No SQL injection vulnerabilities
- [ ] Error handling in try-except blocks
- [ ] Database connections properly closed
- [ ] No duplicate code
- [ ] Feature documented
- [ ] Related files updated

### Workflow: Database Migration

1. **Plan the change**
   - What columns/tables change?
   - What about existing data?
   - Backward compatibility needed?

2. **Add migration code to `create_schema()`**
   ```python
   def create_schema(self):
       cursor = self.connection.cursor()
       
       # Create new table if doesn't exist
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS tasks_new (
               id INTEGER PRIMARY KEY,
               -- New schema here
           )
       """)
       
       # Migrate existing data if needed
       cursor.execute("""
           INSERT INTO tasks_new 
           SELECT * FROM tasks
       """)
       
       self.connection.commit()
   ```

3. **Update Task model** (task.py) if schema changed

4. **Update `_row_to_task()`** to handle new fields

5. **Write tests**
   ```python
   def test_migration_preserves_data():
       db = TaskDatabase(":memory:")
       # Add old-style data
       # Run migration
       # Verify data preserved
   ```

6. **Test with real database**
   ```bash
   # Backup old database
   cp tasks.db tasks.db.bak
   
   # Run application to trigger migration
   python task_manager/main.py
   
   # Verify data
   sqlite3 tasks.db "SELECT COUNT(*) FROM tasks;"
   ```

### Workflow: Performance Optimization

1. **Identify bottleneck**
   - Add timing measurements
   - Profile code: `python -m cProfile script.py`
   - Check slow tests

2. **Analyze the issue**
   - Is it database queries? Add indexes
   - Is it memory? Cache results
   - Is it algorithm? Optimize logic

3. **Implement optimization**
   - Add database index: `CREATE INDEX idx_name ON table(column)`
   - Add caching
   - Optimize algorithm
   - Batch operations

4. **Benchmark improvement**
   ```python
   import time
   
   start = time.time()
   # Perform operation
   elapsed = time.time() - start
   print(f"Took {elapsed:.3f} seconds")
   ```

5. **Verify no regressions**
   ```bash
   pytest --cov=task_manager
   ```

## Useful Commands Reference

```bash
# Virtual environment
python -m venv .venv           # Create
.\.venv\Scripts\activate       # Activate (Windows)
source .venv/bin/activate      # Activate (Mac/Linux)

# Dependency management
pip install -r requirements.txt # Install all
pip list                        # List installed
pip freeze > requirements.txt   # Update requirements

# Testing
pytest                          # Run all tests
pytest tests/test_file.py       # Run specific file
pytest -k test_name             # Run by name
pytest -v                       # Verbose output
pytest -s                       # Show prints
pytest --cov=task_manager       # Coverage report
pytest --cov=task_manager --cov-report=html # HTML report

# Running the app
python task_manager/app.py      # Start web server
python task_manager/main.py     # Start CLI
python -m task_manager.main     # Alternative CLI start

# Database
sqlite3 tasks.db               # Open database
.schema                        # Show schema (in sqlite3)
.mode column                   # Format output (in sqlite3)
SELECT COUNT(*) FROM tasks;    # Check data

# Code quality
python -m pylint task_manager/ # Lint code
python -m black task_manager/  # Format code
python -m isort task_manager/  # Sort imports

# Debugging
python -m pdb script.py        # Run with debugger
pytest --pdb                   # Drop into debugger on failure
python -m cProfile script.py   # Profile performance
```
