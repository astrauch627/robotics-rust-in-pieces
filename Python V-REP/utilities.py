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
    
def Get_Conveyor_Handles(clientID):
    """
    This function returns a list of the handles associated with each component
    in the conveyor belt
    """
    
    # Get handles for conveyor belt, check for errors
    returnCode_ConveyorBelt = [-1] * 3
    ConveyorBelt = [0] * 3
    # Forwarder
    returnCode_ConveyorBelt[0], ConveyorBelt[0] = vrep.simxGetObjectHandle(clientID, 'customizableConveyor_forwarder', vrep.simx_opmode_blocking)
    if returnCode_ConveyorBelt[0] != 0:
        print('Error: object handle for conveyor_forwarder did not return successfully.')
    # end if
    # Texture Shape
    returnCode_ConveyorBelt[1], ConveyorBelt[1] = vrep.simxGetObjectHandle(clientID, 'customizableConveyor_tableTop', vrep.simx_opmode_blocking)
    if returnCode_ConveyorBelt[1] != 0:
        print('Error: object handle for conveyor_tableTop did not return successfully.')
    # end if
    # Proximity Sensor
    returnCode_ConveyorBelt[2], ConveyorBelt[2] = vrep.simxGetObjectHandle(clientID, 'Proximity_sensor', vrep.simx_opmode_blocking)
    if returnCode_ConveyorBelt[2] != 0:
        print('Error: object handle for conveyor_proximitySensor')
    # end if
    
    return ConveyorBelt
    
# end def