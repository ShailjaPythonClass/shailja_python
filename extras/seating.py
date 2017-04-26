# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 10:09:00 2017

@author: jzuber
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def draw_seat(group):
    tickets = []
    for i, row in group.iterrows():
        tickets.extend([(row['name'], row['rank'])]*row['tickets'])
    np.random.shuffle(tickets)
    winning_order = []
    for t in tickets:
        if t not in winning_order:
            winning_order.append(t)
    return winning_order

    
def select_winners(df):
    seats = np.unique(df.seat)
    draw = list(df.groupby('seat').apply(draw_seat))
    num_decided = sum([len(d) > 0 for d in draw])
    now_decided = None
    while num_decided != now_decided:
        num_decided = now_decided
        for name in df.name.unique():
            seats_won = [(seat[0][1], i) 
                            for i, seat in enumerate(draw) 
                            if len(seat) > 0 and seat[0][0] == name]
            if len(seats_won) > 1:
                favorite = min(seats_won)[1]
                forfeiting = [i for (_,i) in seats_won if i != favorite]
                for i in forfeiting:            
                    del draw[i][0]
        now_decided = sum([len(d) > 0 for d in draw])    

    winners = {s[0][0]:seats[i] for i,s in enumerate(draw) if len(s) > 0}        
    return winners

def do_draw(df):                     
    winners = select_winners(df)
            
    while len(winners) < len(df.name.unique()):
        name_inds = [not x for x in  df.name.isin(winners.keys())]
        seat_inds = [not x for x in df.seat.isin(winners.values())]
        new_df = df.loc[[a&b for a,b in zip(name_inds, seat_inds)]].copy()
        new_df.tickets = 1
        new_winners = select_winners(new_df)
        winners.update(new_winners)
    return winners
    
if __name__ == "__main__":
    NUM_TRIALS = 1000
    df = pd.read_csv('../sample_data/seats.csv')
    seat_hist = {name:[] for name in df.name.unique()}

    for _ in range(NUM_TRIALS):
        winners = do_draw(df)
        assert len(set(winners.keys())) == len(winners), 'Names unique'
        assert len(set(winners.values())) == len(winners), 'Seats unique'
        for k,v in winners.iteritems():
            seat_hist[k].append(v)
    for name in seat_hist.keys():
        plt.figure(figsize=[10,4])
        x = seat_hist[name]
        plt.hist(x, bins=range(1,10), rwidth=0.5, align='left')
        plt.title(name)
        
    bins = {k:[sum([x == i for x in v]) for i in range(10)] 
               for k,v in seat_hist.iteritems()}
    for v in bins.values():
        assert sum(v) == NUM_TRIALS, "sum {} is not {}".format(v, NUM_TRIALS)