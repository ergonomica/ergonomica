# -*- encoding: utf-8

import time

from suplemon.suplemon_module import Module


class Date(Module):
    def get_status(self):
        s = time.strftime("%d.%m.")
        if self.app.config["app"]["use_unicode_symbols"]:
            return "" + s
        return s


module = {
    "class": Date,
    "name": "date",
    "status": "top",
}
