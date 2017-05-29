#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ping.py]

Defines the "ping" command.
"""

import os
import platform


def main(argc):
    """ping: Ping HOSTNAMEs.

    Usage:
        ping [-c COUNT] HOSTNAME...

    Options:
        -c --count  Specify the number of times to ping the server.
    """

    out = []

    #os.environ["PATH"] = env.PATH

    for host in argc.args['HOSTNAME']:

        # Ping parameters as function of OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

        out.append(host)
        if os.system("ping " + ping_str + " " + host) == 0:
            out[-1] += " is up"
        else:
            out[-1] += " is not up"
    return out
