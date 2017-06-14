# -*- coding: utf-8 -*-
"""
Created on Wed May 24 11:09:53 2017

@author: jzuber
"""
import keyring
import requests
import progressbar

import pandas as pd

api_key = keyring.get_password('google-api', 'jzuber@wayfair.com')

def get_drive_time(origin_zip, destination_zip):
    """
    Returns driving time from origin to destination in hours.
    """
       
    try:
        origin_zip = '{0:05d}'.format(origin_zip)
    except ValueError:
        origin_zip = '{0:05d}'.format(int(origin_zip))
    
    try:
        destination_zip = '{0:05d}'.format(destination_zip)
    except ValueError:
        destination_zip = '{0:05d}'.format(int(destination_zip))
    
    url = "https://maps.googleapis.com/maps/api/directions/json"
            
    params = {'origin': origin_zip,
              'destination': destination_zip, 
              'mode': 'driving',
              'key': api_key}
              
    response = requests.post(url=url, params=params)
    js = response.json()
    
    return js['routes'][0]['legs'][0]['duration']['value'] / 3600.


        
if __name__ == "__main__":
    df = pd.read_csv('drive_time_pairs.csv')
    df['drive_time'] = 1e10
    
    bar = progressbar.ProgressBar(max_value=len(df))
    for i, row in bar(df.iterrows()):
        time = get_drive_time(row['from_zipcode'], row['to_zipcode'])
        df.loc[i, 'drive_time'] = time        
    print df.head()
    
    