---
name: Task Model Instructions
description: "Use when: creating, modifying, or extending the Task data model in task.py"
applyTo: "task_manager/task.py"
---

# Task Model Development Instructions

## Task Class Structure

When modifying the Task class, follow this structure:

```python
@dataclass
class Task:
    # Required fields at top
    title: str
    
    # Optional fields with defaults
    description: str = ""
    priority: str = "medium"
    
    # Field validation in __post_init__
    
    # Serialization methods (to_dict, from_dict)
    
    # State modification methods (mark_complete, etc.)
    
    # Tag management methods
```

## Adding New Task Fields

When adding new fields to Task:

1. Add the field to the dataclass with appropriate type hint
2. Add default value if optional
3. Add validation in `__post_init__` if needed
4. Update database schema in `database.py`
5. Update `_row_to_task` mapping
6. Add getter/setter methods if needed
7. Write tests for new functionality

## Task Priority Validation

Always validate priority against allowed values:
```python
valid_priorities = ("low", "medium", "high", "critical")
```

## Status vs Completed Fields

Maintain consistency between:
- `status`: Overall status (pending, in_progress, completed)
- `completed`: Boolean flag (deprecated in favor of status)

These should be kept in sync for backward compatibility.

## Tag Management

- Tags are stored as a JSON array in database
- Always check for duplicates before adding
- Maintain tag order for consistency

## Serialization

All public methods for converting Task to/from dict must:
- Use `asdict()` from dataclasses module
- Handle all field types correctly (custom types, optional fields)
- Include error handling for invalid serialization
