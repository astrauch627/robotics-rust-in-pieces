# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:14:03 2019

@author: astra
"""

import kinematics
import math
import numpy as np
import movements
import time
import utilities
import vrep

# IMPORTANT: Must start the simulation before running this!
# simExtRemoteApiStart(19999)

"""
This file calls all other functions required to move the simulation.
"""
    
# Connect to V-REP, get client ID
clientID = utilities.Establish_Connection()

# Get some handles
ConveyorHandles = utilities.Get_Conveyor_Handles(clientID)
ProximitySensor_Handle = ConveyorHandles[2]
base_handle = utilities.Get_Base_Handle(clientID, 1)

# Initialize proximity sensor status
returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
isObjectDetected = detectionState

# Initialize object number
objectID = 0

# Move robot #1 to hover over object
thetas = kinematics.Get_IK_Angles(clientID, [0.5403, -1.100, 0.65], 0, 1)
print(thetas)
movements.Move_To_Position(clientID, thetas, 1)
predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
print("FK prediction: " + str(predicted_loc))
actual_loc = movements.Get_End_Relative_Position(clientID, 1)
print("Actual location: " + str(actual_loc))

# Wait until block has moved in front of proximity sensor
while isObjectDetected == False:
    time.sleep(0.5)
    
    # Re-check for proximity sensor status
    returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
    isObjectDetected = detectionState
# end while

# Block has been detected, lower screwdriver into notch
thetas = kinematics.Get_IK_Angles(clientID, [0.5403, -1.100, 0.611], 0, 1)
movements.Move_To_Position(clientID, thetas, 1)

time.sleep(2)

# Spin screwdriver clockwise
movements.Spin_Screwdriver(clientID, [0.5403, -1.100, 0.611], 1, objectID)


time.sleep(5)

# End simulation
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
vrep.simxGetPingTime(clientID)
print ('All done!')
