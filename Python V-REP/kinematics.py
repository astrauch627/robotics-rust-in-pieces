# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:26:26 2019

@author: astra
"""

import constants
import math
import movements
import numpy as np
import vrep
from scipy.linalg import expm
    
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
    
    # Define BaxterGripper as the end-effector
    # Obtained values for p by moving the gripper to its end position of [0, 0, 0, 0, 0, 0, 0]
    # and getting x, y, z coordinates of BaxterGripper
    p = constants.p_end
    M = np.array([[0.0, 0.0, 1.0, p[0]], [0.0, 1.0, 0.0, p[1]], [-1.0, 0.0, 0.0, p[2]], [0.0, 0.0, 0.0, 1.0]])
    
    # Incrementally multiply each exponential matrix to each other
    T = expm(s1*thetas[0])
    T = np.dot(T, expm(s2*thetas[1]))
    T = np.dot(T, expm(s3*thetas[2]))
    T = np.dot(T, expm(s4*thetas[3]))
    T = np.dot(T, expm(s5*thetas[4]))
    T = np.dot(T, expm(s6*thetas[5]))
    T = np.dot(T, expm(s7*thetas[6]))
    T = np.dot(T, M)
    
    # Parse T to get position of end-effector, relative to the base frame
    pos = np.array([T[0][3], T[1][3], T[2][3]])
    return pos
    
# end def
    
def Find_Screw_Axis(clientID, jointNumber):
    """"
    This function finds the screw axis corresponding to the specified joint
    number.
    """
    
    # Get w and q specific to the input joint number
    w = constants.w[jointNumber-1]
    # q is calculated as the distance vector between the previous joint and the current joint
    q = np.transpose(constants.q[jointNumber-1])
    
    
    # Calculate screw axis
    v = np.transpose(np.dot(skew(-w), q))
    
    
    w_mat = skew(w)
    S = np.array([[w_mat[0][0], w_mat[0][1], w_mat[0][2], v[0]], [w_mat[1][0], w_mat[1][1], w_mat[1][2], v[1]], [w_mat[2][0], w_mat[2][1], w_mat[2][2], v[2]], [0, 0, 0, 0]])
    
    return S
    
    
# end def
    
def skew(A):
    """
    This function finds the skew matrix for the given matrix
    """
    
    A_mat = np.array([[0.0, -A[2], A[1]], [A[2], 0.0, -A[0]], [-A[1], A[0], 0.0]])
    
    return A_mat
    
# end def