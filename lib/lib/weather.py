#!/usr/bin/python
# -*- coding: utf-8 -*-

# pylint's name standards are insane
# pylint: disable=invalid-name

"""
[lib/lib/weather.py]

Defines the "weather" command.
"""

from lib.util.util import run_command

verbs = {}

def weather(env, args, kwargs):
    """[CITYNAME,...]@Return the weather for all cities specified."""
    return [run_command("curl -s wttr.in/%s" % (x.strip().lower())) for x in args]

verbs["weather"] = weather
