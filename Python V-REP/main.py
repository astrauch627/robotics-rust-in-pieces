# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:14:03 2019

@author: astra
"""

import math
import movements
import utilities
import vrep

# IMPORTANT: Must start the simulation before running this!

"""
This file calls all other functions required to move the simulation.
"""
    
# Connect to V-REP, get client ID
clientID = utilities.Establish_Connection()

# Define a series of movements, defined by the angles of each joint
thetas = [90*math.pi/180, -90*math.pi/180, -90*math.pi/180, 90*math.pi/180, 120*math.pi/180, 80*math.pi/180, 2140*math.pi/180]
movements.Move_To_Position(clientID, thetas)

# End simulation
print ('All done!')
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
