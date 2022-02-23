from gi.repository import GObject


class Task(GObject.Object):
    title = GObject.Property(type=str)

    def __init__(self, title: str):
        super().__init__(title=title)
