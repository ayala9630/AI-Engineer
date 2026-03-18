# Feature Implementation Workflow

## Adding a New Feature: Step-by-Step Guide

This guide walks through the process of adding a new feature to the Task Manager project systematically.

## Phase 1: Planning & Design

### 1. Define the Feature
Answer these questions:
- **What problem does it solve?** (e.g., "Users can't prioritize urgent tasks quickly")
- **Who uses it?** (CLI users, web users, API users)
- **What's the minimal viable version?** (Reduce scope to essentials)

### 2. Design the Data Model
If adding new task fields:
- What type of field? (string, boolean, number, enum, datetime, JSON)
- Is it required or optional?
- What are valid values/constraints?
- How does it serialize/deserialize?

**Example**: Adding task tags
```python
# In task.py
tags: list = field(default_factory=list)

def add_tag(self, tag: str):
    """Add a tag to this task."""
    if tag not in self.tags:
        self.tags.append(tag)

def remove_tag(self, tag: str):
    """Remove a tag from this task."""
    if tag in self.tags:
        self.tags.remove(tag)
```

### 3. Design the Interface

**For TaskManager methods**: Define the public API
```python
def add_task_tag(self, task_id: int, tag: str) -> Task:
    """Add a tag to a task."""
    pass

def get_tasks_by_tag(self, tag: str) -> List[Task]:
    """Get all tasks with a specific tag."""
    pass
```

**For API endpoints**: Define routes and parameters
```
POST /api/tasks/<id>/tags - Add tag to task
DELETE /api/tasks/<id>/tags/<tag_name> - Remove tag
GET /api/tasks?tag=<tag_name> - Filter by tag
```

**For CLI**: Define menu options
```
Tags:
  T. Add tag to task
  R. Remove tag from task
  F. Filter by tag
```

## Phase 2: Implementation

### 4. Modify the Data Model (task.py)

Follow the [Task Model Instructions](.github/instructions/task.instructions.md):

```python
# Add field to Task dataclass
tags: list = field(default_factory=list)

# Add validation in __post_init__
def __post_init__(self):
    if not isinstance(self.tags, list):
        raise TypeError("Tags must be a list")
    # Other validations...

# Add methods
def add_tag(self, tag: str):
    """Add tag if not already present."""
    tag = tag.strip().lower()
    if not tag:
        raise ValueError("Tag cannot be empty")
    if tag not in self.tags:
        self.tags.append(tag)
    return self
```

### 5. Update Database Schema (database.py)

Follow the [Database Instructions](.github/instructions/database.instructions.md):

```python
def create_schema(self):
    # Update CREATE TABLE statement
    # Existing columns...
    # tags TEXT DEFAULT '[]',  # JSON array of tags
    
def _row_to_task(self, row):
    # Existing mapping...
    tags = json.loads(row['tags']) if row['tags'] else []
    
    return Task(
        # Existing fields...
        tags=tags
    )

def save_task(self, task: Task) -> Task:
    # Update INSERT/UPDATE statements
    tags_json = json.dumps(task.tags)
    cursor.execute("""
        INSERT INTO tasks (..., tags) 
        VALUES (..., ?)
    """, (..., tags_json))
```

### 6. Add TaskManager Methods (main.py)

Follow the [CLI/TaskManager Instructions](.github/instructions/main.instructions.md):

```python
def add_tag_to_task(self, task_id: int, tag: str) -> Task:
    """Add a tag to a task."""
    task = self.get_task(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    
    task.add_tag(tag)
    return self.database.save_task(task)

def get_tasks_by_tag(self, tag: str) -> list:
    """Get all tasks with a specific tag."""
    all_tasks = self.database.get_all_tasks()
    return [t for t in all_tasks if tag.lower() in [x.lower() for x in t.tags]]

def remove_tag_from_task(self, task_id: int, tag: str) -> Task:
    """Remove a tag from a task."""
    task = self.get_task(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    
    task.remove_tag(tag)
    return self.database.save_task(task)
```

### 7. Add Flask Routes (app.py)

Follow the [Flask Instructions](.github/instructions/app.instructions.md):

```python
@app.route('/api/tasks/<int:task_id>/tags', methods=['POST'])
def add_task_tag(task_id):
    """Add a tag to a task."""
    try:
        data = request.get_json()
        tag = data.get('tag', '').strip()
        
        if not tag:
            return jsonify({
                "success": False,
                "message": "Tag cannot be empty"
            }), 400
        
        task = db.get_task(task_id)
        if not task:
            return jsonify({
                "success": False,
                "message": f"Task {task_id} not found"
            }), 404
        
        task.add_tag(tag)
        updated = db.save_task(task)
        
        return jsonify({
            "success": True,
            "data": asdict(updated),
            "message": f"Tag '{tag}' added to task"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks_filtered():
    """Get tasks with optional filtering by tag, priority, status."""
    try:
        tag_filter = request.args.get('tag')
        priority_filter = request.args.get('priority')
        status_filter = request.args.get('status')
        
        tasks = db.get_all_tasks()
        
        if tag_filter:
            tasks = [t for t in tasks if tag_filter.lower() in [x.lower() for x in t.tags]]
        if priority_filter:
            tasks = [t for t in tasks if t.priority == priority_filter]
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]
        
        return jsonify({
            "success": True,
            "data": [asdict(t) for t in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

### 8. Update CLI Menu (main.py)

```python
def interactive_menu(self):
    while True:
        print("\n===== TASK MANAGER =====")
        print("1. Create New Task")
        print("2. List All Tasks")
        # ... existing options ...
        print("T. Add tag to task")
        print("R. Remove tag from task")
        print("F. Filter tasks by tag")
        print("X. Exit")
        
        choice = input("\nEnter choice: ").strip().lower()
        
        if choice == 't':
            self._add_tag_interactive()
        elif choice == 'r':
            self._remove_tag_interactive()
        elif choice == 'f':
            self._filter_by_tag_interactive()
        # ... handle other choices ...

def _add_tag_interactive(self):
    """CLI for adding a tag to a task."""
    try:
        task_id = int(input("Enter task ID: "))
        tag = input("Enter tag: ").strip()
        
        task = self.add_tag_to_task(task_id, tag)
        print(f"✓ Tag added. Task tags: {', '.join(task.tags)}")
        
    except ValueError as e:
        print(f"✗ Error: {e}")
```

## Phase 3: Testing

### 9. Write Unit Tests

Create tests/test_tags.py:

```python
import pytest
from task_manager.task import Task
from task_manager.database import TaskDatabase
from task_manager.main import TaskManager

class TestTaskTags:
    """Test tag functionality."""
    
    def test_add_tag_to_task(self):
        """Should add tag to task."""
        task = Task(title="Test")
        task.add_tag("urgent")
        
        assert "urgent" in task.tags
    
    def test_prevent_duplicate_tags(self):
        """Should not add duplicate tags."""
        task = Task(title="Test")
        task.add_tag("urgent")
        task.add_tag("urgent")
        
        assert task.tags.count("urgent") == 1
    
    def test_remove_tag_from_task(self):
        """Should remove tag from task."""
        task = Task(title="Test")
        task.add_tag("urgent")
        task.remove_tag("urgent")
        
        assert "urgent" not in task.tags
    
    def test_save_and_retrieve_tags(self):
        """Should persist tags to database."""
        db = TaskDatabase(":memory:")
        task = Task(title="Test")
        task.add_tag("urgent")
        task.add_tag("work")
        
        saved = db.save_task(task)
        retrieved = db.get_task(saved.id)
        
        assert set(retrieved.tags) == {"urgent", "work"}
    
    def test_filter_by_tag(self):
        """Should filter tasks by tag."""
        manager = TaskManager()
        
        t1 = manager.create_task("Task 1")
        t2 = manager.create_task("Task 2")
        
        manager.add_tag_to_task(t1.id, "urgent")
        manager.add_tag_to_task(t2.id, "work")
        
        urgent_tasks = manager.get_tasks_by_tag("urgent")
        assert len(urgent_tasks) == 1
        assert urgent_tasks[0].id == t1.id

class TestTagsAPI:
    """Test tag API endpoints."""
    
    def test_add_tag_via_api(self, client):
        """Should add tag via POST endpoint."""
        # Create task first
        create_resp = client.post('/api/tasks', json={"title": "Test"})
        task_id = create_resp.json['data']['id']
        
        # Add tag
        response = client.post(f'/api/tasks/{task_id}/tags', json={
            "tag": "urgent"
        })
        
        assert response.status_code == 200
        assert "urgent" in response.json['data']['tags']
    
    def test_filter_by_tag_via_api(self, client):
        """Should filter tasks by tag via GET."""
        # Setup tasks with tags...
        
        response = client.get('/api/tasks?tag=urgent')
        
        assert response.status_code == 200
        # Verify only urgent-tagged tasks returned
```

### 10. Run Tests

```bash
# Run tag tests
pytest tests/test_tags.py -v

# Run all tests with coverage
pytest --cov=task_manager --cov-report=html

# Fix any failures
```

## Phase 4: Documentation & Review

### 11. Update Documentation

- [ ] Update README.md with feature description
- [ ] Add example usage to QUICK_REFERENCE.md
- [ ] Document API endpoints in README
- [ ] Update CLI help text

### 12. Code Review Checklist

Before considering feature complete:
- [ ] All tests pass
- [ ] Code coverage > 80%
- [ ] No SQL injection vulnerabilities
- [ ] Error messages are user-friendly
- [ ] Database schema changes documented
- [ ] API responses consistent with other endpoints
- [ ] CLI menu properly formatted
- [ ] No hardcoded values (use constants)
- [ ] Type hints on all functions
- [ ] Docstrings on all public methods

## Phase 5: Integration & Release

### 13. Integration Testing

Test the feature end-to-end:
- [ ] Create task via API → Add tag via API → Retrieve with tag filter
- [ ] Create task via CLI → Add tag via CLI → List filtered tasks
- [ ] Web UI shows tags correctly
- [ ] Tags persist across application restarts

### 14. Update Changelog

Add to CHANGELOG.md:
```
## [1.1.0] - 2026-03-12

### Added
- Task tags feature: users can now add multiple tags to tasks
- Filter tasks by tag via API and CLI
- Tag management endpoints (add, remove, list)
```

### 15. Create Release

Tag the release and note the new feature in release notes.

## Common Patterns for Features

### Adding a Boolean Flag
1. Add field to Task: `active: bool = True`
2. Update database schema: Add column to table
3. Add methods: `activate()`, `deactivate()`
4. Add filters: Sort/filter by status

### Adding a Many-to-One Relationship
1. Add foreign key to Task model
2. Create relationship tables in database
3. Add join queries in database layer
4. Add TaskManager methods for relationship operations

### Adding a Computed Property
1. Add @property method to Task
2. Calculate based on other fields
3. No database storage needed (unless needs indexing)
4. Include in to_dict() for API responses
