# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:41:22 2017

@author: jzuber
"""   
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from clean_data import fix_all_nan
    
from sklearn.tree import DecisionTreeRegressor

def scatter_all(df, interesting):
    ycol = 'logerror'
    for col in interesting:
        plt.figure()
        try:            
            plt.scatter(df[col], df[ycol])            
        except:
            pass
        finally:
            plt.title(col)
            plt.xlabel(col)
            plt.ylabel(ycol)


def three_d_scatter_plots(df, interesting):
    zcol = 'logerror'
    ignores = ['cnt', 'id', 'number', 'date', 'fips', 'flag']
    sub = df.sample(1000)
    for col1 in interesting:        
        for col2 in interesting:            
            if any([x.count(y) for x in [col1, col2] for y in ignores]):
                continue            
            if col1 >= col2:
                continue
            print col1, col2
            try:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter3D(sub[col1], sub[col2], sub[zcol])
            except:
                pass
            finally:
                plt.title("{}, {} vs {}".format(col1, col2, zcol))
                plt.xlabel(col1)
                plt.ylabel(col2)            


def plot_raw_error(df):    
    ycol = 'logerror'
    categorical = get_categorical(df)
    abscol = df[ycol].abs()
    bad = df[(abscol > abscol.median()) & (abscol < 1.0)]
    for col in categorical:
        plt.figure()
        sns.violinplot(col, ycol, data=bad)
        plt.title("Raw error vs " + col)

        
def get_categorical(df):
    categorical = [c for c in df.columns 
                   if len(df[c].unique()) < 10 
                   and len(df[c].unique()) > 1]        
    return categorical
                
if __name__ == "__main__":
    
    try:
        merged = pd.read_hdf('data/merged.hdf5')
    except IOError:
        try:
            traits_df = pd.read_hdf('data/properties_2016.hdf5')
            score_df = pd.read_hdf('data/train_2016.hdf5')
        except IOError:
            traits_df = pd.read_csv('data/properties_2016.csv')
            score_df = pd.read_csv('data/train_2016.csv')
            traits_df.to_hdf('data/properties_2016.hdf5', 'traits_df', mode='w')
            score_df.to_hdf('data/train_2016.hdf5', 'score_df', mode='w')                    
        house_df = traits_df[traits_df.propertylandusetypeid == 261]
        merged = pd.merge(house_df, score_df, on='parcelid')
        del traits_df
        del house_df    
        merged = fix_all_nan(merged)
        merged.to_hdf('data/merged.hdf5', 'merged', mode='w')
    
    interesting = ['airconditioningtypeid',
                 'basementsqft',
                 'bathroomcnt',
                 'bedroomcnt',
                 'calculatedbathnbr',
                 'decktypeid',
                 'finishedfloor1squarefeet',
                 'calculatedfinishedsquarefeet',
                 'finished_living_area',
                 'fips',
                 'fireplacecnt',
                 'fullbathcnt',
                 'garagecarcnt',
                 'garagetotalsqft', 
                 'lotsizesquarefeet',  
                 'regionidzip',
                 'roomcnt',
                 'yearbuilt',
                 'numberofstories',
                 'fireplaceflag', 
                 'transaction_month',]    

    ycol = 'logerror'    
    categorical = get_categorical(merged)
    cat_df = merged[[ycol] + categorical].copy()
    cat_df.replace([-np.inf, np.inf], np.nan, inplace=True)
    cat_df.dropna(inplace=True)

    for col in categorical:
        cat_df[col] = cat_df[col].apply(int)    
    cat_df.describe()
        
    dtree = DecisionTreeRegressor(max_depth=5)
    fit = dtree.fit(cat_df, cat_df[ycol])
        
    cat_df['fit'] = dtree.predict(cat_df)
    cat_df['diff'] = cat_df['fit'] - cat_df[ycol]    
    for col in categorical:
        plt.figure()
        sns.violinplot(col, 'diff', data=cat_df)
        plt.title(col)                
    
    plt.figure()
    plt.scatter(cat_df[ycol], cat_df['fit'])
    plt.title('Actual vs Decision Tree Fit')
    plt.xlabel('Actual')
    plt.ylabel('Decision Tree Fit')
    plt.show()
    
    denom = cat_df[ycol].apply(lambda x: max(np.abs(x), 1e-3))
    inds = denom > 0.25
    plt.figure()
    plt.scatter(cat_df.loc[inds, ycol], cat_df.loc[inds, 'diff'] / denom[inds])
    plt.title('Actual vs Decision Tree Error')
    plt.xlabel('Actual')
    plt.ylabel('Decision Tree Error')
    plt.show()
    
    old_mean = np.abs(cat_df[ycol]).mean()
    old_std = cat_df[ycol].std()
    new_mean = np.abs(cat_df[ycol] - cat_df['fit']).mean()
    new_std = np.abs(cat_df[ycol] - cat_df['fit']).std()
    print (old_mean, old_std), (new_mean, new_std)

    
    