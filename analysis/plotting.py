import analysis.newCalc as ana
import numpy as np
def plotXY(list_hom_Vive,list_hom_laser):
    """Creates a plot of the points of x and y of laser and vive

    Args:
        list_hom_Vive (list): list of 4x4 np.arrays
        list_hom_laser (list): list of 4x4 np.arrays 
    """
    ##First create a list of vive x y 
    list_Vive_XY=[]
    list_Laser_XY=[]
    for i in list_hom_Vive:
        temp=i[0:3,3]
        list_Vive_XY.append(temp[0:2])
    for i in list_hom_laser:
        temp=i[0:3,3,]
        list_Laser_XY.append(temp[0:2])
    print(list_Laser_XY)
    print("\n")
    print(list_Vive_XY)
if __name__=="__main__":
    # data=ana.getDataPairs().listDataPairs
    pairs=ana.getDataPairs()
    pairs.showResults()
    hom_vive=pairs.getListHomMatrixVive_ViveRef()
    hom_laser=pairs.getListHomMatrixLaser_ViveRef()
    plotXY(hom_vive,hom_laser)
    # t=pairs.getListHomMatrixVive()
    # print(t)
    # num=4
    # print("Vive Complete")
    # print(data[num].hom_Vive_registration2measurement)
    # print("Laser")
    # print(ana.calculate_hom_laser2Vive()@data[num].laserDataPoint.hom_registration2measurement@ana.invertHomMatrix(ana.calculate_hom_laser2Vive()))
    # print("Vive incompelte")
    # print(data[num].viveDataPoint.hom_regis2Measurment)

