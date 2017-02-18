#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

# this file is imported from a different directory
# pylint: disable=import-error

# positional arguments are a good standard for commands
# pylint: disable=unused-argument

"""
[lib/lib/write.py]

Defines the "write" command.
"""

verbs = {}

def write(env, args, kwargs):
    """[LINE,...] {out:file}@Write all LINEs to file."""
    open(kwargs['out'], "w").write("\n".join(args))

verbs["write"] = write
