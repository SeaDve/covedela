from gi.repository import Gtk, GObject, Handy

from task import Task


@Gtk.Template(filename="src/task_row.ui")
class TaskRow(Handy.ExpanderRow):
    __gtype_name__ = "CvdlTaskRow"

    _title_label = Gtk.Template.Child()

    _task = None

    def __init__(self, task: Task):
        super().__init__()

        self._task = task
        self._task.bind_property(
            "title",
            self,
            "title",
            flags=GObject.BindingFlags.SYNC_CREATE,
        )
        self._task.notify("title")  # Idk why is this needed
