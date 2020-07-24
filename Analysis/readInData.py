##module that reads in data and then returns it as a matrix 
## used for vive tracker data as well as laser tracker data
import numpy as np
import os


def readViveData(fileLocation):
        return np.loadtxt(fileLocation, delimiter=" ", skiprows=2)
    
def readLaserData(fileLocation):
#     return np.loadtxt(fileLocation, delimiter=",", skiprows=2)
        return np.genfromtxt(fileLocation,delimiter=',')

def getParentDirectoryLevelX(filename,x=1):
    ##finds the x level parent directory of the current working directory
    ##and joins the given filename to that directory and returns it
        current_directory = os.path.dirname(__file__)
        for _ in range(0,x):
            current_directory = os.path.split(current_directory)[0] # Repeat as needed for eg parent of parent dir
        parent_directory=current_directory
        file_path = os.path.join(parent_directory, filename)
        return file_path
def getMeasurementPointData(date, experimentNumber):
        experiment=date+"_Exp"+experimentNumber
        measurementPoints="measurementPoint"
        viveTrackerPointlist=[]
        try:
                counter=1
                while True:
                        filepathMeasPoints="Experiment_Data/"+experiment+"/"+measurementPoints+str(counter)+".txt"
                        filepathToRead=getParentDirectoryLevelX(filepathMeasPoints,x=1)
                        viveTrackerPointlist.append(readViveData(filepathToRead))
                        counter+=1
        except OSError :
                pass
        return viveTrackerPointlist


def getRegistrationPointData(date,experimentNumber):
        experiment=date+"_Exp"+experimentNumber
        regPoints="registrationPoint.txt"
        filepathRegPoint="Experiment_Data/"+experiment+"/"+regPoints
        filepathToRead=getParentDirectoryLevelX(filepathRegPoint,x=1)

        return readViveData(filepathToRead)

def getLaserData(date,experimentNumber):
        experiment=date+"_Exp"+experimentNumber
        laserTracker=experiment+"_laserData.csv"
        filepathLaserData="Experiment_Data/"+experiment+"/"+laserTracker
        filepathToRead=getParentDirectoryLevelX(filepathLaserData,x=1)

        return readLaserData(filepathToRead)