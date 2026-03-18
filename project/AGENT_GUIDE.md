# Comprehensive Project Guide for Agents

Welcome! This guide helps AI agents understand and work with the Task Manager project effectively.

## Quick Navigation

- **Getting Started**: See [Project Setup Guide](#project-setup)
- **Understanding the Code**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Adding Features**: See [FEATURE_GUIDE.md](FEATURE_GUIDE.md)
- **Common Tasks**: See [WORKFLOWS.md](WORKFLOWS.md)
- **Writing Tests**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Coding Guidelines**: See [copilot-instructions.md](copilot-instructions.md)
- **File-Specific Rules**: See `.github/instructions/` folder

---

## Project Setup

### What This Project Is
A Python task management system with three interfaces:
- **CLI** (Command-line): `python task_manager/main.py`
- **Web UI** (Browser): `python task_manager/app.py` → http://localhost:5000
- **REST API** (Programmatic): JSON endpoints via Flask

### Key Technologies
- **Python 3.8+** - Main language
- **Flask** - Web framework
- **SQLite** - Database
- **Jinja2** - HTML templating
- **Pytest** - Testing framework

### Project Structure
```
project/
├── task_manager/              # Main application code
│   ├── task.py              # Task data model
│   ├── database.py          # Database layer
│   ├── main.py              # CLI and TaskManager class
│   ├── app.py               # Flask web server
│   ├── templates/           # HTML templates
│   ├── static/              # CSS and JavaScript
│   └── __init__.py          # Package initialization
├── tests/                     # Test files (create as needed)
├── .github/
│   ├── instructions/        # File-specific coding rules
│   ├── prompts/             # Task templates for agents
│   ├── agents/              # Custom agent definitions
│   └── skills/              # Reusable workflows
├── .venv/                    # Virtual environment (do not edit)
├── tasks.db                  # SQLite database (generated)
├── requirements.txt          # Dependencies
├── README.md                 # User-facing overview
└── [Multiple guides]         # This and related markdown files
```

### First Time Setup
```bash
# 1. Activate virtual environment
.\.venv\Scripts\activate

# 2. Install/verify dependencies
pip install -r requirements.txt

# 3. Test CLI works
python task_manager/main.py

# 4. Test web app works
# In one terminal:
python task_manager/app.py
# Then open: http://localhost:5000
```

---

## Understanding the Project

### Core Concept
Tasks have:
- **Title** (required, unique) - What needs to be done
- **Description** (optional) - More details
- **Priority** (low/medium/high/critical) - How urgent
- **Status** (pending/in_progress/completed) - Current state
- **Created/Updated timestamps** - When was action taken
- **Tags** (optional) - Categories or labels

### Three-Layer Architecture

```
┌─ Web Layer (app.py) ─────────────────────┐
│ Flask routes, REST API, HTML rendering   │ ← HTTP requests from browsers/API clients
├─ Business Logic Layer (main.py) ────────┤
│ TaskManager class, CLI, validation       │ ← Application logic
├─ Data Layer (task.py, database.py) ────┤
│ Task model, SQLite operations            │ ← Persistent storage
└──────────────────────────────────────────┘
```

**Why this structure?**
- Separation of concerns
- Each layer can be tested independently
- Easy to add new interfaces (e.g., REST API, desktop app)
- Clear dependencies make code predictable

### Data Flow

**Creating a task via Web UI:**
1. User fills form, clicks "Create"
2. JavaScript (app.js) sends: `POST /api/tasks` with JSON
3. Flask (app.py) receives request
4. Flask validates using Task dataclass (task.py)
5. Flask calls TaskDatabase (database.py) 
6. Tasks saved to SQLite (tasks.db)
7. New task returned as JSON to frontend
8. JavaScript updates the page

**Creating a task via CLI:**
1. User runs `python task_manager/main.py`
2. CLI displays menu
3. User selects "Create Task"
4. CLI prompts for fields
5. TaskManager (main.py) validates input
6. TaskManager calls TaskDatabase (database.py)
7. Task saved to SQLite (tasks.db)
8. CLI displays confirmation

---

## How Agents Should Work With This Project

### Agent Guidelines

1. **Read Instructions First**
   - Check [copilot-instructions.md](copilot-instructions.md) for project-wide rules
   - Check `.github/instructions/*.md` for file-specific rules before editing a file
   - Refer to [ARCHITECTURE.md](ARCHITECTURE.md) to understand dependencies

2. **Understand Before Coding**
   - Don't modify files without understanding their current state
   - Read related files to understand dependencies
   - Look at existing tests to understand expected behavior

3. **Follow Patterns**
   - Use existing code as templates
   - Follow naming conventions (snake_case for functions, PascalCase for classes)
   - Match code style to existing code in the file
   - Type hint all function parameters and returns

4. **Test Everything**
   - Write tests before or alongside code changes
   - Run `pytest --cov=task_manager` to verify coverage
   - Test both happy paths and error cases
   - Test edge cases (empty input, None values, etc.)

5. **Document Changes**
   - Add docstrings to new functions/methods
   - Update comments if logic changed
   - Update CHANGELOG.md for user-facing changes
   - Update relevant instruction files if patterns changed

6. **Verify Integrity**
   - Ensure no SQL injection vulnerabilities
   - Validate all user input
   - Handle errors explicitly
   - Don't leave databactions open

### Common Agent Tasks

**Task: Fix a bug**
→ See [WORKFLOWS.md: Fixing a Bug](WORKFLOWS.md#workflow-fixing-a-bug)

**Task: Add a new feature**
→ See [FEATURE_GUIDE.md](FEATURE_GUIDE.md)

**Task: Write tests**
→ See [TESTING_GUIDE.md](TESTING_GUIDE.md)

**Task: Modify TaskDatabase**
→ Read [.github/instructions/database.instructions.md](.github/instructions/database.instructions.md) first

**Task: Modify Task model**
→ Read [.github/instructions/task.instructions.md](.github/instructions/task.instructions.md) first

**Task: Modify Flask routes**
→ Read [.github/instructions/app.instructions.md](.github/instructions/app.instructions.md) first

**Task: Modify CLI/TaskManager**
→ Read [.github/instructions/main.instructions.md](.github/instructions/main.instructions.md) first

---

## Important Patterns & Conventions

### Database Operations

**Pattern: Parameterized Queries (ALWAYS)**
```python
# ✓ CORRECT - Safe from SQL injection
cursor.execute("SELECT * FROM tasks WHERE id = ? ", (task_id,))

# ✗ WRONG - SQL injection vulnerability
cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
```

**Pattern: Connection Cleanup**
```python
# ✓ CORRECT - Database connection properly closed
try:
    # database operation
finally:
    if self.connection:
        self.connection.close()

# ✗ WRONG - Connection left open if exception occurs
self.connection.execute(query)
self.connection.close()  # Won't run if exception above
```

### Task Validation

**Always validate at multiple levels:**
1. Task dataclass (type checking, constraints)
2. TaskManager methods (business logic)
3. Flask routes (HTTP request level)

```python
# Level 1: Task dataclass
task = Task(title="", priority="invalid")  # Raises ValueError

# Level 2: TaskManager method
def create_task(self, title, priority):
    if not title.strip():
        raise ValueError("Title required")
    if priority not in {"low", "medium", "high", "critical"}:
        raise ValueError(f"Invalid priority: {priority}")
    
    return self.database.save_task(Task(title=title, priority=priority))

# Level 3: Flask route
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data.get('title'):
        return jsonify({"error": "title required"}), 400
    try:
        task = manager.create_task(data['title'], data.get('priority', 'medium'))
        return jsonify(asdict(task)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
```

### Priority and Status Constants

**Valid Priorities:**
- `"low"` - Can wait
- `"medium"` - Normal (default)
- `"high"` - Should do soon
- `"critical"` - Must do now

**Valid Statuses:**
- `"pending"` - Not started (default)
- `"in_progress"` - Currently working
- `"completed"` - All done

### Type Hints

Always use type hints:
```python
# ✓ CORRECT - Type hints on everything
def get_task(self, task_id: int) -> Optional[Task]:
    """Get a single task by ID."""
    pass

def list_tasks(
    self,
    filter_by_priority: Optional[str] = None
) -> List[Task]:
    """Get all tasks, optionally filtered."""
    pass

# ✗ WRONG - No type hints
def get_task(self, task_id):
    pass
```

### Error Handling

Specific exceptions, not generic:
```python
# ✓ CORRECT - Specific error types
if not title:
    raise ValueError("Title cannot be empty")
if task_id not in self.tasks:
    raise KeyError(f"Task {task_id} not found")

# ✗ WRONG - Generic Exception
if not title:
    raise Exception("Error")
```

### API Response Format

All API endpoints return consistent format:
```json
{
    "success": true,
    "data": { "id": 1, "title": "Task", ... },
    "message": "Task created successfully"
}
```

Or on error:
```json
{
    "success": false,
    "message": "Could not create task",
    "error": "Title required"
}
```

---

## File Reference Quick Guide

| File | Purpose | Instructions |
|------|---------|--------------|
| task.py | Task data model & validation | [task.instructions.md](.github/instructions/task.instructions.md) |
| database.py | SQLite database operations | [database.instructions.md](.github/instructions/database.instructions.md) |
| main.py | CLI interface & TaskManager | [main.instructions.md](.github/instructions/main.instructions.md) |
| app.py | Flask web server & REST API | [app.instructions.md](.github/instructions/app.instructions.md) |
| templates/ | HTML pages | HTML templates using Jinja2 |
| static/ | CSS and JavaScript | Frontend styling and interaction |

---

## Debugging Tips

### Test Fails - How to Debug

```bash
# 1. Run with verbose output
pytest tests/test_file.py::test_name -vv

# 2. Show print statements
pytest tests/test_file.py::test_name -s

# 3. Drop into debugger
pytest tests/test_file.py::test_name --pdb
```

### Application Misbehaves - How to Debug

1. Check the error message carefully
2. Look at which layer the error is in (web, business, data)
3. Add print statements to track execution
4. Check database state: `sqlite3 tasks.db "SELECT * FROM tasks;"`
5. Review [WORKFLOWS.md](WORKFLOWS.md#workflow-debugging-a-test-failure)

### Database is Corrupted

```bash
# Backup and recreate
cp tasks.db tasks.db.bak
rm tasks.db
python task_manager/main.py  # Will recreate fresh database
```

---

## Making Changes Safely

### Before Any Change
1. Understand the current code
2. Understand the dependencies
3. Write tests that verify current behavior
4. Run tests to confirm they pass

### Making the Change
1. Make minimal, focused changes
2. Follow existing patterns
3. Test frequently during implementation
4. Run tests continuously

### Verifying the Change
1. Run suite: `pytest --cov=task_manager`
2. Manually test through CLI/web UI
3. Check for SQL injection vulnerabilities
4. Review error handling
5. Verify docstrings and comments

---

## Getting Help Within the Project

1. **Understanding a component?** → Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Adding a feature?** → Follow [FEATURE_GUIDE.md](FEATURE_GUIDE.md)
3. **Writing tests?** → See [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. **Doing a common task?** → Check [WORKFLOWS.md](WORKFLOWS.md)
5. **Editing specific file?** → Check `.github/instructions/` for that file
6. **Following project style?** → See [copilot-instructions.md](copilot-instructions.md)

---

## Summary

**Key Principles:**
- Layered architecture (Web → Business → Data)
- Strict validation at all levels
- Parameterized queries always
- Type hints everywhere
- Tests for all functionality
- Specific error handling
- Clear dependencies
- Consistent patterns

**Agent Golden Rule:**
*Read the instructions for the file you're editing before you edit it.*

**Development Golden Rule:**
*Test before committing. The more tests, the safer changes are.*

Good luck, agent! The project is well-structured and ready for development. Follow the guides, respect the patterns, and you'll do great work. 🚀
