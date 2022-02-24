from pathlib import Path

from gi.repository import Gtk, GLib, Handy, GObject

from task_row import TaskRow
from clock import Clock

from google_tasks.client import Client

SAVE_FILE_PATH = Path("/home/dave/abcde.txt")


@Gtk.Template(filename="src/window.ui")
class Window(Handy.ApplicationWindow):
    __gtype_name__ = "CvdlWindow"

    _task_list_title_label = Gtk.Template.Child()
    _task_view = Gtk.Template.Child()
    _clock: Clock = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("destroy", self._on_destroy)

        self._client = Client()
        self._setup_task_view()

        GLib.timeout_add(200, self._refresh_clock)
        GLib.timeout_add_seconds(2, self._update_client)

    def _on_destroy(self, win):
        self._task_list.save_to_file(SAVE_FILE_PATH)

    def _refresh_clock(self):
        self._clock.refresh()
        return True

    def _update_client(self):
        self._client.update()
        print(">>> Updating client")
        return True

    def _setup_task_view(self):
        task_list = self._client.get_task_lists()[0]
        task_list.bind_property(
            "title",
            self._task_list_title_label,
            "label",
            flags=GObject.BindingFlags.SYNC_CREATE,
        )
        task_list.notify("title")

        self._task_view.bind_model(task_list, lambda task: TaskRow(task))
