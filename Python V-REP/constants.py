# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 19:17:08 2019

@author: astra
"""

import math

# RML Vectors
accel = 20
jerk = 40
currentVel = [0] * 7
currentAccel = [0] * 7
maxVel = [84*math.pi/180,64*math.pi/180,95*math.pi/180,95*math.pi/180,170*math.pi/180,170*math.pi/180,221*math.pi/180]
maxAccel = [accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180]
maxJerk = [jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180]
targetVel = [0] * 7

# Vector between the previous joint and this one
Dimensions_Joint1 = [0.0000, 0.0000, 0.0865]
Dimensions_Joint2 = [0.0810, 0.0609, 0.2305]
Dimensions_Joint3 = [0.1244, 0.1316, -0.0042]
Dimensions_Joint4 = [0.2755, -0.0474, -0.0082]
Dimensions_Joint5 = [0.1130, -0.1210, -0.0050]
Dimensions_Joint6 = [0.2865, 0.0406, -0.0149]
Dimensions_Joint7 = [0.0739, 0.0958, -0.0042]

# Matrix containing each w vector for each joint.
# Each row i contains w_i
w = [[0, 0, 1], [0, 1, 0], [0, 0, 1], [0, 0, -1], [0, 0, 1], [0, 1, 0], [0, 0, 1]]

# Matrix containing each q vector for each joint.
# Each row i contains q_i
q = [Dimensions_Joint1, Dimensions_Joint2, Dimensions_Joint3, Dimensions_Joint4, Dimensions_Joint5, Dimensions_Joint6, Dimensions_Joint7]