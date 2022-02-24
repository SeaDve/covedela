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
    _next_page_token: Optional[str] = None

    def __init__(self, client: Client, data: dict):
        super().__init__()

        self._client = client
        self._proxy = Proxy(
            data, self, self._push_updates_impl, self._pull_updates_impl
        )
        self._proxy.connect("attribute-changed", self._on_proxy_attribute_changed)
        self.update()
        self.load_more_tasks()

    # Public methods
    def get_id(self) -> str:
        return self._proxy.get_id()

    def update(self):
        self._proxy.update()

        for task in self._cached_tasks.values():
            task.update()

    def load_more_tasks(self):
        response = (
            self._client.service()
            .tasks()
            .list(
                tasklist=self.get_id(), maxResults=100, pageToken=self._next_page_token
            )
            .execute()
        )

        for item in response.get("items", []):
            task = Task(self._client, self, item)
            # task.connect("attribute-changed", self._on_items_changed, 1, 1) # TODO uncomment this
            self._cached_tasks[task.get_id()] = task
            self._on_items_changed(task, None, 0, 1)

        self._next_page_token = response.get("nextPageToken", [])

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
    def _on_items_changed(self, task: Task, pspec, removed: int, added: int) -> None:
        position = list(self._cached_tasks.keys()).index(task.get_id())
        self.items_changed(position, removed, added)

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
        response = (
            self._client.service().tasklists().get(tasklist=self.get_id()).execute()
        )
        return response
