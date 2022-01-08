import time

from gi.repository import Gtk, GLib, Gio, Handy

from task_row import TaskRow
from task import Task

@Gtk.Template(filename="src/window.ui")
class Window(Handy.ApplicationWindow):
    __gtype_name__ = "CvdlWindow"

    _task_view = Gtk.Template.Child()
    _clock_label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Default RPi display dimension
        self.props.default_height = 320
        self.props.default_width = 480

        self._setup_clock()
        self._setup_task_view()

    def _update_clock_label(self):
        local_time = time.localtime()
        formatted_time = time.strftime("%I:%M:%S", local_time)

        self._clock_label.set_label(formatted_time)

        return True

    def _create_task_row(self, task: Task):
        task_row = TaskRow()
        task_row.props.task = task
        return task_row

    def _setup_clock(self):
        GLib.timeout_add(200, self._update_clock_label)

    def _setup_task_view(self):
        model = Gio.ListStore.new(Task)

        for index, val in enumerate(range(10)):
            model.append(Task(f"Task # {index}"))

        self._task_view.bind_model(model, self._create_task_row)
