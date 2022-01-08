from gi.repository import Gtk, GLib, Handy

from task_row import TaskRow
from task import Task
from clock import Clock
from task_list import TaskList


@Gtk.Template(filename="src/window.ui")
class Window(Handy.ApplicationWindow):
    __gtype_name__ = "CvdlWindow"

    _task_view = Gtk.Template.Child()
    _clock: Clock = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._setup_clock()
        self._setup_task_view()

    def _create_task_row(self, task: Task) -> TaskRow:
        task_row = TaskRow()
        task_row.props.task = task
        return task_row

    def _refresh_clock(self):
        self._clock.refresh()
        return True

    def _setup_clock(self):
        GLib.timeout_add(200, self._refresh_clock)

    def _setup_task_view(self):
        model = TaskList()

        for index, val in enumerate(range(10)):
            model.append(Task(f"Task # {index}"))

        self._task_view.bind_model(model, self._create_task_row)
