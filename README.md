# Vive Accuracy Experiment

Herein are stored: all files, tools and data necessary to evaluate and reproduce the experiment conducted to measure the accuracy of the Vive Pro Lighthouse Pose Estimation system.

## Motivation

To use AR in a production environment to control a robot, the AR system has to be calibrated/registrated with the robot coordinate system. This is not a trivial problem especially if it is to be expanded to a larger area on the shop floor where the worker is freely moving.
The AR system which shall be explored belongs to the group of "Head-Mounted Optical See Through Displays" specifically the Hololens. The standard localization of the hololens is the built-in closed source SLAM algorithm. This algorithm yields accuracy value ranging form 7-15mm. This project wants to explore the option of using the vive system to track the hololens in space. The hope is to have a higher accurcy/precision and hence a more accurate robot control.

## Project overview

Initially the (static) accuracy of the vive is tested and in the second step the system is integrated into a Hololens->Robot workflow. This repo only concerns itself with the first step.

### Experiments overview

**Finding accuracy of Vive Pro LH 2.0**
Multiple experiments wherein the Vive system accuracy is checked against a laser tracker. 

**Finding center of Vive Pro LH 2.0**
To easily reference the Vive with external system such as a robot. The KOS of the Vive has to be known

**Recalibration behavior of SteamVR**
The vive 1.0 system has reportedly problems with recalibration in the sense that once an visual contact to an trackable object is lost for a longer period of time. Upon reentry of said object a recalibratino of the interior planes happends. 
This is experiment is to test against that.

## Structure of repo

**Analysis**
All files and scripts relating to the analysis of the experiment data. Such as data reader, plotting function, etc. This contains the analysis pipeline used for the Results/discussion.

**Tools**
Information to the tools used to conduct the experiments

**Procedure**
A detailed description of the procedure and setup of the experiments

**Experiment_Data**
Data obtained through experiments. Also contains more detailed information regarding the experiments, such as any deviation from the standard procedure.

**Results/Discussion**
To be done
Discussion and visual representation of results

