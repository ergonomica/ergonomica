#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

"""
[lib/lib/clear.py]

Defines the "clear" command.
"""

from prompt_toolkit.shortcuts import clear as raw_clear

def clear():
    """Clears the screen."""

    raw_clear()


exports = {'clear': clear}


