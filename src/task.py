from gi.repository import GObject

class Task(GObject.GObject):

    title = GObject.Property(type=str)

    def __init__(self, title: str):
        super().__init__()

        self.props.title = title
