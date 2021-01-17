import analysis.newCalc as ana
import numpy as np
from typing import List
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.tri as tri


def plotXY(list_hom_Vive, list_hom_laser):
    """Creates a plot of the points of x and y of laser and vive

    Args:
        list_hom_Vive (list): list of 4x4 np.arrays
        list_hom_laser (list): list of 4x4 np.arrays
    """
    # First create a list of vive x y
    list_Vive_XY = []
    list_Laser_XY = []
    for i in list_hom_Vive:
        temp = i[0:3, 3]
        list_Vive_XY.append(temp[0:2])
    for i in list_hom_laser:
        temp = i[0:3, 3, ]
        list_Laser_XY.append(temp[0:2])
    print(list_Laser_XY)
    print("\n")
    print(list_Vive_XY)


def plotXYZ(list_hom_Vive, list_hom_laser):
    listViveXYZ = []
    listLaserXYZ = []
    for i in list_hom_Vive:
        temp = i[0:3, 3]
        listViveXYZ.append(temp[0:3])
    for i in list_hom_laser:
        temp = i[0:3, 3, ]
        listLaserXYZ.append(temp[0:3])
    print(listLaserXYZ[0])
    print("\n")
    print(listViveXYZ[0])
    print(listViveXYZ[0].reshape([3, 1])-listLaserXYZ[0])


def plot_heat_map(list_home_laser, list_accuracy):
    # x y plot
    laserXY = np.empty([1, 2])  # nx2 matrix mit x un y werten in
    for i in list_home_laser:
        temp = ana.invertHomMatrix(i)
        laserXY = np.vstack([laserXY, temp[:2, 3].T])  # get x y
    laserXY = laserXY[1:, :]
    # ind = np.argsort(laserXY[:, 1])
    # laserXY = laserXY[ind]
    print(laserXY)
    # fig, ax = plt.subplots()
    x = laserXY[:, 0].tolist()
    x = [i[0] for i in x]
    y = laserXY[:, 1].tolist()
    y = [i[0] for i in y]
    fig, ax = plt.subplots()
    temp = ax.tripcolor(x, y, list_accuracy)
    ax.plot(x, y, 'ko ')
    # ax.set_title('Distance accuracy')
    # set the limits of the plot to the limits of the data
    # ax.axis([x.min(), x.max(), y.min(), y.max()])
    fig.colorbar(temp, ax=ax)
    ax.set_xlim(-200, 3200)
    ax.set_ylim(0, 3200)
    plt.show()


if __name__ == "__main__":
    # data = ana.getDataPairs().listDataPairs
    pairs = ana.getDataPairs()
    # pairs.showResults()
    # pairs.showResultsDistance()
    hom_vive = pairs.getListHomMatrixVive_ViveRef()
    hom_laser = pairs.getListHomMatrixLaser_ViveRef()

    # plotXYZ(hom_vive, hom_laser)
    plot_heat_map(hom_laser, pairs.get_distance_acc())
