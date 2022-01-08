from gi.repository import Gtk, GObject, Handy

from task import Task

@Gtk.Template(filename="src/task_row.ui")
class TaskRow(Handy.ExpanderRow):
    __gtype_name__ = "CvdlTaskRow"

    _title_label = Gtk.Template.Child()

    _task = None
    _title_binding = None

    def __init__(self):
        super().__init__()

    @GObject.Property(type=Task, default=_task)
    def task(self):
        return self._task

    @task.setter
    def task(self, val: Task):
        self._task = val

        if self._title_binding is not None:
            self._title_binding.unbind()

        self._task.bind_property("title", self, "title", flags=GObject.BindingFlags.SYNC_CREATE)
        self._task.notify("title") # IDK why is this needed
