from pathlib import Path

from gi.repository import Gtk, GLib, Handy

from task_row import TaskRow
from task import Task
from clock import Clock
from task_list import TaskList

SAVE_FILE_PATH = Path("/home/dave/abcde.txt")


@Gtk.Template(filename="src/window.ui")
class Window(Handy.ApplicationWindow):
    __gtype_name__ = "CvdlWindow"

    _task_view = Gtk.Template.Child()
    _clock: Clock = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._setup_signals()
        self._setup_clock()
        self._setup_task_view()

    def _on_destroy(self, win):
        self._task_list.save_to_file(SAVE_FILE_PATH)

    def _setup_signals(self):
        self.connect("destroy", self._on_destroy)

    def _refresh_clock(self):
        self._clock.refresh()
        return True

    def _setup_clock(self):
        GLib.timeout_add(200, self._refresh_clock)

    def _setup_task_view(self):
        self._task_list = TaskList()

        for index, val in enumerate(range(10)):
            self._task_list.append(Task(f"Task # {index}"))

        self._task_view.bind_model(self._task_list, lambda task: TaskRow(task))
