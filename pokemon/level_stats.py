# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 16:17:29 2017

@author: jzuber
"""
import math 

# pokemon hp and other stats def
def hp(base, level, iv, ev=16):
    iv = min(level, 63)
    a = math.floor((((2 * base + iv + math.floor(ev/4)) * level)/100))
    return a + level + 10

def otherstat(base, level, iv = None, ev=16):
    if iv is None:
        iv = min(63, level)
    a = math.floor((((2 * base + iv + math.floor(ev/4)) * level)/100))
    return a + 5