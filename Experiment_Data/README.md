# Data obtained from measurements

This folder contains several subfolders which each contain data from one test set. This includes data from teh vie and the laser tracker as well as a YAML regarding the setup (position of lighthouses and laser tracker in regards to the measurement workspace). These workspace measurements are very rough if nothing else has been noted down. All data is raw data extracted from the software. Not Alteration or Processing has been done. Further down each testSet will be explained

## General Settings
The data from the Vive is extracted via [triadOpenVR wrapper](https://github.com/TriadSemi/triad_openvr). On a Windows 10 64bit system. For each position the vive tracker is kept stationary and 1000 measurement points are taken at a freq = 120Hz
The data from the Laser tracker is extracted via software and tranfered to Laptop as .txt or .csv.
The laser tracker is used with TBR 0.5 inch laser reflectors

## Data Naming Scheme

Every test sets is named via the day it was done. Furthermore a "_EXPx" is appended x=1,2,...n. Representing the number of experiment conducted on that day. A testset is considered an experiment if it was done in "one sitting". This is as to prevent change in teh test setup as well as caused by the fact that the Vive Lighthouse system recalibrates itself when either sight of trackers is regained or the system is restarted. This is meant that attention was paid to avoiding that the lighthouse lose sight of the tracker (e.g. not walkign in front)

The data is named regarding its use. RegistrationPoint are refereding to points used for inital registration of the laser reflectors with the connector. Typically there is just one per test set. 
Measurement points are different points within the workspace
laserdata is a list of all measured reflector positions. As the reflector is moved and no annotation is possibel within the program. Exact description of the steps are important.

## Testsets

Every test sets is listed. Any pecularties are explained. Its suitablitliy for further processing is also evaluated.

## 2020.07.10

Tests was conducted using a tripod to hold the tracker and laser reflector and moved within a 1.5x2.50m space. The measurement points mentioned in the data set are marked within the sketch as points the random point are "randomly" located within the space. The origin is marked
The laser tracker measuring procedure was as follows:

* Measure in 3 Points from which origin, x axis, y axis can be computated
* Make a test measurement at y measurement point
* Make a test measurement at the origin point
* Make measurement point for each position 

The problem in this set was that the tripod was moved by hand thus introducing rotation. As only single point measurements were taken no information can be gained regarding the vive positional accuracy without using the vive rotational information. Therefore the position accuracy would become corrupted by the rotation accuracy.

<img src="./experimentSketches/20200710.jpg" width="480">

## 2020.07.17
Two test were conducted with the same setup and procedure. The split was caused to the fact that the Vive Tracker run out of charge and had to be charged. For each measurement position, the laser targets were moved thus allowing to gauge an idea regarding positional and rotational accuracy. The proecdure for the laser tracker was 3 measurements to setup the coordinate system (origin->x->y) then test poitn at y and testpoint at origin. Afterwards for each measurment position the targets were measured and moved in the following fashion (origin position->x axis->y axis->origin position). Thus 4 measurements are taken for each position. The first and last measurements should be within the same (within the std of the laser tracker). 
<img src="./experimentSketches/20200717.jpg" width="480">