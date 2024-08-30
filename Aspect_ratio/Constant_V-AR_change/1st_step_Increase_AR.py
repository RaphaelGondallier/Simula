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
def get_volume():
    data = servermanager.Fetch(python_calculator)
    cell_data = data.GetCellData()
    result_array = cell_data.GetArray('result')
    return result_array.GetValue(0)

def Increase_volume(target_volume):
    # Go to the last iteration of the displacement simulation
    animationScene1 = GetAnimationScene()
    animationScene1.GoToLast()
    
    # Filter names in the filter chain VERIIIIIIIIIIIIIFFFFFFFFFFFFFF -> 2e bloc
    index = "1"
    warp_by_vector_name = "WarpByVector" + index
    cell_size_name = "CellSize" + index
    python_calculator_name = "PythonCalculator" + index
    
    # Find filters in the filter chain
    warp_by_vector = FindSource(warp_by_vector_name)
    cell_size = FindSource(cell_size_name)
    python_calculator = FindSource(python_calculator_name)
    
    # Ensure the filters are selected
    SetActiveSource(python_calculator)
    
    # Define bounds for ScaleFactor and the desired real factor
    low = 0
    high = 10    
    # Calculate parameters
    warp_by_vector.ScaleFactor = 0
    UpdatePipeline()
    V0 = get_volume()
    vol = V0
    epsilon = 1e-5 * target_volume
    #print("V0, target_volume,epsilon,D",V0, target_volume,epsilon,"\n",vol-target_volume)
    i = 0
    
    # Bisection search loop
    while abs(vol - target_volume) > epsilon and i < 500:
        i += 1
        # Calculate the current ScaleFactor
        scale_factor = (low + high) / 2.0
        warp_by_vector.ScaleFactor = scale_factor
        UpdatePipeline()  # Update the global pipeline
    
        # Retrieve the current volume
        vol = get_volume()
        #print(vol, scale_factor)
        # Adjust the bounds of the interval
        if vol < target_volume:
            low = scale_factor
        else:
            high = scale_factor
###########################################################  
# Go to the last iteration of the displacement simulation
animationScene1 = GetAnimationScene()
animationScene1.GoToLast()

AR_inf = 0 
AR_sup = 10
AR = 0.5*(AR_inf+AR_sup)
###########################################################
# intermediare target
###########################################################

# Define bounds for ScaleFactor and the desired real factor
low = -10
high = 0
target_scale = 0.22
warp_by_vector = FindSource("WarpByVector1")
ExtractSurface = FindSource("ExtractSurface1")
python_calculator = FindSource(python_calculator_name)
SetActiveSource(ExtractSurface)

# Calculate parameters
warp_by_vector.ScaleFactor = 0
UpdatePipeline()
AR0 = aspect_ratio()
AR_ = AR0
target_AR = AR0 * target_scale + AR0
epsilon = 1e-5 * target_AR
#print("V0, target_volume,epsilon,D",V0, target_volume,epsilon,"\n",vol-target_volume)

i = 0
# Bisection search loop
while abs(AR_ - target_AR) > epsilon and i < 500:
    i += 1
    # Calculate the current ScaleFactor
    scale_factor = (low + high) / 2.0
    warp_by_vector.ScaleFactor = scale_factor
    UpdatePipeline()  # Update the global pipeline

    # Retrieve the current volume
    AR_ = aspect_ratio()
    #print(vol, scale_factor)
    # Adjust the bounds of the interval
    if AR_ < target_AR:
        high = scale_factor # inverted bc when scale factor decreases, AR increases
    else:
        low = scale_factor
###########################################################    
real_scale = (abs(AR_ - AR0)) / AR0
error = abs(real_scale - target_scale)
# Print the final ScaleFactor and corresponding volume
print(f"Final ScaleFactor: {scale_factor}")
print(f"Final aspect ratio: {AR_}")
print(f"Real scale factor: {real_scale}")
print(f"Error: {error}")
print(f"Iterations: {i}")