# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 19:17:08 2019

@author: astra
"""

import math
import numpy

# RML Vectors
accel = 20
jerk = 40
currentVel = [0] * 7
currentAccel = [0] * 7
maxVel = [84*math.pi/180,64*math.pi/180,95*math.pi/180,95*math.pi/180,170*math.pi/180,170*math.pi/180,221*math.pi/180]
maxAccel = [accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180]
maxJerk = [jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180]
targetVel = [0.05] * 7

# Define constants for forward kinematics
# Define the origin of the base frame as the location of Sawyer_link0_visible
q0 = numpy.array([0.8248, -0.6500, 0.0470])
q1 = numpy.array([0.8656, -0.6541, 0.2425])-q0
q2 = numpy.array([0.9060, -0.5891, 0.3170])-q0
q3 = numpy.array([1.0304, -0.4575, 0.3128])-q0
q4 = numpy.array([1.3059, -0.5049, 0.3045])-q0
q5 = numpy.array([1.4189, -0.6259, 0.2994])-q0
q6 = numpy.array([1.7054, -0.5853, 0.2846])-q0
q7 = numpy.array([1.7793, -0.4895, 0.2805])-q0
q = numpy.array([q1, q2, q3, q4, q5, q6, q7])
w1 = numpy.array([0, 0, 1])
w2 = numpy.array([0, 1, 0])
w3 = numpy.array([1, 0, 0])
w4 = numpy.array([0, -1, 0])
w5 = numpy.array([1, 0, 0])
w6 = numpy.array([0, 1, 0])
w7 = numpy.array([1, 0, 0])
w = numpy.array([w1, w2, w3, w4, w5, w6, w6])