# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:22:55 2012

@author: VHOEYS
"""

import os
import glob
 
#ALL FILES
path = 'D:\Download\My Dropbox\StijnKatrijn\Figuren parset 1'
listing = os.listdir(path)
for infile in listing:
    print "current file is: " + infile
 

#USING WILDCARDS TO SELECT TYPES OF FILES
path = 'sequences/'
for infile in glob.glob(os.path.join(path, '*.fasta')):
    print "current file is: " + infile    