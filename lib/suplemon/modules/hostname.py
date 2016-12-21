# -*- encoding: utf-8

import socket

from suplemon.suplemon_module import Module


class Hostname(Module):
    """Shows the machine hostname in the bottom status bar."""

    def init(self):
        hostinfo = socket.gethostbyaddr(socket.gethostname())
        self.hostname = hostinfo[0]
        # Use shorter hostname if available
        if hostinfo[1]:
            self.hostname = hostinfo[1][0]

    def get_status(self):
        return "host:{0}".format(self.hostname)


module = {
    "class": Hostname,
    "name": "hostname",
    "status": "bottom",
}
