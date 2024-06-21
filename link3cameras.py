# =============================================================================
# Links the 3 cameras in paraview iff 3 cameras are opened
# Make sure to click on the 1st camera before running this macro
# =============================================================================

# trace generated using paraview version 5.12.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find view
renderView2 = FindViewOrCreate('RenderView2', viewtype='RenderView')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# link cameras in two views
AddCameraLink(renderView2, renderView1, 'Link0')

# find view
renderView3 = FindViewOrCreate('RenderView3', viewtype='RenderView')

# link cameras in two views
AddCameraLink(renderView3, renderView2, 'Link1')