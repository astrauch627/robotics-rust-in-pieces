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

# Move robot #1 to hover over object
thetas = kinematics.Get_IK_Angles(clientID, [0.5403, -1.105, 0.65], 0, 1)
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

# Block has been detected, move robot down to block
# TODO: tune these angle values
thetas = [math.radians(-160), math.radians(-90), math.radians(28), math.radians(58), math.radians(0), math.radians(112.4), math.radians(0)]
movements.Move_To_Position(clientID, thetas)

"""
predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
print("FK prediction: " + str(predicted_loc))
actual_loc = movements.Get_End_Relative_Position(clientID)
print("Actual location: " + str(actual_loc))

time.sleep(5)

# Spin the gripper over block
thetas = [math.radians(-160), math.radians(-90), math.radians(28), math.radians(65.45), math.radians(0), math.radians(112.4), math.radians(1000)]
# TODO: tune these angle values
movements.Move_To_Position(clientID, thetas)
predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
print("FK prediction: " + str(predicted_loc))
actual_loc = movements.Get_End_Relative_Position(clientID)
print("Actual location: " + str(actual_loc))

time.sleep(100)

# End simulation
print ('All done!')
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
"""