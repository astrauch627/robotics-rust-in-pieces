# -*- coding: utf-8 -*-
"""
Created on Tue Sep 03 11:48:38 2019

@author: astra
"""

import math
import time
import utilities
import vrep

# IMPORTANT: Must start the simulation before running this!

# Connect to V-REP, get client ID
clientID = utilities.Establish_Connection()

# Get handles for all parts within the V-REP scene
SawyerJoints = utilities.Get_Joint_Handles(clientID)
BaxterGripper = utilities.Get_Gripper_Handle(clientID)
    
# Get handle for cylinder, check for errors
returnCode_Cylinder, Cylinder = vrep.simxGetObjectHandle(clientID, 'Cylinder', vrep.simx_opmode_blocking)
if returnCode_Cylinder != 0:
    print('Error: object handle for Cylinder did not return successfully')
# end if
    
# Get handle for proximity sensor, check for errors
returnCode_Prox, ProximitySensor = vrep.simxGetObjectHandle(clientID, 'Proximity_sensor', vrep.simx_opmode_blocking)
if returnCode_Prox != 0:
    print('Error: object handle for Proximity Sensor did not return successfully')
# end if

# Set up RML vectors
accel = 20
jerk = 40
currentVel = [0] * 7
currentAccel = [0] * 7
maxVel = [84*math.pi/180,64*math.pi/180,95*math.pi/180,95*math.pi/180,170*math.pi/180,170*math.pi/180,221*math.pi/180]
maxAccel = [accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180,accel*math.pi/180]
maxJerk = [jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180,jerk*math.pi/180]
targetVel = [0] * 7

# Define waypoints
numWpts = 7
wpts = [0] * numWpts
wpts[0] = [SawyerJoints[0], 90*math.pi/180]
wpts[1] = [SawyerJoints[1], -90*math.pi/180]
wpts[2] = [SawyerJoints[2], -90*math.pi/180]
wpts[3] = [SawyerJoints[3], 90*math.pi/180]
wpts[4] = [SawyerJoints[4], 120*math.pi/180]
wpts[5] = [SawyerJoints[5], 80*math.pi/180]
wpts[6] = [SawyerJoints[6], 2140*math.pi/180]

# Move the robot!
for i in range(numWpts):
    wpt = wpts[i]
    returnCode_pos = vrep.simxSetJointTargetPosition(clientID, wpt[0], wpt[1], vrep.simx_opmode_oneshot)
    returnCode_vel = vrep.simxSetJointTargetVelocity(clientID, wpt[0], targetVel[i], vrep.simx_opmode_oneshot)
    time.sleep(1.0) # Pause for 1 second while robot moves
    
    # Check for errors
    if returnCode_pos != 1 or returnCode_vel != 1:
        print ('Error: movement not registered correctly')
    # end if
    
    # Get proximity sensor measurements
    returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ProximitySensor, vrep.simx_opmode_oneshot)
    if detectionState:
        print ('Sawyer Robot has been detected within the proximity sensor field!')
        print ('Detected Point: '+str(detectedPoint))
    else:
        print ('Sawyer Robot has not been detected within the proximity sensor field!')
    # end if

# end for


# End simulation
print ('All done!')
vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)

