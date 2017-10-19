#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

class Filesystem(object):
    def __init__(self):
        pass

    def create_file(self, path, contents):
        with open(path, 'wb') as f:
            f.write(contents)


    def directory_create(self, path):
        os.mkdir(path)

    def directory_remove(self, path):


    def file_remove(self, path):

    
            
    def read_file(self, path):
        return open(path, 'rb').read()


    
    def remove_file(self, path):
        
