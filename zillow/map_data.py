# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:09:31 2017

@author: jzuber
"""
import pysal
import progressbar

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.spatial import KDTree
from pysal.contrib.viz import mapping as maps

from clean_data import get_clean_merged_df

def choropleth(shp, bbox, data, title=None):
    data = 1.0 * np.nan_to_num(np.array(data))
    normed = (data - data.min()) / data.ptp()

    if np.min(data) < 0:
        cmap = 'PRGn'
    else:
        cmap = 'viridis'
    shapes = maps.map_poly_shp(shp)
    zips = maps.base_choropleth_classless(shapes,
                                       values=normed,
                                       cmap=cmap)
    zips.set_linewidth(0.75)
    zips.set_edgecolor('0.8')
    fig = plt.figure(figsize=(7, 7))
    ax = maps.setup_ax([zips], [bbox])
    fig.add_axes(ax)
    if title:
        plt.title(title)
    m = mpl.cm.ScalarMappable(cmap=cmap)
    m.set_array(np.unique(data))
    plt.colorbar(m)
    plt.show()

if __name__ == "__main__":
    merged = get_clean_merged_df(False)

    shapefile = "./shapefiles/zillow.shp"
    database_file = "./shapefiles/zillow.dbf"
    shp = pysal.open(shapefile)
    dbf = pysal.open(database_file)

    def find_pgon(lats, lons, pgon_list):
        tree = KDTree(np.array([p.centroid for p in pgon_list]))
        retval = []
        bar = progressbar.ProgressBar(max_value=len(lats))
        for lat, lon in bar(zip(lats, lons)):            
            retval.append(tree.query((lon,lat))[1])
        return retval

    inds = find_pgon(merged.latitude, merged.longitude, shp)
    zip_list = [d[0] for d in dbf]
    zips = [zip_list[i] for i in inds]

    merged['pgons'] = inds
    merged['zips'] = map(int, zips)

    def error_stats(group):
        return pd.Series({'mean_error': group.logerror.mean(),
                          'std_error': group.logerror.std(),
                          'abs_error': np.mean(np.abs(group.logerror))})
    errors = merged.groupby(['pgons', 'zips']).apply(error_stats)
    errors.reset_index(inplace=True)
    
    for col in ['mean_error', 'std_error', 'abs_error']:
        x = errors[col]

        yval = [0 for _ in shp]
        for i, row in errors.iterrows():
            yval[int(row.pgons)] = row[col]

        bbox = [merged.longitude.min(), merged.latitude.min(),
               merged.longitude.max(), merged.latitude.max()]

        choropleth(shp, bbox, yval, title=col)

