# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 11:19:13 2014

@author: stvhoey
"""

# -*- coding: u1,tf-8 -*-
"""
Created on Tue Aug 19 11:15:13 2014

@author: stvhoey
"""

import numpy as np

import matplotlib as mpl
mpl.rcParams['mathtext.default'] = 'regular'
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import LinearLocator

import pandas as pd
from pandas.tseries.offsets import DateOffset, Day, Week, Hour, Minute

#use alternative color-cycle (choose!)
import brewer2mpl
set1 = brewer2mpl.get_map('Paired', 'Qualitative', 8).mpl_colors
set2 = brewer2mpl.get_map('YlGnBu', 'Sequential', 8, reverse = True).mpl_colors
mpl.rcParams['axes.color_cycle'] = set1

#sets to use in plotting:
setblue = brewer2mpl.get_map('Blues', 'Sequential', 6, 
                             reverse = True).mpl_colors
setred = brewer2mpl.get_map('Reds', 'Sequential', 6, 
                             reverse = True).mpl_colors
setorange = brewer2mpl.get_map('Oranges', 'Sequential', 6, 
                             reverse = True).mpl_colors
                             

x = np.arange(1,10,0.1)

def sinusen(xdata, par):
    return sin(x)+ par

plt.figure()
for i,par in enumerate([1,2,3,4,5,6]):
    plt.plot(x, sinusen(x, par), linewidth = 2, color = setred[i])