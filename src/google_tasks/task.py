from __future__ import annotations

from enum import Enum
from typing import Optional

from gi.repository import GObject


class TaskStatus(Enum):
    NEEDS_ACTION = "needsAction"
    COMPLETED = "completed"


class Task(GObject.Object):
    title = GObject.Property(type=str)

    id: str
    etag: str
    updated: str
    parent: str  # readonly
    position: str
    notes: Optional[str]
    status: TaskStatus
    due: Optional[str]
    completed: Optional[str]
    deleted: bool
    hidden: bool

    @staticmethod
    def from_dict(data: dict) -> Task:
        new = Task()
        new.id = data.get("id")
        new.etag = data.get("etag")
        new.props.title = data.get("title")
        new.updated = data.get("updated")
        new.parent = data.get("parent")
        new.position = data.get("position")
        new.notes = data.get("notes")
        new.status = data.get("status")
        new.due = data.get("due")
        new.completed = data.get("completed")
        new.deleted = data.get("deleted")
        new.hidden = data.get("hidden")
        return new

    def update(self):
        pass
