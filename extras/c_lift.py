# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 09:33:34 2017

@author: jzuber
"""
import numpy as np
from scipy.optimize import bisect

def c_lift(a, c):
    """
    Returns the radius of a half-circular obstacle on a line of 
    length 2a whose convex hull is 2a + c units long.
    """
    def calc_c(a, r):
        theta = np.arccos(float(r)/a)
        arc = (np.pi/2 - theta)*r
        line = np.sqrt(r**2 + a**2 - 2*a*r*np.cos(theta))
        return 2*(arc+line - a)
    return bisect(lambda x: calc_c(a, x) - c, 0, a)
    