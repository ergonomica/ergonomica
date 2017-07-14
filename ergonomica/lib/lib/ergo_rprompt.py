#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/rprompt.py]

Defines the "rprompt" command.
"""


def main(argc):
    """
       rprompt: Set the text for the Ergonomica rprompt (next next to prompt).

       Usage:
          rprompt STRING

    """
    
    argc.env.rprompt = argc.args['STRING']
