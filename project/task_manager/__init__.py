"""Task Manager package."""

from .task import Task
from .database import TaskDatabase
from .main import TaskManager

__all__ = ["Task", "TaskDatabase", "TaskManager"]
__version__ = "1.0.0"
