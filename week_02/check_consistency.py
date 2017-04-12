# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 16:30:31 2017

@author: apsingh
"""
import time

import pandas as pd

if __name__ == '__main__':    
    df = pd.read_csv("../sample_data/anon.csv")
    df.sort(columns=['group_id', 'unused', 'category'], inplace=True)    
    
    start = time.clock()
    flags = []
    last = None    
    for i, row in df.iterrows():
        if last is not None \
            and row.source != last.dest \
            and row.group_id == last.group_id \
            and row.category != last.category:
            flags.append(1)
        else:
            flags.append(0)
        last = row
    print sum(flags), (time.clock() - start)

    start = time.clock()    
    failures = (df.shift(1).dest != df.source) & \
                 (df.shift(1).group_id == df.group_id) & \
                 (df.shift(1).category != df.category)
    print sum(failures), (time.clock() - start)
    
    df['failures'] = flags
    
    