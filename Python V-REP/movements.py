# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:28:14 2019

@author: astra
"""

import constants
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
    
    # TODO: move the robot with T somehow below
    
    # Move the robot!
    for i in range(7):
        joint = SawyerJoints[i]
        theta = thetas[i]
        returnCode_pos = vrep.simxSetJointTargetPosition(clientID, joint, theta, vrep.simx_opmode_oneshot)
        returnCode_vel = vrep.simxSetJointTargetVelocity(clientID, joint, constants.targetVel[i], vrep.simx_opmode_oneshot)
        
        # Check for errors
        if returnCode_pos != 1 or returnCode_vel != 1:
            print('Error: movement not registered correctly.')
        # end if
        
        # Pause for one second after the movement
        # This is only for debugging purposes - remove later!!
        time.sleep(1.0)
        
    # end for
    
# end def