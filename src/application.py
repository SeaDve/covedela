import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '1')
from gi.repository import Gtk, Gdk, Gio, Handy

from window import Window

class Application(Gtk.Application):

    def __init__(self):
        super().__init__()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.load_css()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.show_all()

    def load_css(self):
        Handy.init()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./src/style.css")
        display = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
