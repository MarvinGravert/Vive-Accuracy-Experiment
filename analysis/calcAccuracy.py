# import Analysis.readInData as readInData
import analysis.readInData as readInData
import numpy as np
from scipy.spatial.transform import Rotation as R

def getStd(listOfDatSets):
    tempLength=len(listOfDatSets)
    stdAverage=0
    for dataset in listOfDatSets:
        temp=np.std(dataset,axis=0)
        # print(temp)
        stdAverage+=temp
    
    print("overall:",stdAverage/tempLength)

def turnViveDataIntoHomMatrix(viveData):
    meanData=viveData.mean(0)
    meanRot=R.from_quat(meanData[3:])
    meanVec=meanData[0:3]
    return turnIntoHomMatrix(meanRot,meanVec)

def turnIntoHomMatrix(matrix,vec):
    # print(matrix.as_matrix())
    # print(vec)
    below=np.array([[0,0,0,1]])
    tempVec=np.array(vec).reshape(3,1)
    # print(tempVec)
    
    try:
        tmp=np.hstack([matrix.as_matrix(),tempVec])
    except AttributeError :
        tmp=np.hstack([matrix,tempVec])
    # print(tmp)
    return np.vstack([tmp,below])

def invertHomMatrix(homMatrix):
    tempMatrix=homMatrix[0:3,0:3]
    tempVector=homMatrix[0:3,3]

    tempMatrix=np.linalg.inv(tempMatrix)
    tempVector=-tempMatrix.dot(tempVector)
    return turnIntoHomMatrix(tempMatrix,tempVector)

def pruneLaserData(laserData):
    return laserData[0:3]

def buildHomMatrix(args):
    #take three data points from laserpoint data which forms on KOS
    #calc the transform also transform into m (from mm)
    zeroPoint,xPoint,yPoint=args
    xAxis=xPoint-zeroPoint
    yAxis=yPoint-zeroPoint
    xAxis=xAxis/np.linalg.norm(xAxis)
    yAxis=yAxis/np.linalg.norm(yAxis)
    zAxis=np.cross(xAxis,yAxis)
    yAxis=np.cross(xAxis,zAxis)
    tempMatrix=np.array([xAxis,yAxis,zAxis])
    tempVector=-tempMatrix.dot(zeroPoint )
    
    return turnIntoHomMatrix(tempMatrix,tempVector/1000)   

if __name__=="__main__":
    experimentNumber="2"
    date="20200717"

    offset=10
    matrixLaser2Vive=np.array([[-1,0,0],[0,0,1],[0,1,0]])
    vectorLaser2Vive=np.array([72,offset,-72])
    homMatrixLaser2Vive=turnIntoHomMatrix(matrixLaser2Vive,vectorLaser2Vive/1000)
    # print(homMatrixLaser2Vive)

    laserData=readInData.getLaserData(date, experimentNumber)
    regViveData=readInData.getRegistrationPointData(date,experimentNumber)
    measViveData=readInData.getMeasurementPointData(date,experimentNumber)

    # getStd(measViveData)
    # print(len(measurementPoints))
    # print((s[1][:3]))
    
    regHomeMatrix=turnViveDataIntoHomMatrix(regViveData)
    # print(regHomeMatrix)
    listMeasHomMatrix=[]
    for dataset in measViveData:
        t=turnViveDataIntoHomMatrix(dataset)
        listMeasHomMatrix.append(t)
        # print(type(t))
    num=2
    for num in range(0,7):
        vive2=regHomeMatrix@invertHomMatrix(listMeasHomMatrix[num])
        # print(vive2)


        relLaserData=[]
        for e in laserData:
            relLaserData.append(e[0:3])
        relLaserData=relLaserData[5:]
        laserHomMatrix=[]
        del relLaserData[3::4]#remove every 4th element
        for i in range(0,len(relLaserData),3):
            tmp=[relLaserData[i],relLaserData[i+1],relLaserData[i+2]]
            laserHomMatrix.append(buildHomMatrix(tmp))
        # print(laserHomMatrix[num])

        v1=np.linalg.norm(vive2[0:3,3])
        l1=np.linalg.norm(laserHomMatrix[num][0:3,3])
        print(v1-l1)