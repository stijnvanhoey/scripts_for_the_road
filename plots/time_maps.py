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
import matplotlib.pylab as plt
import seaborn as sns
sns.set(style="ticks")

def _intervals(date_array):
    """
    Parameters
    -----------
    date_array : ndarray
        array of python datetime objects

    Returns
    --------
    ndarray
        datetime.timedelta() objects
    """
    return np.diff(date_array)

def _provide_prepost(df, time_unit):
    """
    Based on a pandas DataFrame with in the index the timestamps and
    in the columns the data, two colomns are added, called date_pre and
    date_post with datetime.timedelta values

    Parameters
    ------------
    df : dframe
        pandas dataframe
    time_unit : str (sec, min, hour or day)
        unit to express the time gap
    """
    diffs = _intervals(df.index.to_pydatetime())

    if time_unit == 'sec':
        diffs = [gap.total_seconds() for gap in diffs]
    elif time_unit == 'min':
        diffs = [gap.total_seconds()/60. for gap in diffs]
    elif time_unit == 'hour':
        diffs = [gap.total_seconds()/60./60. for gap in diffs]
    elif time_unit == 'day':
        diffs = [gap.total_seconds()/60./60./24. for gap in diffs]
    elif time_unit == 'month':
        diffs = [gap.total_seconds()/60./60./24./30. for gap in diffs]
    else:
        raise Exception("Only sec, min, hour and day supported!")

    df[''.join(['Time before (',time_unit,')'])] = \
                                    np.concatenate((np.array([np.nan]), diffs))
    df[''.join(['Time after (',time_unit,')'])] = \
                                    np.concatenate((diffs, np.array([np.nan])))

def time_map_density(df, time_unit='sec', *args, **kwargs):
    """time maps creation of a time series dataframe

    As proposed by Max Watson in his paper to improve the plotting of dicrete
    event time series, this fucntion implements the visualisation based on a
    pandas dataframe containing the dates in the index.

    Discrete event can be used to count number of occurences of any event.

    In contrast to the original proposed implementation by Max Watson,
    the provided functions of pandas and seaborn are exploited here.

    The density is shown as a hexbin

    Parameters
    -----------
    timeserie : pd.DataFrame of Series
        The dataset with in the index the datetime information
    time_unit : str (sec, min, hour or day)
        unit to express the time gap in the plot
    *args, **kwargs :
        passed to matplotlib hexbin function

    Notes
    ------
    https://github.com/maxcw/time-maps

    See Also
    ---------
    time_map_varcolor
    """
    _provide_prepost(df, time_unit)

    # Set time_unit
    x = ''.join(['Time before (', time_unit, ')'])
    y = ''.join(['Time after (', time_unit, ')'])

    fig, axs = plt.subplots()
    clab = axs.hexbin(df[x].values,df[y].values, *args, **kwargs)
    fig.colorbar(clab)
    axs.set_xlabel(''.join(('Time before (', time_unit, ')')))
    axs.set_ylabel(''.join(('Time after (', time_unit, ')')))
    #cbar = plt.colorbar()
    #cbar.ax.set_ylabel('Counts')
    #axs = sns.jointplot(x, y, data=df,
    #              kind='hex', stat_func=None)
    return axs

def time_map_varcolor(df, variable,  time_unit='sec', *args, **kwargs):
    """time maps creation of a time series dataframe

    As proposed by Max Watson in his paper to improve the plotting of dicrete
    event time series, this fucntion implements the visualisation based on a
    pandas dataframe containing the dates in the index.

    Discrete event can be used to count number of occurences of any event.

    In contrast to the original proposed implementation by Max Watson,
    the provided functions of pandas and seaborn are exploited here.

    As opposed to the density implementation, the coloring is according to an
    extra variable, listed in the dframe

    Parameters
    -----------
    timeserie : pd.DataFrame of Series
        The dataset with in the index the datetime information
    variable : str
        variable part of the data columns
    time_unit : str (sec, min, hour or day)
        unit to express the time gap in the plot
    *args, **kwargs :
        passed to matplotlib scatter plot

    Notes
    ------
    https://github.com/maxcw/time-maps

    See Also
    ---------
    time_map_density
    """
    if not variable in df.columns:
        raise Exception("variable not part of the dframe")

    _provide_prepost(df, time_unit)

    # Set time_unit
    x = ''.join(['Time before (', time_unit, ')'])
    y = ''.join(['Time after (', time_unit, ')'])

    fig, axs = plt.subplots()
    axs.scatter(df[x], df[y], c=df[variable], *args, **kwargs)

    return axs


if __name__ == '__main__':

#    #rain = pd.read_csv("rain_data_sample.txt", index_col=0,
#    #                   header=None, names=['rain'], parse_dates=True)
    data = pd.read_csv("data_brach_case_nete.csv", index_col=0,
                       parse_dates=True)

    # WET DAYS EXAMPLE
    # select raining days only
    rainy_moments = data[data['rain'].values > 0.]

    #create example plots
    time_map_density(rainy_moments, time_unit='hour', cmap='Blues',
                     gridsize=20,xscale='log', yscale='log',vmax=150)
    #time_map_varcolor(rainy_moments, 'rain', time_unit='hour', cmap='Blues')

    ####
    dateparse = lambda x: pd.datetime.strptime(x, '%Y%m')
    data = pd.read_csv("tijdelijke-werkloosheid.csv",sep=';', index_col=0,
                       parse_dates=0, date_parser=dateparse)

    worklow = data[data["Aantal personen"].values > 50]

    time_map_varcolor(worklow, "Aantal personen", time_unit='month',
                      cmap='Blues')
    time_map_density(worklow, time_unit='month', cmap='Blues',
                     gridsize=20, vmax=150)


