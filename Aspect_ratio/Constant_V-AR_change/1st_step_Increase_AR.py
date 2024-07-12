from paraview.simple import *
import pandas as pd
from math import sqrt
from statistics import mean

import importlib
import sys
import os
macros_dir = '/Users/lisa/.config/ParaView/Macros/'
if macros_dir not in sys.path:
    sys.path.append(macros_dir)
from calculate_aspect_ratio import aspect_ratio

#importlib.reload(calculate_aspect_ratio) #in case you modify calculate_aspect_ratio.py 

# Go to the last iteration of the displacement simulation
animationScene1 = GetAnimationScene()
animationScene1.GoToLast()

# Define bounds for ScaleFactor and the desired real factor
low = -10
high = 0
target_scale = 0.22
warp_by_vector = FindSource("WarpByVector1")
ExtractSurface = FindSource("ExtractSurface1")
SetActiveSource(ExtractSurface)

# Function to retrieve the volume
def get_AR():
    AR = aspect_ratio()
    return AR

# Calculate parameters
warp_by_vector.ScaleFactor = 0
UpdatePipeline()
AR0 = get_AR()
AR = AR0
target_AR = AR0 * target_scale + AR0
epsilon = 1e-5 * target_AR
#print("V0, target_volume,epsilon,D",V0, target_volume,epsilon,"\n",vol-target_volume)

i = 0
# Bisection search loop
while abs(AR - target_AR) > epsilon and i < 500:
    i += 1
    # Calculate the current ScaleFactor
    scale_factor = (low + high) / 2.0
    warp_by_vector.ScaleFactor = scale_factor
    UpdatePipeline()  # Update the global pipeline

    # Retrieve the current volume
    AR = get_AR()
    #print(vol, scale_factor)
    # Adjust the bounds of the interval
    if AR < target_AR:
        high = scale_factor # inverted bc when scale factor decreases, AR increases
    else:
        low = scale_factor
    
real_scale = (abs(AR - AR0)) / AR0
error = abs(real_scale - target_scale)
# Print the final ScaleFactor and corresponding volume
print(f"Final ScaleFactor: {scale_factor}")
print(f"Final aspect ratio: {AR}")
print(f"Real scale factor: {real_scale}")
print(f"Error: {error}")