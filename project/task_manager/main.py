"""Main entry point for Task Manager application."""

import json
from datetime import datetime
from database import TaskDatabase
from task import Task


class TaskManager:
    """Main task management application."""
    
    def __init__(self, db_path: str = "tasks.db"):
        """Initialize the task manager with a database."""
        self.db = TaskDatabase(db_path)
        self.tasks = self.db.load_all_tasks()
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """Add a new task to the system."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            created_at=datetime.now().isoformat()
        )
        self.db.save_task(task)
        self.tasks[task.id] = task
        return task
    
    def list_tasks(self, filter_by: str = None) -> list:
        """List all tasks, optionally filtered by priority."""
        if filter_by:
            return [t for t in self.tasks.values() if t.priority == filter_by]
        return list(self.tasks.values())
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed."""
        if task_id in self.tasks:
            self.tasks[task_id].completed = True
            self.tasks[task_id].completed_at = datetime.now().isoformat()
            self.db.save_task(self.tasks[task_id])
            return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the system."""
        if task_id in self.tasks:
            self.db.delete_task(task_id)
            del self.tasks[task_id]
            return True
        return False


def main():
    """Run the task manager application."""
    manager = TaskManager()
    
    # Example usage
    print("Task Manager - Demo")
    print("-" * 40)
    
    # Add sample tasks
    task1 = manager.add_task("Design database schema", "Plan task table structure", "high")
    task2 = manager.add_task("Implement API endpoints", "Create REST endpoints", "high")
    task3 = manager.add_task("Write unit tests", "Test coverage for core functions", "medium")
    
    # List tasks
    print("\nAll Tasks:")
    for task in manager.list_tasks():
        status = "✓" if task.completed else "○"
        print(f"{status} [{task.priority.upper()}] {task.title} (ID: {task.id})")
    
    # Complete a task
    manager.complete_task(task1.id)
    
    print("\nAfter completing first task:")
    for task in manager.list_tasks():
        status = "✓" if task.completed else "○"
        print(f"{status} [{task.priority.upper()}] {task.title}")


if __name__ == "__main__":
    main()
