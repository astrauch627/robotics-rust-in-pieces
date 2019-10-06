# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:26:26 2019

@author: astra
"""

import constants
import numpy

def Calculate_M():
    """
    This function calculates the M configuration matrix by defining the zero
    position as when the robot points in the +x direction. This occurs when
    all joint angles are set to zero.
    """
    
    # Find the location of frame {M} in {S}
    pos_MinS = numpy.add(constants.Dimensions_Link0, constants.Dimensions_Link1)
    pos_MinS = numpy.add(pos_MinS, constants.Dimensions_Link2)
    pos_MinS = numpy.add(pos_MinS, constants.Dimensions_Link3)
    pos_MinS = numpy.add(pos_MinS, constants.Dimensions_Link4)
    pos_MinS = numpy.add(pos_MinS, constants.Dimensions_Link5)
    pos_MinS = numpy.add(pos_MinS, constants.Dimensions_Link6)
    pos_MinS = numpy.add(pos_MinS, constants.Dimensions_Link7)
    
    M = [[1, 0, 0, pos_MinS[0]], [0, 1, 0, pos_MinS[1]], [0, 0, 1, pos_MinS[2]], [0, 0, 0, 0]]
    
    return M
    
# end def