# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 10:35:04 2014

@author: stvhoey
"""

import datetime
import numpy as np
import pandas as pd

#help :  http://pandas.pydata.org/pandas-docs/stable/groupby.html

#dummy datarange met een uurlijkse frequentie
rng = pd.date_range(start='1/1/2001', end='1/31/2012', freq='H')

#dummy data, random numbers
data = pd.DataFrame(np.random.random(len(rng)), 
                    index=rng, columns=['data1'])

#Elk jaar de laatste waarde kiezen (dit werkt als datetimeindex van pandas)
test = data.groupby([lambda x: x.year]).last()
#maw, op het groupby kan je functies gebruiken (bv. last, maar ook eender welke functie)
#=> http://pandas.pydata.org/pandas-docs/stable/groupby.html#groupby-object-attributes

#handig is ook get_group:
selectjaar = data.groupby([lambda x: x.year]).get_group(2001)

#of dus op functies, hier met lambda-stijl
info_per_year = data.groupby([lambda x: x.year]).apply(lambda x: x.describe())

#of op zelf geschreven functies
def lasttwonumbers(dframe):
    return dframe.ix[-2:]

last2year = data.groupby([lambda x: x.year]).apply(lasttwonumbers)


