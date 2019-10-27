# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:26:26 2019

@author: astra
"""

import constants
import numpy
import scipy.linalg
    
def Predict_FK_Position(clientID, thetas):
    """
    This function predicts the final position of the end-effector, from the
    given set of joint angles.
    """
    
    # Compute screw axes
    s1 = Find_Screw_Axis(clientID, 1)
    s2 = Find_Screw_Axis(clientID, 2)
    s3 = Find_Screw_Axis(clientID, 3)
    s4 = Find_Screw_Axis(clientID, 4)
    s5 = Find_Screw_Axis(clientID, 5)
    s6 = Find_Screw_Axis(clientID, 6)
    s7 = Find_Screw_Axis(clientID, 7)
    p = numpy.array([1.8191, -0.4895, 0.2910]) - constants.q0
    M = numpy.array([[0, 0, 1, p[0]], [0, 1, 0, p[1]], [-1, 0, 0, p[2]], [0, 0, 0, 1]])
    
    # Incrementally multiply each exponential matrix to each other
    T = scipy.linalg.expm(s1*thetas[0])
    T = numpy.dot(T, scipy.linalg.expm(s2*thetas[1]))
    T = numpy.dot(T, scipy.linalg.expm(s3*thetas[2]))
    T = numpy.dot(T, scipy.linalg.expm(s4*thetas[3]))
    T = numpy.dot(T, scipy.linalg.expm(s5*thetas[4]))
    T = numpy.dot(T, scipy.linalg.expm(s6*thetas[5]))
    T = numpy.dot(T, scipy.linalg.expm(s7*thetas[6]))
    T = numpy.dot(T, M)
    
    # Parse T to get position
    pos = numpy.array([T[0][3], T[1][3], T[2][3]]) + constants.q0
    return pos
    
# end def
    
def Find_Screw_Axis(clientID, jointNumber):
    """"
    This function finds the screw axis corresponding to the specified joint
    number.
    """
    
    # Get w and q specific to the input joint number
    w = constants.w[jointNumber-1]
    q = constants.q[jointNumber-1]
    
    # Calculate screw axis
    v = numpy.cross(-1*w, q)
    w_mat = numpy.array([[0, -1*w[2], w[1]], [w[2], 0, -1*w[0]], [-1*w[1], w[0], 0]])
    S = numpy.array([[w_mat[0][0], w_mat[0][1], w_mat[0][2], v[0]], [w_mat[1][0], w_mat[1][1], w_mat[1][2], v[1]], [w_mat[2][0], w_mat[2][1], w_mat[2][2], v[2]], [0, 0, 0, 0]])
    
    return S
    
    
# end def