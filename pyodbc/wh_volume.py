# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:14:24 2017

@author: jzuber
"""

import pyodbc
import unicodecsv

import pandas as pd

import matplotlib.pyplot as plt
if __name__ == "__main__":
    
    query = "SELECT * FROM csn_junk.[CSNZOO\jzuber].wh_numbers"
    
    with pyodbc.connect('DSN=FOX') as con:
        res = con.execute(query)
        with open('output/out.csv', 'wb') as outf:
            writer = unicodecsv.writer(outf)
            writer.writerow([x[0] for x in res.description])
            for row in res:
                writer.writerow(row)   

    with pyodbc.connect('DSN=FOX') as con:
        df = pd.read_sql(query, con)
        
    colnames = {'Date': 'date',
                'WHTotal': 'wh_total',
                'Total Orders': 'total_orders'}
    names = dict([('WH {}'.format(i), 'wh_{}'.format(i)) for i in range(1, 7)])    
    colnames.update(names)
    df.rename(columns=colnames, inplace=True)
    df.date = pd.to_datetime(df.date)
    
#    wh_cols = [col for col in df.columns if 'wh_' in col and col[-1].isdigit()]
#    plt.figure()    
#    for col in wh_cols:
#        plt.plot(df.date, df[col], label=col)
#    plt.legend(bbox_to_anchor=(1.3, 1.0))
#    plt.show()
    df.to_csv('output/daily.csv')
    
    