from gi.repository import Gtk, GObject, Handy

from google_tasks.task import Task


@Gtk.Template(filename="src/task_row.ui")
class TaskRow(Gtk.ListBoxRow):
    __gtype_name__ = "CvdlTaskRow"

    _title_label = Gtk.Template.Child()
    _check_button = Gtk.Template.Child()

    _task = None

    def __init__(self, task: Task):
        super().__init__()

        self._task = task
        self._task.connect("notify::title", self._update_title)
        self._task.connect("notify::is-completed", self._on_task_is_completed_notify)
        self._update_title()
        self._update_check_button()

    def _on_task_is_completed_notify(self, *args) -> None:
        self._update_title()
        self._update_check_button()

    def _update_title(self, *args) -> None:
        if self._task.props.is_completed:
            self._title_label.props.label = (
                f"<span strikethrough='true'>{self._task.props.title}</span>"
            )
        else:
            self._title_label.props.label = self._task.props.title

    def _update_check_button(self, *args) -> None:
        self._check_button.props.active = self._task.props.is_completed
