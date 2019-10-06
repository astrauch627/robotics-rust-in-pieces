# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:14:03 2019

@author: astra
"""

import kinematics
import utilities

# IMPORTANT: Must start the simulation before running this!

"""
This file calls all other functions required to move the simulation.
"""
    
# Connect to V-REP, get client ID
clientID = utilities.Establish_Connection()

M = kinematics.Calculate_M()
print(M)
    