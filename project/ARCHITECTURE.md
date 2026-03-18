# Architecture and File Dependencies

## Project Overview

The Task Manager is a multi-interface task management system supporting CLI, Web UI, and REST API consumption. It follows a layered architecture:

```
┌─────────────────────────────────────┐
│    Presentation Layer               │
│  (Flask Web + API Routes)           │
│        app.py                       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Business Logic Layer             │
│  (TaskManager Class)                │
│        main.py                      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Data Model Layer                 │
│  (Task, TaskDatabase)               │
│  task.py + database.py              │
└─────────────────────────────────────┘
```

## File Dependency Map

```
app.py (Flask Web Application)
  │
  ├─→ imports → TaskDatabase (database.py)
  ├─→ imports → Task (task.py)
  ├─→ renders → templates/index.html
  ├─→ renders → templates/tasks_list.html
  └─→ serves ← static/style.css
  └─→ serves ← static/app.js

main.py (CLI & TaskManager)
  │
  ├─→ imports → TaskDatabase (database.py)
  ├─→ imports → Task (task.py)
  └─→ uses → TaskManager class (defined in main.py)

database.py (Data Persistence)
  │
  ├─→ imports → Task (task.py)
  ├─→ uses → sqlite3 (standard library)
  └─→ creates/uses ← tasks.db (SQLite database file)

task.py (Data Model)
  │
  ├─→ imports → dataclass (standard library)
  └─→ defines → Task class

static/app.js (Frontend JavaScript)
  │
  ├─→ calls ← /api/tasks (GET)
  ├─→ calls ← /api/tasks (POST)
  ├─→ calls ← /api/tasks/<id> (PUT)
  ├─→ calls ← /api/tasks/<id> (DELETE)
  └─→ updates → DOM in index.html/tasks_list.html

static/style.css (Frontend Styling)
  │
  └─→ used by ← templates/index.html
  └─→ used by ← templates/tasks_list.html
```

## Component Details

### task.py (Data Model Layer)
**Purpose**: Define the Task data structure and validation

**Responsibility**:
- Task dataclass definition with type hints
- Field validation in `__post_init__`
- Serialization methods (`to_dict()`, `from_dict()`)
- Task state methods (`mark_complete()`, `mark_pending()`)
- Tag management methods (`add_tag()`, `remove_tag()`)

**No dependencies** on other project modules (only standard library)

**Used by**:
- `database.py` - Creates and validates Task objects
- `main.py` - Passes tasks through TaskManager
- `app.py` - Returns tasks in API responses

**Instructions**: [task.instructions.md](.github/instructions/task.instructions.md)

---

### database.py (Data Persistence Layer)
**Purpose**: Handle all database operations (CRUD, queries)

**Responsibility**:
- SQLite databaction management
- Database schema initialization
- Row-to-Task object mapping (`_row_to_task()`)
- CRUD operations (Create, Read, Update, Delete)
- Filtering and querying
- Transaction management

**Dependencies**:
- `task.py` - For Task dataclass
- `sqlite3` - Standard library database driver

**Used by**:
- `main.py` - TaskManager uses database for persistence
- `app.py` - Flask routes use database for REST operations

**Key Methods**:
- `__init__(db_path)` - Initialize databasction
- `connect()` / `close()` -ction lifecycle
- `create_schema()` - Initialize tables
- `save_task(task)` - Create or update
- `get_task(id)` - Retrieve specific task
- `get_all_tasks()` - Retrieve all tasks
- `delete_task(id)` - Remove a task
- `get_tasks_by_priority(priority)` - Filter by priority
- `get_statistics()` - Get aggregated stats

**Instructions**: [database.instructions.md](.github/instructions/database.instructions.md)

---

### main.py (Business Logic Layer)
**Purpose**: Provide high-level task operations and CLI interface

**Responsibility**:
- TaskManager class providing business-level API
- Input validation and business logic
- CLI menu and interactive interface
- Command processing and execution
- Integration of database operations

**Dependencies**:
- `task.py` - Task data model
- `database.py` - Database operations

**Used by**:
- `app.py` - Can use TaskManager for operations
- Direct execution as CLI: `python -m task_manager.main`

**Key Classes/Functions**:
- `TaskManager` class - Main API
  - `create_task(title, description, priority)` - Create new task
  - `list_tasks(filter_by_priority, filter_by_status)` - Get filtered tasks
  - `get_task(task_id)` - Get single task
  - `update_task(task_id, **kwargs)` - Update task fields
  - `delete_task(task_id)` - Remove task
  - `mark_complete(task_id)` - Mark as complete
  - `get_statistics()` - Get task statistics
- CLI functions
  - `interactive_menu()` - Main CLI loop
  - `process_command(command)` - Execute single command

**Instructions**: [main.instructions.md](.github/instructions/main.instructions.md)

---

### app.py (Presentation/Web Layer)
**Purpose**: Serve web UI and REST API endpoints

**Responsibility**:
- Flask application initialization
- HTML route handlers for web interface
- REST API route handlers
- Request validation and response formatting
- Template rendering
- Static file serving
- Error handling and HTTP status codes

**Dependencies**:
- `flask` - Web framework
- `task.py` - Task dataclass
- `database.py` - Database operations (can use via TaskManager or directly)
- `templates/` - Jinja2 HTML templates
- `static/` - CSS and JavaScript assets

**Used by**:
- Web browsers accessing `http://localhost:5000`
- Frontend JavaScript making API calls

**Route Groups**:

*HTML Routes*:
- `GET /` - Dashboard
- `GET /tasks` - Full task list

*API Routes*:
- `GET /api/tasks` - List all tasks (with optional filtering)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/<id>` - Get specific task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task
- `POST /api/tasks/<id>/complete` - Mark as complete

**Instructions**: [app.instructions.md](.github/instructions/app.instructions.md)

---

### templates/ (HTML Templates)
**Purpose**: Render HTML pages for web interface

**Files**:
- `index.html` - Dashboard/home page
  - Shows task overview and statistics
  - Links to create/manage tasks
  - Includes JavaScript for interactivity

- `tasks_list.html` - Full task listing page
  - Displays all tasks in table/list format
  - Filter controls
  - Individual task actions (edit, delete, complete)

**Dependencies**:
- `Jinja2` template syntax
- `static/style.css` - For styling
- `static/app.js` - For dynamic behavior
- API endpoints from `app.py`

---

### static/ (Frontend Assets)
**Purpose**: Client-side styling and interactivity

**Files**:

`style.css`:
- Visual styling for all pages
- Responsive layout design
- Color scheme and typography
- Component styling (buttons, forms, tables)

`app.js`:
- Dynamic form handling
- API interaction (fetch calls)
- DOM manipulation and updates
- User feedback (messages, alerts)
- Filter application
- Task actions (create, update, delete)

**API Calls Made**:
- `GET /api/tasks` - Load task list
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update existing task
- `DELETE /api/tasks/<id>` - Delete task
- `POST /api/tasks/<id>/complete` - Mark complete

---

## Data Flow Examples

### Creating a Task (Web UI)
1. User fills form in web browser
2. `app.js` validates form data
3. `app.js` calls `POST /api/tasks` (app.py)
4. `app.py` validates request JSON
5. `app.py` creates Task object (task.py)
6. `app.py` calls `database.save_task(task)` (database.py)
7. `database.py` executes INSERT SQL and generates ID
8. Task returned as JSON to app.js
9. `app.js` updates DOM and shows success message

### Creating a Task (CLI)
1. User runs `python task_manager/main.py`
2. `main.py` shows menu and waits for input
3. User selects "Create Task"
4. `main.py` prompts for title, description, priority
5. `main.py` calls `TaskManager.create_task()` (main.py)
6. `TaskManager` validates input and creates Task object
7. `TaskManager` calls `database.save_task()` (database.py)
8. `database.py` executes INSERT SQL and generates ID
9. `main.py` displays confirmation with task details

### Filtering Tasks
1. User applies filter in web UI or CLI
2. Filter parameters passed to `TaskManager.list_tasks()` or API
3. `TaskManager.list_tasks(priority='high')` calls `database.get_all_tasks()`
4. `database.get_all_tasks()` executes SQL query
5. Results mapped to Task objects via `_row_to_task()`
6. TaskManager filters in-memory list
7. Results returned to caller

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    tags TEXT DEFAULT '[]',           -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_status ON tasks(status);
```

## Important Design Patterns

### Pattern: Row Mapping
Database returns raw SQL rows, converted to Task objects:
```python
def _row_to_task(self, row):
    """Convert database row to Task object."""
    return Task(
        id=row['id'],
        title=row['title'],
        priority=row['priority'],
        # ... map all fields
    )
```

### Pattern: Validation Layers
Input validated at multiple layers:
1. **Task dataclass** - Type checking, field constraints
2. **TaskManager** - Business logic validation
3. **API endpoints** - HTTP request validation
4. **Database** - SQL constraints

### Pattern: Error Handling
Errors propagate with context:
```python
try:
    task = Task(title="")  # ValueError
except ValueError as e:
    print(f"Invalid task: {e}")
```

## Configuration & Constants

**Database**:
- Default path: `tasks.db` (in project root)
- Type: SQLite 3
- Auto-initialization on first run

**Flask**:
- Debug mode: Disabled in production
- Host: localhost (127.0.0.1)
- Port: 5000
- Template folder: `task_manager/templates/`
- Static folder: `task_manager/static/`

**Task Constraints**:
- Min title length: 1 character
- Max title length: 255 characters
- Valid priorities: low, medium, high, critical
- Valid statuses: pending, in_progress, completed

## Key Files to Modify for Common Tasks

| Task | Files to Modify |
|------|-----------------|
| Add new Task field | task.py → database.py → app.py/main.py (if UI needed) |
| Add new database query | database.py → main.py/app.py |
| Add new API endpoint | app.py → app.js (if web UI) |
| Add new CLI command | main.py |
| Change task validation | task.py → app.py/main.py (validation calls) |
| Change database schema | database.py → task.py (_row_to_task) → all layers |
| Fix bug in task display | Likely app.js → app.py → database.py depending on where bug occurs |

## Testing Strategy

| Component | Test Type | Test File |
|-----------|-----------|-----------|
| Task model | Unit tests | tests/test_task.py |
| Database | Unit tests + integration | tests/test_database.py |
| TaskManager | Unit tests + mocked DB | tests/test_main.py |
| Flask app | Integration tests | tests/test_app.py |
| Full system | E2E tests | tests/test_integration.py |
