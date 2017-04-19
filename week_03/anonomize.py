# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 11:26:53 2017

@author: jzuber
"""
import pandas as pd

if __name__ == "__main__":        
    # Open a CSV into a pandas dataframe
    df = pd.read_csv("../sample_data/opldata.csv")
    
    df = df.sample(n=100)
    for col in df.columns:
        try:
            df[col] = df[col]*1376 % 500
        except TypeError:
            pass
    new_types = dict(zip(['daopl', 'xdopl', 'ppopl', 'magic'],
                         ['type_1', 'type_2', 'type_3', 'type_4']))
    df['opltype'] = map(lambda x: new_types[x], df['opltype'])
        
    old_col = [u'oplponum', u'oplid', u'oplslmid', u'oplslmoutid', u'opltype']
    new_col = [u'group_id', u'unused', u'source', u'dest', u'category']
    df.rename(columns=dict(zip(old_col, new_col)), inplace=True)
    
    df.to_csv('../sample_data/anon.csv', index=False)