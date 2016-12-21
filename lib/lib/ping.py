#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/ping.py]

Defines the "ping" command.
"""

import os, platform

verbs = {}

def ping(env, args, kwargs):
    """HOSTNAME,..@See if HOSTNAME is up (ping)."""
    out = []
    for host in args:
    
        # Ping parameters as function of OS
        ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

        out.append(host + (" is up" if os.system("ping " + ping_str + " " + host) == 0 else " is not up"))
    return out

    
verbs["ping"] = ping
