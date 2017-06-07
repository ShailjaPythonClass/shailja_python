# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 09:21:29 2017

@author: jzuber
"""

import numpy as np
import pandas as pd
import datetime as dt

from functools import partial

def clean_data(df):
    
    for col, typ in df.dtypes.iteritems():
        if typ is np.dtype('float64') \
            or typ is np.dtype('int64'):
            pass #df[col].fillna(-1, inplace=True)
        elif typ is np.dtype('object'):
            if True in df[col].unique():
                df[col].fillna(False, inplace=True)
            elif 'Y' in df[col].unique():
                df[col].fillna('N', inplace=True)
                df[col] = df[col].apply(lambda x: x == 'Y')                
            else:
                df[col].fillna('', inplace=True)
        
    return df

def fix_all_nan(df):    
    df = clean_data(df)                   
    zero_fills = ['architecturalstyletypeid',
                  'basementsqft', 
                  'bathroomcnt', 
                  'bedroomcnt',
                  'decktypeid',
                  'threequarterbathnbr',
                  'poolcnt',
                  'poolsizesum',
                  'garagecarcnt',
                  'garagetotalsqft',
                  'fireplacecnt',
                  'decktypeid',
                  'taxdelinquencyyear',
                  ]
    for col in zero_fills:
        if col not in df.columns:
            continue
        df[col].fillna(0, inplace=True)

    flags_match_counts = [('fireplaceflag', 'fireplacecnt')]
    for flag, cnt in flags_match_counts:
        df[flag] = df[cnt] > 0    
    
    # Assume no airconditioning
    df['airconditioningtypeid'].fillna(5, inplace=True)
        
    median_fills = ['buildingclasstypeid', 
                    'buildingqualitytypeid',
                    'calculatedbathnbr',
                    'numberofstories',                    
                    'propertylandusetypeid',
                    'unitcnt',
                    
                    ]
    for col in median_fills:
        if col not in df.columns:
            continue
        df[col].fillna(df[col].median(), inplace=True)
    
    false_fills = ['yardbuildingsqft17', 'yardbuildingsqft26',
                   'pooltypeid10', 'pooltypeid2', 'pooltypeid7',
                   ]
    for col in false_fills:
        if col not in df.columns:
            continue
        df[col].fillna(False, inplace=True)
        
    outlier_cull = ['garagetotalsqft', 'lotsizesquarefeet',]
    for col in outlier_cull:
        maxval = df[col].median() + 2.5*df[col].std()
        inds = df[col] > maxval
        df.loc[inds, col] = np.nan
        
    col = 'calculatedfinishedsquarefeet'
    for alt_col in ['finishedsquarefeet%d' % i for i in [6, 12, 15]]:
        if col not in df.columns or alt_col not in df.columns:
            continue
        df[col].fillna(df[alt_col], inplace=True)
    
    # Floor 1 estimates
    col = 'finishedfloor1squarefeet'
    try:
        for alt_col in ['finishedsquarefeet50']:
            if col not in df.columns or alt_col not in df.columns:
                continue
            df[col].fillna(df[alt_col], inplace=True)
        del df['finishedsquarefeet50']
    except:
        pass
    
    try:
        col = 'finishedfloor1squarefeet'
        guess = df['calculatedfinishedsquarefeet'] / df['numberofstories']
        df[col].fillna(guess, inplace=True)
    except:
        pass
    
    # drop empty columns
    badcols = [c for c, cnt in df.count().iteritems() if cnt < len(df)*0.9]
    for col in badcols:
        del df[col]
                
    df.dropna(inplace=True)
    def to_date(x):
        return dt.datetime.strptime(x, '%Y-%m-%d')
    df['transactiondate'] = df['transactiondate'].apply(to_date)
    
    def time_diff(x, period='d'):
        delta = (x - dt.datetime(2000,1,1))
        if period.lower() in ['d', 'day', 'days' ]:
            return delta.days
        elif period.lower() in ['m', 'month', 'months']:
            return delta.days * 12 / 365
        elif period.lower() in ['y', 'year', 'years']:
            return delta.days / 365
        
    to_day = partial(time_diff, period='d')
    df['transaction_day'] = df['transactiondate'].apply(to_day)
    to_month = partial(time_diff, period='m')
    df['transaction_month'] = df['transactiondate'].apply(to_month)
    to_year = partial(time_diff, period='y')
    df['transaction_year'] = df['transactiondate'].apply(to_year)
    
    df.rename(columns={'finishedsquarefeet12': 'finished_living_area',
                       'finishedsquarefeet50': 'finished_sqft_first_floor',
                       'finishedsquarefeet6': 'all_sqft',
                       'pooltypeid10': 'has_spa',
                       'pooltypeid2': 'has_pool_and_spa',
                       'pooltypeid7': 'has_pool_only',
                       'yardbuildingsqft17': 'sqft_of_patio',
                       'yardbuildingsqft26': 'sqft_of_shed' },
                       inplace=True)        
                          
    return df

def balanced_sample(traits_df, typecol='propertylandusetypeid'):
    def balanced_class(num_per_class, len_df):        
        def balance(group):
            n = min(group.propertylandusetypeid.count(), int(num_per_class))
            return group.sample(n=n, replace=False)
        return balance
        
    
    func = balanced_class(1e4, len(traits_df))
    return traits_df.groupby(typecol, group_keys=False).apply(func)

def get_clean_merged_df():
    try:
        merged = pd.read_hdf('data/merged.hdf5', 'merged')
    except IOError:
        try:
            traits_df = pd.read_hdf('data/properties_2016.hdf5',
                                    'traits_df')
            score_df = pd.read_hdf('data/train_2016.hdf5',
                                   'score_df')
        except IOError:
            traits_df = pd.read_csv('data/properties_2016.csv')
            score_df = pd.read_csv('data/train_2016.csv')
            traits_df.to_hdf('data/properties_2016.hdf5', 
                             'traits_df', 
                             mode='w')
            score_df.to_hdf('data/train_2016.hdf5', 'score_df', mode='w')                    
        house_df = traits_df[traits_df.propertylandusetypeid == 261]
        merged = pd.merge(house_df, score_df, on='parcelid')
        del traits_df
        del house_df    
        merged = fix_all_nan(merged)
        merged.to_hdf('data/merged.hdf5', 'merged', mode='w')
    return merged
    
if __name__ == "__main__":
    merged = get_clean_merged_df()
    