---
name: Flask Web Application Instructions
description: "Use when: building Flask routes, modifying the web interface, adding API endpoints, or working with request/response handling"
applyTo: "task_manager/app.py"
---

# Flask Web Application Development Instructions

## Application Architecture

The Flask app (`task_manager/app.py`) serves as the web interface and REST API for the Task Manager. It uses:
- **Flask** for the web framework
- **Jinja2** for HTML templating
- **JSON** for API responses
- **SQLite** (via `TaskDatabase`) for persistence

## Route Structure

### HTML Routes (Rendered Pages)
- `GET /` - Dashboard with task overview and statistics
- `GET /tasks` - Full task list view
- `GET /tasks/create` - Create new task form (future)

### API Routes (JSON Responses)
- `GET /api/tasks` - List all tasks with optional filtering
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task
- `POST /api/tasks/<id>/complete` - Mark task as complete

## Request/Response Patterns

### API Response Format
All API endpoints return JSON in this format:
```python
{
    "success": True/False,
    "data": {...},  # Task object(s) or null
    "message": "Human-readable message",
    "error": "Error details if any"
}
```

### Task Input Validation
When receiving task data via POST/PUT:
1. Validate required fields (title is mandatory)
2. Check priority is in valid set: `low, medium, high, critical`
3. Check status is in valid set: `pending, in_progress, completed`
4. Use Task dataclass for model validation
5. Return 400 Bad Request with error details if invalid

### Filtering Parameters
The `/api/tasks` endpoint accepts query parameters:
- `status=pending|in_progress|completed` - Filter by status
- `priority=low|medium|high|critical` - Filter by priority  
- `sort=date|priority|status` - Sort order

## Error Handling

### HTTP Status Codes
- `200 OK` - Successful read/list operation
- `201 Created` - Task successfully created
- `204 No Content` - Successful delete operation
- `400 Bad Request` - Invalid input data or missing required fields
- `404 Not Found` - Task ID doesn't exist
- `500 Internal Server Error` - Database or server error

### Database Operation Error Handling
```python
try:
    # database operation
    db.save_task(task)
except Exception as e:
    return jsonify({
        "success": False,
        "message": "Failed to save task",
        "error": str(e)
    }), 500
```

## Template Integration

### Context Data for Templates
When rendering templates, pass:
```python
render_template('template.html',
    tasks=all_tasks,
    stats=db.get_statistics(),
    task_count=len(all_tasks)
)
```

### Common Template Variables
- `tasks` - List of Task objects
- `stats` - Dictionary with counts by priority/status
- `active_filters` - Currently applied filters
- `error_message` - Error to display to user

## Adding New Routes

### Checklist for New Routes
1. Define the route path and HTTP method(s)
2. Add input validation if POST/PUT
3. Call appropriate database method
4. Wrap in try-except for error handling
5. Return appropriate HTTP status code
6. Document the route (docstring/comment)
7. Add test cases

### Route Template
```python
@app.route('/api/tasks/<int:task_id>/custom-action', methods=['POST'])
def custom_action(task_id):
    """Perform custom action on a task."""
    try:
        task = db.get_task(task_id)
        if not task:
            return jsonify({
                "success": False,
                "message": f"Task {task_id} not found"
            }), 404
        
        # Perform action
        result = db.perform_action(task)
        
        return jsonify({
            "success": True,
            "data": asdict(result),
            "message": "Action completed successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

## Performance Considerations

- Cache statistics endpoint results when possible
- Limit task list pagination (e.g., 50 tasks per page)
- Use database indexes for frequently filtered columns
- Avoid N+1 queries by prefetching related data
- Compress JSON responses for large lists

## CORS and Security

- Set appropriate CORS headers if needed for frontend requests
- Validate and sanitize all user input
- Use werkzeug security utilities for password if added later
- Don't expose internal error details to client (log them server-side)

## Testing API Routes

Test endpoints with various scenarios:
- Valid input → 200/201 response
- Missing required fields → 400 response
- Invalid IDs → 404 response
- Database errors → 500 response
- Filter combinations for list endpoint
- Concurrent requests to same resource
