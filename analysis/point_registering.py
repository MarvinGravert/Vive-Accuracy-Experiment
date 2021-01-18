"""
This module shall compute the transformation between the vive and laser system
using a point registering algorithm. This will then be in turn used for error
analysis

Procedure:
Take the points from laser measu in laser KOS and the vive tracker center points
in LH KOS. Throw them into point registering alg (use opencv)
"""
import numpy as np
import cv2
import analysis.newCalc as calc
from typing import Tuple


def somepointmatcher(point_list_1, point_list_2):
    pass


def processViveData(viveData):
    """
    Copy of method in newCalc
    see documentation there
    """
    meanData = viveData.mean(0)  # average across all rows
    # handle quaternions and homogenous matrix
    if len(meanData) == 7:
        meanVec = meanData[0:3]*1000  # m->mm
    elif len(meanData) == 12:
        meanVec = np.array([meanData[3], meanData[7], meanData[11]])*1000
    else:
        print("Something went wrong with the vive data import")
        raise ValueError
    return meanVec


def print_points(list_points, regis):
    # print the points in LH system to stdout

    print(f"""
    \tRegistrationpoint:
    \t{regis}
    \t-------------------------
    """)
    for n, point in enumerate(list_points):
        print(f"""
        {n}. {point}
        ------------------------
        """)


def check_adjust_dimension(point_set: np.ndarray
                           ) -> np.ndarray:
    # check data transmitted in column matrix or in row matrix and transform
    # into column matrix
    row, column = point_set.shape
    if row == 3 and column >= 3:
        # column matrix
        return point_set
    elif row >= 3 and column == 3:
        # row matrix
        return point_set.T
    else:
        raise Exception("Data matrix not correct format")


def register_points(point_set_1: np.ndarray,
                    point_set_2: np.ndarray
                    ) -> Tuple[np.ndarray, np.ndarray]:
    """Find optimal affine transformation between the points sets 


            function used: 
            https://docs.opencv.org/4.0.0/d9/d0c/group__calib3d.html#ga396afb6411b30770e56ab69548724715
    Args:
        point_set_1 (np.ndarray): 3xn 
        point_set_2 (np.ndarray): 3xn

    Returns:
        np.ndarray: returns R (3x3 rot matrix), t (3x1 matrix)
    """
    # Input: expects 3xN matrix of points
    # Returns R,t
    # R = 3x3 rotation matrix
    # t = 3x1 column vector

    A = check_adjust_dimension(point_set_1)
    B = check_adjust_dimension(point_set_2)
    A = A.T
    B = B.T
    retval, out, inlier = cv2.estimateAffine3D(src=A,
                                               dst=B,
                                               ransacThreshold=3,
                                               confidence=0.99,
                                               )
    return out[:, :3], out[:, 3]


if __name__ == "__main__":
    data = calc.getDataPairs().listDataPairs
    list_tracker_center_points = list()
    list_laser_points = list()
    """
    Get the point of the center of the tracker as well as the laser tracker
    so further processing can be done
    """
    for datapair in data:
        vivePoint = datapair.viveDataPoint.pointData
        list_tracker_center_points.append(processViveData(vivePoint))
        laserPoint = datapair.laserDataPoint.zeroVec
        list_laser_points.append(laserPoint)
    regisVive = processViveData(data[0].viveDataPoint.regisPointData)
    """
    Printing the points measured
    """
    # print_points(list_tracker_center_points, regisVive)
    # print_points(list_laser_points, [0, 0, 0])
    """
    Register the points
    """
    vive2LaserRot, vive2LaserVec = register_points(
        np.array(list_tracker_center_points),
        np.array(list_laser_points))
    """
    Use matrix to get points into laser systems
    """
    # combine rot and vec
    hom_vive2Laser_base = calc.makeHomogenousMatrix(
        vive2LaserRot, vive2LaserVec)
    # bring all to the laserBasis
    hom_vive_laserRef = list()
    for datapair in data:
        hom_vive_laserRef.append(
            hom_vive2Laser_base@datapair.viveDataPoint.hom_measurement2Lighthouse)
    hom_laser_laserRef = calc.getDataPairs().getListHomMatrixLaser_LaserRef()
    list_laser2Tracker = list()
    for laser, vive in zip(hom_laser_laserRef, hom_vive_laserRef):
        t = laser@vive
        print(t)
        list_laser2Tracker.append(t)
    # print(list_laser2Tracker)
    """
    Compare the vectors again
    """
