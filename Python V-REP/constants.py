# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 19:17:08 2019

@author: astra
"""

import math
import numpy as np


# RML Vectors
accel = 20
jerk = 40
currentVel = [0] * 7
currentAccel = [0] * 7
maxVel = [84*math.pi/180,64*math.pi/180,95*math.pi/180,95*math.pi/180,170*math.pi/180,170*math.pi/180,221*math.pi/180]
maxAccel = [accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180]
maxJerk = [jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180]
targetVel = [0.05] * 7

# Get all joint dimensions in the "standing-up" position
# Note: get these easily from copy-and-paste output from the following lines into the IPython console:
# import utilities
# utilities.Print_q()
q1 = np.array([0.00016701221466064453, -4.595518112182617e-05, 0.08650598675012589])
q2 = np.array([0.08103024959564209, 0.06094813346862793, 0.23050202429294586])
q3 = np.array([0.12441670894622803, 0.13156387209892273, -0.0042396485805511475])
q4 = np.array([0.27543020248413086, -0.04738891124725342, -0.008223026990890503])
q5 = np.array([0.11297750473022461, -0.12102586030960083, -0.005115717649459839])
q6 = np.array([0.28656089305877686, 0.04059720039367676, -0.014771133661270142])
q7 = np.array([0.0738750696182251, 0.0957861840724945, -0.004069805145263672])
q = np.array([q1, q2, q3, q4, q5, q6, q7])
p_end = np.array([1.1244176626205444, 0.16043296456336975, 0.2684154734015465])

# Get all angular velocity vectors - by inspection
w1 = np.array([0.0, 0.0, 1.0])
w2 = np.array([0.0, 1.0, 0.0])
w3 = np.array([1.0, 0.0, 0.0])
w4 = np.array([0.0, 1.0, 0.0])
w5 = np.array([1.0, 0.0, 0.0])
w6 = np.array([0.0, 1.0, 0.0])
w7 = np.array([1.0, 0.0, 0.0])
# save all angular velocity vectors in a matrix for easy retrieval
w = np.array([w1, w2, w3, w4, w5, w6, w7])