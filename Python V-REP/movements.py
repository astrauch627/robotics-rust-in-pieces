# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:28:14 2019

@author: astra
"""

import constants
import numpy
import time
import utilities
import vrep
import vrepConst

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
        #time.sleep(1.0)
        
    # end for
    
# end def
    
def Move_Conveyor_Belt(clientID):
    """
    This function is used to move the conveyor belt until the stopping
    condition has been met.
    """
    
    # Get handles for all conveyor belt parts
    # Forwarder, Texture shape, proximity sensor
    ConveyorBelt_Handles = utilities.Get_Conveyor_Handles(clientID)
    Forwarder_Handle = ConveyorBelt_Handles[0]
    TextureShape_Handle = ConveyorBelt_Handles[1]
    ProximitySensor_Handle = ConveyorBelt_Handles[2]
    
    # Set goal belt velocity
    beltVelocity = 100
    
    # Initialize detection boolean
    isObjectDetected = False
    
    # Move belt until object has been detected in proximity sensor
    while isObjectDetected == False:
        # Object has not arrived at its destination, so keep belt moving
        
        # Move the conveyor belt with velocity of t*beltVelocity
        t = vrep.simxGetLastCmdTime(clientID)
        vrep.simxSetObjectFloatParameter(clientID, TextureShape_Handle, vrepConst.sim_shapefloatparam_init_velocity_x, t*beltVelocity, vrep.simx_opmode_blocking)
        
        relativeLinearVelocity = [beltVelocity, 0, 0]
        returnCode = vrep.simxSetObjectOrientation(clientID, Forwarder_Handle, -1, [0,0,0], vrep.simx_opmode_oneshot)
        
        returnCode, m = vrep.simxGetJointMatrix(clientID, Forwarder_Handle, vrep.simx_opmode_blocking)
        # Set translation components to zero
        m[3] = 0
        m[7] = 0
        m[11] = 0
        # Move data from m into matrix form
        m = [[m[0],m[1],m[2]], [m[4],m[5],m[6]], [m[8], m[9], m[10]]]
        # Compute the absolute velocity vector
        absoluteLinearVelocity = numpy.dot(m, relativeLinearVelocity)
        
        # Set initial velocity of the dynamic rectangle
        vrep.simxSetObjectFloatParameter(clientID, Forwarder_Handle, vrepConst.sim_shapefloatparam_init_velocity_x, absoluteLinearVelocity[0], vrep.simx_opmode_oneshot)
        vrep.simxSetObjectFloatParameter(clientID, Forwarder_Handle, vrepConst.sim_shapefloatparam_init_velocity_y, absoluteLinearVelocity[1], vrep.simx_opmode_oneshot)
        vrep.simxSetObjectFloatParameter(clientID, Forwarder_Handle, vrepConst.sim_shapefloatparam_init_velocity_z, absoluteLinearVelocity[2], vrep.simx_opmode_oneshot)
        
        # Check for proximity sensor status
        returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
        isObjectDetected = detectionState
    # end while
    
    # Object has arrived at destination, so stop belt
    print (isObjectDetected)
    beltVelocity = 0
    
    
    
# end def