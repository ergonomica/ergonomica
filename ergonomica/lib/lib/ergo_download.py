#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_read.py]

Defines the "read" command.
"""

from os.path import basename
import shutil
import requests


def main(argc):
    """
    download: Download a remote file.

    Usage:
       download URL
    """
    
    url = argc.args['URL']
    response = requests.get(url, stream=True)
    with open(basename(url), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    return []
