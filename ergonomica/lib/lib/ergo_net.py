#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_net.py]

Defines the "net" command.
"""

import socket
import requests

def main(argc):
    """net: Various network information commands.
    Usage:
        net ip (local|global)
    """
    
    if argc.args['ip']:
        if argc.args['local']:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            yield s.getsockname()[0]
            s.close()
            
        elif argc.args['global']:
            import requests
            yield requests.get('http://ip.42.pl/raw').text
            

   # argc.env.aliases[argc.args['NAME']] = argc.ns[argc.args['FUNCTION']]
