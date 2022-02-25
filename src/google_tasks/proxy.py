from typing import Callable

from gi.repository import GObject


class Proxy(GObject.Object):
    __gsignals__ = {
        "attribute-changed": (GObject.SignalFlags.RUN_LAST, None, (str,)),
    }

    _data = {}
    _update_body = {}

    _obj: object
    _push_updates_impl: Callable[[object, dict], None]
    _pull_updates_impl: Callable[[object, dict], dict]

    def __init__(
        self,
        initial_data: dict,
        obj: object,
        push_updates_impl: Callable[[object, dict], None],
        pull_updates_impl: Callable[[object, dict], dict],
    ):
        super().__init__()

        self._data = initial_data

        self._obj = obj
        self._push_updates_impl = push_updates_impl
        self._pull_updates_impl = pull_updates_impl

    def set_attribute(self, key: str, value: any) -> None:
        self._update_body[key] = value
        self._push_updates()

    def get_attribute(self, key: str) -> any:
        # self._pull_updates()
        return self._data.get(key)

    def get_id(self) -> str:
        return self._data.get("id")

    def get_etag(self) -> str:
        return self._data.get("etag")

    def update_data(self, new_data: dict):
        old_data = dict(self._data)
        self._data = new_data

        print(">>> Proxy updating data")

        for key, value in self._data.items():
            if old_data.get(key) != new_data.get(key):
                self.emit("attribute-changed", key)

    def update(self):
        self._pull_updates(notify=True)

    def _push_updates(self):
        if not self._update_body:
            return

        self._push_updates_impl(self._obj, self._update_body)
        self._update_body.clear()

    def _pull_updates(self, notify: bool = False):
        old_data = dict(self._data)
        updated_data = self._pull_updates_impl(self._obj, self._data)
        self._data.update(updated_data)

        if notify:
            for key, value in self._data.items():
                if old_data.get(key) != updated_data.get(key):
                    self.emit("attribute-changed", key)
