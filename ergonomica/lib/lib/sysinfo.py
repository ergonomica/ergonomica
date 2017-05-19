#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/sysinfo.py]

Defines the "sysinfo" command.
"""

import platform

verbs = {}

def sysinfo(argc):
    """
    sysinfo: Print system information
     
    Usage:
       sysinfo [-a | --architecture] [-p | --processor] [-r | --release] [-o | --os]

    Options:
       -a --architecture  Print the system bits as well as linkage.
       -p --processor     Print processor name.
       -o --os            Print OS common name.
    """
    args = argc.args

    info = []

    if args['--architecture']:
        info.append(", ".join(platform.architecture()))

    if args['--processor']:
        info.append(platform.processor())

    if args['--os']:
        info.append(platform.platform())
        
    return info

verbs["sysinfo"] = sysinfo
