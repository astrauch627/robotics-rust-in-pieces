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

# Get end-effector handle
joint_handles = utilities.Get_Joint_Handles(clientID)
end_effector_handle = joint_handles[6]
returnCode, base_handle = vrep.simxGetObjectHandle(clientID, 'Sawyer_link0_visible', vrep.simx_opmode_blocking)

# Move robot to hover over object
# TODO: tune these angle values
thetas = [math.radians(-150), math.radians(-90), math.radians(0), math.radians(50), math.radians(0), math.radians(110), math.radians(0)]
movements.Move_To_Position(clientID, thetas)
predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
print("Predicted location of the end-effector: " + str(predicted_loc))
returnCode, actual_loc = vrep.simxGetObjectPosition(clientID, end_effector_handle, base_handle, vrep.simx_opmode_streaming)
print("Actual location of the end-effector: " + str(actual_loc))


# Wait until block has moved in front of proximity sensor
while isObjectDetected == False:
    time.sleep(1)
    
    # Re-check for proximity sensor status
    returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
    isObjectDetected = detectionState
# end while
    
# When block is detected, move robot down to block
# TODO: tune these angle values
thetas = [math.radians(-160), math.radians(-90), math.radians(28), math.radians(58), math.radians(0), math.radians(112.4), math.radians(0)]
movements.Move_To_Position(clientID, thetas)
predicted_loc = kinematics.Predict_FK_Position(thetas)
print("Predicted location of the end-effector: " + str(predicted_loc))

time.sleep(5)

# Spin the gripper over block
thetas = [math.radians(-160), math.radians(-90), math.radians(28), math.radians(65.45), math.radians(0), math.radians(112.4), math.radians(1000)]
# TODO: tune these angle values
movements.Move_To_Position(clientID, thetas)
predicted_loc = kinematics.Predict_FK_Position(thetas)
print("Predicted location of the end-effector: " + str(predicted_loc))

time.sleep(100)

# End simulation
print ('All done!')
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
