---
name: "query-tasks"
description: "Query and filter tasks by various criteria with proper error handling"
parameters:
  - name: filter_type
    type: string
    description: "Filter by: priority, status, or date_range"
    required: true
  - name: filter_value
    type: string
    description: "The value to filter by"
    required: true
---

# Query Tasks Prompt

This prompt generates code to query tasks with various filters and proper error handling.

## Generated Query Code

```python
from task_manager import TaskManager

manager = TaskManager()

# Filter by {{ filter_type }}: {{ filter_value }}
try:
    if "{{ filter_type }}" == "priority":
        results = manager.list_tasks(filter_by="{{ filter_value }}")
        print(f"Found {len(results)} tasks with priority: {{ filter_value }}")
    
    elif "{{ filter_type }}" == "status":
        results = [t for t in manager.list_tasks() if t.status == "{{ filter_value }}"]
        print(f"Found {len(results)} tasks with status: {{ filter_value }}")
    
    elif "{{ filter_type }}" == "completed":
        results = [t for t in manager.list_tasks() if t.completed == {{ filter_value | lower }}]
        print(f"Found {len(results)} tasks (completed={{ filter_value | lower }})")
    
    for task in results:
        print(f"- {task.title} [Priority: {task.priority}] [Status: {task.status}]")

except Exception as e:
    print(f"Error querying tasks: {e}")
finally:
    manager.db.close()
```

## Usage Examples

- Filter by priority: "priority" / "high"
- Filter by status: "status" / "completed"
- Filter by completion: "completed" / "true"
