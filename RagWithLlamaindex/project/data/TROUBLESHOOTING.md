# Troubleshooting & Common Pitfalls Guide

Guide for identifying and resolving common issues in Task Manager development.

## Common Errors & Solutions

### Database Errors

#### Error: "database is locked"
**Cause**: Multiple processes accessing the database simultaneously, or connection not closed properly

**Solution**:
```python
# ✓ CORRECT - Use with statement for automatic cleanup
with TaskDatabase() as db:
    task = db.get_task(1)  # Automatically closes

# ✓ CORRECT - Explicit close in finally
db = TaskDatabase()
try:
    task = db.get_task(1)
finally:
    db.close()  # Ensures close even if exception
```

#### Error: "table tasks has no column named X"
**Cause**: Task dataclass has a field that doesn't exist in database schema

**Solution**:
1. Check database schema: `sqlite3 tasks.db ".schema"`
2. Check Task dataclass fields in task.py
3. Add migration to create_schema() if schema is outdated
4. Or delete tasks.db to recreate fresh (dev only)

#### Error: "UNIQUE constraint failed: tasks.title"
**Cause**: Trying to save a task with a title that already exists

**Solution**:
```python
# ✓ CORRECT - Check before saving
existing = db.get_tasks_by_title(new_title)
if existing:
    raise ValueError(f"Task '{new_title}' already exists")

task.title = new_title
db.save_task(task)
```

#### Error: "Incorrect number of bindings supplied"
**Cause**: Mismatch between SQL placeholders (?) and values supplied

**Solution**:
```python
# ✗ WRONG - 3 placeholders but 2 values
cursor.execute("SELECT * FROM tasks WHERE id = ? AND status = ? AND priority = ?", 
               (task_id, status))

# ✓ CORRECT - 3 placeholders and 3 values
cursor.execute("SELECT * FROM tasks WHERE id = ? AND status = ? AND priority = ?", 
               (task_id, status, priority))
```

---

### Task Validation Errors

#### Error: ValueError: "Priority must be one of..."
**Cause**: Invalid priority value passed to Task

**Solution**:
```python
# Validate before creating Task
valid_priorities = ("low", "medium", "high", "critical")
if priority not in valid_priorities:
    raise ValueError(f"Priority must be one of {valid_priorities}")

task = Task(title=title, priority=priority)
```

#### Error: "Title cannot be empty"
**Cause**: Empty or whitespace-only title

**Solution**:
```python
# ✓ CORRECT - Validate title
title = title.strip()  # Remove whitespace
if not title:
    raise ValueError("Title is required")

task = Task(title=title)
```

#### Error: TypeError: "expected string, got int"
**Cause**: Wrong type passed to field with type hint

**Solution**:
```python
# ✓ CORRECT - Convert types if needed
priority_value = str(priority_value).lower()

# ✓ CORRECT - Validate type
if not isinstance(priority_value, str):
    raise TypeError(f"Priority must be string, got {type(priority_value)}")
```

---

### Flask/Web App Errors

#### Error: 404 Not Found when accessing /api/tasks
**Cause**: Flask app not running or route not registered

**Solution**:
```bash
# 1. Check app is running
python task_manager/app.py

# 2. Verify route exists in app.py
# Look for: @app.route('/api/tasks')

# 3. Check URL is correct
# http://localhost:5000/api/tasks  ✓
# http://localhost:5000/api/task   ✗ (typo)

# 4. Check if database initialization failed
# Look for startup errors in terminal
```

#### Error: 500 Internal Server Error
**Cause**: Unhandled exception in Flask route

**Solution**:
1. Check terminal output for error message
2. Add error handling to route:
   ```python
   @app.route('/api/tasks')
   def get_tasks():
       try:
           tasks = db.get_all_tasks()
           return jsonify({"data": tasks}), 200
       except Exception as e:
           print(f"ERROR: {e}")  # Log error
           return jsonify({"error": str(e)}), 500
   ```
3. Look at error trace in Flask logs

#### Error: "Failed to connect to database"
**Cause**: Database file not found or path error

**Solution**:
```python
# ✓ CORRECT - Check database exists
import os
if not os.path.exists('tasks.db'):
    print("Database doesn't exist, creating...")
    db = TaskDatabase()  # Auto-creates

# ✓ CORRECT - Use absolute path if needed
db_path = os.path.abspath('tasks.db')
database = TaskDatabase(db_path)
```

---

### Test Errors

#### Error: "fixture 'X' not found"
**Cause**: Fixture defined in wrong scope or missing imports

**Solution**:
```python
# ✓ CORRECT - Define in conftest.py for shared fixtures
# tests/conftest.py
import pytest

@pytest.fixture
def db():
    database = TaskDatabase(":memory:")
    yield database
    database.close()

# ✓ CORRECT - Use in any test file
# tests/test_something.py
def test_with_db(db):
    task = db.save_task(Task(title="Test"))
    assert task.id is not None
```

#### Error: "Test passed locally but fails in CI"
**Cause**: Test assumes specific order or timing

**Solution**:
```python
# ✗ WRONG - Relies on test order
def test_one():
    global_task = Task(title="Test")

def test_two():
    assert global_task is not None  # Fails if run first

# ✓ CORRECT - Independent tests
def test_creates_task():
    task = Task(title="Test")
    assert task is not None

def test_validates_priority():
    with pytest.raises(ValueError):
        Task(title="Test", priority="invalid")
```

#### Error: "AssertionError: assert [] == [...]"
**Cause**: Query returned empty list when data expected

**Solution**:
1. Check test data setup:
   ```python
   def test_get_tasks(db):
       # Setup
       task = Task(title="Test")
       saved = db.save_task(task)
       
       # Execute
       results = db.get_all_tasks()
       
       # Assert
       assert len(results) > 0
       assert any(t.id == saved.id for t in results)
   ```

2. Verify database is using in-memory for testing:
   ```python
   db = TaskDatabase(":memory:")  # ✓ CORRECT for tests
   ```

#### Error: "Test timeout - test took too long"
**Cause**: Infinite loop or blocking operation

**Solution**:
```python
# ✓ CORRECT - Set timeout
def test_with_timeout():
    import signal
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Test took too long")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)  # 5 second timeout
    
    try:
        # Your test code
        pass
    finally:
        signal.alarm(0)  # Cancel alarm
```

---

### Common Logic Errors

#### Bug: Task marked complete but status shows "pending"
**Cause**: Converting bool completed to status incorrectly

**Solution**:
- Always check consistency between status and completed fields
- Consider migrating away from duplicate fields:
  ```python
  # ✗ PROBLEMATIC - Status and completed can get out of sync
  status: str  # "pending", "in_progress", "completed"
  completed: bool
  
  # ✓ BETTER - Single source of truth
  status: str = "pending"  # No separate completed field
  ```

#### Bug: Filtering by priority returns wrong tasks
**Cause**: Case-sensitivity mismatch

**Solution**:
```python
# ✓ CORRECT - Normalize case
query_priority = priority.lower()
tasks = [t for t in all_tasks if t.priority.lower() == query_priority]

# In database:
cursor.execute(
    "SELECT * FROM tasks WHERE LOWER(priority) = LOWER(?)",
    (priority,)
)
```

#### Bug: SQL injection vulnerability
**Cause**: String interpolation in SQL instead of parameterized queries

**Solution**:
```python
# ✗ WRONG - SQL injection vulnerability!
query = f"SELECT * FROM tasks WHERE priority = '{priority}'"
cursor.execute(query)

# ✓ CORRECT - Use parameterized query
cursor.execute("SELECT * FROM tasks WHERE priority = ?", (priority,))
```

---

## Performance Issues

### Problem: App is slow when loading tasks

**Diagnosis**:
```python
import time

@app.route('/api/tasks')
def get_tasks():
    start = time.time()
    tasks = db.get_all_tasks()
    print(f"Query took {time.time() - start:.3f}s")  # Log duration
    return jsonify([asdict(t) for t in tasks])
```

**Solutions** (in order of impact):

1. **Add database indexes** (most common):
   ```python
   cursor.execute("CREATE INDEX idx_status ON tasks(status)")
   cursor.execute("CREATE INDEX idx_priority ON tasks(priority)")
   ```

2. **Filter in database, not in-memory**:
   ```python
   # ✗ SLOW - Loads all, filters in Python
   tasks = db.get_all_tasks()
   filtered = [t for t in tasks if t.priority == 'high']
   
   # ✓ FAST - Filters in database
   filtered = db.get_tasks_by_priority('high')
   ```

3. **Limit data returned**:
   ```python
   # ✓ CORRECT - Paginate results
   @app.route('/api/tasks?page=1&limit=50')
   def get_tasks_paginated(page=1, limit=50):
       offset = (page - 1) * limit
       tasks = db.get_all_tasks()[offset:offset + limit]
       return jsonify(tasks)
   ```

4. **Cache frequently accessed data**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_statistics():
       return db.calculate_statistics()
   
   # Clear cache when data changes
   get_statistics.cache_clear()
   ```

---

## Debugging Strategies

### Strategy 1: Print Debugging

```python
# Add strategic print statements
def save_task(self, task: Task) -> Task:
    print(f"DEBUG: Saving task: {task.title}")
    
    cursor.execute("""INSERT INTO tasks (title, priority, status) 
                      VALUES (?, ?, ?)""",
                   (task.title, task.priority, task.status))
    print(f"DEBUG: Inserted with ID: {cursor.lastrowid}")
    
    self.connection.commit()
    print("DEBUG: Committed to database")
```

### Strategy 2: Logging (Better)

```python
import logging

logger = logging.getLogger(__name__)

def save_task(self, task: Task) -> Task:
    logger.debug(f"Saving task: {task.title}")
    
    # ... database operations ...
    
    logger.info(f"Task saved with ID: {task.id}")
```

### Strategy 3: Debugger Breakpoints

```python
# Python debugger
import pdb

def problematic_function():
    x = 1
    pdb.set_trace()  # Execution stops here
    y = x + 2
    pdb.set_trace()  # Can step through


# In pytest
pytest --pdb tests/test_file.py  # Drops into debugger on failure
```

### Strategy 4: Unit Testing

```python
# Write small tests to isolate problem
def test_task_save_preserves_title():
    db = TaskDatabase(":memory:")
    task = Task(title="My Task")
    
    saved = db.save_task(task)
    retrieved = db.get_task(saved.id)
    
    assert retrieved.title == "My Task"
```

---

## Prevention Checklist

Before committing code:

- [ ] All tests pass: `pytest`
- [ ] Coverage maintained: `pytest --cov=task_manager`
- [ ] No SQL injection: All queries use ? placeholders
- [ ] Proper error handling: Try-except with specific exceptions
- [ ] Type hints: All functions have them
- [ ] Docstrings: Public methods documented
- [ ] Database cleanup: Connections closed in finally blocks
- [ ] Input validation: All user input validated
- [ ] Edge cases tested: Empty, None, boundary values
- [ ] Performance considered: No N+1 queries, indexes where needed

---

## When Code is Completely Broken

### Step 1: Isolate the Problem
```bash
# Run tests to see what's failing
pytest --tb=short

# Run specific failing test with verbose output
pytest tests/test_file.py::test_name -vvs
```

### Step 2: Revert Recent Changes
```bash
# If using git
git diff task_manager/file.py  # See what changed
git checkout task_manager/file.py  # Revert to last version

# Or manually restore from backup if not using git
```

### Step 3: Start Fresh
```bash
# Backup the old code
cp task_manager/file.py task_manager/file.py.bak

# Delete problematic database
rm tasks.db

# Run application again to see if it starts
python task_manager/main.py
```

### Step 4: Debug Systematically
1. Add one line at a time
2. Test after each line
3. Identify which line breaks it
4. Fix that one issue

---

## Getting Help

### When stuck:
1. Check [AGENT_GUIDE.md](AGENT_GUIDE.md)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand structure
3. Look at [WORKFLOWS.md](WORKFLOWS.md) for common patterns
4. Read [FEATURE_GUIDE.md](FEATURE_GUIDE.md) for step-by-step approaches
5. Check file-specific instructions in `.github/instructions/`
6. Write a small test to understand the issue
7. Add print/debug statements to trace execution

Remember: **If tests pass, the code is correct.** Trust the tests!
