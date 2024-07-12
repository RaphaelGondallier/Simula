#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:39:14 2024

@author: Raphaël Gondallier de Tugny
"""

# =============================================================================
# Define here the required features to compute the aspect ratio of a specific case:
# - the slice of the neck
#       advice: apply a big scale factor to see how the neck is going to shrink and put the plane here
# - the region of the aneurysm (so that the slice doesn't cut the rest of the artery)
# - the dome of the aneurysm (from which the candidates points to compute the maximal height will be taken)
# =============================================================================

# trace generated using paraview version 5.12.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

from paraview.simple import *
import pandas as pd
from math import sqrt
from statistics import mean
    
neck_slice_origin = [0.05910284542310764, 0.12623879522894743, 0.0693343226145506]
neck_slice_normal = [-0.7957711341027185, -0.2338067476748584, -0.5586436313702846]
aneurysm_clip_center = [0.05774242127364203, 0.12587777110051873, 0.06873685905599719]
aneurysm_clip_radius = 0.003220599472964041
dome_clip_center = [0.05625439625551745, 0.12550990139226945, 0.06765723462132578] 
dome_clip_radius = 0.0027496650990392743
# find source
boundaries000000vtu= GetActiveSource()

# Slice of the border only
slice1 = Slice(registrationName='Slice1', Input=boundaries000000vtu)
slice1.SliceType = 'Plane'
slice1.SliceType.Origin = neck_slice_origin
slice1.SliceType.Normal = neck_slice_normal
UpdatePipeline(time=0.0, proxy=slice1)

# Restricts the zone to the aneurysm
clip3 = Clip(registrationName='Clip3', Input=slice1)
clip3.ClipType = 'Sphere'
clip3.ClipType.Center = aneurysm_clip_center
clip3.ClipType.Radius = aneurysm_clip_radius
UpdatePipeline(time=0.0, proxy=clip3)

# Defines dome
clip_dome = Clip(registrationName='Clip_dome', Input=boundaries000000vtu)
clip_dome.ClipType = 'Sphere'
clip_dome.ClipType.Center = dome_clip_center
clip_dome.ClipType.Radius = dome_clip_radius
UpdatePipeline(time=0.0, proxy=clip_dome)
