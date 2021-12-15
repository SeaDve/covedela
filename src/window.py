from gi.repository import Gtk

class Window(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
