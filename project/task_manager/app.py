"""Flask web application for Task Manager."""

# Ensure compatibility when running on Python builds where pkgutil.get_loader
# may be unavailable (newer Pythons). Provide a lightweight shim before
# importing Flask so Flask's internal package discovery works.
import pkgutil
import importlib.util
import ast

# Backwards-compatibility for libraries expecting deprecated AST node classes
if not hasattr(ast, 'Str'):
    ast.Str = ast.Constant

if not hasattr(pkgutil, 'get_loader'):
    def _get_loader(name):
        # Try to find a spec normally
        try:
            spec = importlib.util.find_spec(name)
        except ValueError:
            spec = None
        loader = None
        origin = None

        if spec is not None:
            loader = spec.loader
            origin = getattr(spec, 'origin', None)
        else:
            # fallback: try to inspect already-imported module
            import sys
            mod = sys.modules.get(name)
            if mod is not None:
                loader = getattr(mod, '__loader__', None)
                origin = getattr(mod, '__file__', None)

        # If we still don't have information, return None so normal import machinery handles it
        if loader is None and origin is None:
            return None

        class LoaderShim:
            def __init__(self, loader, origin):
                self._loader = loader
                self._origin = origin
            def get_filename(self, fullname):
                # Prefer loader.get_filename if available
                if self._loader is not None:
                    try:
                        return self._loader.get_filename(fullname)
                    except Exception:
                        pass
                return self._origin

        return LoaderShim(loader, origin)
    pkgutil.get_loader = _get_loader

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from database import TaskDatabase
from task import Task
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Database will be created per-request to avoid threading issues
def get_db():
    """Get database connection for current request."""
    db = TaskDatabase()
    return db

@app.route('/')
def index():
    """Display all tasks."""
    db = get_db()
    tasks = db.load_all_tasks()
    tasks_list = sorted(tasks.values(), key=lambda t: t.created_at, reverse=True)
    db.close()
    
    return render_template('index.html', tasks=tasks_list)

@app.route('/filter/<priority>')
def filter_by_priority(priority):
    """Filter tasks by priority."""
    db = get_db()
    tasks = db.load_all_tasks()
    filtered = [t for t in tasks.values() if t.priority == priority]
    filtered.sort(key=lambda t: t.created_at, reverse=True)
    db.close()
    
    return render_template('tasks_list.html', tasks=filtered, active_filter=priority)

@app.route('/completed')
def completed_tasks():
    """Show only completed tasks."""
    db = get_db()
    tasks = db.load_all_tasks()
    completed = [t for t in tasks.values() if t.completed]
    completed.sort(key=lambda t: t.completed_at, reverse=True)
    db.close()
    
    return render_template('tasks_list.html', tasks=completed, active_filter='completed')

@app.route('/pending')
def pending_tasks():
    """Show only pending tasks."""
    db = get_db()
    tasks = db.load_all_tasks()
    pending = [t for t in tasks.values() if not t.completed]
    pending.sort(key=lambda t: t.created_at, reverse=True)
    db.close()
    
    return render_template('tasks_list.html', tasks=pending, active_filter='pending')

@app.route('/api/task/add', methods=['POST'])
def add_task():
    """API endpoint to add a new task."""
    data = request.get_json()
    db = get_db()
    
    try:
        task = Task(
            title=data.get('title', 'Untitled'),
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            created_at=datetime.now().isoformat()
        )
        
        if task.priority not in ('low', 'medium', 'high', 'critical'):
            db.close()
            return jsonify({'success': False, 'error': 'Invalid priority'}), 400
        
        db.save_task(task)
        db.close()
        return jsonify({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'priority': task.priority,
                'completed': task.completed
            }
        })
    except Exception as e:
        db.close()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/task/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """API endpoint to mark task as complete."""
    db = None
    try:
        db = get_db()
        task = db.load_task(task_id)
        
        if not task:
            if db:
                try:
                    db.close()
                except:
                    pass
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        task.mark_complete()
        db.save_task(task)
        if db:
            try:
                db.close()
            except:
                pass
        
        return jsonify({
            'success': True,
            'task': {
                'id': task.id,
                'title': task.title,
                'completed': task.completed,
                'completed_at': task.completed_at
            }
        })
    except Exception as e:
        if db:
            try:
                db.close()
            except:
                pass
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/task/<task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """API endpoint to toggle task completion status."""
    db = None
    try:
        db = get_db()
        task = db.load_task(task_id)
        
        if not task:
            if db:
                try:
                    db.close()
                except:
                    pass
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        task.completed = not task.completed
        if task.completed:
            task.status = 'completed'
            task.completed_at = datetime.now().isoformat()
        else:
            task.status = 'pending'
            task.completed_at = None
        
        db.save_task(task)
        if db:
            try:
                db.close()
            except:
                pass
        
        return jsonify({
            'success': True,
            'completed': task.completed,
            'status': task.status
        })
    except Exception as e:
        if db:
            try:
                db.close()
            except:
                pass
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/task/<task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """API endpoint to delete a task."""
    db = None
    try:
        db = get_db()
        print(f"Attempting to delete task with ID: {task_id}")
        
        success = db.delete_task(task_id)
        print(f"Delete result: {success}")
        
        if not success:
            if db:
                try:
                    db.close()
                except:
                    pass
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        if db:
            try:
                db.close()
            except:
                pass
        return jsonify({'success': True})
    except Exception as e:
        if db:
            try:
                db.close()
            except:
                pass
        print(f"Error during delete: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/api/task/<task_id>/edit', methods=['POST'])
def edit_task(task_id):
    """API endpoint to edit a task."""
    db = get_db()
    try:
        task = db.load_task(task_id)
        
        if not task:
            db.close()
            return jsonify({'success': False, 'error': 'Task not found'}), 404
        
        data = request.get_json()
        if not data:
            db.close()
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            priority = data['priority']
            if priority not in ('low', 'medium', 'high', 'critical'):
                db.close()
                return jsonify({'success': False, 'error': 'Invalid priority'}), 400
            task.priority = priority
        
        success = db.save_task(task)
        db.close()
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to save task'}), 500
    except Exception as e:
        if 'db' in locals():
            db.close()
        print(f"Error editing task {task_id}: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    """API endpoint for task statistics."""
    db = get_db()
    try:
        tasks = db.load_all_tasks()
        db.close()
        
        tasks_list = list(tasks.values())
        
        total = len(tasks_list)
        completed = sum(1 for t in tasks_list if t.completed)
        pending = total - completed
        
        priority_breakdown = {
            'critical': sum(1 for t in tasks_list if t.priority == 'critical'),
            'high': sum(1 for t in tasks_list if t.priority == 'high'),
            'medium': sum(1 for t in tasks_list if t.priority == 'medium'),
            'low': sum(1 for t in tasks_list if t.priority == 'low'),
        }
        
        return jsonify({
            'total': total,
            'completed': completed,
            'pending': pending,
            'priority_breakdown': priority_breakdown,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
        })
    except Exception as e:
        if 'db' in locals():
            db.close()
        print(f"Error getting stats: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("Task Manager Web UI starting...")
    print("Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    app.run(debug=False, host='localhost', port=5000, threaded=True)
