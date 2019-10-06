# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:15:07 2019

@author: astra
"""

import sys
import vrep

def Establish_Connection():
    """
    This function opens the connection with the running V-REP simulation and
    returns the client ID associated with that connection.
    """
    
    # clean up command, closes all opened connections
    vrep.simxFinish(-1)

    # connect to V-REP
    clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

    if clientID != -1:
        print ('Connected to remote API server')
    else:
        print ('Connection not successful, check that V-REP simulation is running!')
        sys.exit('Error: Could not connect')
    # end if
    
    return clientID
    
# end def
    
def Get_Joint_Handles(clientID):
    """
    This function returns a list of the handle associated with each Sawyer
    robot joint.
    """
    
    # Get handles for robot joints, check for errors
    returnCode_SawyerJoints = [-1] * 7
    SawyerJoints = [0] * 7
    for i in range(7):
        returnCode_SawyerJoints[i], SawyerJoints[i] = vrep.simxGetObjectHandle(clientID, 'Sawyer_joint'+str(i+1), vrep.simx_opmode_blocking)
        if returnCode_SawyerJoints[i] != 0:
            print('Error: object handle for Sawyer_joint'+str(i+1)+' did not return successfully.')
        # end if
    # end for
    
    return SawyerJoints
    
# end def
    
def Get_Gripper_Handle(clientID):
    """
    This function returns the handle associated with the Baxter Gripper.
    """
    
    # Get handle for robot gripper, check for errors
    returnCode_BaxterGripper, BaxterGripper = vrep.simxGetObjectHandle(clientID, 'BaxterGripper', vrep.simx_opmode_blocking)
    if returnCode_BaxterGripper != 0:
        print('Error: object handle for BaxterGripper did not return successfully.')
    # end if
    
    return BaxterGripper
    
# end def