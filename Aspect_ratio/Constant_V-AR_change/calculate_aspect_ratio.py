#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:39:14 2024

@author: Raphaël Gondallier de Tugny
"""

# trace generated using paraview version 5.12.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

from paraview.simple import *
import pandas as pd
from math import sqrt
from statistics import mean

def aspect_ratio():
    
    def distance(pt1, pt2):
        return sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 + (pt1[2]-pt2[2])**2 )
    
    def export_import_data(input_, csv_name):
    	clipDisplay = Show(input_, spreadSheetView1, 'SpreadSheetRepresentation')
    	ExportView(f'{path}/{csv_name}', view=spreadSheetView1, RealNumberNotation='Mixed', RealNumberPrecision=6)
    	data = pd.read_csv(rf"{path}/{csv_name}")
    	data_array = data.values
    	points = data_array[:,1:4].tolist() #depending on the file you use, the position of the points in the array could change
                                         #usually [:,5:8] or [:,1:4]
    	return points
    
    # =============================================================================
    # INPUTS
    # =============================================================================
    path = "/Users/lisa/Documents/Simula/AspectRatio/Case8"
    neck_slice_origin = [0.05910284542310764, 0.12623879522894743, 0.0693343226145506]
    neck_slice_normal = [-0.7957711341027185, -0.2338067476748584, -0.5586436313702846]
    aneurysm_clip_center = [0.05774242127364203, 0.12587777110051873, 0.06873685905599719]
    aneurysm_clip_radius = 0.003220599472964041
    dome_clip_center = [0.05625439625551745, 0.12550990139226945, 0.06765723462132578] 
    dome_clip_radius = 0.0027496650990392743
    # find source
    boundaries000000vtu= GetActiveSource()
    
    # =============================================================================
    # AVERAGE DIAMETER
    # =============================================================================
    
    slice1 = FindSource("Slice1")
    clip3 = FindSource("Clip1")
    spreadSheetView1 = CreateView('SpreadSheetView')
    # Caculates centroid and average diameter
    border_neck_points = export_import_data(clip3, 'border_neck_points.csv')
    x_mean = sum([border_neck_points[i][0] for i in range(len(border_neck_points))])/len(border_neck_points)
    y_mean = sum([border_neck_points[i][1] for i in range(len(border_neck_points))])/len(border_neck_points) 
    z_mean = sum([border_neck_points[i][2] for i in range(len(border_neck_points))])/len(border_neck_points)
    centroid = x_mean, y_mean, z_mean
    avg_neck_diameter = 2 * mean( [distance(centroid, neck_point) for neck_point in border_neck_points] )
    
    # =============================================================================
    # HEIGHT
    # =============================================================================
    # # To display the neck plane: Slice of the whole mesh: threshold is not applied here
    # slice2 = Slice(registrationName='Slice2', Input=boundaries000000vtu)
    # slice2.SliceType = 'Plane'
    # slice2.SliceType.Origin = neck_slice_origin
    # slice2.SliceType.Normal = neck_slice_normal
    # UpdatePipeline(time=0.0, proxy=slice2)
    
    # # Restricts the zone to the aneurysm
    # clip4 = Clip(registrationName='Clip4', Input=slice2)
    # clip4.ClipType = 'Sphere'
    # clip4.ClipType.Center = aneurysm_clip_center
    # clip4.ClipType.Radius = aneurysm_clip_radius
    # UpdatePipeline(time=0.0, proxy=clip4)
    
    clip_dome = FindSource("Clip_dome1")
    
    dome_points = export_import_data(clip_dome, 'dome_points.csv')
    
    distance_max = 0
    for i, dome_point in enumerate(dome_points):
    	xi, yi, zi = dome_point[0], dome_point[1], dome_point[2]
    	n_x, n_y, n_z = slice1.SliceType.Normal[0], slice1.SliceType.Normal[1], slice1.SliceType.Normal[2]
    	x0, y0, z0 = slice1.SliceType.Origin
    	lambda_ = (n_x*(x0-xi) + n_y*(y0-yi) + n_z*(z0-zi)) / (n_x**2 + n_y**2 + n_z**2) # parameter of the parametric equation of a 
                                                                                         # line going through neck_point and perpendicular 
    																																																			# to the neck plane
    	intersection = [xi+n_x*lambda_, yi+n_y*lambda_, zi+n_z*lambda_] # intersection between the neck plane and the previous line
    	distance_ = distance(dome_point, intersection)
    
    # plots lines
    	line = Line(registrationName=f'Line{i}')
    	line.Point1 = dome_point
    	line.Point2 = intersection
    	UpdatePipeline(time=0.0, proxy=line)
    
    	if distance_ > distance_max:
    		distance_max = distance_
    		intersection_max = intersection
    		dome_point_max = dome_point
            
    #plots maximal height
    line = Line(registrationName='LineMax')
    line.Point1 = dome_point_max
    line.Point2 = intersection_max
    UpdatePipeline(time=0.0, proxy=line)
    renderView1 = GetActiveViewOrCreate('RenderView')
    lineDisplay = GetDisplayProperties(line, view=renderView1)
    # change solid color
    lineDisplay.AmbientColor = [0.8588235294117647, 0.0, 0.0]
    lineDisplay.DiffuseColor = [0.8588235294117647, 0.0, 0.0]

    print("Centroid: ", centroid)
    print("Average neck diameter: ", avg_neck_diameter, " m")
    print(f"Height = {distance_max} m")
    print(f"Aspect ratio = {distance_max/avg_neck_diameter}")

    return distance_max/avg_neck_diameter

aspect_ratio()