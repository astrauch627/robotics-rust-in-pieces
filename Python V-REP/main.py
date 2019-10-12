# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:14:03 2019

@author: astra
"""

import kinematics
import math
import movements
import time
import utilities
import vrep

# IMPORTANT: Must start the simulation before running this!

"""
This file calls all other functions required to move the simulation.
"""
    
# Connect to V-REP, get client ID
clientID = utilities.Establish_Connection()

# Get proximity sensor handle
ConveyorHandles = utilities.Get_Conveyor_Handles(clientID)
ProximitySensor_Handle = ConveyorHandles[2]

# Check for proximity sensor status
returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
isObjectDetected = detectionState

# Move robot to hover over object
thetas1 = [0, 0, 0, 0, 0, 0, 0]
movements.Move_To_Position(clientID, thetas1)

# Wait until block has moved in front of proximity sensor
while isObjectDetected == False:
    time.sleep(1)
    
    # Re-check for proximity sensor status
    returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
    isObjectDetected = detectionState
# end while
    
# When block is detected, move robot down to block
thetas2 = [1, 0, 0, 0, 0, 0, 0]
movements.Move_To_Position(clientID, thetas2)

# Spin the gripper over block
thetas3 = [1, 0, 0, 0, 0, 0, 0]
movements.Move_To_Position(clientID, thetas3)

# End simulation
print ('All done!')
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
