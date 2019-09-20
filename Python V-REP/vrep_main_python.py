# -*- coding: utf-8 -*-
"""
Created on Tue Sep 03 11:48:38 2019

@author: astra
"""

import vrep
import sys

# clean up command, closes all opened connections
vrep.simxFinish(-1)

# connect to V-REP
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print ('Connected to remote API server')
else:
    print ('Connection not successful')
    sys.exit('Error: Could not connect')
# end if
    

errorCode_IkTip, IkTip = vrep.simxGetObjectHandle(clientID, 'IRB4600_IkTip', vrep.simx_opmode_oneshot_wait)
errorCode_IkTarget, IkTarget = vrep.simxGetObjectHandle(clientID, 'IRB4600_IkTarget', vrep.simx_opmode_oneshot_wait)
errorCode_auxJoint, auxJoint = vrep.simxGetObjectHandle(clientID, 'IRB4600_auxJoint', vrep.simx_opmode_oneshot_wait)
# Make sure all handles exist
if errorCode_IkTip == 8:
    print ('Error: object handle does not exist')
# end if
if errorCode_IkTarget == 8:
    print ('Error: object handle does not exist')
# end if
if errorCode_auxJoint == 8:
    print ('Error: object handle does not exist')
# end if
