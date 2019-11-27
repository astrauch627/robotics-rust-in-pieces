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
q1 = np.array([0.00017562508583068848, -6.079673767089844e-05, 0.0865059569478035])
q2 = q1 + np.array([0.08101996779441833, 0.061007797718048096, 0.23033541440963745])
q3 = q2 + np.array([0.12449720501899719, 0.13155832886695862, -0.001925140619277954])
q4 = q3 + np.array([0.27539753913879395, -0.04745444655418396, -0.0074124932289123535])
q5 = q4 + np.array([0.1129949688911438, -0.1209714412689209, -0.0047979652881622314])
q6 = q5 + np.array([0.286724328994751, 0.040557026863098145, -0.011303991079330444])
q7 = q6 + np.array([0.07393085956573486, 0.09581425786018372, -0.0027441680431365967])
q = np.array([q1, q2, q3, q4, q5, q6, q7])
p_end = np.array([1.1437733471393585, 0.16148796677589417, 0.2759023681282997])

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