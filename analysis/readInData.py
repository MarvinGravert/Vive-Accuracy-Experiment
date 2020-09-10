#!/usr/bin/env python3
# ##module that reads in data and then returns it as a matrix 
## used for vive tracker data as well as laser tracker data
import numpy as np
import os
import logging

def readViveData(fileLocation):
        return np.loadtxt(fileLocation, delimiter=" ", skiprows=2)
    
def readLaserData(fileLocation):
        return np.genfromtxt(fileLocation,delimiter=',', skip_header=1)

def getParentDirectoryLevelX(filename,parentLevel=1):
        """find the parent directory of the current working directory and joins\
                the given filename to that directory and returns it.
        Possible to specify the "parent" level. E.g. parentLevel=2 returns \
                the parent directory of the parent directory
        Usage: access to a known file in a different directory further up the\
                file tree.
        Args:
            filename ([string]): [filename which will be joined to parent directory]
            parentLevel (int, optional): [how high up the tree the target directory is]. Defaults to 1.

        Returns:
            [string]: [filename joined to parent directory]
        """
        current_directory = os.path.dirname(__file__)
        for _ in range(0,parentLevel):
            current_directory = os.path.split(current_directory)[0] # Repeat as needed for eg parent of parent dir
        parent_directory=current_directory
        file_path = os.path.join(parent_directory, filename)
        return file_path
def getMeasurementPointData(date, experimentNumber):
        """Imports measurement data from a Vive measurement experiment. This functino handles\
                the import of all measurement points taken during (date,experimentnumber)
                The assumed location is in Experiment_data, in a folder which name consits
                of {date}_Exp{number}. Within the file all measurementPointX.txt are read in 
        Args:
            date ([string]): [date of experiment, format yyyy.mm.dd]
            experimentNumber ([string]): [numbe of the experiment performed on the date]

        Returns:
            [list of numpy arrays]: list of measurements taken at individual. format is \
                    x,y,z,w,i,j,k
        """
        experiment=date+"_Exp"+experimentNumber
        measurementPoints="measurementPoint"
        viveTrackerPointlist=[]
        try:
                counter=1
                while True:
                        filepathMeasPoints="Experiment_Data/"+experiment+"/"+measurementPoints+str(counter)+".txt"
                        filepathToRead=getParentDirectoryLevelX(filepathMeasPoints,parentLevel=1)
                        viveTrackerPointlist.append(readViveData(filepathToRead))
                        counter+=1
        except OSError :
                print("es wurden ", counter-1, "Punkte importiert")
        return viveTrackerPointlist


def getRegistrationPointData(date,experimentNumber):
        """Imports the Vive data set taken at the intial position which all further measurement\
                are referenced to. Date and experiementNumber specify the experiment

        Args:
            date ([String]): Date of experiment format yyyy.mm.dd
            experimentNumber (String): number of experiment performed on that day

        Returns:
            numpy.array: measurement data format is x,y,z,w,i,j,k
        """
        experiment=date+"_Exp"+experimentNumber
        regPoints="registrationPoint.txt"
        filepathRegPoint="Experiment_Data/"+experiment+"/"+regPoints
        filepathToRead=getParentDirectoryLevelX(filepathRegPoint,parentLevel=1)

        return readViveData(filepathToRead)

def getLaserData(date,experimentNumber):
        """Imports the laser data. Includes the full data set. 
                Date and experiementNumber specify the experiment
        Args:
            date (string): [Date of experiment, format yyyy.mm.dd]
            experimentNumber (string): [number of experiment perforemd that day]

        Returns:
            [numpy.array]: [measured data format as specified by Leica, see text file]
        """
        experiment=date+"_Exp"+experimentNumber
        laserTracker=experiment+"_laserData.csv"
        filepathLaserData="Experiment_Data/"+experiment+"/"+laserTracker
        filepathToRead=getParentDirectoryLevelX(filepathLaserData,parentLevel=1)

        return readLaserData(filepathToRead)

if __name__=="__main__":
        experimentNumber="1"
        date="20200827"

        v=getLaserData(date,experimentNumber)
        print(v)