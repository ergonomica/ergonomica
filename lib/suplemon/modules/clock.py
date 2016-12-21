# -*- encoding: utf-8

import time

from suplemon.suplemon_module import Module


class Clock(Module):
    """Shows a clock in the top status bar."""
    def get_status(self):
        s = time.strftime("%H:%M")
        if self.app.config["app"]["use_unicode_symbols"]:
            return "\u231A" + s
        return s


module = {
    "class": Clock,
    "name": "clock",
    "status": "top",
}
