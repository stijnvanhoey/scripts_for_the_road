#
# Idea and initial implementation by Max C. Watson,
# https://github.com/maxcw/time-maps
# see also:
# https://districtdatalabs.silvrback.com/time-maps-visualizing-discrete-events-across-many-timescales
#
# The original of Max Watson is here reimplemented
#
# created by S. Van Hoey
#

import datetime
import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import matplotlib.pylab as plt

import requests

def _get_prepost_values(timeserie):
    """
    """
    return pre, post


def intervals(times):
    """
    given an array of timestamps,
    returns an array of separation times between the timestamps
    """
    shifted_times= times[:-1]
    shifted_times = np.insert(shifted_times,0,0) ## add zero to beginning to array
    seps= times - shifted_times
    seps=seps[1:] # remove dummy first element

    return seps

def build_time_map(timeserie):
    """

    Parameters
    -----------
    timeserie : pd.Series

    """
    xcoords, ycoords = _get_prepost_values(timeserie)

    plt.subplot(121) # first, a plot of the points themselves

    plt.plot(xcoords,ycoords,'b.')

    plt.xlim((0,1))
    plt.ylim((0,1))

    plt.subplot(122) # let's make a heatmap

    Nside=1024 # this is the number of bins along x and y.

    H = np.zeros((Nside,Nside)) # the 'histogram' matrix that counts the number of points in each grid-square

    x_heat = (Nside-1)*xcoords # the xy coordinates scaled to the size of the matrix
    y_heat = (Nside-1)*ycoords # subtract 1 since Python starts counting at 0, unlike Fortran and R

    for i in range(len(xcoords)): # loop over all points to calculate the population of each bin

    	H[int(x_heat[i]), int(y_heat[i])] = H[int(x_heat[i]), int(y_heat[i])] + 1 # int() outputs an integer.

    	# in Python, the above line can actually be accomplished more compactly:
    	# H[x_heat[i], y_heat[i]]  +=1

    H = ndi.gaussian_filter(H,8) # here, 8 specifies the width of the Gaussian kernel in the x and y directions
    H = np.transpose(H) # so that the orientation is the same as the scatter plot
    # to bring out the individual points more, you can do: H=np.sqrt(H)
    plt.imshow(H, origin='lower')

    plt.show()


rain = pd.read_csv("rain_data_sample.txt")




