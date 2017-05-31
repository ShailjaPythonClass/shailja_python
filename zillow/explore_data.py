# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:41:22 2017

@author: jzuber
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def clean_data(traits_df):
    
    for col, typ in traits_df.dtypes.iteritems():
        if typ is np.dtype('float64') \
            or typ is np.dtype('int64'):
            pass #traits_df[col].fillna(-1, inplace=True)
        elif typ is np.dtype('object'):
            if True in traits_df[col].unique():
                traits_df[col].fillna(False, inplace=True)
            elif 'Y' in traits_df[col].unique():
                traits_df[col].fillna('N', inplace=True)
                traits_df[col] = traits_df[col].apply(lambda x: x == 'Y')                
            else:
                traits_df[col].fillna('', inplace=True)
    
    traits_df['airconditioningtypeid'].fillna(5, inplace=True)
    
    zero_fills = ['architecturalstyletypeid',
                  'basementsqft', 
                  'bathroomcnt', 
                  'bedroomcnt',
                  'decktypeid',
                  'threequarterbathnbr',
                  ]
    for col in zero_fills:
        traits_df[col].fillna(0, inplace=True)
        
    false_fills = ['fireplaceflag']
    for col in false_fills:
        traits_df[col].fillna(False, inplace=True)
    
    median_fills = ['buildingclasstypeid', 
                    'buildingqualitytypeid',
                    'calculatedbathnbr',
                    'numberofstories',
                    'propertycountylandusecode',
                    'propertylandusetypeid',
                    'propertyzoningdesc',
                    ]
    for col in median_fills:
        traits_df[col].fillna(traits_df[col].median(), inplace=True)            
        
    col = 'calculatedfinishedsquarefeet'
    for alt_col in ['finishedsquarefeet%d' % i for i in [6, 12, 15]]:
        traits_df[col].fillna(traits_df[alt_col], inplace=True)
    
    col = ['finishedfloor1squarefeet']
    for alt_col in ['finishedsquarefeet50']:
        traits_df[col].fillna(traits_df[alt_col], inplace=True)
    guess = traits_df['calculatedfinishedsquarefeet'] \
            / traits_df['numberofstories']
    traits_df[col].fillna(guess, inplace=True)
          
    traits_df['fireplacecnt'].fillna(1*traits_df['fireplaceflag'])
    traits_df['fireplaceflag'] = traits_df['fireplacecnt'] > 0
            
    return traits_df

def balanced_sample(traits_df, typecol='propertylandusetypeid'):
    def balanced_class(num_per_class, len_df):        
        def balance(group):
            n = min(group.propertylandusetypeid.count(), int(num_per_class))
            return group.sample(n=n, replace=False)
        return balance
        
    
    func = balanced_class(1e4, len(traits_df))
    return traits_df.groupby(typecol, group_keys=False).apply(func)
    
    
if __name__ == "__main__":
    try:
        traits_df = traits_backup.copy()        
    except (NameError, AttributeError):
        traits_df = pd.read_csv('data/properties_2016.csv')
        traits_backup = traits_df.copy()        
        
    
    try:
        score_df = score_backup.copy()
    except (NameError, AttributeError):
        score_df = pd.read_csv('data/train_2016.csv')
        score_backup = score_df.copy()
                        
    house_df = traits_df[traits_df.propertylandusetypeid == 261]
    
    merged = pd.merge(house_df, score_df, on='parcelid')
    del traits_df
    del house_df
    
    for col in merged.columns:
        plt.figure()
        try:
            plt.scatter(merged[col], merged.logerror)            
        except:
            pass
        finally:
            plt.title(col)