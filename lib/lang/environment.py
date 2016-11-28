#!/usr/bin/python

import os

class environment:
    def __init__(self):
        self.run = True
        self.directory = os.getcwd()
        self.user = os.getenv("USER")
        self.home = os.getenv(key="HOME")
        self.verbs = {}
        self.namespace = {}

ENV = environment()
