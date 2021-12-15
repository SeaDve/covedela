import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from window import Window

class Application(Gtk.Application):

    def __init__(self):
        super().__init__()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()
