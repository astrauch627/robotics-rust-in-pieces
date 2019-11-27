# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:28:14 2019

@author: astra
"""

import kinematics
import math
import numpy as np
import time
import utilities
import vrep

def Move_To_Position(clientID, thetas, robotID):
    """
    This function is used to move the robot to the position defined by the
    angles, thetas, for each respective joint.
    """
    
    # Get list of the handles of each robot link
    SawyerJoints = utilities.Get_Joint_Handles(clientID, robotID)
    
    # Move the robot!
    for i in range(7):
        joint = SawyerJoints[i]
        theta = thetas[i]
        returnCode = vrep.simxSetJointTargetPosition(clientID, joint, theta, vrep.simx_opmode_oneshot)
        if (returnCode != vrep.simx_return_ok and returnCode != vrep.simx_return_novalue_flag):
            print('Error: movement not registered correctly.')
        # end if
        
    # end for
    
    time.sleep(0.1)
    
# end def
    
def Get_End_Relative_Position(clientID, robotID):
    """
    This function is used to return the position (x,y,z) of the dummy object
    that is used to represent the origin of the end-effector frame, relative
    to the location of the dummy object that represents the origin of the base
    frame.
    """
    
    # Get handle for the base frame origin dummy object
    returnCode, baseHandle = vrep.simxGetObjectHandle(clientID, 'Base_Frame_Origin#'+str(robotID), vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for Base_Frame_Origin did not return successfully.')
    # end if
    
    # Get handle for the end-effector frame origin dummy object
    returnCode, endHandle = vrep.simxGetObjectHandle(clientID, 'End_Frame_Origin#'+str(robotID), vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for End_Frame_Origin did not return successfully.')
    # end if
    
    # Get position, check for error
    returnCode, basePos = vrep.simxGetObjectPosition(clientID, baseHandle, -1, vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error '+str(returnCode)+' : object position for Base_Frame_Orign did not return successfully.')
    # end if
    returnCode, endPos = vrep.simxGetObjectPosition(clientID, endHandle, -1, vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error '+str(returnCode)+' : object position for End_Frame_Orign did not return successfully.')
    # end if
    pos = np.subtract(endPos, basePos)
    
    return pos
    
# end def
    
def Spin_Screwdriver(clientID, currPos, robotID, objID):
    """
    This function simulates the movement of the screwdriver and screw.
    """
    
    # Get handles
    returnCode, screwHandle = vrep.simxGetObjectHandle(clientID, 'Screw_Visible#'+str(objID), vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error '+str(returnCode)+' : object handle for Screw_Visible did not return successfully.')
    # end if
    
    # Calculate predicted height change after spinning 30deg
    dh = (30/180)*0.0005*math.pi*np.tan(math.radians(60))
       
    # Initialize current positions and orientations
    currAngle = 0
    returnCode, currPos_screw = vrep.simxGetObjectPosition(clientID, screwHandle, -1, vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error '+str(returnCode)+' : object position for Screw_Visible did not return successfully.')
    # end if
    
    # spin in 30 degree increments
    for i in range(72):
        # Adjust desired position
        desiredPos = np.array(currPos) - np.array([0, 0, dh])
        desiredPos_screw = np.array(currPos_screw) - np.array([0, 0, dh])
        desiredAngle = currAngle + 30
        
        thetas = kinematics.Get_IK_Angles(clientID, desiredPos, desiredAngle, robotID)
        Move_To_Position(clientID, thetas, robotID)
        #time.sleep(0.1)
        returnCode = vrep.simxSetObjectPosition(clientID, screwHandle, -1, desiredPos_screw, vrep.simx_opmode_blocking)
        if returnCode != vrep.simx_return_ok:
            raise Exception('Error '+str(returnCode)+' : object position for Screw_Visible did not set successfully.')
        # end if
        returnCode = vrep.simxSetObjectOrientation(clientID, screwHandle, -1, [0, 0, -math.radians(desiredAngle)], vrep.simx_opmode_blocking)
        if returnCode != vrep.simx_return_ok:
            raise Exception('Error '+str(returnCode)+' : object orientation for Screw_Visible did not set successfully.')
        # end if
        
        # Iterate
        currPos = desiredPos
        currPos_screw = desiredPos_screw
        currAngle = desiredAngle
    # end if
    
# end def