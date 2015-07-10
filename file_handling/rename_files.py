# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:22:55 2012

@author: VHOEYS
"""

import os
import sys
import glob


def replace_in_name(path, name, replacement):
    """
    Rename the files in the folder by replacing a specific text
    """
    listing = os.listdir(path)
    for infile in listing:
        if name in infile:
            print "current file is: " + infile
            print "renamed file is: " + infile.replace(name, replacement)
            os.rename(infile, infile.replace(name, replacement))



if __name__ == "__main__":
    replace_in_name(sys.argv[1], sys.argv[2], sys.argv[3])