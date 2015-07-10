# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 18:21:27 2014

@author: stvhoey

Original idea: http://square.github.io/cubism/
adapted python code: http://nbviewer.ipython.org/gist/phobson/5045887
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, MaxNLocator
 
def _make_patch_spines_invisible(ax):
    """make spines invisible of current ax
    """
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False) 
 
def _dframe_folds(dframe, height, nfolds=3):
    """
    extend a pd.DataFrame with extra columns for each folding part to plot,
    splitting the original series based on the given amount of folds.
    """  
    for i in range(1, nfolds + 1):
        dframe["fold"+str(i)] = dframe.iloc[:, i-1] - height
    #positive values are full height => change them to height
    dframe[dframe.iloc[:, 1:] > 0] = height
    #negative values more negative than  height => zeros
    dframe[dframe.iloc[:, 1:] < - height] = 0.0
    #still negative values are now (height - value)
    dframe[dframe.iloc[:, 1:] < 0.0] = height - \
                        np.abs(dframe[dframe.iloc[:, 1:] < 0.0])
    return dframe
        
def _get_alpha(nfolds, minalpha = 0.3):
    """int -> float
    """
    return max(1.0/nfolds, minalpha)
        
def singleax(ax, variable, height=None, nfolds=3, color = "grey"):   
    """
    """
    variable = pd.DataFrame(variable)
    
    alpha = _get_alpha(nfolds)
    if not height:
        #hier berekenen
        height = np.abs(variable.iloc[:, 0]).max()/nfolds

    variable_ext = _dframe_folds(variable, 
                                 height, nfolds=nfolds)
    for i in range(1, nfolds + 1):
        try:
            x = variable_ext.index.to_datetime()
        except:
            x = variable_ext.index            
        y = variable["fold" + str(i)].values
        
        ax.fill_between(x, 0, y, color=color, alpha=alpha)
        
        ax.set_xlim([x.min(), x.max()])
        ax.set_ylim([0, height])
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)    
    
    return ax  
   
def horizon_plot(dframe, nfolds=3, common_height=True, color="grey"):
    """
    Plotting timeseries is often resulting in bad distinction in the lower 
    values and only distinguishing the high peaks. Folding the dataseries puts 
    the peaks as more dark regions in a more common range on the y-axis.
    As such, clarity in the patterns is given for the entire timeserie.    
       
    Parameters
    -----------
    dframe ; pd.DataFrame
        dataFrame with the set of variables plotted as rows. The index is 
        used as x-axis values.
    nfolds : int
        number of folding the dataseries
    common_height : boolean
        if True, all rows (variables) have the same relative height (based on 
        the max value of all variables); if False, every variable is treated
        independently
    
    Notes
    ------
    Original idea: http://square.github.io/cubism/
    
    Reference
    ----------
    http://vis.berkeley.edu/papers/horizon/
    """
    nvar = len(dframe.columns)
    
    #bereken gemeenschappelijk hoogte
    if common_height:
        allheight = np.abs(dframe.max(axis=1)).max()/nfolds
        print "Common height is", allheight 
    else:
        allheight = None
    alpha = _get_alpha(nfolds)    

    #MAKE FIG
    fig, axs = plt.subplots(nvar, 1, figsize=(16, 6), facecolor='white')
    fig.subplots_adjust(hspace=0)
    
    isleft = True
    for i, var in enumerate(dframe.columns):
        print i, var
        singleax(axs[i], dframe[var], height=allheight, 
                 nfolds=nfolds, color=color)

        #clean up figure
        axs[i].spines['right'].set_visible(False)   
        axs[i].spines['left'].set_visible(False) 
        axs[i].set_xlabel('')   
        axs[i].tick_params(axis='x', pad=5, direction='out')
        
        if isleft:
            isleft = False
            axs[i].spines['left'].set_visible(False)
            axs[i].yaxis.set_major_locator(MaxNLocator(3))

            #extra axis info about max when value higher than height
            if dframe[var].max() > allheight:
                fake_ax = axs[i].twinx()       
                fake_ax.spines["right"].set_position(('outward', 40))
                _make_patch_spines_invisible(fake_ax)     
                
                fake_ax.set_ylim(0, dframe[var].max())
                fake_ax.yaxis.set_major_locator(LinearLocator(2))
                
                #color darkgrey
                [tt.set_color(color) for tt in fake_ax.get_yticklabels()]
                [tt.set_alpha(min(0.95,alpha*nfolds)) for tt in fake_ax.get_yticklabels()]                 
            
            axs[i].yaxis.tick_right()  
            #color lightgrey
            [tt.set_color(color) for tt in axs[i].get_yticklabels()]
            [tt.set_alpha(alpha*2) for tt in axs[i].get_yticklabels()]
            
        else:
            isleft = True
            axs[i].spines['right'].set_visible(False)
            axs[i].yaxis.set_major_locator(MaxNLocator(3))

            #extra axis info about max when value higher than 
            if dframe[var].max() > allheight:
                fake_ax = axs[i].twinx() 
                fake_ax.spines['left'].set_position(('outward', 40))
                _make_patch_spines_invisible(fake_ax) 
                
                fake_ax.yaxis.set_ticks_position('left')
                fake_ax.yaxis.set_label_position('left')
    
                fake_ax.set_ylim(0, dframe[var].max())
                fake_ax.yaxis.set_major_locator(LinearLocator(2))  
                
                #color darkgrey
                [tt.set_color(color) for tt in fake_ax.get_yticklabels()]
                [tt.set_alpha(min(0.95,alpha*nfolds)) for tt in fake_ax.get_yticklabels()] 
            
            axs[i].yaxis.tick_left()
            #color lightgrey
            [tt.set_color(color) for tt in axs[i].get_yticklabels()]
            [tt.set_alpha(alpha*2) for tt in axs[i].get_yticklabels()]
        
        #xlabels in the last plot, hiding in the others
        if not axs[i].is_last_row():
            plt.setp(axs[i].get_xminorticklabels(), visible=False)
            plt.setp(axs[i].get_xmajorticklabels(), visible=False)
                
        #info about the variables
        axs[i].text(0.01, 0.9, var, transform=axs[i].transAxes, 
                    fontsize=14,verticalalignment='top')
        
    

    return fig, axs
       

#real data
flowdata = load("FlowData")
raindata = load("RainData")
raindata = raindata.drop(['P05_038', 'P06_040'], axis=1)

#EXAMPLE FLOW
#fig, ax = horizon_plot(flowdata[["L06_347", "LS06_348", "LS06_34D", 
#                                 "LS06_34E"]]["02/2010":"15/01/2011"], 
#                       nfolds = 6, common_height = True, color = "#252525")

#EXAMPLE RAIN
fig, ax = horizon_plot(raindata["09/2010":"15/01/2011"], 
                       nfolds = 4, common_height = True, 
                       color = "#252525") #grey: 

#EXAMPLE DUMMY

#dates = pd.date_range(start="01/01/2010", end="31/12/2010", freq='D')
#dummydata = pd.DataFrame(np.reshape(np.random.uniform(0, 80, len(dates)*6), (len(dates), 6)), index=dates)

#fig, ax = horizon_plot(dummydata, 
#                       nfolds = 3, common_height = True, color = "#252525") #grey: 







"""
#TODO:
(1/) Oplosing voor Y-as indeling: gewoon aanduiden gaat niet, want x aantal keer,
mss ook zo telkens een as naast plaatsen; of bepaalde highlights aangeven;
op browser interactief te doen...
=> de huidige idee, gewoon de eerste hoogte ernaast + extra lijn met hoogste schaal => SOLVED

(3/) Vergelijkbaarheid tussen de plots: Onderlinge schaalverhouding ook weergeven
in de plot! (klein schaal lijkt nu eigenlijk meer te zijn...). Maw, vergelijkbaar maken 
met de grootste  => SOLVED 

TODO: COLORBAR
        #add colourscale
        # Add colorbar, make sure to specify tick locations to match desired ticklabels
        
#    cbar = fig.colorbar(axs[0], ticks=[dframe.min(axis=1).min(),dframe.max(axis=1).max()])
#    cbar.ax.set_yticklabels(['min', 'max'])

#    sm = plt.cm.ScalarMappable(cmap="Greys", 
#                               norm=plt.normalize(vmin=dframe.min(axis=1).min(), 
#                                                  vmax=dframe.max(axis=1).max()),)
#    # fake up the array of the scalar mappable. Urgh...
#    sm._A = []
#    fig.colorbar(sm)        
#   
#    from matplotlib import colors
#    my_cmap = colors.ListedColormap([color]*nfolds)
#    # this is a hack to get at the _lut array, which stores RGBA vals
#    my_cmap._init()    
#    # use some made-up alphas, you would use the ones specified by f
#    temp = [alpha]*nfolds
#    alphas = [aa+aa*i/2 for i, aa in enumerate(temp)]
#    print alphas, alpha, temp
#    # overwrite the alpha channel of the jet colour map
#    my_cmap._lut[:-3,-1] = alphas
#
#    cax,kw = mpl.colorbar.make_axes([ax for ax in axs.flat])
#    #cmap = plt.cm.get_cmap('Greys', 3)
#    cmap = my_cmap
#    sm = plt.cm.ScalarMappable(cmap=cmap, 
#                               norm=plt.normalize(vmin=dframe.min(axis=1).min(), 
#                                                  vmax=dframe.max(axis=1).max()))
#                                                     
#    sm._A = []
#    fig.colorbar(sm, cax=cax, **kw)

#    # Create a fake colorbar
#    from matplotlib.colors import LinearSegmentedColormap
#    customcmap = [(x/24.0,  x/48.0, 0.05) for x in range(nfolds)]
#    ctb = LinearSegmentedColormap.from_list('custombar', customcmap, N=2048)
#    # Trick from http://stackoverflow.com/questions/8342549/
#    # matplotlib-add-colorbar-to-a-sequence-of-line-plots
#    sm = plt.cm.ScalarMappable(cmap=ctb, norm=plt.normalize(vmin=dframe.min(axis=1).min(), 
#                                                  vmax=dframe.max(axis=1).max()))
#    # Fake up the array of the scalar mappable
#    sm._A = []
#     
#    # Set colorbar, aspect ratio
#    cbar,kw = mpl.colorbar.make_axes([ax for ax in axs.flat])
#    cbar.solids.set_edgecolor("face")
#    # Remove colorbar container frame
#    cbar.outline.set_visible(False)
#    # Fontsize for colorbar ticklabels
#    cbar.ax.tick_params(labelsize=16)
#    # Customize colorbar tick labels
#    mytks = np.arange(round(dframe.min(axis=1).min()),round(dframe.max(axis=1).max()),int(nfolds))
#    cbar.set_ticks(mytks)
#    cbar.ax.set_yticklabels([str(a) for a in mytks], alpha=a)
#     
#    # Remove color bar tick lines, while keeping the tick labels
#    cbarytks = plt.getp(cbar.ax.axes, 'yticklines')
#    plt.setp(cbarytks, visible=False)

"""






##normal plot
#fig, ax = plt.subplots()
#pos = np.ma.masked_less(yy, 0)
#neg = np.ma.masked_greater(yy, 0)
#ax.fill_between(xx, neg, y2=0, color='CornflowerBlue', alpha=0.5)
#ax.fill_between(xx, pos, y2=0, color='DarkGreen', alpha=0.5)
#ax.xaxis.grid(False)
#ax.yaxis.grid(False)
#
#ax.set_xlim([xx.min(), xx.max()])
#ax.set_ylim([neg.min(), pos.max()])
#ax.set_yticks([])




    
    