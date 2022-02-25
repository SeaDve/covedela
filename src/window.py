from pathlib import Path
from datetime import datetime

from gi.repository import Gtk, GLib, Handy, GObject, Gio

from task_row import TaskRow
from clock import Clock

from google_tasks.task import Task
from google_tasks.client import Client

SAVE_FILE_PATH = Path("/home/dave/abcde.txt")


@Gtk.Template(filename="src/window.ui")
class Window(Handy.ApplicationWindow):
    __gtype_name__ = "CvdlWindow"

    _refresh_button = Gtk.Template.Child()
    _task_list_title_label = Gtk.Template.Child()
    _task_view = Gtk.Template.Child()
    _clock: Clock = Gtk.Template.Child()
    _current_task_view = Gtk.Template.Child()

    _today_tasks = Gio.ListStore.new(Task)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("destroy", self._on_destroy)
        self._refresh_button.connect("clicked", self._update_client)

        self._client = Client()
        self._setup_task_view()
        self._setup_current_task_view()

        GLib.timeout_add(200, self._refresh_clock)

    def _on_destroy(self, win):
        self._task_list.save_to_file(SAVE_FILE_PATH)

    def _refresh_clock(self):
        self._clock.refresh()
        return True

    def _update_client(self, *args):
        self._client.update()
        print(">>> Updating client")

    def _create_task_row(self, task) -> TaskRow:
        print(task._proxy._data)
        return TaskRow(task)

    def _setup_task_view(self):
        task_list = self._client.get_task_lists()[0]
        task_list.bind_property(
            "title",
            self._task_list_title_label,
            "label",
            flags=GObject.BindingFlags.SYNC_CREATE,
        )
        task_list.notify("title")

        task_list.connect("items-changed", self._on_task_list_items_changed)

        self._task_view.bind_model(task_list, self._create_task_row)
        self._task_list = task_list

    def _setup_current_task_view(self):
        def create(task):
            print(f"TEST {task._proxy._data}")
            print(self._today_tasks.get_n_items())

            row = Gtk.ListBoxRow()
            row.props.selectable = False
            row.props.activatable = True
            row.props.action_name = "app.show-qr"

            label = Gtk.Label()
            label.props.margin = 6
            task.bind_property(
                "title", label, "label", flags=GObject.BindingFlags.SYNC_CREATE
            )
            task.notify("title")
            row.add(label)

            return row

        self._current_task_view.bind_model(self._today_tasks, create)
        self._on_task_list_items_changed(None, None, None, None)

    def _on_task_list_items_changed(
        self, task_list, position: int, removed: int, added: int
    ) -> None:
        for task in self._task_list._cached_tasks.values():
            today = datetime.now().date()

            if (
                not task.props.is_completed
                and task.props.due_date is not None
                and task.props.due_date.date() == today
            ):
                self._today_tasks.append(task)
