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

# Define forward kinematics constants
q0 = numpy.array([0.8248, -0.6500, 0.0470])
q1 = numpy.array([0.8655, -0.6540, 0.2425])-q0
q2 = numpy.array([0.9406, -0.4902, 0.3157])-q0
q3 = numpy.array([1.2043, -0.4583, 0.3080])-q0
q4 = numpy.array([1.3399, -0.5926, 0.3025])-q0
q5 = numpy.array([1.5916, -0.6257, 0.2918])-q0
q6 = numpy.array([1.7188, -0.5189, 0.2817])-q0
q7 = numpy.array([1.8191, -0.4895, 0.2910])-q0
q = numpy.array([q1, q2, q3, q4, q5, q6, q7])
w1 = numpy.array([0, 0, 1])
w2 = numpy.array([0, 1, 0])
w3 = numpy.array([1, 0, 0])
w4 = numpy.array([0, -1, 0])
w5 = numpy.array([1, 0, 0])
w6 = numpy.array([0, 1, 0])
w7 = numpy.array([1, 0, 0])
w = numpy.array([w1, w2, w3, w4, w5, w6, w6])