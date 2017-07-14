#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[lib/lib/ergo_net.py]

Defines the "net" command.
"""

import socket
import requests
import netifaces

def main(argc):
    """net: Various network information commands.
    Usage:
        net ip (local|global)
        net mac INTERFACE
        net interfaces
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

    elif argc.args['mac']:
        yield netifaces.ifaddresses(argc.args['INTERFACE'])[netifaces.AF_LINK][0]['addr']
        
    elif argc.args['interfaces']:
        yield netifaces.interfaces()

   # argc.env.aliases[argc.args['NAME']] = argc.ns[argc.args['FUNCTION']]
