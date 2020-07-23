# Data obtained from measurements

This folder contains several subfolders which each contain data from one test set. This includes data from teh vie and the laser tracker as well as a YAML regarding the setup (position of lighthouses and laser tracker in regards to the measurement workspace). These workspace measurements are very rough if nothing else has been noted down. All data is raw data extracted from the software. Not Alteration or Processing has been done. Further down each testSet will be explained

## General Settings
The data from the Vive is extracted via [triadOpenVR wrapper](https://github.com/TriadSemi/triad_openvr). On a Windows 10 64bit system.
The data from the Laser tracker is extracted via software and tranfered to Laptop as .txt or .csv.
The laser tracker is used with TBR 0.5 inch laser reflectors

## Data Naming Scheme

Every test sets is named via the day it was done. Furthermore a "_EXPx" is appended x=1,2,...n. Representing the number of experiment conducted on that day. A testset is considered an experiment if it was done in "one sitting". 

The data is named regarding its use. RegistrationPoint are refereding to points used for inital registration of the laser reflectors with the connector. Typically there is just one per test set. 
Measurement points are different points within the workspace
laserdata is a list of all measured reflector positions. As the reflector is moved and no annotation is possibel within the program. Exact description of the steps are important.

## Testsets

Every test sets is listed. Any pecularties are explained. Its suitablitliy for further processing is also evaluated.

## 2020.07.10

Tests was 
![Sketch for EXP2020.07.10](./experimentSketches/20200710.jpg "test")

## 2020.07.17
