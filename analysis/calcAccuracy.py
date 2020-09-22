#!/usr/bin/env python3
# # import Analysis.readInData as readInData
#TODO: Laserdata reasonable filter: check between 1 and 4 measurement if below threshold
#TODO: Better result display: Show: overall accuracy per point std, overall std
#TODO: check in turnVivedataIntoMatrix if minus infront of meanvec
import analysis.readInData as readInData
import numpy as np
from scipy.spatial.transform import Rotation as R

# def getStd(listOfDatSets):
#     tempLength=len(listOfDatSets)
#     stdAverage=0
#     for dataset in listOfDatSets:
#         temp=np.std(dataset,axis=0)
#         # print(temp)
#         stdAverage+=temp
    
#     print("overall:",stdAverage/tempLength)

def turnViveDataIntoHomMatrix(viveData):
    '''
    Takes the data from the vive (format x y z w i j k) and returns a homogenous matrix
    Input: array of row vectors 
    Output: Homogenous matrix represnting the transformation
    '''    
    meanData=viveData.mean(0)#average across all rows
    w,i,j,k=meanData[3:]
    meanRot=R.from_quat([w,i,j,k])
    meanVec=meanData[0:3]
    return turnIntoHomMatrix(meanRot,meanVec)#potentially put a minus

def turnIntoHomMatrix(matrix,vec):
    '''
    Takes a 3x3 matrix and a 3x1 vector and turns them into a homogenous matrix. No changes are done to 
    either and they are simply put into a matrix
    '''
    below=np.array([[0,0,0,1]])
    tempVec=np.array(vec).reshape([3,1])
    
    try:
        tmp=np.hstack([matrix.as_matrix(),tempVec])
    except AttributeError :
        tmp=np.hstack([matrix,tempVec])
    return np.vstack([tmp,below])

def invertHomMatrix(homMatrix):
    tempMatrix=homMatrix[0:3,0:3]
    tempVector=homMatrix[0:3,3]

    tempMatrix=np.linalg.inv(tempMatrix)
    tempVector=-tempMatrix.dot(tempVector)
    return turnIntoHomMatrix(tempMatrix,tempVector)

def pruneLaserData(laserData):
    return laserData[0:3]

def buildHomMatrixfromLaser(args):
    #take three data points from laserpoint data which forms on KOS
    #calc the transform also transform into m (from mm)
    zeroPoint,xPoint,yPoint=args
    
    xAxis=xPoint-zeroPoint
    yAxis=yPoint-zeroPoint
    xAxis=xAxis/np.linalg.norm(xAxis)
    yAxis=yAxis/np.linalg.norm(yAxis)
    zAxis=np.cross(xAxis,yAxis)
    # yAxis=np.cross(zAxis,xAxis)
    # xAxis=np.cross(zAxis,yAxis)
    tempMatrix=np.array([xAxis,yAxis,zAxis])
    
    tempMatrix=np.array([xAxis,yAxis,zAxis]).transpose()
    tempMatrix=np.linalg.inv(tempMatrix)
    tempVector=-tempMatrix.dot(zeroPoint/1000)
    
    return turnIntoHomMatrix(tempMatrix,tempVector)   

def getMatrices(experimentNumber,date):
    ##RESULT 3 Matrices:
    #Homogenous Matrix  Lighthouse to Tracker at zero: registration point
    #list ofHomMatrix: Vive2Tracker at x measurement Points 
    #list HomMatrix: zero lasertracker to x measuremetn point (laser2measurement Point
    #read data into Matrix
    laserData=readInData.getLaserData(date, experimentNumber)
    regViveData=readInData.getRegistrationPointData(date,experimentNumber)
    measViveData=readInData.getMeasurementPointData(date,experimentNumber)

    ######Processing of data#######
    #make homegenous matrix (homMatrix) out of data
    regHomMatrix=turnViveDataIntoHomMatrix(regViveData)

    listMeasHomMatrix=[]
    for dataset in measViveData:
        t=turnViveDataIntoHomMatrix(dataset)
        listMeasHomMatrix.append(t)

    relLaserData=[]
    for e in laserData:
        relLaserData.append(e[0:3])
    relLaserData=relLaserData[5:]
    laserHomMatrix=[]
    del relLaserData[3::4]#remove every 4th element
    for i in range(0,len(relLaserData),3):
        tmp=[relLaserData[i],relLaserData[i+1],relLaserData[i+2]]
        laserHomMatrix.append(buildHomMatrixfromLaser(tmp))
    return [regHomMatrix,listMeasHomMatrix,laserHomMatrix]

if __name__=="__main__":
    
    #define which dataset
    experimentNumber="2"
    # date="20200917"
    # date="20200717"
    date="20200918"
    #set transformation between reflectors and trakcer
    offset=10
    #black
    matrixLaser2Vive=np.array([[-1,0,0],[0,0,1],[0,1,0]])
    vectorLaser2Vive=np.array([62,offset,-62])
    #red
    matrixLaser2Vive=np.array([[0,-1,0],[0,0,1],[-1,0,0]])
    # matrixLaser2Vive=np.array([[0,1,0],[1,0,0],[0,0,-1]])#fixed so that this aligns
    matrixLaser2Vive=np.linalg.inv(matrixLaser2Vive.transpose())
    vectorLaser2Vive=np.array([62,offset,62])/1000#solid mistake 72 statt 62...
    homMatrixLaser2Vive=turnIntoHomMatrix(matrixLaser2Vive,vectorLaser2Vive)
    # print(homMatrixLaser2Vive)
    
    
    regHomMatrix,listMeasHomMatrix,laserHomMatrix=getMatrices(experimentNumber,date)
    # print(laserHomMatrix)
    ######Analysis#######
    #calc the transformation between registrationpoint and x measurementpoint
    #compare the transformation with the one of the lasertracker (or rather the norm of the distance traveld)
    sumAcc=0
    accArray=[]
    for num in range(0,len(listMeasHomMatrix)): 

        vive2=listMeasHomMatrix[num]@invertHomMatrix(regHomMatrix)
        vive2=invertHomMatrix(homMatrixLaser2Vive)@invertHomMatrix(listMeasHomMatrix[num])@regHomMatrix@homMatrixLaser2Vive

        v1=np.linalg.norm(vive2[0:3,3])
        l1=np.linalg.norm(laserHomMatrix[num][0:3,3])
        # print((v1-l1)*1000)
        print(np.sqrt(((v1-l1)*1000)**2))
        sumAcc+=np.sqrt(((v1-l1)*1000)**2)
        accArray.append(np.sqrt(((v1-l1)*1000)**2))
    sumAcc/=len(listMeasHomMatrix)
    print("sum: ",sumAcc)
    print("std: ",np.std(accArray))
    # p=np.array([72,offset,72,1000])/1000
    # t=listMeasHomMatrix[0]@p
    # t0=regHomMatrix@p
    # print(t)
    # print(t0)
    # print(t-t0)
    # print(np.linalg.norm(t-t0))


    ##testing transformation 
    # t=invertHomMatrix(homMatrixLaser2Vive)@listMeasHomMatrix[0]@invertHomMatrix(regHomMatrix)@homMatrixLaser2Vive
    # print(t)
    t=invertHomMatrix(homMatrixLaser2Vive)@invertHomMatrix(listMeasHomMatrix[3])@regHomMatrix@homMatrixLaser2Vive
    print(t)
    print(laserHomMatrix[3])
    # x is correct
    # y needs to be -z
    # z needs to be y


    # s=buildHomMatrixfromLaser([np.array([3.0,0.0,0.0]),np.array([3.0,2.0,0.0]), np.array([-1.0,0.0,0.0])])#
    # print(s)
    # a=np.array([-4485.1332,660.3783,-395.7873])
    # b=np.array([-4584.3205,734.3694,-390.3263])
    # c=np.array([-4559.0378,561.0136,-396.2159])
    # d=np.array([-4584.3205,734.3694,-390.3263,1000]).reshape([4,1])/1000#c=y axis

    # t=buildHomMatrixfromLaser([a,b,c])
    # print(t)
    # print(t@d)
    