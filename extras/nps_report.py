import pyodbc
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import WinUtils.io_utils as winio

def nps(group):
    counts = group['']
    total = counts.sum()
    detractor = group.npstype == 'detractor'
    det_frac = sum(counts[detractor]) / total
    promoter = group.npstype == 'promoter'
    pro_frac = sum(counts[promoter]) / total
    pct = 100*(pro_frac-det_frac)
    return pd.Series({'NPS':pct})

if __name__ == "__main__":
    with open('queries/Exclusive brands NPS.sql', 'r') as inf:
        query = inf.read()    
    nps_df = winio.pull_from_sql(query, 'SQLADHOC01')
        
    with_nps = nps_df.groupby(['npsyear', 'npsmonth', 'shipclass']).apply(nps)
    with_nps.reset_index(inplace=True)

    lp = with_nps[with_nps.shipclass=='lp']
    sp = with_nps[with_nps.shipclass=='sp']
    plt.plot(12*(map(int,lp.npsyear)-2016)+lp.npsmonth, lp.NPS)
    
    lp_time = np.array(map(lambda x: 12*(int(x) - 2016), lp.npsyear)) + \
                np.array(map(int, lp.npsmonth))
    sp_time = np.array(map(lambda x: 12*(int(x) - 2016), sp.npsyear)) + \
                np.array(map(int, sp.npsmonth))
    plt.figure()
    plt.plot(lp_time, lp.NPS)
    plt.plot(sp_time, sp.NPS)
    plt.show()
                
    
    
    