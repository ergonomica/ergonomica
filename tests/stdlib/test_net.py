#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
[tests/stdlib/test_net.py]

Tests the net command.
"""

import os
import unittest
import socket
import requests
import netifaces

from ergonomica import ergo

class TestNet(unittest.TestCase):
    """Tests the net command."""

    def test_net_localip(self):
        """
        Tests the net command getting the local IP.
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.assertEqual(ergo("net ip local"), s.getsockname()[0])
        s.close()

    def test_net_globalip(self):
        """
        Tests the net command getting the global IP.
        """

        self.assertEqual(ergo("net ip global"),
                              requests.get("http://ip.42.pl/raw").text)

    def test_interfaces(self):
        """
        Test the net command getting a list of all network interfaces.
        """

        self.assertEqual(ergo("net interfaces"), netifaces.interfaces())
 
        
    def test_net_mac(self):
        """
        Tests the net command getting the MAC address.
        """

        for interface in netifaces.interfaces():
            self.assertEqual(ergo("net mac {}".format(interface)),
                             netifaces.ifaddresses(interface)\
                             [netifaces.AF_LINK][0]['addr'])
