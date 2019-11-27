# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:15:07 2019

@author: astra
"""

import movements
import numpy as np
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
    
def Get_Joint_Handles(clientID, robotID):
    """
    This function returns a list of the handle associated with each Sawyer
    robot joint.
    """
    
    # Get handles for robot joints, check for errors
    returnCode_SawyerJoints = [-1] * 7
    SawyerJoints = [0] * 7
    for i in range(7):
        returnCode_SawyerJoints[i], SawyerJoints[i] = vrep.simxGetObjectHandle(clientID, 'Sawyer_joint'+str(i+1)+'#'+str(robotID), vrep.simx_opmode_blocking)
        if returnCode_SawyerJoints[i] != vrep.simx_return_ok:
            raise Exception('Error: object handle for Sawyer_joint'+str(i+1)+' did not return successfully.')
        # end if
    # end for
    
    return SawyerJoints
    
# end def
    
def Get_Conveyor_Handles(clientID):
    """
    This function returns a list of the handles associated with each component
    in the conveyor belt
    """
    
    # Initialize list of handles
    ConveyorBelt = [0] * 3
    
    # Forwarder
    returnCode, ConveyorBelt[0] = vrep.simxGetObjectHandle(clientID, 'customizableConveyor_forwarder', vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for conveyor_forwarder did not return successfully.')
    # end if
    
    # Texture Shape
    returnCode, ConveyorBelt[1] = vrep.simxGetObjectHandle(clientID, 'customizableConveyor_tableTop', vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for conveyor_tableTop did not return successfully.')
    # end if
    
    # Proximity Sensor
    returnCode, ConveyorBelt[2] = vrep.simxGetObjectHandle(clientID, 'Proximity_sensor', vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for conveyor_proximitySensor')
    # end if
    
    return ConveyorBelt
    
# end def
    
def Get_Base_Handle(clientID, robotID):
    """
    This function returns the handle associated with the robot's base. The base
    is defined as link 0 on the Sawyer robot.
    """
    
    # Get handle and return code
    returnCode, base_handle = vrep.simxGetObjectHandle(clientID, 'Sawyer_link0_visible#'+str(robotID), vrep.simx_opmode_blocking)
    # Use return code to check for errors
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error: object handle for Sawyer_link0_visible did not return successfully.')
    # end if
    
    return base_handle

# end def
    
def Print_q(robotID):
    """
    This function prints out all of the robot's joint dimensions. Copy-and-paste
    this output into constants.py
    """
    
    clientID = Establish_Connection()
    
    # Move the robot into the "zero" position
    thetas = [0, 0, 0, 0, 0, 0, 0]
    movements.Move_To_Position(clientID, thetas, robotID)
    
    print('Copy the following lines into constants.py:')
    print(' ')
    
    # Set the dummy object as the previous joint handle
    returnCode, baseHandle = vrep.simxGetObjectHandle(clientID, 'Base_Frame_Origin#'+str(robotID), vrep.simx_opmode_blocking)
    if returnCode != vrep.simx_return_ok:
        raise Exception('Error '+str(returnCode)+': object handle for Base_Frame_Origin did not return successfully')
    # end if
    prevJointHandle = baseHandle
    for i in range(1,8):
        # Get current joint handle
        returnCode, currJointHandle = vrep.simxGetObjectHandle(clientID, 'Joint'+str(i)+'_Origin#'+str(robotID), vrep.simx_opmode_blocking)
        if returnCode != vrep.simx_return_ok:
            raise Exception('Error '+str(returnCode)+': object handle for Joint'+str(i)+'_Origin did not return successfully')
        # end if
        
        # Get joint dimensions and print
        returnCode, currPos = vrep.simxGetObjectPosition(clientID, currJointHandle, -1, vrep.simx_opmode_blocking)
        if returnCode != vrep.simx_return_ok:
            raise Exception('Error '+str(returnCode)+': position for Joint'+str(i)+'_Origin did not return successfully')
        # end if
        returnCode, prevPos = vrep.simxGetObjectPosition(clientID, prevJointHandle, -1, vrep.simx_opmode_blocking)
        if returnCode != vrep.simx_return_ok:
            raise Exception('Error '+str(returnCode)+': position for Joint'+str(i-1)+'_Origin did not return successfully')
        # end if
        pos = np.subtract(currPos, prevPos)
        if (i == 1):
            print('q'+str(i)+' = np.array(['+str(pos[0])+', '+str(pos[1])+', '+str(pos[2])+'])')
        else:
            print('q'+str(i)+' = q'+str(i-1)+' + np.array(['+str(pos[0])+', '+str(pos[1])+', '+str(pos[2])+'])')
        
        # Update previous joint handle
        prevJointHandle = currJointHandle
    # end for
    
    print('q = np.array([q1, q2, q3, q4, q5, q6, q7])')
    
    # Get the relative location of the end-effector
    end_pos = movements.Get_End_Relative_Position(clientID, robotID)
    print('p_end = np.array(['+str(end_pos[0])+', '+str(end_pos[1])+', '+str(end_pos[2])+'])')
    
# end def