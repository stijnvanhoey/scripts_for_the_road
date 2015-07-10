# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 16:32:51 2012

@author: VHOEYS
"""

#f=open('D:\Modellen\Version2012\HPC\Article_HESS_Nete_2\Model_runs\joblist','r')

import fileinput

fnew=open('D:\Modellen\Version2012\HPC\Article_HESS_Nete_2\Model_runs\jobremake.sh','w')

for line in fileinput.input('D:\Modellen\Version2012\HPC\Article_HESS_Nete_2\Model_runs\joblist'):
    if not 'Job' in line:
        fnew.write('qalter -l walltime=03:00:00 ')
        fnew.write(line[:5])
#        fnew.write(' ')
        fnew.write('\n')
   

fileinput.close()
fnew.close()