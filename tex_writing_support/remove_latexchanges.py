# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 16:44:48 2014

@author: stvhoey

Additional poser to the changes-package in latex, to remove all \added, 
\replaced and \deleted in the .tex-file to make new revision
"""

import re

texfile = open("testfile.tex", "r")
newtexfile = open("adaptedfile.tex", "w")

for line in texfile.readlines():
    p = re.compile('\\\\replaced{ ( [^}]* ) }{ ( [^}]* ) }', re.VERBOSE)
    line = p.sub(r'\1',line)
    
    q = re.compile('\\\\added{ ( [^}]* ) }', re.VERBOSE)
    line = q.sub(r'\1', line)

    r = re.compile('\\\\deleted{ ( [^}]* ) }', re.VERBOSE)
    line = r.sub(r'', line)
    newtexfile.write(line)
texfile.close()
newtexfile.close()