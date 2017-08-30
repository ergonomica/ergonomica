#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/rprompt.py]

Defines the "rprompt" command.
"""


def rprompt(argc):
    """
       rprompt: Set the text for the Ergonomica rprompt (next next to prompt).

       Usage:
          rprompt STRING

    """

    argc.env.rprompt = argc.args['STRING']


exports = {'rprompt': rprompt}


