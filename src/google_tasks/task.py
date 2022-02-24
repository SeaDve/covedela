from __future__ import annotations

from enum import Enum
from datetime import datetime
from typing import Optional

from gi.repository import GObject

from .proxy import Proxy


class TaskStatus(Enum):
    NEEDS_ACTION = "needsAction"
    COMPLETED = "completed"


class Task(GObject.Object):
    _client = None
    _proxy: Proxy
    _task_list = None

    def __init__(self, client, task_list, initial_data: dict):
        super().__init__()

        self._client = client
        self._task_list = task_list
        self._proxy = Proxy(
            initial_data, self, self._push_updates_impl, self._pull_updates_impl
        )
        self.update()

    def get_id(self) -> str:
        return self._proxy.get_id()

    def update(self):
        self._proxy.update()

    @GObject.Property(type=str)
    def title(self):
        return self._proxy.get_attribute("title")

    @GObject.Property(type=object)
    def last_updated(self):
        return datetime.fromisoformat(self._proxy.get_attribute("updated"))

    @GObject.Property(type=str)  # Readonly
    def parent_task_id(self):
        return self._proxy.get_attribute("parent")

    @GObject.Property(type=int)
    def position(self):
        return int(self._proxy.get_attribute("position"))

    @GObject.Property(type=bool, default=False)
    def is_completed(self):
        status = self._proxy.get_attribute("status")
        if status == "needsAction":
            return False
        elif status == "completed":
            return True
        else:
            print(f"Error: Invalid status: {status}")
            return False

    @GObject.Property(type=object)  # Optional
    def due_date(self):
        return datetime.fromisoformat(self._proxy.get_attribute("due"))

    @GObject.Property(type=object)  # Optional
    def completed_date(self):
        return datetime.fromisoformat(self._proxy.get_attribute("completed"))

    @GObject.Property(type=bool, default=False)
    def deleted(self):
        return self._proxy.get_attribute("deleted")

    @GObject.Property(type=bool, default=False)
    def hidden(self):
        return self._proxy.get_attribute("hidden")

    def _on_proxy_attribute_changed(self, proxy: Proxy, attribute_name: str):
        if attribute_name == "title":
            self.notify("title")
        elif attribute_name == "updated":
            self.notify("last-updated")

    @staticmethod
    def _push_updates_impl(self, update_body: dict):
        self._client.service().tasks().patch(
            tasklist=self._task_list.get_id(), task=self.get_id(), body=update_body
        ).execute()

    @staticmethod
    def _pull_updates_impl(self, body: dict) -> dict:
        response = (
            self._client.service()
            .tasks()
            .get(tasklist=self._task_list.get_id(), task=self.get_id())
            .execute()
        )
        return response
