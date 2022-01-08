import time
import datetime

from gi.repository import Gtk


@Gtk.Template(filename="src/clock.ui")
class Clock(Gtk.Bin):
    __gtype_name__ = "CvdlClock"

    _time_label = Gtk.Template.Child()
    _date_label = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    def _refresh_time(self):
        local_time = time.localtime()
        formatted_time = time.strftime("%I:%M:%S", local_time)

        self._time_label.set_label(formatted_time)

    def _refresh_date(self):
        today = datetime.date.today()
        formatted_date = today.strftime("%a %b %d, %Y")

        self._date_label.set_label(formatted_date)

    def refresh(self):
        self._refresh_time()
        self._refresh_date()
