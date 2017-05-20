#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[DOCS/gen_docs.py]

Automatic docs generation for Ergonomica, in Ergonomica.
"""

import ergonomica
from ergonomica.lib.util.util import expand_path
from ergonomica.lib.load_commands import verbs as _verbs

verbs = {}

def make_title(string):
    return string + "\n" + "-" * len(string) + "\n"

def gen_docs(argc):
    """gen_docs: Generate the Ergonomica defaults documentation.
    
    Usage:
       gen_docs TARGET
    """

    global _verbs

    target = expand_path(argc.env, argc.args['TARGET'])
    out = ""

    # load into reST format
    for command in _verbs:
        out += make_title(command)
        out += _verbs[command].__doc__ + "\n"
    
    # dump to file
    open(target, "w").write(out)

verbs['gen_docs'] = gen_docs
