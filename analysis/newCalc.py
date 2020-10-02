import analysis.readInData as readInData
import numpy as np
from scipy.spatial.transform import Rotation as R #numpy doesnt have quaternion support natively
import logging
import analysis.const as const
import sys

class LaserDataPoint():
    """Represents the data point measured by the laser system 
    differnce lies in the point and  the axis 
    """
    def __init__(self,zeroVec, xVec, yVec, num):
        """
        Args:
            zeroVec (numpy.array): zero pos of new measurement point in laser KOS
            xVec (numpy.array): x position point in laser KOS
            yVec (numpy.array): y position point in laser KOS
            num (int): number of measurement point
        """
        self.zeroVec,self.xVec,self.yVec,self.num=zeroVec,xVec,yVec,num
        self.hom_registration2measurement=buildHomMatrixfromLaser(self.zeroVec,self.xVec,self.yVec)

    
class ViveDataPoint():
    """Represents a measurement point taken from the vive system
    """
    def __init__(self,pointData,regisPointData,num):
        """
        Args:
            pointData (numpy.array): data taken at measurement point
            regisPointData (numpy.array): data taken at zero position, used as reference
            num (int): number of measurement point
        """
        self.pointData=pointData#data taken at this point
        self.regisPointData=regisPointData##data at the origin of the system
        self.num=num
        self.hom_measurement2Lighthouse=self.processDataIntoHomogenMatrix(self.pointData)
        self.hom_registration2Lighthouse=self.processDataIntoHomogenMatrix(self.regisPointData)

        self.hom_regis2Measurment=invertHomMatrix(self.hom_measurement2Lighthouse)@self.hom_registration2Lighthouse

        self.std=np.std(self.pointData,axis=0)

    def processDataIntoHomogenMatrix(self,viveData):
        """Takes the data taken at a vive measurement point and returns the homogenous transformation
        from the tracked element (the tracker) to the lighthouse. 
        The n measurements are averaged, the translation is transformed to milimeters

        Args:
            viveData ([type]): [description]

        Returns:
            numpy.array: homogenous matrix
        """
        '''
        Takes the data from the vive (format x y z w i j k) and returns a homogenous matrix
        Input: array of row vectors 
        Output: Homogenous matrix represnting the transformation
        '''    
        meanData=viveData.mean(0)#average across all rows
        #handle quaternions and homogenous matrix
        if len(meanData)==7:
            w,i,j,k=meanData[3:]
            meanRot=R.from_quat([w,i,j,k])
            # meanRot=R.from_quat([i,j,k,w])
            meanVec=meanData[0:3]*1000#m->mm
            return makeHomogenousMatrix(meanRot,meanVec)
        if len(meanData)==12:
            meanRot=np.array([meanData[0:3],meanData[4:7],meanData[8:11]])
            meanVec=np.array([meanData[3],meanData[7],meanData[11]])*1000
            return makeHomogenousMatrix(meanRot,meanVec)
        else:
            logging.warning("Something went wrong with the vive data import")
    

class CollectionDataPairs():
    def __init__(self,listDataPairs):
        self.listDataPairs=listDataPairs
        sumAcc=0
        accCollect=[]
        for i in listDataPairs:
            sumAcc+=i.distanceAcc
            accCollect.append(i.distanceAcc)
        self.acc=sumAcc/len(listDataPairs)
        self.std=np.std(accCollect,0)
    def getListHomMatrixVive_ViveRef(self):
        listHomVive=[]
        for i in self.listDataPairs:
            listHomVive.append(i.viveDataPoint.hom_regis2Measurment)
        return listHomVive
    def getListHomMatrixLaser_LaserRef(self):
        listHomLaser=[]
        for i in self.listDataPairs:
            listHomLaser.append(i.laserDataPoint.hom_registration2measurement)
        return listHomLaser
    def getListHomMatrixLaser_ViveRef(self):
        listHomLaser=[]
        temp=calculate_hom_laser2Vive()
        for i in self.listDataPairs:
            listHomLaser.append(temp@i.laserDataPoint.hom_registration2measurement@invertHomMatrix(temp))
        return listHomLaser
    def getListHomMatrixVive_LaserRef(self):
        listHomViveComplete=[]
        for i in self.listDataPairs:
            listHomViveComplete.append(i.hom_Vive_registration2measurement)
        return listHomViveComplete
    def showResults(self):
        print(f"Overall Accuracy: {self.acc}")
        print(f"Standard deviation: {self.std}")
    def showResultsDistance(self):
        for i in self.listDataPairs:
            print(i.distanceAcc)

class DataPair():
    def __init__(self,viveDataPoint, LaserDataPoint,hom_laser2vive):
        self.viveDataPoint=viveDataPoint
        self.laserDataPoint=LaserDataPoint
        self.hom_laser2vive=hom_laser2vive
        self.num=self.checkNum()
        self.hom_Vive_registration2measurement=invertHomMatrix(self.hom_laser2vive)@self.viveDataPoint.hom_regis2Measurment@self.hom_laser2vive
        # if self.num==1:
        #     print(self.hom_Vive_registration2measurement)
        #     print(self.laserDataPoint.hom_registration2measurement)
        self.distanceAcc=self.pointAccuracyDistance(self.hom_Vive_registration2measurement,self.laserDataPoint.hom_registration2measurement)



    def pointAccuracyDistance(self,hom_vive,hom_laser):
        viveDistanceNorm=np.linalg.norm(hom_vive[:3,3])
        laserDistanceNorm=np.linalg.norm(hom_laser[:3,3])
        # print(np.linalg.norm(viveDistanceNorm-laserDistanceNorm))
        return np.linalg.norm(viveDistanceNorm-laserDistanceNorm)

    def checkNum(self):
        
        if not self.viveDataPoint.num==self.laserDataPoint.num:
            logging.warning("measurement points are not aligned")
        return self.viveDataPoint.num
    def showResult(self):
        s=f"Num {self.num} Accuracy: {self.distanceAcc}"
        return s
        
def buildHomMatrixfromLaser(originPoint,xPoint,yPoint):
    """Takes three points given in System A. Returns Transform A->B whereby B is defined by the three points
        The points cant be colinear (or as assumed to not be colinear)
        
    Args:
        basePoints ([list of np.array]): [holds three points each represented by an array]

    Returns:
        [np.array]: [transformation matrix ]
    """
    #take three data points from laserpoint data which forms on KOS
    #calc the transform also transform into m (from mm)
    #TODO Create a plane via the Z vector and compare the distance between the plane and the three points
    #TODO if idealized via cross product check the angle difference between idalized and new axis
    
    xAxis=xPoint-originPoint
    yAxis=yPoint-originPoint
    xAxis=xAxis/np.linalg.norm(xAxis)
    yAxis=yAxis/np.linalg.norm(yAxis)

    zAxis=np.cross(xAxis,yAxis)
    yAxis=np.cross(zAxis,xAxis)
    # xAxis=np.cross(zAxis,yAxis)

    
    tempMatrix=np.array([xAxis,yAxis,zAxis])
    tempVector=-tempMatrix.dot(originPoint)
    return makeHomogenousMatrix(tempMatrix,tempVector) 

def makeHomogenousMatrix(matrix,vec):
    """Takes a 3x3 matrix and a 3x1 vector and turns them into a homogenous matrix. No changes are done to 
    either and they are simply put into a matrix.
    This can handle numpy arrays and scipy.rot matrices

    Args:
        matrix ([numpy.array, or scipy.rotation]): 3x3 matrix
        vec ([numpy.array]): 3x1 vector or 1x3 vector

    Returns:
        [numpy.array]: 4x4 homogenous matrix
    """
    
    below=np.array([[0,0,0,1]])
    tempVec=np.array(vec).reshape([3,1])
    
    try:
        tmp=np.hstack([matrix.as_matrix(),tempVec])#if it isnt a scipy.rotation an error will be thrown
    except AttributeError :
        tmp=np.hstack([matrix,tempVec])
    return np.vstack([tmp,below])

def reasonable(laserData):
    """Takes the unproccessed laser data and does the following reasonability checks:
    1. Was the reference system via the frist three data points corrected made?
    2. Are measurement 1 and 4 of each data point within an acceptable range? Thus showing no motion within measurements taken
    3. Is the whole data set complete and useable?
    If check 1 fails, no array will be output. If check 2  or 3 fail for a measurement point, that point will be deleted. 
    The verified laserData is returned.

    Args:
        laserData (numpy.array): [nx24]. first 5 rows reference system. following measurement in groups of 4

    Returns:(not used atm)
        list([numpy.array],[list]): [mx24] m<=n can return empty array if data is not suitable; list of position number of excluded measurement points
    """
    closeProgramFlag=False
    ##Check if total std is good enough
    if max(laserData[:,6])>const.THRESHOLD_FOR_EXCLUSION:#total std of the measurement is handed over by the laser
        logging.warning('laserThreshold exceeded. Dataset will not be considered')
        closeProgramFlag=True 
        
    ##Check if the reference was created correctly. First three points base system, next two are test
    baseSys=laserData[0:3,0:3]
    testSys=laserData[3:5,0:3]
    T=buildHomMatrixfromLaser(baseSys[0,:],baseSys[1,:],baseSys[2,:])
    #Compare y vector with new y vector
    #TODO: check distance of x,y points from plane created by z vector and zero point
    #TODO: output angle error (non rectangluarness) between x and y axis pre transform
    #TODO: check that the non rectangluarness isnt above threshold
    test_y_vector=np.append(testSys[0,:],[1],0)
    test_zero_point=np.append(testSys[1,:],[1],0)
    base_y_vector=T@np.append(baseSys[2,:],[1],0)#yVector in base system
    base_zero_vector=T@np.append(baseSys[0,:],[1],0)#zeroVector in base system
    diffYVector=np.linalg.norm(test_y_vector-base_y_vector)
    diffZeroVector=np.linalg.norm(test_zero_point-base_zero_vector)
    if diffYVector>const.THRESHOLD_FOR_EXCLUSION or diffZeroVector>const.THRESHOLD_FOR_EXCLUSION:
        logging.warning('laserThreshold exceeded. Dataset will not be considered') 
        closeProgramFlag=True
        
    ##Check if dataset is complete? Check if data is in groups of four and points 1 and 4 are roughly the same 
    ##also check if they points are not colinear
    dataToCheck=laserData[5:,:3]#first 5 data points dont matter
    numRows=np.size(dataToCheck,0)
    if not numRows%4:
        logging.info("Data rows match up")
        closeProgramFlag=False
    else:
        logging.warning("Data rows does not match ")
        closeProgramFlag=True
        return closeProgramFlag
    ##Check difference between 1 and 4 if below threshold. Basically check if it has been moved
    for i in range(0,int(numRows/4)):
        zero=dataToCheck[i*4]
        zero_Check=dataToCheck[i*4+3]
        zeroDiff=np.linalg.norm(zero-zero_Check)
        if zeroDiff>const.THRESHOLD_FOR_EXCLUSION:
            logging.warning(f"Measurement {i} Deviation too large. The error is {zeroDiff}")
    return not closeProgramFlag
def preProcessLaser(laserdata):
    """ Preprocess the laser data for later use:
    -cut away all data thats not related to position
    -truncate the data used for initialisation of the KOS
    Args:
        laserdata (numpy.array): [Raw data from the laser printer ]

    Returns:
        [numpy.array]: [PreprocessData]
    """
    preparedData=laserdata[5:,:3]
    preparedData=np.delete(preparedData,np.s_[3::4],0)
    return preparedData

def invertHomMatrix(homMatrix):
    """invert a homogenous matrix
    Source. https://mathematica.stackexchange.com/questions/106257/how-do-i-get-the-inverse-of-a-homogeneous-transformation-matrix
    Args:
        homMatrix (numpy.array): 4x4 unscaled homogenous matrix

    Returns:
        numpy.array: 4x4 unscaled homogenous matrix
    """
    tempMatrix=homMatrix[0:3,0:3]
    tempVector=homMatrix[0:3,3]

    tempMatrix=np.linalg.inv(tempMatrix)
    tempVector=-tempMatrix@(tempVector)
    return makeHomogenousMatrix(tempMatrix,tempVector)

def calculate_hom_laser2Vive():
    """calculate homogenous matrix from laser target holder system to vive tracker
        the position of the vive in the laser KOS is independent of the chosen KOS (black or red)
        the roation depends on which KOS system was chosen (black or red)

    Returns:
        numpy.array: 4x4 transformation matrix
    """    
    vivePosition=np.array([62,62,-const.TARGET_HOLDER_OFFSET])#in laser system
    if const.COORDINATE_SYSTEM=="BLACK":
        rot_laser2Vive=np.matrix(const.LASER2VIVE_ROT_MATRIX_BLACK)
    if const.COORDINATE_SYSTEM=="RED":
        rot_laser2Vive=np.matrix(const.LASER2VIVE_ROT_MATRIX_RED)
    hom_laser2Vive=makeHomogenousMatrix(rot_laser2Vive,-rot_laser2Vive@vivePosition)
    # print(hom_laser2Vive)
    return hom_laser2Vive

def main():
    logging.basicConfig(level=logging.INFO,format='%(name)s - %(levelname)s - %(message)s')
    ##########BASE INFORMATION########
    experimentNumber=const.EXPERIMENT_NUMBER
    date=const.DATE
    logging.info(f"Considering Data from Experiment {const.EXPERIMENT_NUMBER} on {const.DATE}")
    ####READ In LASER DATA and check it####
    laserData=readInData.getLaserData(date, experimentNumber)
    if not reasonable(laserData):#if failed
        sys.exit()
    ##Preprocess laserData
    preProcLaserData=preProcessLaser(laserData)
    #####READ in Vive Data####
    viveData_regisPoint=readInData.getRegistrationPointData(date,experimentNumber)
    viveData_measurePoints=readInData.getMeasurementPointData(date,experimentNumber)
    ##Get transformation from laser system to vive
    hom_laser2vive=calculate_hom_laser2Vive()
    ################Create vive point ot laser point connection###############
    counter=1#point 0 is the registration point 
    laserCounter=0#helper to iterate over laser array
    list_dataPairs=[]
    for viveDataPoint in viveData_measurePoints:
        tempVive=ViveDataPoint(viveDataPoint,viveData_regisPoint,counter)
        tempLaser=LaserDataPoint(preProcLaserData[laserCounter*3,:],preProcLaserData[laserCounter*3+1,:],\
            preProcLaserData[laserCounter*3+2,:],counter)
        list_dataPairs.append(DataPair(tempVive,tempLaser,hom_laser2vive))
        counter+=1
        laserCounter+=1
    ##show results
    for i in list_dataPairs:
        print(i.showResult())
    CollectionDataPairs(list_dataPairs).showResults()
def getDataPairs():
    #logging.basicConfig(level=logging.INFO,format='%(name)s - %(levelname)s - %(message)s')
    ##########BASE INFORMATION########
    experimentNumber=const.EXPERIMENT_NUMBER
    date=const.DATE
    logging.info(f"Considering Data from Experiment {const.EXPERIMENT_NUMBER} on {const.DATE}")
    ####READ In LASER DATA and check it####
    laserData=readInData.getLaserData(date, experimentNumber)
    if not reasonable(laserData):#if failed
        sys.exit()
    ##Preprocess laserData
    preProcLaserData=preProcessLaser(laserData)
    #####READ in Vive Data####
    viveData_regisPoint=readInData.getRegistrationPointData(date,experimentNumber)
    viveData_measurePoints=readInData.getMeasurementPointData(date,experimentNumber)
    ##Get transformation from laser system to vive
    hom_laser2vive=calculate_hom_laser2Vive()
    ################Create vive point ot laser point connection###############
    counter=1#point 0 is the registration point 
    laserCounter=0#helper to iterate over laser array
    list_dataPairs=[]
    for viveDataPoint in viveData_measurePoints:
        tempVive=ViveDataPoint(viveDataPoint,viveData_regisPoint,counter)
        tempLaser=LaserDataPoint(preProcLaserData[laserCounter*3,:],preProcLaserData[laserCounter*3+1,:],\
            preProcLaserData[laserCounter*3+2,:],counter)
        list_dataPairs.append(DataPair(tempVive,tempLaser,hom_laser2vive))
        counter+=1
        laserCounter+=1
    return CollectionDataPairs(list_dataPairs)

if __name__=="__main__":
    main()
    # t=np.array([[-0.05826370418071747, 0.9980254173278809, 0.02346029318869114, -1.4323045015335083], [-0.008331798948347569, 0.02301337756216526, -0.9997003078460693, -0.6669083833694458], [-0.998266339302063, -0.05844183266162872, 0.00697462260723114, -0.9444524645805359],[0,0,0,1]])
    # print(t)
    # print(invertHomMatrix(t))