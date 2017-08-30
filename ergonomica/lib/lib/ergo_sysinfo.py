#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_sysinfo.py]

Defines the "sysinfo" command.
"""

import platform
import psutil

def sysinfo(argc):
    """
    sysinfo: Print system information

    Usage:
       sysinfo stat [-apoc]
       sysinfo dyn  [-u]

    Options:
       -a --architecture   Print the system bits as well as linkage.
       -p --processor      Print processor name.
       -o --os             Print OS common name.
       -c --cpu-count       Print the number of CPUs on the system.
       -u --percent-usage  Print percent CPU usage for each CPU.
    """

    args = argc.args

    info = []

    if args['stat']:

        if args['--architecture']:
            info.append(", ".join(platform.architecture()))

        if args['--processor']:
            info.append(platform.processor())

        if args['--os']:
            info.append(platform.platform())

        if args['--cpu-count']:
            info.append(str(psutil.cpu_count()))


    elif args['dyn']:

        if args['--percent-usage']:
            info.append(psutil.cpu_percent(percpu=True))

    return info


exports = {'sysinfo': sysinfo}


