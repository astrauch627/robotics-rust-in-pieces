# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:28:14 2019

@author: astra
"""

import constants
import numpy as np
import time
import utilities
import vrep

def Move_To_Position(clientID, thetas):
    """
    This function is used to move the robot to the position defined by the
    angles, thetas, for each respective joint.
    """
    
    # Get list of the handles of each robot link
    SawyerJoints = utilities.Get_Joint_Handles(clientID)
    
    # Move the robot!
    for i in range(7):
        joint = SawyerJoints[i]
        theta = thetas[i]
        returnCode_pos = vrep.simxSetJointTargetPosition(clientID, joint, theta, vrep.simx_opmode_blocking)
        returnCode_vel = vrep.simxSetJointTargetVelocity(clientID, joint, constants.targetVel[i], vrep.simx_opmode_blocking)
        
        # Check for errors
        if returnCode_pos != 0 or returnCode_vel != 0:
            print('Error: movement not registered correctly.')
        # end if
        
    # end for
    
    # Pause for sim to register robot's movement
    time.sleep(2)
    
# end def
    
def Get_End_Relative_Position(clientID):
    """
    This function is used to return the position (x,y,z) of the dummy object
    that is used to represent the origin of the end-effector frame, relative
    to the location of the dummy object that represents the origin of the base
    frame.
    """
    
    # Get handle for the base frame origin dummy object
    returnCode, baseHandle = vrep.simxGetObjectHandle(clientID, 'Base_Frame_Origin', vrep.simx_opmode_blocking)
    if returnCode != 0:
        print('Error: object handle for Base_Frame_Origin did not return successfully.')
    # end if
    
    # Get handle for the end-effector frame origin dummy object
    returnCode, endHandle = vrep.simxGetObjectHandle(clientID, 'End_Frame_Origin', vrep.simx_opmode_blocking)
    if returnCode != 0:
        print('Error: object handle for End_Frame_Origin did not return successfully.')
    # end if
    
    # Get position, check for error
    returnCode, basePos = vrep.simxGetObjectPosition(clientID, baseHandle, -1, vrep.simx_opmode_blocking)
    if returnCode != 0:
        print('Error '+str(returnCode)+' : object position for Base_Frame_Orign did not return successfully.')
    # end if
    returnCode, endPos = vrep.simxGetObjectPosition(clientID, endHandle, -1, vrep.simx_opmode_blocking)
    if returnCode != 0:
        print('Error '+str(returnCode)+' : object position for End_Frame_Orign did not return successfully.')
    # end if
    pos = np.subtract(endPos, basePos)
    
    return pos
    
# end def