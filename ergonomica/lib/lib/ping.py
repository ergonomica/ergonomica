#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/ping.py]

Defines the "ping" command.
"""

import os
import platform

verbs = {}

def ping(env, args, kwargs):
    """[HOSTNAME,...]@See if HOSTNAME is up (ping)."""
    out = []

    os.environ["PATH"] = env.PATH

    for host in args:

        # Ping parameters as function of OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

        out.append(host)
        if os.system("ping " + ping_str + " " + host) == 0:
            out[-1] += " is up"
        else:
            out[-1] += " is not up"
    return out


verbs["ping"] = ping
