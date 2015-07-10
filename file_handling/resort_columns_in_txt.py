# -*- coding: utf-8 -*-
"""
Created on Thu May 30 09:30:37 2013

@author: VHOEYS

Sort the row information and make comma-seperate.

This is a very case-specific solution, since the textfile contains some 
specialities. Pure regular expression solution would be better, but this
works fine and is easy-to read
"""

import re
import fileinput

#this definition was actually not needed
def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

inputfile='industrie.txt'
fnew=open('industrie_sort.txt','w')

for line in fileinput.input(inputfile):
    splitted = line.split()
    
    #Print first element    
    fnew.write(splitted[0])
    fnew.write(',')    
    
    #Print company name
    for j,elem in enumerate(splitted[1:splitted.index('BZV')]):
        fnew.write(elem)
        if j != (splitted.index('BZV')-2):
            fnew.write(' ')
        
    #Print BZV
    fnew.write(',') 
    fnew.write('BZV') 
    fnew.write(',')
    
    #print number BZV
    i1 = splitted[splitted.index('BZV')+1].index('kg')
    fnew.write(str(float(str(splitted[splitted.index('BZV')+1][:i1]).replace(",", "."))))
    fnew.write(',')
    #convert to number and make ,-> .
    
    fnew.write(splitted[splitted.index('BZV')+1][i1:])
    
    #Print Nt
    fnew.write(',') 
    fnew.write('Nt') 
    fnew.write(',')    
    
    #print number Nt
    i1 = splitted[splitted.index('Nt')+1].index('kg')
    fnew.write(str(float(str(splitted[splitted.index('Nt')+1][:i1]).replace(",", "."))))
    fnew.write(',')
    fnew.write(splitted[splitted.index('Nt')+1][i1:])    
    
    fnew.write('\n')  

fileinput.close()
fnew.close()

