import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")
from gi.repository import Gtk, Gdk, Gio, Handy, GdkPixbuf

from window import Window


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="io.github.seadve.Covedela")

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.load_css()
        self.setup_actions()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.show_all()
        win.fullscreen()

    def on_show_qr(self, *args):
        print("showing qr code")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("qr.jpg", 300, 300)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        window = Gtk.Window(transient_for=self.props.active_window, modal=True)
        window.add(image)
        window.show_all()
        window.connect("button-press-event", lambda win, key: win.close())
        window.connect("key-press-event", lambda win, key: win.close())
        window.fullscreen()

    def on_quit(self, action, args):
        self.quit()

    def setup_actions(self):
        show_qr_action = Gio.SimpleAction.new("show-qr", None)
        show_qr_action.connect("activate", self.on_show_qr)
        self.add_action(show_qr_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)

        self.set_accels_for_action("app.quit", ("<Control>q",))

    def load_css(self):
        Handy.init()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./src/style.css")
        display = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            display,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
