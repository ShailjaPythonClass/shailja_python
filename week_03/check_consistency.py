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
    prev_row = df.shift(1)
    failures = (prev_row.dest != df.source) & \
                 (prev_row.group_id == df.group_id) & \
                 (prev_row.category != df.category)
    print sum(failures), (time.clock() - start)
    
    sum([a != b for a,b in zip(flags, failures)])
    df['failures'] = flags
    
    