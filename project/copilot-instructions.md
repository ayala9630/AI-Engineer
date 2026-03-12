---
name: Task Manager Project Guidelines
description: Comprehensive guidelines for Task Manager development. Use when: writing code for the task manager project, implementing features, or refactoring existing code.
applyTo: "task_manager/**"
---

# Task Manager Project Coding Guidelines

## Core Principles

1. **Data Integrity**: Always validate input before persisting to database
2. **Error Handling**: Use explicit try-catch blocks with meaningful error messages
3. **Type Safety**: Use type hints on all functions and class methods
4. **Modularity**: Keep functions focused on single responsibilities
5. **Documentation**: Add docstrings to all public methods

## Code Style

- Follow PEP 8 guidelines
- Max line length: 100 characters
- Use meaningful variable names (no single letters except loop counters)
- Use type hints throughout

## Database Operations

- Always use parameterized queries to prevent SQL injection
- Wrap database calls in try-catch blocks
- Implement connection cleanup in finally blocks
- Log database errors with context

## Testing Requirements

Before committing task_manager code:
- Write unit tests for new methods
- Test edge cases (empty inputs, None values, invalid data)
- Aim for >80% code coverage
- Use pytest as the test framework

## Performance Considerations

- Use database indexes for frequently queried columns
- Batch database operations when possible
- Limit in-memory task lists to reasonable sizes
- Cache read-heavy operations when appropriate

## Design Patterns

- Use dataclasses for data models
- Implement factory patterns for object creation
- Use context managers for resource cleanup
- Apply dependency injection for testability

## Priority Levels

Task priorities follow this hierarchy:
- `critical`: Blocking issues, security concerns
- `high`: Core functionality, performance
- `medium`: Nice-to-have features, optimization
- `low`: Documentation, minor improvements

## Naming Conventions

- Classes: PascalCase (`TaskManager`, `TaskDatabase`)
- Functions/methods: snake_case (`load_all_tasks`, `create_schema`)
- Constants: UPPER_SNAKE_CASE (`DEFAULT_DB_PATH`)
- Private members: prefix with underscore (`_row_to_task`)
