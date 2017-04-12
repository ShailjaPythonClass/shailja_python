# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:09:48 2017

@author: jzuber
"""
import warnings

import numpy as np
import pandas as pd

from datetime import datetime

try:
    # For pandas > 0.19
    from pandas_datareader import data as web
except ImportError: 
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from pandas.io.data import data as web

def get_px(stock, start, end):
    return web.get_data_yahoo(stock, start, end)['Adj Close']

if __name__ == "__main__":    
    start_date = datetime(2016,1,1)
    end_date = datetime(2016, 4, 21)

    stocks = {'tech':['GOOGL', 'MSFT', 'LNKD', 'YHOO', 'FB','HPQ','AMZN'],
              'auto':['TM','F','GM','HMC','NSANY','HYMTF'],
              'housing':['HD','WMT','LOW']}
    
    tech_rets = [get_px(n, start_date, end_date) for n in stocks['tech']]    
    df = pd.DataFrame(dict(zip(stocks['tech'], tech_rets)))
    
    print np.roll([1,2,4,8], -1)
    