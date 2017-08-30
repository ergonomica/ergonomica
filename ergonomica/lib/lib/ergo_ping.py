#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ping.py]

Defines the "ping" command.
"""

import os
import platform


def ping(argc):
    """ping: Ping HOSTNAMEs.

    Usage:
        ping HOSTNAMES...
        ping [-c COUNT] HOSTNAMES...

    Options:
        -c --count  Specify the number of times to ping the server.
    """

    out = []

    for host in argc.args['HOSTNAMES']:

        # Ping parameters as function of OS
        if argc.args['COUNT']:
            ping_str = ("-n 1" if platform.system().lower() == "windows" else "-c 1").replace("1", argc.args.get('COUNT', '1'))
        else:
            ping_str = ""

        out.append(host)
        if os.system("ping " + ping_str + " " + host) == 0:
            out[-1] += " is up"
        else:
            out[-1] += " is not up"
    return out


exports = {'ping': ping}


