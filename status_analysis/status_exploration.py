# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:01:50 2017

@author: jzuber
"""
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    datapath = 'data/'
    datecols = ['new_eta', 'original_eta', 'actual_receive_date']
    df = pd.read_csv(datapath + 'anon.csv', parse_dates=datecols)        
    plt.figure(figsize=(12,5))    
    plt.plot_date(df.original_eta, df.actual_receive_date, ydate=True)
    plt.xlabel('Original ETA')
    plt.ylabel('Received date')
    
    
    

    
    
    