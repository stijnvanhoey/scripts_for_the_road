# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:22:55 2012

@author: VHOEYS
"""

import os
import glob

#USING WILDCARDS TO SELECT TYPES OF FILES
path = '/media/DATA/Githubs/bw10_courses'
for infile in glob.glob(os.path.join(path, '.access*')):
    print "current file is: " + infile
    #os.remove(infile)


for root, subFolders, files in os.walk(path):
    for ffile in files:
        if '.access^' in ffile:
            print root, ffile
            os.remove(os.path.join(root, ffile))

