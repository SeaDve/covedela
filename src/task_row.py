from gi.repository import Gtk, GObject, Handy

from google_tasks.task import Task


@Gtk.Template(filename="src/task_row.ui")
class TaskRow(Handy.ExpanderRow):
    __gtype_name__ = "CvdlTaskRow"

    _title_label = Gtk.Template.Child()
    _check_button = Gtk.Template.Child()

    _task = None

    def __init__(self, task: Task):
        super().__init__()

        print(task._proxy._data)

        self._task = task
        self._task.connect("notify::title", self._update_title)
        self._task.connect("notify::is-completed", self._update_check_button)
        self._update_title()
        self._update_check_button()

    def _update_title(self, *args) -> None:
        self.props.title = self._task.title

    def _update_check_button(self, *args) -> None:
        self._check_button.props.active = self._task.props.is_completed
