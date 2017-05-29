#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/cow.py]

Defines the "cow" command.
"""


def main(argc):
    """cow: Make a cow say STRING.

    Usage:
        cow STRING
    """

    string = args[0]
    s = " " + "_" * (len(string) + 2) + "\n"
    s += "< %s >\n" % string
    s += " " + "-" * (len(string) + 2)
    s += """
    \\   ^__^
     \\  (oo)\\_______
         (__)\\        )\\/\\
              ||----w |
              ||     ||"""
    return s
