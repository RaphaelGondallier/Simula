from paraview.simple import *
import pandas as pd
from math import sqrt
from statistics import mean
import time

def aspect_ratio(neck_slice, aneurysm_clip, clip_dome, spreadSheetView):
    
    def distance(pt1, pt2):
        return sqrt( (pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 + (pt1[2]-pt2[2])**2 )
    
    def export_import_data(input_, csv_name):
    	clipDisplay = Show(input_, spreadSheetView1, 'SpreadSheetRepresentation')
    	ExportView(f'{path}/{csv_name}', view=spreadSheetView1, RealNumberNotation='Mixed', RealNumberPrecision=6)
    	data = pd.read_csv(rf"{path}/{csv_name}")
    	data_array = data.values
    	points = data_array[:,5:8].tolist() #depending on the file you use, the position of the points in the array could change
    	return points
    
    path = "/Users/lisa/Documents/Simula/AspectRatio/Case8"    
    
    # =============================================================================
    # AVERAGE DIAMETER
    # =============================================================================
    # Caculates centroid and average diameter
    border_neck_points = export_import_data(aneurysm_clip, 'border_neck_points.csv')
    x_mean = sum([border_neck_points[i][0] for i in range(len(border_neck_points))])/len(border_neck_points)
    y_mean = sum([border_neck_points[i][1] for i in range(len(border_neck_points))])/len(border_neck_points) 
    z_mean = sum([border_neck_points[i][2] for i in range(len(border_neck_points))])/len(border_neck_points)
    centroid = x_mean, y_mean, z_mean
    avg_neck_diameter = 2 * mean( [distance(centroid, neck_point) for neck_point in border_neck_points] )
    
    # =============================================================================
    # HEIGHT
    # =============================================================================    
    dome_points = export_import_data(clip_dome, 'dome_points.csv')
    
    distance_max = 0
    for i, dome_point in enumerate(dome_points):
    	xi, yi, zi = dome_point[0], dome_point[1], dome_point[2]
    	n_x, n_y, n_z = neck_slice.SliceType.Normal[0], neck_slice.SliceType.Normal[1], neck_slice.SliceType.Normal[2]
    	x0, y0, z0 = neck_slice.SliceType.Origin
    	lambda_ = (n_x*(x0-xi) + n_y*(y0-yi) + n_z*(z0-zi)) / (n_x**2 + n_y**2 + n_z**2) # parameter of the parametric equation of a 
                                                                                         # line going through neck_point and perpendicular 
    																																																			# to the neck plane
    	intersection = [xi+n_x*lambda_, yi+n_y*lambda_, zi+n_z*lambda_] # intersection between the neck plane and the previous line
    	distance_ = distance(dome_point, intersection)
    
    	if distance_ > distance_max:
    		distance_max = distance_
    		intersection_max = intersection
    		dome_point_max = dome_point
    #print(f"Aspect ratio = {distance_max/avg_neck_diameter}")

    return distance_max/avg_neck_diameter

def get_volume(python_calculator):
    data = servermanager.Fetch(python_calculator)
    cell_data = data.GetCellData()
    result_array = cell_data.GetArray('result')
    return result_array.GetValue(0)

def set_AR(target_AR, warp_by_vector, ExtractSurface, slice1, clip1, clip_dome1, spreadSheetView1):
    global AR_Scale_factor 
    # Define bounds for ScaleFactor and the desired real factor
    low = -10 # negative SF to shrink the neck
    high = 9 # In case the temporary target AR is smaller than the initial one, SF has to be positive
    #SetActiveSource(ExtractSurface)

    # Calculate parameters
    warp_by_vector.ScaleFactor = 0
    UpdatePipeline()
    AR0 = aspect_ratio(slice1, clip1, clip_dome1, spreadSheetView1)
    AR_ = AR0
    epsilon = 1e-5 * target_AR
    #print("V0, target_volume,epsilon,D",V0, target_volume,epsilon,"\n",vol-target_volume)

    i = 0
    # Bisection search loop
    while abs(AR_ - target_AR) > epsilon and i < 500: #/!\ target_AR is not the final target here but a AR_predform from the largest dichotomy
        i += 1
        # Calculate the current ScaleFactor
        scale_factor = (low + high) / 2.0
        warp_by_vector.ScaleFactor = scale_factor
        UpdatePipeline()  # Update the global pipeline

        # Retrieve the current volume
        AR_ = aspect_ratio(slice1, clip1, clip_dome1, spreadSheetView1)
        # Adjust the bounds of the interval
        if AR_ < target_AR:
            high = scale_factor # inverted bc when scale factor decreases, AR increases
        else:
            low = scale_factor
        AR_Scale_factor = scale_factor
        print(f"AR/bounds(small dicho): {AR_}, {low}, {high}")
    # real_scale = (abs(AR_ - AR0)) / AR0
    # error = abs(real_scale - target_scale)
    # # Print the final ScaleFactor and corresponding volume
    # print(f"Final ScaleFactor: {scale_factor}")
    # print(f"Final aspect ratio: {AR_}")
    # print(f"Real scale factor: {real_scale}")
    # print(f"Error: {error}")
    # print(f"Iterations: {i}")
    
def Increase_volume(V0, warp_by_vector, python_calculator):
    global j, V_Scale_factor
    # Go to the last iteration of the displacement simulation
    animationScene1 = GetAnimationScene()
    animationScene1.GoToLast()
    
    # Ensure the filters are selected
    #SetActiveSource(python_calculator)
    
    # Define bounds for ScaleFactor and the desired real factor
    low = -9 # if the AR temporarly gets smaller than the initial one because of the iterative procces, SF has to be negative
    high = 10    
    # Calculate parameters
    warp_by_vector.ScaleFactor = 0
    UpdatePipeline()
    Vi = get_volume(python_calculator)
    vol = Vi
    epsilon = 1e-5 * V0
    #print("V0, target_volume,epsilon,D",V0, target_volume,epsilon,"\n",vol-target_volume)
    i = 0
    
    # Bisection search loop
    while abs(vol - V0) > epsilon and i < 500:
        i += 1
        # Calculate the current ScaleFactor
        scale_factor = (low + high) / 2.0
        warp_by_vector.ScaleFactor = scale_factor
        UpdatePipeline()  # Update the global pipeline
    
        # Retrieve the current volume
        vol = get_volume(python_calculator)
        #print(vol, scale_factor)
        # Adjust the bounds of the interval
        if vol < V0:
            low = scale_factor
        else:
            high = scale_factor
        V_Scale_factor = scale_factor
    print(f"Volume at iteration {j}: {vol}\n")
    
###########################################################  
# Go to the last iteration of the displacement simulation
start_time = time.time()

animationScene1 = GetAnimationScene()
animationScene1.GoToLast()

# =============================================================================
# INPUTS
# =============================================================================
# V0 calculation prerequisite
python_calculator1 = FindSource("PythonCalculator1")

# AR calculation prerequisites
slice1 = FindSource("Slice1")
clip1 = FindSource("Clip1")
clip_dome1 = FindSource("Clip_dome1")
spreadSheetView1 = CreateView('SpreadSheetView')

slice2 = FindSource("Slice2")
clip2 = FindSource("Clip2")
clip_dome2 = FindSource("Clip_dome2")

# Set AR prerequisites
warp_by_vector1 = FindSource("WarpByVector1")
ExtractSurface1 = FindSource("ExtractSurface1")

# Increase volume prerequisites
warp_by_vector2 = FindSource("WarpByVector2")
python_calculator2 = FindSource("PythonCalculator2")
# =============================================================================
# MAIN
# =============================================================================
warp_by_vector1.ScaleFactor = 0
warp_by_vector2.ScaleFactor = 0
AR0 = aspect_ratio(slice1, clip1, clip_dome1, spreadSheetView1)
target_scale = 0.22
target_AR = AR0 * target_scale + AR0
print(f"AR0 and target AR: {AR0}, {target_AR}")
epsilon = 1e-5 * target_AR
j=0
AR_final=AR0
iter_max = 25
AR_inf = 0 
AR_sup = 2.571
V0 = get_volume(python_calculator1)
print(f"Initial volume: {V0}")
AR_Scale_factor = 0 # global variable
V_Scale_factor = 0 # global variable
while abs(AR_final-target_AR) > epsilon and j < iter_max:
    print(f"AR_inf, AR_sup: {AR_inf}, {AR_sup}")
    AR_predeform = 0.5*(AR_inf+AR_sup) # This AR is bigger than the target because it is the 
                                       # one before the volume is reset. Thus, it is not the 
                                       # one used for the shutdown test.
    set_AR(AR_predeform, warp_by_vector1, ExtractSurface1, slice1, clip1, clip_dome1, spreadSheetView1) # Modifies the mesh to reach AR_theo
    Increase_volume(V0, warp_by_vector2, python_calculator2) # Resets aneurysm's volume to V0
    
    # Check if the tested AR_theo leads to the correct final AR
    AR_final = aspect_ratio(slice2, clip2, clip_dome2, spreadSheetView1) # AR is changed now that volume has been reset
    if AR_final < target_AR: # The final AR, after volume rest is used for the shutdown  test
        AR_inf = AR_predeform
    else:
        AR_sup = AR_predeform
    j+=1

end_time = time.time()
execution_time = end_time - start_time
print(f"Aspect ratio goal: {target_AR}")
print(f"Final aspect ratio: {AR_final}")
print(f"Final AR scale factor: {AR_Scale_factor}")
print(f"Final V scale factor: {V_Scale_factor}")
print(f"Iterations: {j}")
print(f"Execution time: {execution_time/60} min")
