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
q1 = np.array([0.00017049908638000488, -4.6312808990478516e-05, 0.08648266643285751])
q2 = q1 + np.array([0.08151283860206604, 0.06099781394004822, 0.2299564778804779])
q3 = q2 + np.array([0.12470394372940063, 0.13143983483314514, -0.0005479753017425537])
q4 = q3 + np.array([0.2754673361778259, -0.04757729172706604, -0.004028260707855225])
q5 = q4 + np.array([0.11295616626739502, -0.12105304002761841, -0.001822352409362793])
q6 = q5 + np.array([0.28688281774520874, 0.0403885543346405, -0.007017552852630615])
q7 = q6 + np.array([0.07401466369628906, 0.09576916694641113, -0.0021599233150482178])
q = np.array([q1, q2, q3, q4, q5, q6, q7])
p_end = np.array([1.144591599702835, 0.16081437468528748, 0.2913980856537819])

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