"""Task model definition."""

import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


@dataclass
class Task:
    """Represents a single task in the system."""
    
    title: str
    description: str = ""
    priority: str = "medium"  # low, medium, high, critical
    status: str = "pending"  # pending, in_progress, completed
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False
    tags: list = field(default_factory=list)
    
    def __post_init__(self):
        """Validate priority values."""
        valid_priorities = ("low", "medium", "high", "critical")
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of {valid_priorities}")
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for serialization."""
        return asdict(self)
    
    def mark_complete(self):
        """Mark task as completed."""
        self.completed = True
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()
    
    def add_tag(self, tag: str):
        """Add a tag to the task."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the task."""
        if tag in self.tags:
            self.tags.remove(tag)
