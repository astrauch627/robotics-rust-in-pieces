# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:26:26 2019

@author: astra
"""

import constants
import numpy
    
def Calculate_T(thetas):
    """
    This function calculates the transformation matrix to move the robot to
    specified joint angles.
    """
    
    # Initialize T as a 4x4 identity matrix
    T = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    
    # Evaluate T as the product of all e matrices and M
    for i in range(7):
        w = constants.w[i]
        q = constants.q[i]
        e = Calculate_eS(w, q, thetas[i])
        T = numpy.dot(T, e)
    # end for
    M = Calculate_M()
    T = numpy.dot(T, M)
    
    return T
    
# end def
    
def Calculate_eS(w, q, theta):
    """
    This function calculates the e^([S]*theta) matrix for the specified joint
    angle, theta.
    """
    
    # Calculate e^([S]*theta)
    ew = Calculate_ew(w, theta)
    
    # Calculate v
    v = numpy.cross(numpy.dot(-1, w), q)
    
    # Calculate the upper right corner of the e^([S]*theta)
    upper_right = numpy.dot(theta, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    upper_right = numpy.add(upper_right, numpy.dot(1-numpy.cos(theta), skew(w)))
    upper_right = numpy.add(upper_right, numpy.dot(theta - numpy.sin(theta), numpy.dot(skew(w), skew(w))))
    upper_right = numpy.dot(upper_right, v)
    
    eS = [[ew[0][0], ew[0][1], ew[0][2], upper_right[0]], [ew[1][0], ew[1][1], ew[1][2], upper_right[1]], [ew[2][0], ew[2][1], ew[2][2], upper_right[2]], [0, 0, 0, 1]]
    
    return eS
    
# end def
    
def Calculate_ew(w, theta):
    """
    This function calculates the e^([w]*theta) matrix for the specified joint
    angle, theta.
    """
    
    # Caclulate e^([w]*theta)
    # e^([w]*theta) = I + sin(theta)*[w] + (1-cos(theta))*[w]^2
    ew = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    ew = numpy.add(ew, numpy.dot(numpy.sin(theta), skew(w)))
    ew = numpy.add(ew, numpy.dot((1-numpy.cos(theta)), numpy.dot(skew(w), skew(w))))
    
    return ew
    
# end def
    
def skew(a):
    """
    This function calculates the skew symmetric matrix of the input array.
    """
    
    # Print an error if the input array is not 3x1.
    size = numpy.shape(a)
    if (size[0] != 3):
        print("Error: wrong dimensions as input for kinematics.skew()")
    # end if
    
    # Define skew matrix from a
    a_hat = [[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]]
    
    return a_hat
    
# end def
    
def Calculate_M():
    """
    This function calculates the M configuration matrix by defining the zero
    position as when the robot points in the +x direction. This occurs when
    all joint angles are set to zero.
    """
    
    # Find the location of frame {b} in {s}
    pos_bs = numpy.add(constants.Dimensions_Joint1, constants.Dimensions_Joint2)
    pos_bs = numpy.add(pos_bs, constants.Dimensions_Joint3)
    pos_bs = numpy.add(pos_bs, constants.Dimensions_Joint4)
    pos_bs = numpy.add(pos_bs, constants.Dimensions_Joint5)
    pos_bs = numpy.add(pos_bs, constants.Dimensions_Joint6)
    pos_bs = numpy.add(pos_bs, constants.Dimensions_Joint7)
    
    M = [[1, 0, 0, pos_bs[0]], [0, 1, 0, pos_bs[1]], [0, 0, 1, pos_bs[2]], [0, 0, 0, 0]]
    
    return M
    
# end def