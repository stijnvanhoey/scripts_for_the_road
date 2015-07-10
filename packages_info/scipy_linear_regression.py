# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 18:11:52 2012

@author: VHOEYS

Example of linear regression in python
show some interesting properties of python
"""

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

def LinRegress(x,y, percentile=0.1, plotit=True, saveit=False):
    '''
    Perform linear regression on input data and plot the data, fitted curve and chosen percentile
    '''
    b, a, r, p, e = st.linregress(x, y)

    eps = y - a - b*x # error of fitting and measured data
    x1 = np.linspace(x.min(), x.max()) # x axis to plot the Prediction Interval
    # variace of fitting error
    e_pi = np.var(eps)*(1+1.0/n + (x1-x.mean())**2/np.sum((x-x.mean())**2))
    # z value using the t distribution and with dof = n-2
    z = st.t.ppf(0.95, n-2)
    # prediction interval
    pi = np.sqrt(e_pi)*z
    zl = st.t.ppf(0.10, n-2) # z at 0.1
    zu = st.t.ppf(0.90, n-2) # z at 0.9
    ll = a + b*x1 + np.sqrt(e_pi)*zl # 10 %
    ul = a + b*x1 + np.sqrt(e_pi)*zu # 90 %
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(x,y,'ro', label='measured')
    ax.plot(x,a+b*x,label='fitted')
    ax.plot(x1,ll,'--', label='10%')
    ax.plot(x1,ul,'--', label='90%')
    ax.xlabel('x')
    ax.ylabel('y')
    ax.legend(loc='best')
    ax.grid()
    
    return fig




'''
Linear Regression and prediction interval
'''

# generate the data
n = 100 # length of the data
x = np.random.rand(n)  #random error on data
y = 3 + 7*x + np.random.randn(n)

# perform linear regression
b, a, r, p, e = st.linregress(x, y)

eps = y - a - b*x # error of fitting and measured data
x1 = np.linspace(x.min(), x.max()) # x axis to plot the Prediction Interval
# variace of fitting error
e_pi = np.var(eps)*(1+1.0/n + (x1-x.mean())**2/np.sum((x-x.mean())**2))
# z value using the t distribution and with dof = n-2
z = st.t.ppf(0.95, n-2)
# prediction interval
pi = np.sqrt(e_pi)*z
zl = st.t.ppf(0.10, n-2) # z at 0.1
zu = st.t.ppf(0.90, n-2) # z at 0.9
ll = a + b*x1 + np.sqrt(e_pi)*zl # 10 %
ul = a + b*x1 + np.sqrt(e_pi)*zu # 90 %

#plot
plt.plot(x,y,'ro', label='measured')
plt.plot(x,a+b*x,label='fitted')
plt.plot(x1,ll,'--', label='10%')
plt.plot(x1,ul,'--', label='90%')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc='best')
plt.grid()
#plt.savefig('lin_regress.png')
plt.show()

