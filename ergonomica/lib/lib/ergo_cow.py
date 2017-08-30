#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/cow.py]

Defines the "cow" command.
"""


def cow(argc):
    """cow: Make a cow say STRING.

    Usage:
        cow STRING
    """

    string = argc.args['STRING']
    out = " " + "_" * (len(string) + 2) + "\n"
    out += "< %s >\n" % string
    out += " " + "-" * (len(string) + 2)
    out += """
    \\    ^__^
     \\   (oo)\\_______
         (__)\\        )\\/\\
              ||----w |
              ||     ||"""
    return out

exports = {'cow': cow}


