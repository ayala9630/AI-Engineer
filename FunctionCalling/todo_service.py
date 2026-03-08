import uuid
from typing import List, Optional, Dict

class Task:
    def __init__(self, title: str, description: str, task_type: str, start_date: str, end_date: str, status: str = "Pending"):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.task_type = task_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    def to_dict(self):
        return self.__dict__

tasks_db: List[Task] = []

def get_tasks(status: Optional[str] = None) -> List[Dict]:
    """שליפת משימות, אפשרות לסינון לפי סטטוס."""
    if status:
        return [t.to_dict() for t in tasks_db if t.status.lower() == status.lower()]
    return [t.to_dict() for t in tasks_db]

def add_task(title: str, description: str, task_type: str, start_date: str, end_date: str) -> Dict:
    """הוספת משימה חדשה."""
    new_task = Task(title, description, task_type, start_date, end_date)
    tasks_db.append(new_task)
    return {"message": "Task created successfully", "task": new_task.to_dict()}

def update_task(task_id: str, status: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    """עדכון משימה קיימת."""
    for task in tasks_db:
        if task.id == task_id:
            if status:
                task.status = status
            if end_date:
                task.end_date = end_date
            return {"message": "Task updated successfully", "task": task.to_dict()}
    return {"error": "Task not found"}

def delete_task(task_id: str) -> Dict:
    """מחיקת משימה לפי מזהה."""
    global tasks_db
    initial_len = len(tasks_db)
    tasks_db = [t for t in tasks_db if t.id != task_id]
    
    if len(tasks_db) < initial_len:
        return {"message": "Task deleted successfully"}
    return {"error": "Task not found"}