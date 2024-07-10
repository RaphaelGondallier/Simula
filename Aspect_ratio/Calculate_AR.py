# trace generated using paraview version 5.12.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

#### import the simple module from the paraview
from paraview.simple import *
import pandas as pd
from math import sqrt
from statistics import mean

def distance(pt1, pt2):
    return sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 + (pt1[2]-pt2[2])**2 )

path = "/Users/lisa/Documents/Simula/AspectRatio/Case9"

# find source
case9_el047_nocap_boundaries000000vtu = FindSource('case9_el047_nocap_boundaries000000.vtu')

############################
##### AVERAGE DIAMETER ####
###########################

# create a new 'Threshold'
threshold2 = Threshold(registrationName='Threshold2', Input=case9_el047_nocap_boundaries000000vtu)

# Properties modified on threshold2
threshold2.LowerThreshold = 33.0
threshold2.UpperThreshold = 33.0
UpdatePipeline(time=0.0, proxy=threshold2)

# Slice of the border only
slice1 = Slice(registrationName='Slice1', Input=threshold2)
slice1.SliceType = 'Plane'
slice1.SliceType.Origin = [0.12312038894168996, 0.13432140154647867, 0.06351039414662109] #INPUT
slice1.SliceType.Normal = [0.261893954620752, -0.07346556709702588, -0.9622964028739877] #INPUT
UpdatePipeline(time=0.0, proxy=slice1)

# create a new 'Clip'
clip3 = Clip(registrationName='Clip3', Input=slice1)
clip3.ClipType = 'Sphere'
clip3.ClipType.Center = [0.12330716453601878, 0.13530589404617496, 0.06256396502637897] # INPUT
clip3.ClipType.Radius = 0.004 # INPUT
UpdatePipeline(time=0.0, proxy=clip3)

spreadSheetView1 = CreateView('SpreadSheetView')
clip3Display = Show(clip3, spreadSheetView1, 'SpreadSheetRepresentation')

# Caculate centroid and average diameter
ExportView(f'{path}/test1.csv', view=spreadSheetView1, RealNumberNotation='Mixed',
    RealNumberPrecision=6)
data = pd.read_csv(rf"{path}/test1.csv")
data_array = data.values
border_neck_points = data_array[:,1:4].tolist()
x_mean = sum([border_neck_points[i][0] for i in range(len(border_neck_points))])/len(border_neck_points)
y_mean = sum([border_neck_points[i][1] for i in range(len(border_neck_points))])/len(border_neck_points) 
z_mean = sum([border_neck_points[i][2] for i in range(len(border_neck_points))])/len(border_neck_points)
centroid = x_mean, y_mean, z_mean
print("Centroid: ", centroid)
avg_neck_diameter = 2 * mean( [distance(centroid, neck_point) for neck_point in border_neck_points] )
print("Average neck diameter: ", avg_neck_diameter, " m")

###################
##### HEIGHT ####
##################

# Slice of the whole mesh
slice2 = Slice(registrationName='Slice2', Input=case9_el047_nocap_boundaries000000vtu)
slice2.SliceType = 'Plane'
slice2.SliceType.Origin = [0.12312038894168996, 0.13432140154647867, 0.06351039414662109] #INPUT
slice2.SliceType.Normal = [0.261893954620752, -0.07346556709702588, -0.9622964028739877] #INPUT
UpdatePipeline(time=0.0, proxy=slice2)

clip3Display = Show(slice2, spreadSheetView1, 'SpreadSheetRepresentation')

ExportView(f'{path}/neck_points.csv', view=spreadSheetView1, RealNumberNotation='Mixed',
    RealNumberPrecision=6)
data2 = pd.read_csv(rf"{path}/neck_points.csv")
data_array2 = data2.values
neck_points = data_array2[:,1:4].tolist()

distance_max = 0
for dome_point in dome_points:
    xi, yi, zi = neck_point[0], neck_point[1], neck_point[1]
    n_x, n_y, n_z = slice2.SliceType.Normal[0], slice2.SliceType.Normal[0], slice2.SliceType.Normal[0]
    x0, y0, z0 = slice2.SliceType.Origin
    lambda_ = (n_x*(x0-xi) + n_y*(y0-yi) + n_z*(z0-zi)) / (n_x**2 + n_y**2 + n_z**2) # parameter of the parametric equation of a 
                                                                                     # line going through neck_point and perpendicular 
																																																			# to the neck plane
    intersection = (xi+n_x*lambda_, yi+n_y*lambda_, zi+n_z*lambda_) # intersection between the neck plane and the previous line
    distance = distance(neck_point, intersection)
    if distance > distance_max:
        distance_max = distance

print(f"Height = {distance_max}")
