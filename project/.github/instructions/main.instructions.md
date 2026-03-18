---
name: CLI and TaskManager Class Instructions
description: "Use when: working with TaskManager class, CLI functionality, or the main entry point"
applyTo: "task_manager/main.py"
---

# CLI and TaskManager Class Development Instructions

## TaskManager Class Purpose

The `TaskManager` class in `main.py` provides:
- High-level task operations (create, read, update, delete)
- Business logic layer above the database
- CLI interface for terminal-based usage
- Validation and error handling

## Class Structure

```python
class TaskManager:
    def __init__(self):
        self.database = TaskDatabase()
    
    # CRUD operations
    def create_task(self, title, description="", priority="medium")
    def list_tasks(self, filter_by_priority=None, filter_by_status=None)
    def get_task(self, task_id)
    def update_task(self, task_id, **kwargs)
    def delete_task(self, task_id)
    
    # Utility operations
    def mark_complete(self, task_id)
    def get_statistics(self)
    
    # CLI interface
    def interactive_menu()
    def process_command(command)
```

## TaskManager Methods

### Creating Tasks
```python
def create_task(self, title, description="", priority="medium"):
    """Create and save a new task."""
    # 1. Validate inputs (title not empty, priority valid)
    # 2. Create Task object
    # 3. Save to database via self.database.save_task()
    # 4. Return created task with ID
    # 5. Handle exceptions and return meaningful errors
```

### Listing Tasks
```python
def list_tasks(self, filter_by_priority=None, filter_by_status=None):
    """Get all tasks with optional filtering."""
    # 1. Retrieve all tasks from database
    # 2. Apply priority filter if provided
    # 3. Apply status filter if provided
    # 4. Return filtered list
    # 5. Handle empty results gracefully
```

### Updating Tasks
```python
def update_task(self, task_id, **kwargs):
    """Update specific fields of a task."""
    # 1. Get existing task
    # 2. Validate which fields are being updated
    # 3. Validate new values (e.g., priority format)
    # 4. Save updated task
    # 5. Return updated task
```

## CLI Interface Patterns

### Interactive Menu
The CLI should provide a menu-driven interface:

```
===== TASK MANAGER =====
1. Create New Task
2. List All Tasks
3. Mark Task as Complete
4. Delete Task
5. View Statistics
6. Exit

Enter choice (1-6): 
```

### Input Handling

```python
def interactive_menu():
    while True:
        display_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            create_task_interactive()
        elif choice == "2":
            list_tasks_interactive()
        # ... handle other choices
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
```

### Error Handling in CLI
- Catch exceptions from TaskManager methods
- Display friendly error messages to user
- Don't show raw database errors
- Guide user on valid inputs

## Adding New Operations

### Checklist for New Methods
1. Define the method signature with clear parameters
2. Add docstring explaining what it does
3. Validate input parameters
4. Call appropriate database methods
5. Handle exceptions appropriately
6. Return results in expected format
7. Add to CLI menu if user-facing
8. Add corresponding tests

### Example: New Method
```python
def duplicate_task(self, task_id, new_title=None):
    """Create a copy of an existing task."""
    # Get original task
    original = self.get_task(task_id)
    if not original:
        raise ValueError(f"Task {task_id} not found")
    
    # Create copy with new title
    new_title = new_title or f"Copy of {original.title}"
    
    # Create and return new task
    return self.create_task(
        title=new_title,
        description=original.description,
        priority=original.priority
    )
```

## Input Validation

### Required Validations
- **Task ID**: Must be positive integer, must exist in database
- **Title**: Must not be empty, max 255 characters
- **Description**: Optional, max 2000 characters
- **Priority**: Must be one of: low, medium, high, critical
- **Status**: Must be one of: pending, in_progress, completed

### Validation Pattern
```python
def _validate_priority(self, priority):
    """Validate priority value."""
    valid_priorities = ("low", "medium", "high", "critical")
    if priority not in valid_priorities:
        raise ValueError(f"Priority must be one of {valid_priorities}")
    return priority

def _validate_title(self, title):
    """Validate task title."""
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")
    if len(title) > 255:
        raise ValueError("Title must be max 255 characters")
    return title.strip()
```

## Statistics and Reporting

The `get_statistics()` method should return:
```python
{
    "total_tasks": 10,
    "completed_tasks": 3,
    "pending_tasks": 5,
    "in_progress_tasks": 2,
    "by_priority": {
        "critical": 1,
        "high": 3,
        "medium": 4,
        "low": 2
    },
    "by_status": {
        "pending": 5,
        "in_progress": 2,
        "completed": 3
    }
}
```

## Database Interaction

- Always use the `self.database` instance
- Let database raise exceptions; don't catch and swallow them
- Call appropriate database methods (don't duplicate database logic)
- Maintain consistency with database operations

## Testing TaskManager

- Test each method with valid, invalid, and edge-case inputs
- Mock the database for unit tests
- Test error handling and exception messages
- Test CLI input parsing
- Test filter combinations
- Verify statistics calculations
