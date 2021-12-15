import time

from gi.repository import Gtk, GLib, Gio, Handy

from task_row import TaskRow
from task import Task

class Window(Handy.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Default RPi display dimension
        self.props.default_height = 320
        self.props.default_width = 480

        self._build_ui()
        self._setup_clock()
        self._setup_task_view()

    def _update_clock_label(self):
        local_time = time.localtime()
        formatted_time = time.strftime("%I:%M:%S", local_time)

        self._clock_label.set_label(formatted_time)

        return True

    def _build_ui(self):
        main_box = Gtk.Box(spacing=6, margin=6)
        self.add(main_box)

        # Left Box
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.add(left_box)

        task_view_header_label = Gtk.Label(label="Tasks", xalign=0)
        task_view_header_label.get_style_context().add_class("title-2")
        left_box.add(task_view_header_label)

        task_view_scrolled_window = Gtk.ScrolledWindow(vexpand=True)
        left_box.add(task_view_scrolled_window)

        self._task_view = Gtk.ListBox(margin=6)
        self._task_view.get_style_context().add_class("content")
        task_view_scrolled_window.add(self._task_view)

        # Right Box
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.add(right_box)

        self._clock_label = Gtk.Label(label="00:00:00", margin=6)
        self._clock_label.get_style_context().add_class("clock-label")
        right_box.add(self._clock_label)

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
