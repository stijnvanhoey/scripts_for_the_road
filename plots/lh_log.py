# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 11:01:32 2014

@author: stvhoey
"""

import random
import numpy as np

N = 10 #aantal samples
x1 = np.logspace(0.001, 10, N+1, endpoint=True)
samples = np.zeros(N)

#shuffle intervals
temp = [[x1[i], x1[i+1]] for i in range(10)]
random.shuffle(temp)

for i,interval in enumerate(temp):
    print interval[0], interval[1]
    samples[i] = np.random.uniform(interval[0], interval[1], 1)
    
    

