#!/usr/bin/python
# -*- coding: utf-8 -*-


# pylint's name standards are insane
# pylint: disable=invalid-name

# no other way to do it
# pylint: disable=line-too-long

# this file is imported from a different directory
# pylint: disable=import-error

# needed to make the import work
# pylint: disable=wrong-import-position

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/cp.py]

Defines the "cp"/"copy" command.
"""

import re
import subprocess

verbs = {}

def free(ENV, args, kwargs):
    """@(MacOS doesn't have a free command) Return memory statics."""

    #
    # ALL CREDIT GOES TO drfrogsplat(http://apple.stackexchange.com/users/1587/drfrogsplat)
    #
    
    # Get process info
    ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0]
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0]

    # Iterate processes
    processLines = ps.split('\n')
    sep = re.compile('[\s]+')
    rssTotal = 0 # kB
    for row in range(1,len(processLines)):
        rowText = processLines[row].strip()
        rowElements = sep.split(rowText)
        try:
            rss = float(rowElements[0]) * 1024
        except:
            rss = 0 # ignore...
        rssTotal += rss

        # Process vm_stat
        vmLines = vm.split('\n')
        sep = re.compile(':[\s]+')
        vmStats = {}
        for row in range(1,len(vmLines)-2):
            rowText = vmLines[row].strip()
            rowElements = sep.split(rowText)
            vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

    return "Wired Memory:\t\t%d MB" % (vmStats["Pages wired down"]/1024/1024) + \
           "\nActive Memory:\t\t%d MB" % (vmStats["Pages active"]/1024/1024) + \
           "\nInactive Memory:\t%d MB" % (vmStats["Pages inactive"]/1024/1024) + \
           "\nFree Memory:\t\t%d MB" % (vmStats["Pages free"]/1024/1024) + \
           "\nReal Mem Total (ps):\t%.3f MB" % (rssTotal/1024/1024)

verbs["free"] = free
verbs["memory"] = free
verbs["mem"] = free
