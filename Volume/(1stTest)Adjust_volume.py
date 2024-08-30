#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:17:53 2024

@author: rdetugny
"""
import matplotlib.pyplot as plt

# =============================================================================
# This script was made before the Paraview macro to compute the 
# target volumes and make a prediction of the corresponding scale
# factor, based on a linear approximation.
# =============================================================================
def TargetVolumes(V0):
    V1upopt=V0*0.11+V0
    V1downopt=V0*-0.11+V0
    print(V1upopt,V1downopt)

#%% Case 3
V0=5.654463918811926e-8
V1opt=V0*0.11+V0

V1L=[5.02747394419825e-8,5.03348648287061e-8,5.063779195450746e-8,5.068656323980955e-8,5.069904435386983e-8,5.094346949342594e-8,5.937297773538264e-8,5.966428368530951e-8,6.235448877206166e-8,6.258569382822684e-8,6.273798710923732e-8,6.281496498906916e-8,6.287663082112336e-8,6.296924705086345e-8]
RG=[]
for V1 in V1L:
    RG.append((V1-V0)/V0)
print(RG)

scale=[-2425,-2400,-2275,-2255,-2249.88444383636,-2150,1000,1100,2000,2075.4542327244576,2125,2150,2170,2200]
plt.plot(scale,RG)
plt.show()

slope=(RG[-1]-RG[0])/(scale[-1]-scale[0])
ScalePred=-0.11/slope
print("Prediction: ", ScalePred)

#%% Case 8
V0=2.016245397844541e-8
V1opt=V0*0.11+V0

scale=[-5000,-4950,-4900,-4720,2150,4200,4300,4380,4420]
V1L=[1.79280136713846e-8,1.7948933984070933e-8,1.7969871866227376e-8,1.8045494458362733e-8,2.1214133137522228e-8,2.227089646060378e-8,2.23237994230597e-8,2.236622174075885e-8,2.2387471430299605e-8]
RG=[]
for V1 in V1L:
    RG.append((V1-V0)/V0)
print(RG)

plt.plot(scale,RG)
plt.show()

slope=(RG[-1]-RG[0])/(scale[-1]-scale[0])
ScalePred=-0.11/slope
print("Prediction: ", ScalePred)

#%% Case 9
V0=3.068941826909448e-8
V1upopt=V0*0.11+V0
V1downopt=V0*-0.11+V0

scale=[-2900,-2700,1500,2386,2400,2600,4420]
V1L=[2.7305888693540575e-8,2.7524880334507335e-8,3.261817146126859e-8,3.3818417394814315e-8, 3.383775751620318e-8,3.411518235769362e-8,3.674890886465099e-8]
RG=[]
for V1 in V1L:
    RG.append((V1-V0)/V0)
print(RG)

plt.plot(scale,RG)
plt.show()

slope=(RG[-1]-RG[0])/(scale[-1]-scale[0])
ScalePred=0.11/slope
print("Prediction: ", ScalePred)

#%% Case 11
V0=7.078389445862514e-7
V1upopt=V0*0.11+V0
V1downopt=V0*-0.11+V0

scale=[-10753.0938271605,-10740.75185185185,-10728.40987654321,10000]
V1L=[ 6.298961178416251e-7,6.299801089651286e-7,6.300641209723018e-7,7.885741515366036e-7]
RG=[]
for V1 in V1L:
    RG.append((V1-V0)/V0)
print(RG)

plt.plot(scale,RG)
plt.show()

slope=(RG[-1]-RG[0])/(scale[-1]-scale[0])
ScalePred=0.11/slope
print("Prediction: ", ScalePred)

#%% Case 12
V0=3.598907189454834e-7
V1upopt=V0*0.11+V0
V1downopt=V0*-0.11+V0

scale=[-10400,9166.666666666666]
V1L=[3.200666240363392e-7,3.9975023065282296e-7]
RG=[]
for V1 in V1L:
    RG.append((V1-V0)/V0)
print(RG)

plt.plot(scale,RG)
plt.show()

slope=(RG[-1]-RG[0])/(scale[-1]-scale[0])
ScalePred=0.11/slope
print("Prediction: ", ScalePred)

#%% Case 16
V0=4.1751591560628284e-7
V1upopt=V0*0.11+V0
V1downopt=V0*-0.11+V0

scale=[-9755.555555555555,7778]
V1L=[3.706958088367964e-7,4.639253504187358e-7]
RG=[]
for V1 in V1L:
    RG.append((V1-V0)/V0)
print(RG)

plt.plot(scale,RG)
plt.show()

slope=(RG[-1]-RG[0])/(scale[-1]-scale[0])
ScalePred=0.11/slope
print("Prediction: ", ScalePred)
