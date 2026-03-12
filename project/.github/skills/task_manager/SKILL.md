---
name: "TaskManagerDevelopment"
description: "Multi-step development workflow for adding new features to Task Manager with proper structure, testing, and documentation"
---

# Task Manager Development Skill

## Overview

This skill provides a complete workflow for adding new features to the Task Manager system. It ensures:
- Code quality through testing
- Documentation consistency
- Database schema integrity
- Performance considerations

## Workflow Stages

### Stage 1: Feature Design

1. Define feature requirements
2. Identify affected components
3. Plan database changes (if needed)
4. Design new classes/functions

### Stage 2: Model Updates (task.py)

If adding new fields to Task:
- Add dataclass field with type hints
- Implement validation in `__post_init__`
- Add getter/setter methods if needed
- Document new fields

### Stage 3: Database Schema (database.py)

If storing new data:
- Update create_schema() with table changes
- Implement data migration for existing databases
- Update _row_to_task() mapping
- Update save_task() INSERT/UPDATE

### Stage 4: Core Implementation

- Update TaskManager class
- Implement new methods
- Add error handling
- Write inline documentation

### Stage 5: Testing

Write comprehensive tests for:
- Happy path scenarios
- Edge cases and boundary conditions
- Error handling
- Database operations

Files affected:
- tests/test_task_manager.py
- tests/test_database.py
- tests/fixtures/

### Stage 6: Documentation

Update:
- Docstrings for new methods
- README.md with feature overview
- API documentation if applicable
- Add usage examples

### Stage 7: Code Review

- Check code style (PEP 8)
- Verify test coverage (>80%)
- Ensure database constraints
- Validate documentation

## Feature Template

Use this structure for new features:

```python
# 1. Data model (task.py)
@dataclass
class Task:
    new_field: type = default_value

# 2. Database (database.py)
def save_task(self, task: Task):
    # Include new_field in INSERT/UPDATE

# 3. Manager (main.py)
def new_feature_method(self, parameters):
    """Feature description."""
    pass

# 4. Tests (tests/test_*.py)
def test_new_feature():
    pass

# 5. Docs
# Update README, docstrings
```

## Quick Feature Checklist

- [ ] Feature requirements documented
- [ ] Data model updated (if needed)
- [ ] Database schema changed (if needed)
- [ ] Implementation complete
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] Code review passed

## Supported Operations

This skill can guide you through:
- Adding new task fields
- Creating new query/filter methods
- Implementing bulk operations
- Adding task validation rules
- Integrating external systems
- Performance optimizations

## Example: Adding Task Color Field

**Stage 1**: Define that tasks should have colors for UI
**Stage 2**: Add `color: str = "default"` to Task dataclass
**Stage 3**: Update database to store color
**Stage 4**: Add color validation method
**Stage 5**: Write tests for color feature
**Stage 6**: Update docs with example usage
**Stage 7**: Review and merge

## Related Resources

- See `.github/instructions/task.instructions.md`
- See `.github/instructions/database.instructions.md`
- See `.github/agents/testing.agent.md` for test writing
- See `.github/agents/refactoring.agent.md` for code improvements
