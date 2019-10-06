# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:28:14 2019

@author: astra
"""

import utilities
import vrep

def Move_To_Zero_Position(clientID):
    """
    This function is used in the simulation initialization, moves the robot
    to the zero position which is defined as pointing the application tool
    straight up in the positive z-direction.
    """
    
    # Get list of the handles of each robot link
    SawyerJoints = utilities.Get_Joint_Handles(clientID)
    
    # Move each joint to the zero position
    # Move the robot!
    for joint in SawyerJoints:
        returnCode_pos = vrep.simxSetJointTargetPosition(clientID, joint, 0, vrep.simx_opmode_oneshot)
        returnCode_vel = vrep.simxSetJointTargetVelocity(clientID, joint, 0, vrep.simx_opmode_oneshot)
        
        # Check for errors
        if returnCode_pos != 1 or returnCode_vel != 1:
            print ('Error: movement not registered correctly')
        # end if
    
    # end for
    
# end def