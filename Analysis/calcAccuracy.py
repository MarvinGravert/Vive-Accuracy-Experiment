import readInData
import numpy as np

def getStd(listOfDatSets):
    tempLength=len(listOfDatSets)
    stdAverage=0
    for dataset in listOfDatSets:
        temp=np.std(dataset,axis=0)
        print(temp)
        stdAverage+=temp
    
    print("overall:",stdAverage/tempLength)
if __name__=="__main__":
    experimentNumber="1"
    date="20200717"


    s=readInData.getLaserData(date, experimentNumber)
    t=readInData.getMeasurementPointData(date,experimentNumber)

    getStd(t)
    # print((s[1][:3]))