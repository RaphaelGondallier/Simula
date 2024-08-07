# trace generated using paraview version 5.12.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 12

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
xdmf = GetActiveSource()

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=xdmf)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1.ClipType)

# Properties modified on clip1
clip1.ClipType = 'Sphere'

# Properties modified on clip1.ClipType
clip1.ClipType.Center = [0.0725, 0.135, 0.0565]
clip1.ClipType.Radius = 0.0063

UpdatePipeline(time=0.0, proxy=clip1)