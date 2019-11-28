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

#############################################################################
### Setup - move robots 1 and 2 into position
#############################################################################

thetas = [math.radians(90), math.radians(-100), math.radians(0), math.radians(125), math.radians(0), math.radians(-25), math.radians(0)]
movements.Move_To_Position(clientID, thetas, 2)
time.sleep(1)

print('------ Robot #1: screwdriver is just above the stopping point of the block ------')
thetas = kinematics.Get_IK_Angles(clientID, [0.5403, -1.100, 0.65], 0, 1)
print('IK Angles: ' + str(thetas))
predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
print("FK prediction: " + str(predicted_loc))
movements.Move_To_Position(clientID, thetas, 1)
time.sleep(1)
actual_loc = movements.Get_End_Relative_Position(clientID, 1)
print("Actual location: " + str(actual_loc))
print(' ')

for i in range(4):

    objectID = i+1
    
    ##############################################################################
    ### Use proximity sensors to periodically check for the arrival of a block.
    ##############################################################################
    
    # Initialize object detected state to false
    isObjectDetected = False
    
    # Wait until block has moved in front of proximity sensor
    while isObjectDetected == False:
        time.sleep(0.5)
        
        # Re-check for proximity sensor status
        returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor_Handle, vrep.simx_opmode_streaming)
        isObjectDetected = detectionState
    # end while
    
    ##############################################################################
    ### Robot #1 lowers screwdriver into screwhead notch.
    ##############################################################################
    
    # Block has been detected, lower screwdriver into notch
    print('------ Robot #1: screwdriver is in notch ------')
    thetas = kinematics.Get_IK_Angles(clientID, [0.5403, -1.100, 0.614], 0, 1)
    print('IK Angles: ' + str(thetas))
    predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
    print("FK prediction: " + str(predicted_loc))
    movements.Move_To_Position(clientID, thetas, 1)
    time.sleep(0.5)
    actual_loc = movements.Get_End_Relative_Position(clientID, 1)
    print("Actual location: " + str(actual_loc))
    print(' ')
    
    ##############################################################################
    ### Robot #2 aligns suction with block, turns on suction.
    ##############################################################################
    
    movements.Toggle_Suction(clientID, "on")
    time.sleep(0.5)
    thetas = [math.radians(90), math.radians(-94.3), math.radians(0), math.radians(120), math.radians(0), math.radians(-25.7), math.radians(0)]
    movements.Move_To_Position(clientID, thetas, 2)
    
    ##############################################################################
    ### Robot #1 screws the screw into place.
    ##############################################################################
    
    # Spin screwdriver clockwise
    thetas = movements.Spin_Screwdriver(clientID, [0.5403, -1.100, 0.614], 1, objectID)
    time.sleep(0.5)
    
    print('------ Robot #1: after screwing is completed ------')
    print('IK Angles: ' + str(thetas))
    predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
    print("FK prediction: " + str(predicted_loc))
    actual_loc = movements.Get_End_Relative_Position(clientID, 1)
    print("Actual location: " + str(actual_loc))
    print(' ')

    ##############################################################################
    ### Robot #1 returns to hover over the stopping place for the blocks.
    ##############################################################################
    
    print('------ Robot #1: screwdriver is just above the stopping point of the block ------')
    thetas = kinematics.Get_IK_Angles(clientID, [0.5403, -1.100, 0.65], 0, 1)
    print('IK Angles: ' + str(thetas))
    predicted_loc = kinematics.Predict_FK_Position(clientID, thetas)
    print("FK prediction: " + str(predicted_loc))
    movements.Move_To_Position(clientID, thetas, 1)
    time.sleep(0.5)
    actual_loc = movements.Get_End_Relative_Position(clientID, 1)
    print("Actual location: " + str(actual_loc))
    print(' ')
    
    ##############################################################################
    ### Robot #2 removes block from belt.
    ##############################################################################
    
    movements.Toggle_Suction(clientID, "off")
    thetas = [math.radians(90), math.radians(-80), math.radians(0), math.radians(95), math.radians(0), math.radians(-15), math.radians(0)]
    movements.Move_To_Position(clientID, thetas, 2)
    time.sleep(0.5)
    
    ##############################################################################
    ### Robot #2 returns to near the stopping place for the blocks.
    ##############################################################################
    
    thetas = [math.radians(90), math.radians(-100), math.radians(0), math.radians(125), math.radians(0), math.radians(-25), math.radians(0)]
    movements.Move_To_Position(clientID, thetas, 2)
    time.sleep(1)

# end for

# End simulation
print('------ Clean up ------')
vrep.simxGetPingTime(clientID)
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
print ('All done!')
