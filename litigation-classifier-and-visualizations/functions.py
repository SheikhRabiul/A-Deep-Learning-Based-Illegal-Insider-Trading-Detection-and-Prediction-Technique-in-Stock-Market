# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:04:36 2018

@author: Sheikh Rabiul Islam
"""

#sample code for feature scalling: feature ranking result is scalled in the range of  0 to 1
def scale_a_number(inpt, to_min, to_max, from_min, from_max):
    return (to_max-to_min)*(inpt-from_min)/(from_max-from_min)+to_min

def scale_a_list(l, to_min, to_max):
    return [scale_a_number(i, to_min, to_max, min(l), max(l)) for i in l]
