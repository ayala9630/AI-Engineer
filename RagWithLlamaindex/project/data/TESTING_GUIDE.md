# Testing Guide for Task Manager Project

## Testing Framework

This project uses **pytest** for all testing. Install it via:
```bash
pip install pytest pytest-cov
```

## Test Structure

Tests should be organized as follows:
```
tests/
├── __init__.py
├── test_task.py           # Task model tests
├── test_database.py       # Database operations tests
├── test_taskmanager.py    # TaskManager class tests
├── test_app.py            # Flask app/API tests
└── conftest.py            # Shared fixtures
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_task.py
```

### Run specific test
```bash
pytest tests/test_task.py::test_task_creation
```

### Run with coverage
```bash
pytest --cov=task_manager --cov-report=htmlcov
```

### Run with verbose output
```bash
pytest -v
```

### Run with print output captured
```bash
pytest -s
```

## Test Patterns

### Unit Test Template
```python
import pytest
from task_manager.task import Task

class TestTaskCreation:
    """Test task model creation and validation."""
    
    def test_create_task_with_default_values(self):
        """Should create task with default priority and status."""
        task = Task(title="Buy milk")
        
        assert task.title == "Buy milk"
        assert task.priority == "medium"
        assert task.status == "pending"
        assert task.id is None
    
    def test_create_task_with_custom_values(self):
        """Should create task with specified values."""
        task = Task(
            title="Review PR",
            description="Check code quality",
            priority="high"
        )
        
        assert task.title == "Review PR"
        assert task.description == "Check code quality"
        assert task.priority == "high"
    
    def test_invalid_priority_raises_error(self):
        """Should raise ValueError for invalid priority."""
        with pytest.raises(ValueError):
            Task(title="Test", priority="mega-high")
```

### Database Test Template with In-Memory Database
```python
import pytest
from task_manager.database import TaskDatabase
from task_manager.task import Task

@pytest.fixture
def db():
    """Create in-memory database for testing."""
    database = TaskDatabase(db_path=":memory:")
    yield database
    database.close()

class TestTaskDatabase:
    """Test database operations."""
    
    def test_save_and_retrieve_task(self, db):
        """Should save task and retrieve it."""
        task = Task(title="Test Task")
        saved = db.save_task(task)
        
        retrieved = db.get_task(saved.id)
        assert retrieved.title == "Test Task"
        assert retrieved.id == saved.id
    
    def test_update_task(self, db):
        """Should update task fields."""
        task = Task(title="Original", priority="low")
        saved = db.save_task(task)
        
        saved.title = "Updated"
        saved.priority = "high"
        updated = db.save_task(saved)
        
        retrieved = db.get_task(updated.id)
        assert retrieved.title == "Updated"
        assert retrieved.priority == "high"
    
    def test_delete_task(self, db):
        """Should delete task from database."""
        task = Task(title="To Delete")
        saved = db.save_task(task)
        
        db.delete_task(saved.id)
        
        retrieved = db.get_task(saved.id)
        assert retrieved is None
```

### Flask API Test Template
```python
import pytest
from task_manager.app import app
from task_manager.database import TaskDatabase

@pytest.fixture
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    app.db = TaskDatabase(db_path=":memory:")
    
    with app.test_client() as client:
        yield client
    
    app.db.close()

class TestTaskAPI:
    """Test REST API endpoints."""
    
    def test_get_empty_task_list(self, client):
        """Should return empty list when no tasks exist."""
        response = client.get('/api/tasks')
        
        assert response.status_code == 200
        assert len(response.json['data']) == 0
    
    def test_create_task_via_api(self, client):
        """Should create task via POST endpoint."""
        response = client.post('/api/tasks', json={
            "title": "API Task",
            "priority": "high"
        })
        
        assert response.status_code == 201
        assert response.json['success'] is True
        assert response.json['data']['title'] == "API Task"
    
    def test_create_task_missing_title_returns_400(self, client):
        """Should reject task without title."""
        response = client.post('/api/tasks', json={
            "priority": "high"
        })
        
        assert response.status_code == 400
        assert response.json['success'] is False
```

## Test Coverage Goals

- **Task Model**: 90%+ coverage
  - Validation tests
  - Serialization/deserialization
  - Status transitions

- **Database Layer**: 85%+ coverage
  - CRUD operations
  - Error conditions
  - Schema initialization

- **TaskManager**: 80%+ coverage
  - Business logic
  - CLI operations
  - Filtering and sorting

- **Flask App**: 75%+ coverage
  - Route handlers
  - Error responses
  - Request validation

## Testing Procedures

### Before Adding Features
1. Write tests for expected behavior
2. Write tests for edge cases
3. Write tests for error conditions
4. Implement feature
5. Run tests and verify all pass

### Before Committing Code
1. Run full test suite: `pytest`
2. Check coverage: `pytest --cov=task_manager`
3. Fix any failing tests
4. Ensure coverage meets minimum (70% for code, 80% for critical paths)

### Debugging Test Failures
```bash
# Show print statements and logs
pytest -s

# Show extra info and local variables
pytest -vv

# Run only failing tests from last run
pytest --lf

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb
```

## Mocking Patterns

### Mock Database for Testing TaskManager
```python
from unittest.mock import MagicMock, patch
from task_manager.main import TaskManager
from task_manager.task import Task

def test_taskmanager_with_mocked_db():
    """Test TaskManager without real database."""
    with patch('task_manager.main.TaskDatabase') as MockDB:
        mock_db = MagicMock()
        MockDB.return_value = mock_db
        
        # Setup mock behavior
        test_task = Task(id=1, title="Test")
        mock_db.get_task.return_value = test_task
        
        # Test
        manager = TaskManager()
        result = manager.get_task(1)
        
        # Verify
        assert result.title == "Test"
        mock_db.get_task.assert_called_once_with(1)
```

### Mock External APIs
```python
@patch('requests.get')
def test_with_external_api_mocked(mock_get):
    """Test code that calls external API."""
    mock_get.return_value.json.return_value = {"status": "ok"}
    
    # Your test code here
```

## Continuous Testing

### Watch Mode (Testing on File Changes)
```bash
pytest-watch
```

### Pytest Configuration
Create `pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers -v
```

## Integration Testing

For testing multiple components together:

```python
def test_complete_workflow():
    """Test full task creation and update workflow."""
    db = TaskDatabase(":memory:")
    manager = TaskManager()
    
    # Create
    task = manager.create_task("Integration Test")
    assert task.id is not None
    
    # Retrieve
    retrieved = manager.get_task(task.id)
    assert retrieved.title == "Integration Test"
    
    # Update
    retrieved.priority = "high"
    updated = manager.update_task(task.id, priority="high")
    assert updated.priority == "high"
    
    # Complete
    manager.mark_complete(task.id)
    final = manager.get_task(task.id)
    assert final.status == "completed"
```

## Performance Testing

```python
import time

def test_create_many_tasks_performance():
    """Ensure task creation stays fast with many tasks."""
    db = TaskDatabase(":memory:")
    manager = TaskManager()
    
    start = time.time()
    for i in range(1000):
        manager.create_task(f"Task {i}")
    elapsed = time.time() - start
    
    # Should complete in under 5 seconds
    assert elapsed < 5.0
```
