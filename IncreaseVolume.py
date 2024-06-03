#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:49:13 2024

@author: Raphael Gondalier de Tugny
"""

from paraview.simple import *

# =============================================================================
# Description:
# This Paraview macro is designed to increase the volume of an aneurysm by 
# applying the desired growth rate (V1-V0)/V0 with the dichotmy method.
#
# Prerequisites:
# - Open the displacement.xdmf file and apply the clip filter with the desired 
#   spatial division (e.g., a sphere encompassing the aneurysm).
# - Create a WarpByVector filter, to which the CellSize is applied.
# - Apply a PythonCalculator with the formula for computing the volume 
#   sum(abs(Volume)). Ensure the calculator is applied to cells, not points.
#  
# Inputs:
# Choose your target_scale line 56
# Ensure the index corresponds to the number in the names of the required filters.
# The bounds set for the scale factor should be sufficiently wide to avoid any issues. 
# If these bounds are reached, please adjust them.
#
# Outputs:
# The script applies the correct scale factor to the aneurysm and prints the 
# scale factor, the final volume of the aneurysm, the actual scale factor, 
# and the error.
# =============================================================================

# Go to the last iteration of the displacement simulation
animationScene1 = GetAnimationScene()
animationScene1.GoToLast()

# Filter names in the filter chain
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
target_scale = 0.11

# Function to retrieve the volume
def get_volume():
    data = servermanager.Fetch(python_calculator)
    cell_data = data.GetCellData()
    result_array = cell_data.GetArray('result')
    return result_array.GetValue(0)

# Calculate parameters
warp_by_vector.ScaleFactor = 0
UpdatePipeline()
V0 = get_volume()
vol = V0
target_volume = V0 * target_scale + V0
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

real_scale = (abs(vol - V0)) / V0
error = abs(real_scale - target_scale)
# Print the final ScaleFactor and corresponding volume
print(f"Final ScaleFactor: {scale_factor}")
print(f"Final Volume: {vol}")
print(f"Real scale factor: {real_scale}")
print(f"Error: {error}")
