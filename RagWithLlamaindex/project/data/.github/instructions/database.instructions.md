---
name: Database Development Instructions
description: "Use when: implementing database operations, adding new queries, or modifying the database schema"
applyTo: "task_manager/database.py"
---

# Database Development Instructions

## Database Design Principles

1. **Schema First**: Define schema clearly before writing code
2. **Constraints**: Use database constraints (CHECK, FOREIGN KEY, UNIQUE)
3. **Normalization**: Keep data properly normalized
4. **Error Handling**: Catch and log all database errors

## Connection Management

### Proper Connection Lifecycle

```python
def __init__(self):
    self.connection = None
    self.connect()

def connect(self):
    self.connection = sqlite3.connect(self.db_path)
    self.connection.row_factory = sqlite3.Row

def close(self):
    if self.connection:
        self.connection.close()
```

Always explicitlyctions in finally blocks.

## Query Guidelines

### Parameterized Queries

ALWAYS use parameterized queries (? placeholders):
```python
cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
```

Never use string formatting/f-strings for SQL:
```python
# WRONG - SQL injection vulnerability
cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
```

### Row Mapping

Use the `_row_to_task()` helper to convert database rows to Task objects. This centralizes the mapping logic.

## Schema Operations

### Creating Tables

- Use `CREATE TABLE IF NOT EXISTS` to allow idempotent initialization
- Define all constraints explicitly
- Include meaningful column comments (via migrations if using a framework)

### Adding New Columns

When adding new fields to tasks table:

1. Write migration code in `create_schema()` using `ALTER TABLE`
2. Use `IF NOT EXISTS` clause if adding optional columns
3. Update `_row_to_task()` to map new fields
4. Update `save_task()` INSERT/UPDATE statement
5. Document the schema change

## Performance Considerations

- Create indexes on frequently queried columns (id, status, priority)
- Use transactions for batch operations
- Commit frequently but not excessively
- Use VACUUM periodically on large databases

## Testing Database Code

- Use in-memory SQLite (`:memory:`) for unit tests
- Test transaction rollback behavior
- Test constraint violations
- Verify data integrity after operations
