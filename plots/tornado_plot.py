#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Stijnvh
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from matplotlib.ticker import MaxNLocator

def TornadoSensPlot(parnames,parvals,gridbins=4,midwidth=0.5,
                    setequal=False,plotnumb=True,parfontsize=12,
                    bandwidth=0.75):
    '''
    Plot to show sensitivity analysis results of a global sensitivity analysis,
    data is sorted by the algorithm

    Dependencies= numpy, matplotlib

    Parameters
    ------------
    parnames: list
        list of strings with the different parameter names in
    parvals: array
        arra with the sensitivity outputs
    gridbins: int
        maximum number of gridlines on the axis ticks (default 4)
    midwidth: float
        define width between the two subplots to adjust to parname-length
    setequal: True | False
        Set positive and negative value ax equal (True) of not (False)
    plotnumb: True | False
        Plot the sensitivity values at the end of the bars
    parfontsize: integer
        default=12, but with latex symbols, larger values is appropriate
    bandwidth: float
        default=0.75, defines the width of the bars, range [0.0,1.0]

    Returns
    --------
    Tornado plot fig

    Examples
    ---------

    >>> rtndval = 100 #between -100 en 100
    >>> parnames = ['par1','par2','par3','par4','par5','par6','par7','par8','par9','par10']
    >>> parvals = (rtndval+rtndval) * np.random.random_sample(10) - rtndval
    >>> TornadoSensPlot(parnames,parvals,gridbins=5,midwidth=0.4,
                        setequal=True,plotnumb=True,parfontsize=12,bandwidth=0.4)

    Notes
    --------
    To achieve a 2-line parameter values use a slash-n in the parameter names

    Contact for information: Stijn Van Hoey
    '''

    pars=parnames
    #sort the data and pars-list
    ids = np.argsort(np.abs(parvals))
    parssort = [pars[i] for i in ids]
    parvalssort = parvals[ids]

    #differentiate positive and negative effects
    posval=np.where(parvalssort >= 0, parvalssort, 0)
    negval=np.where(parvalssort < 0, parvalssort, 0)

    #use white backgrounds and lines
    matplotlib.rc('axes', facecolor = 'white')
#    matplotlib.rc('figure.subplot', wspace=.65)
    matplotlib.rc('grid', color='white')
    matplotlib.rc('grid', linewidth=1.5)

    # Make figure background the same colors as axes
    fig = plt.figure(figsize=(8,6), facecolor='white')

    # --- Negative effects --- left
    axleft  = fig.add_subplot(121)

    # Keep only top and right spines
    axleft.spines['left'].set_color('none')
    axleft.spines['bottom'].set_color('none')
    axleft.xaxis.set_ticks_position('top')
    axleft.yaxis.set_ticks_position('right')
    axleft.spines['top'].set_position(('data',len(pars)-bandwidth))
    axleft.spines['top'].set_color('w')

    # Set axes limits
    if setequal==True:
        axleft.set_xlim(-max(posval.max(),np.abs(negval).max()),0)
    else:
        axleft.set_xlim(negval.min(),0)
    axleft.set_ylim(0,len(pars))
    #Labels
    majorLocator= MaxNLocator(nbins=gridbins)
    axleft.xaxis.set_major_locator(majorLocator)
    axleft.get_xticklines()[-1].set_markeredgewidth(0)
    for label in axleft.get_xticklabels():
        label.set_fontsize(10)
    axleft.set_yticks([])

    # Plot data
    for i in range(len(pars)):
        # positive data
        value = negval[i]
        p = patches.Rectangle(
            (0, i+(1.-bandwidth)/2.), value, bandwidth, fill=True, transform=axleft.transData,
            lw=0, facecolor='grey', alpha=0.8)

        #plot numbers as text on end of bars
        if plotnumb==True:
            if value < 0.0:
                axleft.text(value+0.15*negval.min(),i+bandwidth/2.+(1.-bandwidth)/2., str(np.round(value,decimals=2)),
                            family='Helvetica Neue', size=10, color='0.',
                            horizontalalignment="center", verticalalignment="center")
        axleft.add_patch(p)
    # Add a grid
    axleft.grid()

    # --- Positive effects ---
    axright = fig.add_subplot(122, sharey=axleft)
    fig.subplots_adjust(wspace=midwidth)
    # Keep only top and left spines
    axright.spines['right'].set_color('none')
    axright.spines['bottom'].set_color('none')
    axright.xaxis.set_ticks_position('top')
    axright.yaxis.set_ticks_position('left')
    axright.spines['top'].set_position(('data',len(pars)-bandwidth))
    axright.spines['top'].set_color('w')
    # Set axes limits
    if setequal==True:
        axright.set_xlim(0,max(posval.max(),np.abs(negval).max()))
    else:
        axright.set_xlim(0,posval.max())
    axright.set_ylim(0,len(pars))
    #Labels
    majorLocator2= MaxNLocator(nbins=gridbins)
    axright.xaxis.set_major_locator(majorLocator2)
    for label in axright.get_xticklabels():
        label.set_fontsize(10)
    axright.get_xticklines()[1].set_markeredgewidth(0)

    axright.set_yticks(np.arange(0,11,1))
    axright.set_yticklabels([],visible=False)
    # Plot data
    for i in range(len(pars)):
        # Negative data
        value = posval[i]
        p = patches.Rectangle(
            (0, i+(1.-bandwidth)/2.), value, bandwidth, fill=True, transform=axright.transData,
            lw=0, facecolor='grey', alpha=0.8)
        axright.add_patch(p)

        #plot numbers as text on end of bars
        if plotnumb==True:
            if value > 0.0:
                axright.text(value+0.1*posval.max(),i+bandwidth/2.+(1.-bandwidth)/2., str(np.round(value,decimals=2)),
                            family='Helvetica Neue', size=10, color='0.',
                            horizontalalignment="center", verticalalignment="center")
    # Add a grid
    axright.grid()

    # Y axis labels
    # We want them to be exactly in the middle of the two y spines
    for i in range(len(pars)):
        x1,y1 = axleft.transData.transform_point((0,i+.5))
        x2,y2 = axright.transData.transform_point((0,i+.5))
        x,y = fig.transFigure.inverted().transform_point(((x1+x2)/2,y1) )
        plt.text(x, y, parssort[i], transform=fig.transFigure, size=parfontsize,
                 horizontalalignment='center', verticalalignment='center')
    return fig



# ----------
# Data to be represented as output of the sensitivity analysis
rtndval=70
#parnames = [r'$\alpha$',r'$\beta$',r'$k_s$',r'$k$',r'$\rho$','K',r'$k_o$',r'$k_i$',r'$k_b$',r'$b_e$']
parnames = ['par1','par2','par3','par4','par5','par6','par7','par8','par9','par10']
parvals = (rtndval+rtndval) * np.random.random_sample(10) - rtndval   #tussen -3 en 3
TornadoSensPlot(parnames,parvals,gridbins=5,midwidth=0.4,setequal=True,plotnumb=True,parfontsize=12,bandwidth=0.4)
