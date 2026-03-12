# Task Manager Development Skill - Assets

## Templates

### New Feature Template

```python
# Feature: [Description]
# Database: [Yes/No]
# Impact: [Components affected]

class New Feature:
    """Implementation of [feature]."""
    
    def __init__(self):
        pass
    
    def method(self):
        """Method description."""
        pass
```

### Test Template

```python
import pytest
from task_manager import [Module]

class Test[Feature]:
    """Tests for [feature]."""
    
    @pytest.fixture
    def setup(self):
        pass
    
    def test_happy_path(self, setup):
        pass
    
    def test_edge_case(self, setup):
        pass
```

### Migration Template

```python
# Migration: [Description]

def migrate_database(self):
    """Migrate database to support [feature]."""
    cursor = self.connection.cursor()
    try:
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN new_column TYPE DEFAULT value
        """)
        ction.commit()
    except sqlite3.Error as e:
        print(f"Migration failed: {e}")
```

## Checklists

### Before Starting Feature Development

- [ ] Requirements documented and reviewed
- [ ] Affected files identified
- [ ] Database schema planned (if applicable)
- [ ] API/function signatures defined
- [ ] Test strategy outlined

### During Implementation

- [ ] Code follows project style guide
- [ ] All functions have type hints
- [ ] Error handling implemented
- [ ] Comments explain complex logic
- [ ] Docstrings updated

### Before Commit

- [ ] All tests passing
- [ ] Coverage >80%
- [ ] Code review requested
- [ ] Documentation updated
- [ ] No debug statements left

## Code Examples

### Adding a New Task Field

```python
# Step 1: Update model
@dataclass
class Task:
    due_date: Optional[str] = None
    
    def __post_init__(self):
        if self.due_date:
            self._validate_date(self.due_date)

# Step 2: Update database
cursor.execute("""
    ALTER TABLE tasks 
    ADD COLUMN due_date TEXT
""")

# Step 3: Update mapping
row['due_date'] = row['due_date'] or None

# Step 4: Write tests
def test_task_with_due_date():
    task = Task(title="Test", due_date="2026-03-20")
    assert task.due_date == "2026-03-20"
```

## Troubleshooting

### Database Not Updating

1. Check schema creation is idempotent
2. Verify ALTER TABLE syntax for SQLite
3. Ensure connection.commit() is called
4. Use in-memory DB for testing (:memory:)

### Test Coverage Low

1. Use pytest --cov to identify gaps
2. Add tests for error cases
3. Test boundary conditions
4. Mock external dependencies

### Type Hints Issues

1. Import Optional from typing if needed
2. Use Union for multiple types
3. Import types before dataclass
4. Validate in __post_init__

## Performance Tips

- Use database indexes for filtered queries
- Cache rarely-changing data
- Batch database operations
- Profile code with different dataset sizes
