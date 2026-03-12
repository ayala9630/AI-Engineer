"""Database operations for task persistence."""

import json
import sqlite3
from pathlib import Path
from typing import Dict, Optional
from task import Task


class TaskDatabase:
    """Handles all database operations for tasks."""
    
    def __init__(self, db_path: str = "tasks.db"):
        """Initialize database connection and create schema if needed."""
        self.db_path = db_path
        self.connect()
        self.create_schema()
    
    def connect(self):
        """Establish database connection."""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
    
    def create_schema(self):
        """Create the tasks table if it doesn't exist."""
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                completed_at TEXT,
                completed INTEGER DEFAULT 0,
                tags TEXT,
                CONSTRAINT valid_priority CHECK (priority IN ('low', 'medium', 'high', 'critical'))
            )
        """)
        self.connection.commit()
    
    def save_task(self, task: Task) -> bool:
        """Save or update a task in the database."""
        try:
            cursor = self.connection.cursor()
            tags_json = json.dumps(task.tags) if task.tags else "[]"
            
            cursor.execute("""
                INSERT OR REPLACE INTO tasks 
                (id, title, description, priority, status, created_at, completed_at, completed, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id,
                task.title,
                task.description,
                task.priority,
                task.status,
                task.created_at,
                task.completed_at,
                1 if task.completed else 0,
                tags_json
            ))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def load_task(self, task_id: str) -> Optional[Task]:
        """Load a single task from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_task(row)
        return None
    
    def load_all_tasks(self) -> Dict[str, Task]:
        """Load all tasks from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        
        tasks = {}
        for row in rows:
            task = self._row_to_task(row)
            tasks[task.id] = task
        return tasks
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert a database row to a Task object."""
        tags = json.loads(row['tags']) if row['tags'] else []
        
        return Task(
            id=row['id'],
            title=row['title'],
            description=row['description'] or "",
            priority=row['priority'],
            status=row['status'],
            created_at=row['created_at'],
            completed_at=row['completed_at'],
            completed=bool(row['completed']),
            tags=tags
        )
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
