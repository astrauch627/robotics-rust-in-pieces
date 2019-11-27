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
    
def Get_IK_Angles(clientID, worldCoords, rotAngle, robotID):
    """
    This function uses analytical inverse kinematics to find a solution of
    joint angles in radians that will bring the end-effector to a given
    coordinate location. Assumes Joint1 = -90, Joint3 = 0, Joint5 = 0.
    """
    
    # Get position of base frame origin in world frame coordinates
    returnCode, baseHandle = vrep.simxGetObjectHandle(clientID, 'Base_Frame_Origin#'+str(robotID), vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for Base_Frame_Origin did not return successfully.')
    # end if
    returnCode, basePos = vrep.simxGetObjectPosition(clientID, baseHandle, -1, vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error '+str(returnCode)+' : object position for Base_Frame_Orign did not return successfully.')
    # end if
    
    # Convert from world frame to base frame
    coordsInBaseFrame = np.array(worldCoords) - np.array(basePos)
    #x = coordsInBaseFrame[0]
    y = coordsInBaseFrame[1]
    z = coordsInBaseFrame[2]
    
    # Define constant joint lengths
    L01y = constants.q2[1]
    L01z = constants.q2[2]
    L02 = np.absolute(constants.q4[0] - constants.q2[0])
    L04 = np.absolute(constants.q6[0] - constants.q4[0])
    L06 = np.absolute(constants.p_end[0] - constants.q6[0])
    
    # Define coordiante locations of points (2) and (6)
    y2 = -L01y
    z2 = L01z
    y6 = y
    z6 = z + L06
    
    # Find Joint4 angle
    a = np.sqrt((y6-y2)**2.0 + (z6-z2)**2.0)
    phi4 = np.arccos((L02**2.0+L04**2.0-a**2.0)/(2.0*L02*L04))
    theta4 = np.radians(180.0) - phi4
    
    # Find Joint2 angle
    phi2 = np.arcsin((L04*np.sin(phi4))/a)
    gamma = np.arccos(np.absolute(y2-y6)/a)
    theta2 = -phi2 - gamma
    
    # Find Joint6 angle
    theta6 = math.radians(90) - (theta2 + theta4)
    
    # Define constant joint angles
    theta1 = math.radians(-90)
    theta3 = math.radians(0)
    theta5 = math.radians(0)
    theta7 = math.radians(rotAngle)
    
    # Return list of all joint angles
    thetas = [theta1, theta2, theta3, theta4, theta5, theta6, theta7]
    return thetas
    
# end def