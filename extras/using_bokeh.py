# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:13:31 2017

@author: jzuber
"""

from bokeh.plotting import figure, output_file, show
from bokeh.charts import Area, defaults
from bokeh.layouts import row

def test_plots():
    # output to static HTML file
    output_file("line.html")
    
    triple_plot = figure(title="Some Plots", plot_width=400, plot_height=400)
    multi_plot = figure(title="A Multiplot", plot_width=400, plot_height=400)
    
    # add a circle renderer with a size, color, and alpha
    multi_plot.multi_line([[1, 3, 2], [3, 4, 6, 6]], 
                          [[2, 1, 4], [4, 7, 8, 5]],
                          color=["firebrick", "navy"], 
                          alpha=[0.8, 0.3], 
                          line_width=4)
    triple_plot.line(x=[4, 5, 6], 
           y=[1, 2, 3],            
           color="black",
           line_width=4,
           legend="Line")
    triple_plot.wedge(x=[4, 5, 6], 
            y=[1, 2, 3], 
            radius=0.2, 
            start_angle=0.4, 
            end_angle=[4.8, 5.2, 6.3],
            color="firebrick", 
            alpha=0.6, 
            direction="clock",
            legend="Wedge")
    triple_plot.circle(x=[1, 2, 3], 
             y=[1, 2, 3], 
            radius=0.2,             
            color="navy", 
            alpha=0.6,
            legend="circle")
    
    # show the results
    triple_plot.legend.location = 'top_left'
    show(multi_plot)
    show(triple_plot)
    
    
def area_charts():
    defaults.width = 400
    defaults.height = 400
    
    # create some example data
    data = dict(
        python=[2, 3, 7, 5, 26, 221, 44, 233, 254, 265, 266, 267, 120, 111],
        pypy=[12, 33, 47, 15, 126, 121, 144, 233, 254, 225, 226, 267, 110, 130],
        jython=[22, 43, 10, 25, 26, 101, 114, 203, 194, 215, 201, 227, 139, 160],
    )
    
    area1 = Area(data, title="Area Chart", legend="top_left",
                 xlabel='time', ylabel='memory')
    
    area2 = Area(data, title="Stacked Area Chart", legend="top_left",
                 stack=True, xlabel='time', ylabel='memory')
    
    output_file("area.html", title="area.py example")
    
    show(row(area1, area2))
    
if __name__ == "__main__":
    test_plots()
    area_charts()