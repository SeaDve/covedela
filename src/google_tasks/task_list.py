from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Dict

from gi.repository import Gio, GObject

from .task import Task
from .proxy import Proxy

if TYPE_CHECKING:
    from .client import Client


class TaskList(GObject.Object, Gio.ListModel):
    # id: str
    # etag: str
    # title: str
    # updated: str

    _client: Client
    _proxy: Proxy
    _cached_tasks: Dict[str, Task] = {}

    def __init__(self, client: Client, data: dict):
        super().__init__()

        self._client = client
        self._proxy = Proxy(
            data, self, self._push_updates_impl, self._pull_updates_impl
        )
        self._proxy.connect("attribute-changed", self._on_proxy_attribute_changed)

        self.update()

        for task in self._get_tasks():
            self._cached_tasks[task.get_id()] = task
            position = list(self._cached_tasks.keys()).index(task.get_id())
            self.items_changed(position, 0, 1)

    # Public methods
    def get_id(self) -> str:
        return self._proxy.get_id()

    def update(self):
        self._proxy.update()

        updated_tasks = self._get_tasks()

        for updated_task in updated_tasks:
            stored_task = self._cached_tasks.get(updated_task.get_id())
            if stored_task is None:
                self._cached_tasks[updated_task.get_id()] = updated_task
                position = list(self._cached_tasks.keys()).index(updated_task.get_id())
                self.items_changed(position, 0, 1)
                continue
            stored_task.update(updated_task)

        # FIXME broken
        being_found: Task = None
        is_found = False

        for task in self._cached_tasks.values():
            for updated_task in updated_tasks:
                being_found = updated_task
                if updated_task.get_id() == task.get_id():
                    is_found = True

        if not is_found and being_found is not None:
            print(">>> TaskList removing")
            position = list(self._cached_tasks.keys()).index(being_found.get_id())
            self._cached_tasks.pop(being_found.get_id())
            self.items_changed(position, 1, 0)
        else:
            print(">>> Still found, not removing")

    # GObject Properties
    @GObject.Property(type=str)
    def title(self):
        return self._proxy.get_attribute("title")

    @GObject.Property(type=str)
    def last_updated(self):
        return self._proxy.get_attribute("updated")

    # GObject Virtual methods
    def do_get_item(self, position) -> Optional[Task]:
        try:
            return list(self._cached_tasks.values())[position]
        except IndexError:
            return None

    def do_get_item_type(self):
        return Task.get_type()

    def do_get_n_items(self):
        return len(self._cached_tasks)

    # Private methods
    def _get_tasks(self) -> List[Task]:
        tasks: List[Task] = []

        page_to_load: Optional[str] = None

        while True:
            response = (
                self._client.service()
                .tasks()
                .list(
                    tasklist=self.get_id(),
                    showHidden=True,
                    showCompleted=True,
                    maxResults=100,
                    pageToken=page_to_load,
                )
                .execute()
            )

            for item in response.get("items", []):
                task = Task(self._client, self, item)
                tasks.append(task)

            page_to_load = response.get("nextPageToken")

            if not page_to_load:
                break

        return tasks

    def _on_proxy_attribute_changed(self, proxy: Proxy, attribute_name: str):
        if attribute_name == "title":
            self.notify("title")
        elif attribute_name == "updated":
            self.notify("last-updated")

    @staticmethod
    def _push_updates_impl(self, update_body: dict):
        self._client.service().tasklists().patch(
            tasklist=self.get_id(), body=update_body
        ).execute()

    @staticmethod
    def _pull_updates_impl(self, body: dict) -> dict:
        print(">>> TaskList pulling updates")
        response = (
            self._client.service().tasklists().get(tasklist=self.get_id()).execute()
        )
        return response
