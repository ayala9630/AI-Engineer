---
name: "quick-add-task"
description: "Quickly create a new task in the Task Manager system"
parameters:
  - name: title
    type: string
    description: "The task title"
    required: true
  - name: priority
    type: string
    description: "Priority level: low, medium, high, or critical"
    required: false
    default: "medium"
  - name: description
    type: string
    description: "Optional task description"
    required: false
---

# Quick Add Task

This prompt helps you add a task to the Task Manager system with all required fields filled in properly.

Create the following code to add a new task:

```python
from task_manager import TaskManager

manager = TaskManager()
task = manager.add_task(
    title="{{ title }}",
    description="{{ description }}",
    priority="{{ priority }}"
)

print(f"Task created: {task.id}")
print(f"Title: {task.title}")
print(f"Priority: {task.priority}")
```

Then run: `python task_manager/main.py`

## Generated Code

The above will:
1. Initialize the TaskManager
2. Create a new task with the provided parameters
3. Save to database
4. Return the created Task object

## Tips

- Use `priority` values: low, medium, high, critical
- Description can be empty if not needed
- Task ID is auto-generated (UUID)
- Task is automatically saved to database
