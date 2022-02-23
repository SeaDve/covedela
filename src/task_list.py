from __future__ import annotations

import json
from pathlib import Path

from gi.repository import Gio, GObject

from task import Task


class TaskList(GObject.Object, Gio.ListModel):
    def __init__(self):
        super().__init__()

        self.list = []

    @classmethod
    def load_from_file(cls, path: Path) -> TaskList:
        with path.open() as file:
            json_obj = json.loads(file.read())

            task_list = cls()

            for item in json_obj:
                title = item["title"]
                task_list.append(Task(title))

            return task_list

    def save_to_file(self, path: Path) -> None:
        task_dict = []

        for task in self:
            task_dict.append(
                {
                    "title": task.props.title,
                }
            )

        content_to_write = json.dumps(task_dict)

        with path.open(mode="a+") as file:
            file.truncate(0)
            file.seek(0)
            file.write(content_to_write)

    def do_get_item(self, position):
        return self.list[position]

    def do_get_item_type(self):
        return Task.get_type()

    def do_get_n_items(self):
        return len(self.list)

    def append(self, task: Task) -> None:
        self.list.append(task)

        self.items_changed(self.get_n_items() - 1, 0, 1)
