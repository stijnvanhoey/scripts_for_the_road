#!/usr/bin/env python
"""
@author: Stijnvh
"""

# -*- coding: utf-8 -*-
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def TornadoComparePar(axs, parval1, parval2, parnames, plotfreq = True, 
                      plotminmax = True, plotinfotext = True,
                      *args,  **kwargs):
    '''
    Compare 2 parameter distributions in a Tornado-style plot
    
    Parameters
    -------------
    axs: axes.AxesSubplot object
        an subplot instance where the graph will be located,
        this supports the use of different subplots
    parval1: array
        values of the first parameter
    parval2: array
        values of the second parameter
    parnames: list of strings
        parameter names to show with graph
    plotfreq: bool, True|False
        frequency numbers plotted on top of the bins or not 
        (this is less relevant when using density plots)
    plotminmax: bool, True|False
        indicate the min and max values of the parameters
    plotinfotext: str
        if False, nothing is shown, else a text with info is puted on top
    *args, **kwargs:
        These argument are directed to the numpy.histogram() function
        eg. density, number of bins,...

    Returns
    --------        
    axes.AxesSubplot object
    
    Notes
    -------
    Plotting the frequencies on y-axis is not supported, since the lower graph 
    would get negative frequencies
    
    Examples
    ---------
    
    >>> nMC = 1000
    >>> parval1 = np.random.gamma(5.5,size=nMC)   
    >>> parval2 = np.random.gamma(8.0,size=nMC)   
    >>> parnames = ['par1','par2']
    >>> fig = plt.figure(figsize=(15,6))
    >>> axs = plt.subplot(111, axisbelow=True)    
    >>> axs = TornadoComparePar(axs,parval1,parval2,parnames,plotfreq =True,
                                plotminmax=True, 
                                plotinfotext = 'Posterior distributions',
                                bins=25,density=False)
        
    Contact for information: Stijn Van Hoey
    '''
    
    hist, bin_edges = np.histogram(parval1, *args, **kwargs)
    hist2, bin_edges2 = np.histogram(parval2, *args, **kwargs)

    parmin1 = parval1.min()
    parmax1 = parval1.max()
    parmin2 = parval2.min()
    parmax2 = parval2.max()

    bwidth = bin_edges[1]-bin_edges[0]
    axs.bar(bin_edges[:-1], hist, width=(bin_edges[1]-bin_edges[0])*0.95, 
            facecolor='0.3', edgecolor='white')
    
    if plotfreq == True:
        for i in range(hist.size):
            if hist[i] > 0.0:
                plt.text(bin_edges[i]+bwidth/2, hist[i]+0.025*hist2.max(),
                         "%.1f"%hist[i], color='0.3', size=8,
                         horizontalalignment='center',  
                         verticalalignment='bottom')
    
    bwidth2 = bin_edges2[1]-bin_edges2[0]
    axs.bar(bin_edges2[:-1], -hist2, width=(bin_edges2[1]-bin_edges2[0])*0.95, 
            facecolor='0.5', edgecolor='white')
    
    if plotfreq == True:
        for i in range(hist2.size):
            if hist2[i] > 0.0:
                plt.text(bin_edges2[i]+bwidth2/2, -hist2[i]-0.025*hist2.max(),
                         "%.1f"%hist2[i], color='0.5', size=8,
                         horizontalalignment='center',  
                         verticalalignment='top')
    
    if plotminmax == True:
        #Plot the place where the parameter minimum and maximum 
        #values are located
        plt.text(parmin1, hist.max()/2., 'min', color='0.3', size=12,
                         horizontalalignment='center',  
                         verticalalignment='bottom')
                         
        xspot, yspot = np.array([[parmin1, parmin1],  
                        [0.0, hist.max()*0.9/2.]])                         

        axs.add_line(mlines.Line2D(xspot, yspot, linestyle='--', 
                            linewidth=1., color='0.3'))                         
        
        plt.text(parmax1, hist.max()/2., 'max', color='0.3', size=12,
                         horizontalalignment='center',  
                         verticalalignment='bottom')
                    
        xspot, yspot = np.array([[parmax1, parmax1],  
                        [0.0, hist.max()*0.9/2.]])                         
        axs.add_line(mlines.Line2D(xspot, yspot, linestyle='--', 
                              linewidth=1. , color='0.3'))
                         
        plt.text(parmin2, -hist2.max()/2., 'min', color='0.5', size=12,
                         horizontalalignment='center',  
                         verticalalignment='top')
                         
        xspot, yspot = np.array([[parmin2, parmin2], 
                         [0.0, -hist2.max()*0.9/2.]])                         

        axs.add_line(mlines.Line2D(xspot, yspot, linestyle='--', 
                              linewidth=1. , color='0.5'))
                         
        plt.text(parmax2, -hist2.max()/2., 'max', color='0.5', size=12,
                         horizontalalignment='center',  
                         verticalalignment='top')

        xspot, yspot = np.array([[parmax2, parmax2], 
                        [0.0,-hist2.max()*0.9/2.]])                         

        axs.add_line(mlines.Line2D(xspot, yspot, linestyle='--', 
                            linewidth=1., color='0.5'))                        
    
    axs.set_ylim([-hist2.max(), +hist.max()])
    axs.set_xticks([])
    axs.set_yticks([+hist.max()/2., -hist2.max()/2.])
    axs.set_yticklabels([parnames[0], parnames[1]], size=20)
    labels = axs.get_yticklabels()
    labels[0].set_rotation(90)
    labels[0].set_color('0.3')
    labels[1].set_rotation(90)
    labels[1].set_color('0.5')
    
    axs.spines['top'].set_color('none')
#    axs.spines['left'].set_color('none')
    axs.spines['right'].set_color('none')
    axs.spines['bottom'].set_color('none')
    axs.yaxis.set_ticks_position('left')
    
    if plotinfotext:
        axs.text(bin_edges[-1]*0.7, hist.max(), plotinfotext, 
                 color='black', size=24,
                 horizontalalignment='left', 
                 verticalalignment='top')
                 
#        Change this to add extra text information
#        axs.text(bin_edges[-1]*0.7,hist.max()*0.8,
#                 "Comparison of two structures", color='.4', size=14,
#                 horizontalalignment='left', verticalalignment='top')

    return axs


# ----------
# Clean histogram for parameter posterior distirbution
#nMC=1000
#binss=30
#
#parval1 = np.random.gamma(5.5,size=nMC)   
#parval2 = np.random.gamma(8.0,size=nMC)   
#
## ----------
#parnames = ['par1','par2']
#txt="Posterior \n distributions"
#fig = plt.figure(figsize=(15,6), dpi=72,facecolor="white")
#axs = plt.subplot(111, axisbelow=True)    
#axs = TornadoComparePar(axs,parval1,parval2,parnames,plotfreq =True, 
#                        plotminmax=True, plotinfotext = txt,bins=25,
#                        density=False)
#

